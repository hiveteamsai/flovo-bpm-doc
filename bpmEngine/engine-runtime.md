# Flovo BPM Motoru — Runtime Mimarisi (orkestrasyon ↔ yürütme · durum · kalıcılık)

> **Durum:** 🟢 Tasarım (v0.40). **Amaç:** Motorun **sistem olarak nasıl koştuğunu** tanımlar — [`flovo-bpm-engine.md`](./flovo-bpm-engine.md)
> §4.4'teki **senkron** yürütme döngüsünü, karar verilen yığın üzerinde (**Go stateless worker + NATS JetStream + PostgreSQL Partial
> Event Sourcing**) **event-driven, kalıcı, kaldığı yerden devam eden** bir mimariye çevirir. Bu doküman `flovo-bpm-engine.md`
> **§2.2 (orkestrasyon↔yürütme)** · **§8 (kalıcılık/durum)** · **§4.5 (paralel dallanma)** bölümlerini **doldurur**.
>
> **Yığın:** [`tech-stack/go.md`](./tech-stack/go.md) (Hexagonal, goroutine) · [`tech-stack/nats-jetstream.md`](./tech-stack/nats-jetstream.md)
> (job/olay omurgası) · [`tech-stack/postgresql.md`](./tech-stack/postgresql.md) (`workflow_events` append-only + durum).
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

- **`ProcessInstance.executionState`** (YENİ alan) = `new` · `running` · `waiting` · `failed` · `done`
  (→ [`models/enums/process-execution-state.md`](./models/enums/process-execution-state.md)). Bu, **`workflow_events`'ten türetilen bir
  projeksiyondur** (hızlı sorgu: "koşan/bekleyen/hatalı süreçler"); kaynak-hakikat olay log'udur.
- **Mevcut konum** = o instance'ın **en güncel aktif `ProcessStepInstance`**'ı (`processStepId` = aktif adım).
- **Askı kaydı** = `waiting` iken **`InstanceAwaitingUser`** (kim aksiyon alabilir) + timer bekleniyorsa scheduler kaydı.
- **Biriken parametreler** = son `ProcessStepInstance.processStepActionParameter` (**`ActionTransfer`** JSON: `parameters`/`changeList`/`action`).

> **KARAR:** Motor yürütme-durumu **`Instance.statusId`'ye karıştırılmaz.** `statusId` = kullanıcının gördüğü **iş durumu**
> (Onay Bekliyor, Reddedildi…); `executionState` = **motorun** iç konumu. İkisi bağımsız evrilir.

## 2. Bileşenler (orkestrasyon ↔ yürütme)
| Bileşen | Rol | Durum |
|---|---|---|
| **Worker** (Go, goroutine havuzu) | JetStream'den **step-ready** iş çeker, **tek adımı** koşar, durum yazar, sonrakini enqueue eder | **Durumsuz** (yatay ölçek) |
| **Orkestratör** (mantıksal) | Aksiyon→sonraki-adım çevirimi, **uyandırma** (timer/olay), **at-most-once** (idempotency), retry/backoff | Worker içinde + scheduler |
| **NATS JetStream** | İş kuyruğu + olay omurgası (`FLOVO_EVENTS`, durable consumer, `Nats-Msg-Id`) | Kalıcı, sıralı, replay |
| **PostgreSQL** | `workflow_events` (append-only kaynak) + durum projeksiyonu + `ProcessInstance`/`ProcessStepInstance`/`InstanceAwaitingUser` + `InstanceValue` | Kaynak-hakikat |
| **Scheduler** (lider-seçimli tek) | Timer/`SchedulerJob` süreleri dolunca **uyandırma olayı** üretir | Tekil (leader) |

> **Orkestrasyon↔yürütme ayrımı:** *durum DB'de, kuyruk yalnız iş/olay taşır, worker'lar durumsuz* (n8n dersi 1–2). Bir worker
> çökse başka worker aynı işi devralır (JetStream redelivery + idempotency); iş **kaybolmaz**.

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
Worker bir `step_ready` işini çeker ve **tek adımı** koşar:
1. **Yükle:** `ProcessInstance` + aktif adım tasarımı (`ProcessStep.settings`) + form değeri (`InstanceValue`) + gelen `ActionTransfer`.
2. **Evrensel giriş kuralı (§4.2):** gelen `changeList` boş değilse forma **merge** (aynı TX; write-path → §3.1 · [`tech-stack/postgresql.md`](./tech-stack/postgresql.md)).
3. **İşi yap:** adım tipine göre (HTTP Request, Karşılaştırma, Switch, Değer Atama, Timer…) — tipe-özel `settings` şeması →
   [`models/service-settings/jsonTemplateModels/process-step-settings/`](./models/service-settings/jsonTemplateModels/process-step-settings/index.md).
4. **Aksiyon seç:** sonucu bir **aksiyon koduna** eşle (`true`/`false`/`default`/response.action) → o kodlu `ProcessStepAction`.
5. **Kalıcılaştır (tek TX):** `ProcessStepInstance` (executionDate + üretilen `processStepActionParameter`) + `workflow_events`
   (StepCompleted, `version++`) + varsa `InstanceValue`/outbox. **Atomik.**
6. **İlerlet:** seçilen aksiyonun `targetProcessStepId`'si için **yeni `step_ready`** enqueue (`mergeParameter` ise gelen+üretilen
   birleşir → §4.4 pseudo). Terminal otomatik adım (giden aksiyon yok) → kol biter (§4.4 `break`).

> **Hız:** Bir worker turu = birkaç küçük Postgres yazımı + bir NATS publish; ağır iş (HTTP Request) adımın kendi içinde.

### 4.3 İnsan / bekleme adımı (SUSPEND)
Adım **Kullanıcı / Kullanıcı Grubu / Üst Form Kullanıcı** ise (veya **Processing** `autoAction`'sız, **Timer** beklemesi):
1. Worker **atananı çöz** (`userType`/`userGroupType`) → **`InstanceAwaitingUser`** kayıtlarını **senkronla** (ekle/sil).
2. `workflow_events` (Suspended) + `ProcessInstance.executionState=waiting` yaz; **`suspended.v1`** yayınla (FE "aksiyon bekliyor").
3. **Worker serbest** — kuyrukta iş kalmaz. Süreç **günlerce** bu durumda durabilir (kaynak tutmaz).

> **Atama çözülemezse** → hata/`onFail` (§6). **Adım atlama** (`skipIfPreApproved`/`skipIfUserProcessStarter`) → beklemeye geçmeden
> `skipWithThisProcessStepActionId` otomatik tetiklenir (§4.4).

### 4.4 Devam (RESUME)
Bir **dış olay** süreci uyandırır:
- **Kullanıcı aksiyonu:** `POST /instances/{id}/actions/{code}` (→ [`flovo-customer-api.md`](./flovo-customer-api.md)) → aktör
  **`InstanceAwaitingUser`'a karşı doğrulanır** (grup üyeliği okuma-anı; ilk aksiyon ilerletir — grup eşiği yok).
- **Timer:** scheduler süre dolunca `resume.v1` yayınlar (§7).
- **Webhook/Processing:** dış çağrı `resume.v1` tetikler.

Uyandırmada: `ProcessStepInstance` **aksiyon alanları** dolar (`atUserId`/`atApiKeyId` · `actionTriggerDate` · `processStepActionId` ·
`processStepActionParameter` = taşınan `ActionTransfer` · vekaletse `atDelegateUserId`) + `workflow_events` (ActionTaken) yazılır →
`executionState=running` → seçilen aksiyonun hedefi için **yeni `step_ready`** enqueue. **Form bilgisi** aksiyon isteğinin
**response'unda** döner (§6.3 — beş form-döndüren adım).

### 4.5 Bitiş
**Süreç Bitişi** / **Alt Süreç Bitişi** → `workflow_events` (Ended) + `executionState=done`. Ana süreçte yetkililer sonradan
erişebilir/geri-taşıyabilir (`processEnd.userGroupIds`); alt süreçte geri-taşıma yoktur.

## 5. Idempotency & at-most-once
- **`Nats-Msg-Id` + olay `version`:** Her `step_ready`/`resume` işi bir mesaj-id taşır; worker işlemeden önce `workflow_events`'in
  o instance için **son version**'ını kontrol eder → **zaten ilerlemişse atla** (nats-jetstream.md idempotency deseninin aynısı).
  Böylece **at-least-once teslim + redelivery + sırasız** süreci **iki kez ilerletmez**.
- **Aksiyon idempotency:** aynı `ProcessStepInstance`'a iki kez aksiyon (double-click / retry) → ilk ActionTaken kazanır, ikincisi
  version uyuşmazlığıyla reddedilir (optimistic concurrency).

## 6. Hata & retry (flovo-bpm-engine §7 tie-in)
- **Adım hatası:** `workflow_events` (StepFailed) → adımın **`onFail` kodlu aksiyonu** varsa o dala yönlendir (§7.1).
- **Retry (altyapı):** geçici hata (HTTP 5xx, DB lock) → **JetStream redelivery** + **BPM-düzeyi max-deneme + backoff**; tükenirse
  **dead-letter** (`failed.v1`) → `executionState=failed`.
- 🟦 **AÇIK:** her adımda `onFail` zorunlu mu · **süreç-seviye global hata yakalayıcı** · telafi/compensation · retry politika değerleri → todo (Hata yönetimi).

## 7. Timer & uyandırma
- **Scheduler (lider-seçimli tek instance):** aktif timer'ları/`SchedulerJob`'ları izler; süre dolunca `resume.v1` yayınlar →
  ilgili süreç uyanır. Lider seçimi = **en-fazla-bir-kez** tetikleme (çok-örneklilikte tek scheduler; NATS/DB lider kilidi).
- **ServiceTrigger:** `timer` (cron) → yeni bağımsız ana süreç; `associate` → alt-süreç (→ [`models/service-settings/service-trigger.md`](./models/service-settings/service-trigger.md)).
- 🟦 **AÇIK:** `timer` DST/saat-dilimi · scheduler lider-seçim mekanizması (NATS KV lock vs Postgres advisory lock) · `async` kaskad derinlik sınırı → todo.

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
| Süreç tanımı | `Service`/`ProcessStep`/`ProcessStepAction`/… | Tasarım (design-time; → [`settings-api.md`](./settings-api.md)) |
| Yürütme kaydı | `ProcessInstance` (+ `executionState`) · `ProcessStepInstance` zinciri | Kim/ne zaman/hangi adım/hangi aksiyon + biriken `ActionTransfer` |
| **Olay log (kaynak)** | **`workflow_events`** (append-only) | Her geçiş (Start/StepCompleted/Suspended/ActionTaken/Failed/Ended) + `version` → replay + audit + saga |
| Askı kaydı | `InstanceAwaitingUser` | `waiting` iken kim aksiyon alabilir (dinamik grup) |
| Form değeri | `InstanceValue` (+ `InstanceAttr` projeksiyon) | Alan değerleri (§3.1) |
| İş durumu | `Instance.statusId` | Kullanıcının gördüğü durum (motordan ayrı) |

- **Yaşam döngüsü:** `new → running ⇄ waiting → done/failed`; `workflow_events` **kaynak**, `executionState` + `workflow_projection`
  **türetilmiş** (replay ile yeniden kurulabilir — Partial Event Sourcing).
- 🟦 **AÇIK (pruning/saklama):** tamamlanan süreçlerin `workflow_events` **saklama süresi / arşiv / KVKK** → todo (denetim izi/loglama).

## 10. Ölçekleme & çok-kiracılık
- **Yatay ölçek:** worker'lar durumsuz → JetStream consumer'ları **eklenerek** ölçeklenir (lag büyürse worker ekle).
- **İzolasyon:** her tablo `organizationId` + **RLS** (Pattern B v2); NATS **tenant-bazlı account**; partition `HASH(service_id)`
  (postgresql.md). Bir kiracının yükü diğerini görmez.
- **On-prem/bulut:** K8s/Helm; worker `Deployment` (replica-N), scheduler tek (leader). → [`tech-stack/kubernetes-helm.md`](./tech-stack/kubernetes-helm.md).

## 11. Açık noktalar (→ [`todo.md`](./todo.md))
`workflow_events`/`workflow_projection` **model dosyaları** (henüz yalnız tech-stack'te kavram) · retry politika değerleri +
global hata yakalayıcı + compensation · scheduler **lider-seçim** mekanizması · `timer` DST · `async` kaskad derinlik sınırı ·
**fork/join** (ertelendi) · `workflow_events` **pruning/KVKK** · optimistic concurrency çakışma UX'i.

---

*Oluşturma: 2026-08-28. flovo-bpm-engine §2.2/§8/§4.5 doldurma.*
