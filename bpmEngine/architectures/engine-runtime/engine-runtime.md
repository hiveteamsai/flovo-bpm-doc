# Flovo BPM Motoru — Runtime Mimarisi (orkestrasyon ↔ yürütme · durum · kalıcılık)

> **Durum:** 🟢 Tasarım (v0.40) · 📝 **v0.44 güncellemesi — onay bekliyor** (iki-TX adım · outbox-in-event · 409 sözleşmesi · projeksiyon/timer modelleri;
> kararlar/açık sorular → [`engine-runtime-plan.md`](./engine-runtime-plan.md)). **Amaç:** Motorun **sistem olarak nasıl koştuğunu** tanımlar — [`flovo-bpm-engine.md`](../engine-core/flovo-bpm-engine.md)
> §4.4'teki **senkron** yürütme döngüsünü, karar verilen yığın üzerinde (**Go stateless worker + NATS JetStream + PostgreSQL Partial
> Event Sourcing**) **event-driven, kalıcı, kaldığı yerden devam eden** bir mimariye çevirir. Bu doküman `flovo-bpm-engine.md`
> **§2.2 (orkestrasyon↔yürütme)** · **§8 (kalıcılık/durum)** · **§4.5 (paralel dallanma)** bölümlerini **doldurur**.
>
> **Doküman ailesi (v0.44):** bu dosya = **ana spec**; ayrıntı alt-dokümanlar → [`engine-runtime-errors.md`](./engine-runtime-errors.md) (hata · retry · onFail · kurtarma · guard) ·
> [`engine-runtime-scheduler.md`](./engine-runtime-scheduler.md) (timer · timeout · cron · uyandırma) · [`engine-runtime-retention.md`](./engine-runtime-retention.md) (saklama · KVKK).
> **Modeller:** [`WorkflowEvent`](../../models/processInstances/workflow-event.md) (`workflow_events`) · [`WorkflowProjection`](../../models/processInstances/workflow-projection.md) ·
> [`WorkflowTimer`](../../models/processInstances/workflow-timer.md) · enum [`WorkflowEventType`](../../models/enums/workflow-event-type.md).
>
> **Yığın:** [`tech-stack/go.md`](../../tech-stack/go.md) (Hexagonal, goroutine) · [`tech-stack/nats-jetstream.md`](../../tech-stack/nats-jetstream.md)
> (job/olay omurgası) · [`tech-stack/postgresql.md`](../../tech-stack/postgresql.md) (`workflow_events` append-only + durum).
> **Semantik (değişmeyen):** yürütme algoritması → `flovo-bpm-engine.md` §4 · veri akışı → §3 · bekle/devam → §6.

---

## 0. Temel reframe: senkron döngü → dağıtık olay-akışı
`flovo-bpm-engine.md` §4.4 döngüsü **tek bir `while`** gibi yazılır (okunabilirlik için). Gerçek motor bunu **parçalara** böler:

| Senkron döngüdeki adım | Dağıtık karşılığı |
|---|---|
| `while adım != BİTİŞ` | Süreç **kalıcı durum**tur (Postgres); döngü **yok**, her tur bir **olay** tetikler |
| otomatik adım `işiniYap()` | Bir **iş (job)** NATS'a düşer → **durumsuz worker** bir adımı koşar |
| insan-tetiklemeli `bekle()` | Süreç **askıya alınır** (durum yazılır, worker serbest); iş kuyrukta **kalmaz** |
| `adım = gelenAction.targetProcessStepId` | Worker sonraki adımı **enqueue eder** (yeni job) veya süreç **beklemeye** geçer |
| devam (kullanıcı aksiyonu) | Dış **olay** (API/timer/webhook) süreci **uyandırır** → yeni job |

> **Sonuç:** Süreç bir process değil, **Postgres'te duran durum + NATS'ta akan olaylar**dır. Worker'lar durumsuzdur; günlerce
> bekleyen bir süreç **hiçbir kaynak tutmaz** (n8n dersi 8: kalıcılaştır-ve-devam-et).

## 1. Yürütme durumu (execution state machine)
Her `ProcessInstance` bir **yürütme durumu** taşır (form iş-durumu `Instance.statusId`'den **ayrı**):

```
        ┌─────────────────────────── (dış olay/timer) ───────────────────────────┐
        ▼                                                                          │
  new ──▶ running ──(otomatik adım zinciri)──▶ running ──(insan/timer/processing)─▶ waiting
        │                                            │                             (askıda; worker serbest)
        │                                            ├──(BİTİŞ düğümü)──▶ done
        └──(hata + onFail yok)──▶ failed ◀───────────┘
```

- **`ProcessInstance.executionState`** (YENİ alan) = `new` · `running` · `waiting` · `failed` · `done` · **`cancelled`** (📝 v0.44 öneri — admin iptali; → plan Q6)
  (→ [`models/enums/process-execution-state.md`](../../models/enums/process-execution-state.md)). Bu, **`workflow_events`'ten türetilen bir
  projeksiyondur** (hızlı sorgu: "koşan/bekleyen/hatalı süreçler"); kaynak-hakikat olay log'udur.
- **Motor imleci** = [`WorkflowProjection`](../../models/processInstances/workflow-projection.md) (süreç başına 1 satır): `lastVersion` (optimistic concurrency) ·
  `executionState` + **`waitReason`** (`humanTask`/`processing`/`timer`/`retry`/`subProcess` → [`WorkflowWaitReason`](../../models/enums/workflow-wait-reason.md)) ·
  aktif adım · `attempt` · guard sayaçları · `lastError`. `ProcessInstance.executionState` bunun **kopyası**dır (liste sorguları join'siz; aynı TX).
- **Mevcut konum** = o instance'ın **en güncel aktif `ProcessStepInstance`**'ı (`processStepId` = aktif adım; projeksiyonda `activeProcessStepInstanceId`).
- **Askı kaydı** = `waiting` iken **`InstanceAwaitingUser`** (kim aksiyon alabilir) + timer/timeout/retry bekleniyorsa **[`WorkflowTimer`](../../models/processInstances/workflow-timer.md)** (`armed`, `dueAt`).
- **Biriken parametreler** = son `ProcessStepInstance.processStepActionParameter` (**`ActionTransfer`** JSON: `parameters`/`changeList`/`action`) —
  kaynak kopya `workflow_events.payload`'dadır (stepCompleted/actionTaken snapshot; → workflow-event §2).

> **KARAR:** Motor yürütme-durumu **`Instance.statusId`'ye karıştırılmaz.** `statusId` = kullanıcının gördüğü **iş durumu**
> (Onay Bekliyor, Reddedildi…); `executionState` = **motorun** iç konumu. İkisi bağımsız evrilir.

## 2. Bileşenler (orkestrasyon ↔ yürütme)
| Bileşen | Rol | Durum |
|---|---|---|
| **Worker** (Go, goroutine havuzu) | JetStream'den **step-ready** iş çeker, **tek adımı** koşar, durum yazar, sonrakini enqueue eder | **Durumsuz** (yatay ölçek) |
| **Orkestratör** (mantıksal) | Aksiyon→sonraki-adım çevirimi, **uyandırma** (timer/olay), **at-most-once** (idempotency), retry/backoff | Worker içinde + scheduler |
| **NATS JetStream** | İş kuyruğu + olay omurgası (`FLOVO_EVENTS`, durable consumer, `Nats-Msg-Id`) | Kalıcı, sıralı, replay |
| **PostgreSQL** | [`workflow_events`](../../models/processInstances/workflow-event.md) (append-only kaynak **+ outbox-in-event**) + [`workflow_projection`](../../models/processInstances/workflow-projection.md) (imleç) + [`workflow_timer`](../../models/processInstances/workflow-timer.md) + `ProcessInstance`/`ProcessStepInstance`/`InstanceAwaitingUser` + `InstanceValue` | Kaynak-hakikat |
| **Scheduler** (durumsuz, **yatay ölçeklenir**) | `workflow_timer`'da dolan kayıtları **Postgres'te claim eder** (`FOR UPDATE SKIP LOCKED`), `timerFired` yazar, `resume.v1` yayınlar; **lider seçimi gerekmez** (📝 v0.44 R7); advisory lock yalnız housekeeping | Replica-N (→ [`engine-runtime-scheduler.md`](./engine-runtime-scheduler.md)) |
| **Outbox relay** (housekeeping) | Commit edilmiş ama yayınlanamamış `dispatch`'leri yeniden yayınlar (`publishedAt IS NULL`) | Tekil (advisory lock), zararsız çoğaltılabilir |

> **Orkestrasyon↔yürütme ayrımı:** *durum DB'de, kuyruk yalnız iş/olay taşır, worker'lar durumsuz* (n8n dersi 1–2). Bir worker
> çökse başka worker aynı işi devralır (JetStream redelivery + idempotency); iş **kaybolmaz**. Commit sonrası publish kaçarsa **relay** tamamlar
> (→ workflow-event §3.5) — "süreç `running`'de takılı" durumu oluşmaz.

## 3. NATS subject'leri (BPM)
Mevcut `flovo.{aggregate}.{verb}.{version}` desenine (nats-jetstream.md) BPM ekler:

| Subject | Ne taşır | Üreten → Tüketen |
|---|---|---|
| `flovo.workflow.step_ready.v1` | Koşulacak adım işi (`processInstanceId` + hedef `processStepId` + gelen `ActionTransfer`) | Orkestratör → Worker |
| `flovo.workflow.step_completed.v1` | Adım tamamlandı (audit/saga/realtime) | Worker → dinleyiciler |
| `flovo.workflow.suspended.v1` | Süreç beklemeye geçti (realtime: "aksiyon bekliyor") | Worker → FE bildirim |
| `flovo.workflow.resume.v1` | Uyandırma (kullanıcı aksiyonu / timer / webhook) | API·Scheduler → Worker |
| `flovo.workflow.failed.v1` | Adım hatası (onFail yönlendirmesi / dead-letter) | Worker → hata akışı |

## 4. Yürütme akışı (adım-adım)

### 4.1 Başlatma
Kullanıcı/API süreci başlatır (`processStart` / `subProcessStart` / ServiceTrigger) → `ProcessInstance` (`executionState=new`) +
ilk `workflow_events` (StartRequested) yazılır → ilk **`step_ready`** işi enqueue → `running`.

### 4.2 Otomatik adım (worker turu — tek atomik iş)
Worker bir `step_ready` işini çeker ve **tek adımı** koşar — **iki TX** (📝 v0.44 R4; → workflow-event §3.2):
1. **Yükle + idempotency:** `WorkflowProjection` (`lastVersion`, `attempt`) + `ProcessInstance` + aktif adım tasarımı (`ProcessStep.settings`) + form değeri (`InstanceValue`) +
   gelen `ActionTransfer`. Job'ın `messageId`'si `workflow_events`'te varsa → **zaten işlendi, ACK ve atla** (§5.1). `stepStarted` var ama sonucu yoksa → **in-doubt** (→ errors §3).
2. **TX-A — `stepStarted`:** `version+1` · `ProcessStepInstance` (executionDate) · **evrensel giriş kuralı:** gelen `changeList` boş değilse forma **merge**
   (write-path → §3.1 · [`tech-stack/postgresql.md`](../../tech-stack/postgresql.md)) + `InstanceValueOutbox` · projeksiyon (`attempt`, `autoStepRun++`, `totalSteps++`). **Commit.**
3. **İşi yap:** adım tipine göre (HTTP Request, Karşılaştırma, Switch, Değer Atama, Timer…) — tipe-özel `settings` şeması →
   [`models/service-settings/jsonTemplateModels/process-step-settings/`](../../models/service-settings/jsonTemplateModels/process-step-settings/index.md). Yan etki **burada**; süre sınırı 60 s (guard).
4. **Aksiyon seç:** sonucu bir **aksiyon koduna** eşle (`true`/`false`/`default`/response.action) → o kodlu `ProcessStepAction`. Hata → sınıflandır (→ errors §1).
5. **TX-B — `stepCompleted` | `stepFailed`:** `version+1` · `ProcessStepInstance` (üretilen `processStepActionParameter`) · **`dispatch`** = sonraki `step_ready`
   (outbox-in-event) · projeksiyon · hata ise retry timer / onFail seçimi (→ errors §2/§4). **Commit** → publish (`publishedAt`).
6. **İlerlet:** seçilen aksiyonun `targetProcessStepId`'si için `dispatch`'teki **`step_ready`** yayınlanır (`mergeParameter` ise gelen+üretilen
   birleşir → §4.4 pseudo). Terminal otomatik adım (giden aksiyon yok) → `ended(terminalStep)`, kol biter (§4.4 `break`).

> **Hız:** Bir worker turu = **iki** küçük Postgres TX + bir NATS publish; ağır iş (HTTP Request) adımın kendi içinde. Saf-hesap adımlarda (Değer Atama,
> Karşılaştırma, Switch) TX-A/TX-B **tek TX'e katlanabilir** (yan etki yok → in-doubt riski yok; uygulama optimizasyonu, semantik aynı).

### 4.3 İnsan / bekleme adımı (SUSPEND)
Adım **Kullanıcı / Kullanıcı Grubu / Üst Form Kullanıcı** ise (veya **Processing** `autoAction`'sız, **Timer** beklemesi):
1. Worker **atananı çöz** (`userType`/`userGroupType`) → **`InstanceAwaitingUser`** kayıtlarını **senkronla** (ekle/sil).
2. `workflow_events` (Suspended) + `ProcessInstance.executionState=waiting` yaz; **`suspended.v1`** yayınla (FE "aksiyon bekliyor").
3. **Worker serbest** — kuyrukta iş kalmaz. Süreç **günlerce** bu durumda durabilir (kaynak tutmaz).

> **Atama çözülemezse** → hata/`onFail` (§6). **Adım atlama** (`skipIfPreApproved`/`skipIfUserProcessStarter`) → beklemeye geçmeden
> `skipWithThisProcessStepActionId` otomatik tetiklenir (§4.4).

### 4.4 Devam (RESUME)
Bir **dış olay** süreci uyandırır:
- **Kullanıcı aksiyonu:** `POST /instances/{id}/actions/{code}` (→ [`flovo-customer-api.md`](../api/flovo-customer-api.md)) → aktör
  **`InstanceAwaitingUser`'a karşı doğrulanır** (grup üyeliği okuma-anı; ilk aksiyon ilerletir — grup eşiği yok).
- **Timer:** scheduler süre dolunca `resume.v1` yayınlar (§7).
- **Webhook/Processing:** dış çağrı `resume.v1` tetikler.

Uyandırmada (**API katmanında senkron**, worker'a gitmeden): `ProcessStepInstance` **aksiyon alanları** dolar (`atUserId`/`atApiKeyId` · `actionTriggerDate` · `processStepActionId` ·
`processStepActionParameter` = taşınan `ActionTransfer` · vekaletse `atDelegateUserId`) + `workflow_events` (`actionTaken`, `version = lastVersion+1`,
`messageId = Idempotency-Key`) yazılır → bekleyen `taskTimeout` timer'ı `cancelled` → `executionState=running` → seçilen aksiyonun hedefi için `dispatch` **`step_ready`**.
**Version çakışması → 409** (§5.2). **Form bilgisi** aksiyon isteğinin **response'unda** döner (§6.3 — beş form-döndüren adım).
Timer/timeout uyandırması scheduler tarafından aynı kurallarla yapılır (→ [`engine-runtime-scheduler.md`](./engine-runtime-scheduler.md) §4).

### 4.5 Bitiş
**Süreç Bitişi** / **Alt Süreç Bitişi** → `workflow_events` (Ended) + `executionState=done`. Ana süreçte yetkililer sonradan
erişebilir/geri-taşıyabilir (`processEnd.userGroupIds`); alt süreçte geri-taşıma yoktur.

## 5. Idempotency · optimistic concurrency · çakışma sözleşmesi
### 5.1 Worker / scheduler tarafı (sessiz)
- **`messageId` (Nats-Msg-Id) UNIQUE:** her `step_ready`/`resume` işi bir mesaj-id taşır; `workflow_events.messageId`'de varsa → **zaten işlendi, ACK ve atla**.
- **`version` (optimistic concurrency):** yazan `WorkflowProjection.lastVersion + 1` ile INSERT eder; UNIQUE (`processInstanceId`,`version`) ihlali = başkası ilerletti →
  TX geri alınır, **ACK ve atla** (log). Böylece **at-least-once teslim + redelivery + sırasız** süreci **iki kez ilerletmez** (nats-jetstream.md deseninin aynısı).
- **Publish tarafı:** commit sonrası publish kaçarsa **relay** `dispatch`'i yeniden yayınlar; çift yayın yukarıdaki kurallarla zararsızdır (→ workflow-event §3.5).

### 5.2 API tarafı — kullanıcı aksiyonu çakışma sözleşmesi (📝 v0.44 R15 · Q17)
`POST /instances/{id}/actions/{code}` (+ header **`Idempotency-Key`**, FE her tıklamada UUID; Customer API'de zorunlu — → [`flovo-customer-api.md`](../api/flovo-customer-api.md)):

| Durum | Tespit | Yanıt | FE davranışı |
|---|---|---|---|
| **Aynı tıklamanın tekrarı** (double-click / ağ retry) | `Idempotency-Key` `workflow_events.messageId`'de var | **200** — ilk isteğin sonucuyla **aynı** (güncel form/durum; replay) | hiçbir şey (zaten ilerledi) |
| **Başkası ilerletti** (aynı gruptan iki kişi: Onayla ↔ Reddet) | version çakışması **veya** `ProcessStepInstance` zaten `actionTriggerDate` dolu | **409** `processAlreadyAdvanced` `{ currentExecutionState, activeProcessStepCode, actionTakenAt, actionTakenByDisplay? }` | "Bu kayıt az önce işlendi" + formu yenile |
| **Eski görünüm** (FE farklı adımı gösteriyor) | isteğin opsiyonel `expectedProcessStepInstanceId` ≠ aktif | **409** `staleView` (+ güncel durum) | formu yenile |
| **Aktör atanmamış** | `InstanceAwaitingUser`'da yok (grup üyeliği okuma-anı; vekalet dâhil) | **403** `notAssigned` | mesaj |
| **Aksiyon kodu adımda yok** | `ProcessStepAction` eşleşmez | **422** `unknownAction` | mesaj (tasarım hatası) |
| **Süreç bekliyor değil** (`running`/`failed`/`done`) | `executionState ≠ waiting(humanTask\|processing)` | **409** `notAwaitingAction` (+ durum) | mesaj + yenile |

- `actionTakenByDisplay` yalnız **aynı organizasyon** içinde ve yetki varsa döner (kişisel veri).
- Header yoksa replay yapılamaz → çift tıklama **409** alır (zararsız ama kötü UX) → zorunluluk Q17.

## 6. Hata & retry (flovo-bpm-engine §7 tie-in) — 📝 tam spec: [`engine-runtime-errors.md`](./engine-runtime-errors.md)
- **Sınıflandırma:** her deneme `stepCompleted` **ya da** `stepFailed{errorClass}` üretir — `transient` · `permanent` · `design` · `inDoubt` · `guard`
  (→ [`WorkflowErrorClass`](../../models/enums/workflow-error-class.md)). Yalnız **`transient`** yeniden denenir.
- **Retry:** BPM-düzeyi **`WorkflowTimer(kind=retry)`** + `suspended(waitReason=retry)` (JetStream NAK değil); varsayılan `5 deneme · 10 s ×3 · cap 600 s · jitter` (öneri Q7);
  adım-bazlı `retryPolicy` override (öneri). JetStream `MaxDeliver` yalnız worker crash-loop koruması.
- **`onFail` (opsiyonel):** kalıcı hata / retry tükendi → adımın `onFail` aksiyonu (hata `parameters.error` ile taşınır) → yoksa **`failed`** (dead-letter, `failed.v1`,
  süreç-yöneticisi bildirimi). Servis-düzeyi global hata adımı **post-MVP** (Q10); compensation **post-MVP** iskelet (Q11).
- **Kurtarma:** admin `retry` / `skip(actionCode)` / `cancel` — hepsi **olay** (`recovered` / `cancelled`); projeksiyon elle düzenlenmez.
- **Guard'lar:** ardışık otomatik adım 200 · toplam adım 10 000 · alt süreç derinliği 8 · senkron bekleme 3 · ServiceTrigger kaskadı 20 · worker turu 60 s → `failed(guard)` (Q13).

## 7. Timer & uyandırma — 📝 tam spec: [`engine-runtime-scheduler.md`](./engine-runtime-scheduler.md)
- **Zaman = tablo:** uyanması gereken her şey [`WorkflowTimer`](../../models/processInstances/workflow-timer.md)'da `armed` satırdır — `stepTimer` (Timer adımı / `timerStart`) ·
  `taskTimeout` (insan adımı timeout) · `retry` (backoff) · `serviceTriggerCron` (cron sonraki tetik).
- **Scheduler (durumsuz, replica-N):** her saniye dolan satırları **`FOR UPDATE SKIP LOCKED`** ile claim eder → aynı TX'te `timerFired` (+ `dispatch resume.v1`) → publish.
  **Lider seçimi gerekmez** (R7; at-most-once = satır kilidi + `messageId=timer:{id}`); advisory lock yalnız housekeeping (relay sweep · stuck detector · pruning).
- **Uygulama kuralı (R14):** timer yalnız süreç **`waiting`** iken uygulanır; `running` → `deferred (+30 s)`; `done` → `cancelled`. Tek aktif kol korunur.
  `timerStart` ile kurulmuş Timer, süreç **başka insan adımında** beklerken dolarsa o beklemeyi **kapatır** (preemption) ve Timer'ın `default` hedefine gider.
- **ServiceTrigger:** `timer` (cron) → scheduler saat dilimi (`FLOVO_SCHEDULER_TZ`, vars. `Europe/Istanbul` — org timezone alanı yok) ile önceden hesaplanmış `dueAt`;
  kaçırılan tetik **bir kez** yakalanır (Q15). `associate` → alt-süreç (→ [`models/service-settings/service-trigger.md`](../../models/service-settings/service-trigger.md));
  `async=false` runtime karşılığı **öneri:** tetikleyen süreç `waiting(subProcess)`, alt sürecin `ended`'i uyandırır (Q9).

## 8. Paralel dallanma & join (flovo-bpm-engine §4.5) — KARAR
- 🟩 **KARAR (MVP): tek aktif kol.** Bir `ProcessInstance`'ta **aynı anda tek aktif adım** ilerler (doğrusal/dallı yürüme; her
  aksiyon → tek hedef). Eşzamanlılık **ayrı `ProcessInstance`'larla** sağlanır: **Form List** alt-servisleri ServiceTrigger/
  `subProcessStart` ile **bağımsız süreçler** olarak koşar (ana süreçle paralel ama **ayrı** instance).
- 🟦 **ERTELENDİ:** Bir adımın **aynı anda birden çok sonraki adımı** tetiklemesi (fork) + **join/senkronizasyon** (n8n çok-girdili
  birleştirme muadili) — bu MVP'de **yok**; gerekirse ayrı tasarım → todo. Bu karar state machine'i **tek-konum** tutar (basit, kanıtlanabilir).

## 9. Kalıcılık & yaşam döngüsü (flovo-bpm-engine §8)
**Ne saklanır:**
| Katman | Nesne | İçerik |
|---|---|---|
| Süreç tanımı | `Service`/`ProcessStep`/`ProcessStepAction`/… | Tasarım (design-time; → [`settings-api.md`](../api/settings-api.md)) |
| Yürütme kaydı | `ProcessInstance` (+ `executionState`) · `ProcessStepInstance` zinciri | Kim/ne zaman/hangi adım/hangi aksiyon + biriken `ActionTransfer` |
| **Olay log (kaynak)** | **[`workflow_events`](../../models/processInstances/workflow-event.md)** (append-only, aylık RANGE partition) | Her geçiş (12 tip → [`WorkflowEventType`](../../models/enums/workflow-event-type.md)) + `version` + `messageId` + `dispatch` → replay + audit + idempotency + outbox |
| **Motor imleci (türetilmiş)** | [`workflow_projection`](../../models/processInstances/workflow-projection.md) (1–1) | `lastVersion` · `executionState`/`waitReason` · aktif adım · `attempt` · guard sayaçları · `lastError` |
| **Zamanlayıcı** | [`workflow_timer`](../../models/processInstances/workflow-timer.md) | `armed` uyandırma kayıtları (timer/timeout/retry/cron); fired/cancelled 30 gün |
| Askı kaydı | `InstanceAwaitingUser` | `waiting(humanTask)` iken kim aksiyon alabilir (dinamik grup) |
| Form değeri | `InstanceValue` (+ `InstanceAttr` projeksiyon) | Alan değerleri (§3.1) |
| İş durumu | `Instance.statusId` | Kullanıcının gördüğü durum (motordan ayrı) |

- **Yaşam döngüsü:** `new → running ⇄ waiting → done | failed → (recovered → running) | cancelled`; `workflow_events` **kaynak**, `executionState` + `workflow_projection` +
  `ProcessStepInstance` motor alanları + `InstanceAwaitingUser` + `workflow_timer` armed-seti **türetilmiş** (replay ile yeniden kurulabilir — Partial Event Sourcing; aynı TX'te yazılır).
- **Saklama / pruning / KVKK** → 📝 [`engine-runtime-retention.md`](./engine-runtime-retention.md): sıcak 3 ay → soğuk 21 ay → MinIO arşiv 10 yıl (öneri Q18) → partition drop;
  KVKK silme hakkı = **pseudonymization** (tombstone user; aktör kolonları + payload yolları) — hukuki karar Q19.

## 10. Ölçekleme & çok-kiracılık
- **Yatay ölçek:** worker'lar durumsuz → JetStream consumer'ları **eklenerek** ölçeklenir (lag büyürse worker ekle).
- **İzolasyon:** her tablo `organizationId` + **RLS** (Pattern B v2); NATS **tenant-bazlı account**; partition `HASH(service_id)`
  (postgresql.md). Bir kiracının yükü diğerini görmez.
- **On-prem/bulut:** K8s/Helm; worker `Deployment` (replica-N), scheduler `Deployment` (replica-N, Postgres claim — lider yok). → [`tech-stack/kubernetes-helm.md`](../../tech-stack/kubernetes-helm.md).

## 11. Açık noktalar
📝 **v0.44:** bu konunun tüm kararları (R1–R17) ve açık soruları (Q1–Q22) **inceleme süresince** → [`engine-runtime-plan.md`](./engine-runtime-plan.md);
kesinleşince kalanlar [`todo.md`](../../todo.md)'ye taşınır. Bu turda **dokümanla karşılanan** eski açık noktalar: `workflow_events`/`workflow_projection` model dosyaları ·
retry politika değerleri · global hata yakalayıcı (post-MVP kararı) · compensation (post-MVP iskelet) · scheduler lider-seçim (claim modeliyle gereksiz) ·
`timer` DST/TZ · `async` kaskad derinlik sınırı (guard) · pruning/KVKK · optimistic-concurrency çakışma UX'i. **Fork/join** ertelendi (Q22 teyit).

---

*Oluşturma: 2026-08-28. flovo-bpm-engine §2.2/§8/§4.5 doldurma. Güncelleme: 2026-08-31 (v0.44) — iki-TX adım · outbox-in-event · 409 sözleşmesi · projeksiyon/timer modelleri · alt-doküman ailesi.*
