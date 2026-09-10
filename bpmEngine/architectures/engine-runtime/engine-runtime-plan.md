# Motor Runtime — Açık Sorular & Geliştirme Planı (çalışma dosyası)

> **Durum:** 🟡 AÇIK — v0.44 çalışma dosyası. **Çalışma-zamanı mimarisi** konusunun (todo Tier 1 "Çalışma-zamanı mimarisi" + bağlı kalemler) tüm
> **kararları (R)**, **açık soruları (Q)** ve **geliştirme planını** tek yerde tutar. Kullanıcı incelemesi → geri bildirim → dokümanlar güncellenir →
> kararlar kesinleşince **todo.md güncellenir** (o zamana dek todo'ya dokunulmaz — kullanıcı kararı).
>
> **Kural hatırlatması:** kalıcı açık-soru listesi **`todo.md`**'dir; bu dosya konu-odaklı **geçici çalışma alanı**dır. Kapanınca kararlar ilgili dokümanların
> gövdesine, kalan sorular todo'ya taşınır; bu dosya `commitNotes/`'a atıfla arşivlenir.

---

## 0. Doküman haritası (bu konu için ne nerede)
| Doküman | Rol | Durum |
|---|---|---|
| [`engine-runtime.md`](./engine-runtime.md) | Runtime mimarisi **ana spec** (state machine · bileşenler · akış · idempotency · ölçek) | 🟢 v0.40 + 📝 v0.44 güncellemeleri |
| [`engine-runtime-errors.md`](./engine-runtime-errors.md) | Hata sınıfları · retry · in-doubt · onFail · dead-letter · kurtarma · guard'lar · compensation | 📝 YENİ v0.44 — onay bekliyor |
| [`engine-runtime-scheduler.md`](./engine-runtime-scheduler.md) | Scheduler claim modeli · WorkflowTimer yaşam döngüsü · timeout/stepTimer/retry/cron · TZ/DST · housekeeping | 📝 YENİ v0.44 — onay bekliyor |
| [`engine-runtime-retention.md`](./engine-runtime-retention.md) | Saklama katmanları · partition/arşiv · KVKK pseudonymization · kısa-ömürlü tablolar | 📝 YENİ v0.44 — onay bekliyor |
| [`models/processInstances/workflow-event.md`](../../models/processInstances/workflow-event.md) | `WorkflowEvent` (`workflow_events`) — kaynak günlük + idempotency + version + outbox-in-event | 📝 YENİ v0.44 |
| [`models/processInstances/workflow-projection.md`](../../models/processInstances/workflow-projection.md) | `WorkflowProjection` — motor imleci (lastVersion · state · waitReason · attempt · guard sayaçları) | 📝 YENİ v0.44 |
| [`models/processInstances/workflow-timer.md`](../../models/processInstances/workflow-timer.md) | `WorkflowTimer` — zamanlanmış uyandırma (4 tür) | 📝 YENİ v0.44 |
| Enum'lar: [`workflow-event-type`](../../models/enums/workflow-event-type.md) · [`workflow-wait-reason`](../../models/enums/workflow-wait-reason.md) · [`workflow-timer-kind`](../../models/enums/workflow-timer-kind.md) · [`workflow-timer-status`](../../models/enums/workflow-timer-status.md) · [`workflow-error-class`](../../models/enums/workflow-error-class.md) | | 📝 YENİ v0.44 |
| [`models/enums/process-execution-state.md`](../../models/enums/process-execution-state.md) | `cancelled` değeri eklendi (öneri Q6) | 📝 güncellendi |
| [`research/engine-runtime/motor-runtime-v0-44-ozet-detay.html`](../../research/engine-runtime/motor-runtime-v0-44-ozet-detay.html) | **Özet + detay HTML anlatımı** (inceleme/sunum yardımcısı; bağlayıcı değil — dokümanlar esas) → [`research/engine-runtime/index.md`](../../research/engine-runtime/index.md) | 📝 anlatım (2026-09-01) |
| [`research/engine-runtime/motor-mimari-semasi-v0-45.html`](../../research/engine-runtime/motor-mimari-semasi-v0-45.html) | **Metot-düzeyi mimari şeması** (çağrı ağacı · 3 akış · metot × tablo matrisi) — **öneri**; **R18 inline devam + Q23** adayı burada doğdu (plana işlenmesi bekliyor) | 📝 öneri (2026-09-01) |
| Güncellenen mevcutlar | `flovo-bpm-engine.md §7` · `process-step-action.md §5` · `process-instance.md` · `process-step-instance.md` · `scheduler-job.md` · `service-trigger.md` · `process-step.md §3.7` · `flovo-customer-api.md` · `tech-stack/postgresql.md` · `tech-stack/nats-jetstream.md` · indeksler | 📝 v0.44 |

---

## 1. İnceleme rehberi (kullanıcı için)
Önerilen okuma sırası: **workflow-event.md → workflow-projection.md → engine-runtime.md (§1, §4, §5) → errors → scheduler + workflow-timer → retention**.
Her dokümanda **📝 / 🟦 öneri** işaretli yerler karar bekler; bu dosyadaki **R** numaralarıyla eşleşir. Geri bildirim biçimi (öneri): `R4: kabul` · `Q7: maxAttempts 8 olsun` ·
`workflow-event §2 stepFailed.detail 4 KB` — dokümanlar buna göre güncellenir, §5 review log'a işlenir.

---

## 2. Kararlar — bu turda **önerilen** (onay bekliyor)
> Her satır: **öneri** · gerekçe · alternatif(ler) · etkilenen dokümanlar. Onaylanınca "✅" işareti + tarih; reddedilince alternatife dönüş.

| # | Karar (öneri) | Gerekçe | Alternatif | Etki |
|---|---|---|---|---|
| **R1** | **`WorkflowEvent` modeli**: 12 olay tipi (`startRequested · stepStarted · stepCompleted · stepSkipped · suspended · actionTaken · timerFired · stepFailed · failed · recovered · cancelled · ended`), `version` süreç-başına monoton, `messageId` UNIQUE, `causationId`/`correlationId` | state machine'in her kenarı bir olay; audit + replay + idempotency tek tabloda | daha az tip (6: engine-runtime v0.40 listesi) — retry/skip/kurtarma görünmez kalır | workflow-event.md · enum |
| **R2** | **Payload = `ActionTransfer` tam snapshot** (kaynak); `ProcessStepInstance.processStepActionParameter` = okuma kopyası | replay değişebilir tablolara bağımlı olmasın; paket küçük | payload'da yalnız PSI referansı (tek kopya, replay PSI'ya bağımlı) | workflow-event §2/§7 · process-step-instance.md |
| **R3** | **Aktör kolonda** (`actorUserId/actorApiKeyId/actorDelegateUserId`), payload'da değil | KVKK anonimleştirme kolon-hedefli, indekslenebilir | payload içinde | workflow-event · retention §4 |
| **R4** | **Otomatik adım = iki TX** (`stepStarted` → yan etki → `stepCompleted/stepFailed`); in-doubt kuralı | yan etkinin (HTTP POST) ikinci kez koşmasını görünür kılar | tek TX (basit; çift POST riski) | workflow-event §3.2 · errors §3 · engine-runtime §4.2 |
| **R5** | **Outbox-in-event**: `dispatch` + `publishedAt` kolonları; ayrı workflow outbox tablosu yok; relay sweep | commit↔publish boşluğu kapanır; `InstanceValueOutbox` ile aynı ilke, ekstra tablo yok | ayrı `workflow_outbox` tablosu · publish-önce-commit (kayıp riski) | workflow-event §3.5 · scheduler §7 |
| **R6** | **`WorkflowProjection` ayrı tablo** (sıcak imleç); `ProcessInstance.executionState` **kopya** kalır | sıcak satır izolasyonu + rebuild kolaylığı + liste join'siz | yalnız `ProcessInstance` kolonları · yalnız projeksiyon (Q5) | workflow-projection.md · process-instance.md |
| **R7** | **`WorkflowTimer` tek tablo (4 tür)** + scheduler **Postgres claim (`FOR UPDATE SKIP LOCKED`)** → **lider seçimi gerekmez**; advisory lock yalnız housekeeping | at-most-once satır kilidiyle; yatay ölçek; ek altyapı yok | NATS KV lock · Postgres advisory lock ile tek lider (build-plan §6.4 önerisi) | workflow-timer.md · scheduler §1/§7 · engine-runtime §2/§7/§10 |
| **R8** | **Retry = BPM-düzeyi `WorkflowTimer(kind=retry)`**, JetStream NAK-delay değil; `MaxDeliver` yalnız crash-loop koruması | dayanıklı + görünür + timer'la aynı mekanizma | JetStream NAK + backoff (görünmez, stream'e bağlı) | errors §2.3 · nats-jetstream.md |
| **R9** | **`onFail` opsiyonel**; sıra: adım `onFail` → (post-MVP global) → **`failed`**; `guard` doğrudan `failed` | build-plan §6.5 ile uyumlu; MVP basit | `onFail` zorunlu (designer yükü) | errors §4–§5 · flovo-bpm-engine §7 |
| **R10** | Hata bilgisi `onFail`'e **`ActionTransfer.parameters.error`** rezerve anahtarıyla taşınır | no-code erişim (Değer Atama `parameters.error.message`) | ayrı alan / taşınmaz | errors §4.1 · action-transfer.md (not) |
| **R11** | **Kurtarma = olay** (`recovered{retry\|skip}` · `cancelled`); projeksiyon elle düzenlenmez; `retry now` | audit bütünlüğü | admin doğrudan state düzeltir | errors §6 · enum |
| **R12** | **Compensation post-MVP**; iskelet (`compensationProcessStepId`, ters sırada compensation kolu) şimdiden tanımlı | build-plan §6.3 | MVP'ye al | errors §8 |
| **R13** | **`waiting` tek durum + `waitReason`** (`humanTask/processing/timer/retry/subProcess`); ayrı `retrying` state yok | enum küçük, listeler `waitReason` ile ayrışır | `retrying` ayrı `executionState` | workflow-projection · enum wait-reason · process-execution-state |
| **R14** | **Timer uygulaması yalnız `waiting`'de**; `running` → `deferred` (+30 s); `done` → cancel | tek aktif kol korunur | timer fire'ı kuyruğa al ve otomatik zincir bitince uygula (eşdeğer, daha karmaşık) | scheduler §4.1 · workflow-timer §2 |
| **R15** | **Aksiyon çakışma sözleşmesi**: `Idempotency-Key` ile **200 replay** · başkası ilerletmiş → **409 `processAlreadyAdvanced`** (+ güncel durum) · atanmamış → **403 `notAssigned`** · FE eski görünüm → **409 `staleView`** (opsiyonel `expectedProcessStepInstanceId`) | double-click ile gerçek yarışı ayırır; FE tek mesaj + yenile | her çakışma 409 | engine-runtime §5.2 · flovo-customer-api.md |
| **R16** | **Retention: aylık RANGE partition → detach (soğuk) → MinIO JSONL.gz arşiv (object-lock) → drop**; **KVKK = pseudonymization** (tombstone user; kolon + payload yolları; arşivde read-time redaction) | append-only korunur, DELETE yok; denetim izi ↔ silme hakkı uzlaşır | satır silme · anonimleştirme yok | retention · workflow-event §4/§7 |
| **R17** | **Guard limitleri**: ardışık otomatik adım **200** · toplam adım **10 000** · alt süreç derinliği **8** · senkron bekleme derinliği **3** · ServiceTrigger kaskadı **20** · worker turu **60 s** — sistem konfig | sonsuz döngü + kaskad korumaları tek yerde; todo "aksiyon zinciri sonsuz döngü" + ServiceTrigger (2)(3) kapanır | org-bazlı limit | errors §7 · workflow-projection |

---

## 3. Açık sorular (karar bekliyor) — örnekli
> **Öncelik:** 🔴 Faz 1 yazımını bloklar · 🟠 Faz 1 içinde netleşmeli · 🟢 sonra / post-MVP. Her soru: bağlam · **öneri** · örnek.

### 3.1 Model (WorkflowEvent · Projection · Timer)
- [ ] **Q1 🟠 Fiziksel tablo adı** — yerleşik `workflow_events` (çoğul; 10+ dokümanda) ↔ konvansiyon `workflow_event` (model adının snake_case'i).
  **Öneri:** konvansiyona uy (`workflow_event`), dokümanlardaki `workflow_events` ifadesini bir geçişte düzelt. _(workflow-event §0)_
- [ ] **Q2 🟠 Partition stratejisi** — `RANGE(occurredAt)` aylık (saklama = drop) ↔ değer tablolarıyla aynı `HASH(service_id)`.
  **Öneri:** RANGE — olay tablosu zamanla yaşlanır; örnek: 24 ay sonra Ocak-2027 partition'ı tek `DROP` ile gider, 3 GB DELETE yok. _(workflow-event §4 · retention §3)_
- [ ] **Q3 🟠 `stepFailed.payload.detail` boyutu ve ham gövde** — JSONB'de özet ≤ **2 KB**; ham HTTP response MinIO'ya (kısa retention) mı, hiç mi?
  **Öneri:** ≤ 2 KB özet + `debugCapture` bayrağı açık adımlarda 7 gün MinIO. Örnek: ERP 422 gövdesi 40 KB XML → JSONB'ye girmez. _(workflow-event §2 · retention §4.3)_
- [ ] **Q4 🟢 `correlationId` semantiği** — kök = **host** zinciri (`parentProcessInstanceId`, v0.24 kararı) mı, **tetikleyen** süreç mi?
  **Öneri:** host zinciri (mevcut kararla tutarlı); tetikleyen bilgisi `startRequested.payload`'da. Örnek: kredi kartı ekstre satırı alt süreci → kök = masraf formunun ana süreci. _(workflow-event §1)_
- [ ] **Q5 🟠 `executionState` kopyası** `ProcessInstance`'ta kalsın mı? **Öneri:** kalsın (liste join'siz; aynı TX). _(workflow-projection §0)_
- [ ] **Q6 🔴 `ProcessExecutionState.cancelled`** eklensin mi? Kurtarma `cancel` için gerekli. **Öneri:** evet (6. değer). Alternatif: `done` + payload `endType=cancelled` (yanıltıcı). _(process-execution-state.md)_

### 3.2 Hata & dayanıklılık
- [ ] **Q7 🔴 Retry varsayılanları + `ProcessStep.retryPolicy` kolonu** — `maxAttempts 5 · 10 s ×3 · cap 600 s · jitter ±20 %` (≈ 6,7 dk) yeterli mi? Adım-bazlı override **ortak JSONB kolon** olsun mu?
  Örnek: ERP gece bakımı 30 dk → HTTP Request adımına `retryPolicy {maxAttempts: 8, maxDelaySeconds: 900}`. **Öneri:** değerler kabul + kolon eklensin. _(errors §2)_
- [ ] **Q8 🟠 JetStream `MaxDeliver`** = 3 ve aşımı → `failed(inDoubt)`; ack-wait süresi (öneri 90 s > worker turu 60 s). _(errors §2.3 · nats-jetstream.md)_
- [ ] **Q10 🟠 Servis-düzeyi global hata adımı** (`Service.onFailProcessStepId`) — MVP mi post-MVP mi? Örnek: tüm HTTP hataları "Admin'e bildir → Admin Kullanıcı adımı"na gitsin, her adıma `onFail` bağlamadan.
  **Öneri:** post-MVP (build-plan §6.5); iskelet errors §4'te. _(errors §4)_
- [ ] **Q11 🟢 Compensation iskeleti** (`compensationProcessStepId`, ters sıra) kabul mü? **Öneri:** kabul, tasarım post-MVP. _(errors §8)_
- [ ] **Q12 🟠 Kurtarma yetkisi** — kim `retry/skip/cancel` yapar? **Öneri:** yeni org yetkisi `processAdminUserGroupId` (permissions genişletilebilirlik sorusuyla birlikte: yeni yetki = Organization'a yeni `*UserGroupId`). KVKK silme-hakkı işlemi de aynı yetki mi, ayrı mı? _(errors §6 · retention §5 · permissions §5)_
- [ ] **Q13 🟠 Guard limit değerleri** (R17) — 200 / 10 000 / 8 / 3 / 20 / 60 s. Örnek: Switch→Değer Atama→Switch döngüsü 200 adımda `failed(guard)`; kullanıcı formu "süreç hatası" görür. _(errors §7)_
- [ ] **Q21 🟠 İdempotent adım listesi + HTTP `idempotencyKeyHeader`** — in-doubt'ta hangi adımlar güvenle tekrar koşar? HTTP Request `settings`'e `idempotencyKeyHeader` (ör. `Idempotency-Key`) eklensin mi? _(errors §3 · process-step-settings/http-request.md)_

### 3.3 Zamanlayıcı & uyandırma
- [ ] **Q14 🟠 `deferred` politikası** — +30 s, üst sınır 20 (alarm, devam). Süreç günlerce `running`'de takılı kalsa (bug) timer ne olur? **Öneri:** stuck detector devreye girer; timer denemeye devam eder. _(scheduler §4.1)_
- [ ] **Q15 🟠 Cron TZ/DST/kaçırma** — `FLOVO_SCHEDULER_TZ=Europe/Istanbul` (org alanı yok — v0.33); DST standart semantik; kaçırılan tetik **bir kez** yakala, `> 24 h` ise atla; en sık **1 dk**.
  Örnek: her Pazartesi 09:00 rapor süreci; sistem Pzt 08:00–11:00 kapalı → 11:00'de **bir** süreç başlar. _(scheduler §5 · service-trigger.md)_
- [ ] **Q16 🟢 Süre hesabı sabitlenmesi** — `workCalendar` `dueAt` kurulumda hesaplanır, takvim değişse yeniden hesaplanmaz; takvim = **organizasyonun** (atananın kişisel takvimi değil). _(scheduler §6)_
- [ ] **Q20 🟠 Lider-seçim teyidi** — `SKIP LOCKED` claim ile lider gereksiz (R7); advisory lock yalnız housekeeping. todo'daki "NATS KV ↔ Postgres advisory" ikilemi bu kararla **kapanır** — teyit. _(scheduler §1)_
- [ ] **Q9 🟠 ServiceTrigger `async=false` runtime karşılığı** — "tetiklendiği yerde bekler" (v0.25) event-driven motorda **worker bloke edemez**. **Öneri:** tetikleyen süreç `suspended(waitReason=subProcess, waitingForProcessInstanceId)`; alt sürecin `ended` olayı uyandırır (tek-çocuk join). Tetik **API isteğinden** geliyorsa (ilişki yazımı FE'den) istek en fazla N s bekler, sonra **202 pending** döner. Örnek: masraf formuna kart satırı eklendi → `whenAddedAssociate` alt süreci `async=false` → ana süreç `waiting(subProcess)`, alt süreç bitince devam. _(service-trigger.md · workflow-wait-reason · workflow-projection §5)_

### 3.4 Eşzamanlılık & API
- [ ] **Q17 🟠 `Idempotency-Key` zorunlu mu?** FE her tıklamada UUID üretir; header yoksa replay yok (çift tıklama 409 alır). **Öneri:** Customer API'de **zorunlu**, FE'de zorunlu. `expectedProcessStepInstanceId` opsiyonel. _(engine-runtime §5.2)_

### 3.5 Saklama & KVKK
- [ ] **Q18 🟠 Retention süreleri + org politikası** — sıcak 3 ay · soğuk 21 ay · arşiv **10 yıl** (TTK 82 hizası — **hukuk teyidi**); `Organization.retentionPolicy` alanı eklensin mi? _(retention §2)_
- [ ] **Q19 🔴 (hukuki) Silme hakkı ↔ denetim izi** — pseudonymization (tombstone) kabul edilebilir mi; arşivde read-time redaction yeterli mi; `nameSurname` snapshot'ları için payload yol listesi bakımı kimde? _(retention §4)_

### 3.6 Ertelenen (teyit)
- [ ] **Q22 🟢 Fork/join** — MVP "tek aktif kol" kalır; Q9 (`subProcess` bekleme) tek-çocuk join'dir ve fork/join'e **kapı açmaz**. Teyit edilince todo maddesi "ertelendi (post-MVP)" olarak kapanır. _(engine-runtime §8)_

---

## 4. Geliştirme planı (dokümantasyon — build-plan F1.A/B/C eşlemesi)
| Adım | İş | build-plan | Bağımlılık | Durum |
|---|---|---|---|---|
| **P1** | `WorkflowEvent` + `WorkflowProjection` + enum'lar (model) | F1.A.1 · F1.A.2 | — | 📝 taslak yazıldı (v0.44) → **inceleme** |
| **P2** | `engine-runtime.md` §1/§2/§4/§5/§9 güncelleme (iki-TX, outbox-in-event, 409 sözleşmesi, projeksiyon) | F1.A | P1 | 📝 yazıldı |
| **P3** | Hata & dayanıklılık spec (`engine-runtime-errors.md`) | F1.B.1–B.4 | P1 | 📝 yazıldı |
| **P4** | Scheduler & `WorkflowTimer` (`engine-runtime-scheduler.md` + model) | F1.C.1 (+ timer beklemesi) | P1 | 📝 yazıldı |
| **P5** | Retention/KVKK (`engine-runtime-retention.md`) | (todo denetim izi/loglama — runtime kolu) | P1 | 📝 yazıldı |
| **P6** | **Kullanıcı incelemesi** → R/Q kararları → dokümanlara işleme (bu dosya §5) | — | P1–P5 | ⬜ **sıradaki** |
| **P7** | Onaylanan model değişiklikleri: `process-step.md` `retryPolicy` (Q7) · `service.md` `onFailProcessStepId` (Q10, post-MVP işareti) · `organization.md` `retentionPolicy` (Q18) · permissions `processAdminUserGroupId` (Q12) · http-request `idempotencyKeyHeader` (Q21) | F1.B / F1.E | P6 | ⬜ |
| **P8** | Customer API: `POST …/actions/{code}` 409/403/200-replay şeması + `Idempotency-Key`; admin `recover` ucu; KVKK `erasure` ucu | F2.G / Customer API | P6 | ⬜ |
| **P9** | `todo.md` güncellemesi (çözülenler → commitNotes; kalanlar tek satır) + `bpm-engine-build-plan.md` durum panosu | — | P6–P8 | ⬜ (kullanıcı kararı: en sonda) |
| **P10** | Grup D (adım-içi yürütme spec'leri) yazımına geçiş — bu konu kapanmış olur | F1.D | P9 | ⬜ |

**DoD (bu konu için):** R1–R17 karara bağlandı · Q1–Q22 kapatıldı veya todo'ya taşındı · `engine-runtime*.md` + 3 model + 5 enum 🟢 · build-plan F1.A.1/A.2/B.1–B.4/C.1 ✅.

---

## 5. Review log (kullanıcı geri bildirimi → değişiklik)
| Tarih | Geri bildirim | Uygulanan değişiklik | Dosyalar |
|---|---|---|---|
| 2026-08-31 | — (ilk taslak seti oluşturuldu) | — | — |

---

*Oluşturma: 2026-08-31 (v0.44).*
