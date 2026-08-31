# Model — WorkflowProjection (`workflow_projection` — türetilmiş yürütme durumu / motor imleci)

> **Durum:** 📝 TASLAK v0.44 — **onay bekliyor** (→ [`../../engine-runtime-plan.md`](../../engine-runtime-plan.md) §2 **R6**).
> **Yeni model.** Kaynak → [`workflow-event.md`](./workflow-event.md) · runtime → [`../../engine-runtime.md`](../../engine-runtime.md) §1/§9.
> **Amaç:** Her `ProcessInstance` için **tek satırlık, sık güncellenen** "motor imleci": son olay sürümü, yürütme durumu + bekleme sebebi, aktif adım,
> deneme sayacı, sonraki retry zamanı, döngü-koruma sayaçları ve son hata özeti. Worker/scheduler/API **her turda** bu satırı okur
> (`lastVersion` → optimistic concurrency) ve aynı TX'te günceller. `workflow_events`'ten **tamamen yeniden kurulabilir**.

## 0. Neden ayrı tablo (ProcessInstance kolonları değil)
- **Sıcak satır izolasyonu:** her adımda güncellenir (MVCC yeniden-yazım); `ProcessInstance` ise **kayıt** niteliğinde, seyrek değişir.
- **Rebuild kolaylığı:** `TRUNCATE workflow_projection` + replay — `ProcessInstance`'a dokunmadan.
- **`ProcessInstance.executionState` yine kalır:** liste sorguları ("bekleyen/koşan süreçler") join'siz çalışsın diye **kopya** olarak; ikisi **aynı TX'te**
  yazılır (→ plan Q5: kopya tutulsun mu, yoksa yalnız projeksiyon mu?).

## 1. Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `processInstanceId` | int | **PK**, FK → ProcessInstance.id | 1 – 1. |
| `organizationId` | int | (denormalize) | RLS Pattern B v2. |
| `lastVersion` | int | — | Uygulanan son `WorkflowEvent.version`. Yazan `version = lastVersion + 1` üretir (→ workflow-event §3.3). |
| `lastEventId` | bigint | FK → WorkflowEvent.id | Son olay (hızlı erişim). |
| `executionState` | [`ProcessExecutionState`](../enums/process-execution-state.md) | — | `new`/`running`/`waiting`/`failed`/`done`/`cancelled`. `ProcessInstance.executionState` ile **aynı değer**. |
| `waitReason` | [`WorkflowWaitReason`](../enums/workflow-wait-reason.md)`?` | — | `waiting` iken **ne** bekleniyor (`humanTask`/`processing`/`timer`/`retry`/`subProcess`); diğer durumlarda null. |
| `activeProcessStepInstanceId` | int? | FK → ProcessStepInstance.id | Mevcut konum — en güncel aktif adım çalıştırması (`done`/`cancelled`'da son adım). |
| `activeProcessStepId` | int? | FK → ProcessStep.id | Aktif adım tasarımı (denormalize; liste/filtre için). |
| `attempt` | int | — | Aktif adımın **deneme sayısı** (1 = ilk; retry'da artar; yeni adıma geçince 1'e döner). |
| `nextRetryAt` | datetime? | — | `waitReason = retry` iken sonraki deneme zamanı (bilgi; asıl tetik `WorkflowTimer`). |
| `lastError` | JSONB? | — | Son `stepFailed`/`failed` özeti `{ errorClass, errorCode, message, at }` — admin listesi/detay için; başarılı adımda temizlenir. |
| `autoStepRun` | int | — | **Döngü koruması:** son askıdan (insan/timer beklemesi) bu yana **ardışık otomatik adım** sayısı; `suspended` → 0. Limit → errors §7. |
| `totalSteps` | int | — | Bu süreçte açılan toplam `ProcessStepInstance` sayısı (toplam adım limiti). |
| `waitingSince` | datetime? | — | `waiting`'e geçiş zamanı (SLA/yaşlanma raporu; `running`'de null). |
| `lastEventAt` | datetime | — | Son olay zamanı — **stuck detector**: `running` ve `lastEventAt < now() - X` → alarm (→ scheduler §7). |
| `updatedAt` | datetime | — | Satır güncelleme zamanı. |

## 2. Güncelleme kuralı
- **Yalnız olay yazan TX günceller** (upsert). Olay yoksa projeksiyon değişmez — projeksiyon **asla** tek başına düzenlenmez (admin "düzelt" yok; kurtarma da bir **olaydır**: `recovered`).
- **Replay:** `processInstanceId` için olaylar `version` sırasıyla uygulanır; aynı fonksiyon **canlı yazımda ve replay'de** kullanılır (tek `apply(event)`).
- **Tutarlılık denetimi (housekeeping):** rastgele örneklemle `lastVersion` ↔ `MAX(version)` karşılaştırması; sapma = alarm + o sürecin rebuild'i.

## 3. İndeksler · RLS
| Nesne | Tanım | Ne için |
|---|---|---|
| PK | `processInstanceId` | 1 – 1 |
| B-tree | (`organizationId`, `executionState`, `waitReason`) | "hatalı süreçler", "retry bekleyenler", "onay bekleyenler" listeleri |
| B-tree (partial) | (`lastEventAt`) `WHERE executionState = 'running'` | stuck detector taraması |
| B-tree (partial) | (`nextRetryAt`) `WHERE waitReason = 'retry'` | operasyon görünürlüğü |
| RLS | `organizationId` | Pattern B v2 |

## 4. İlişkiler
- **1 – 1** → `ProcessInstance` (`processInstanceId`).
- **N – 1** → `WorkflowEvent` (`lastEventId`), `ProcessStepInstance` (`activeProcessStepInstanceId`), `ProcessStep` (`activeProcessStepId`).

## 5. Notlar / açık noktalar
- **`executionState` kopyası (Q5):** `ProcessInstance` ve projeksiyonda aynı değerin iki yerde durması bilinçli (liste perf); alternatif = `ProcessInstance`'tan kaldırıp
  her listeyi projeksiyona join'lemek.
- **`InstanceAwaitingUser` ile sınır:** kim aksiyon alabilir → `InstanceAwaitingUser` (form-odaklı, kullanıcı listesi); süreç nerede/neyi bekliyor → **bu tablo** (süreç-odaklı).
- **Alt süreç bekleme (`subProcess`)** ServiceTrigger `async=false` runtime karşılığı olarak öneri — kabul edilirse `waitingForProcessInstanceId` alanı eklenir (→ plan Q9).

*Oluşturma: 2026-08-31.*
