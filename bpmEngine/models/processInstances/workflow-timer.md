# Model — WorkflowTimer (`workflow_timer` — zamanlanmış uyandırma kaydı)

> **Durum:** 📝 TASLAK v0.44 — **onay bekliyor** (→ [`../../engine-runtime-plan.md`](../../engine-runtime-plan.md) §2 **R7**).
> **Yeni model.** Davranış → [`../../engine-runtime-scheduler.md`](../../engine-runtime-scheduler.md) · kaynak olay → [`workflow-event.md`](./workflow-event.md) (`timerFired`).
> **Amaç:** Motorun **"şu anda uyan"** kayıtları — Timer adımı süresi · insan-görev **timeout**'u · **retry** backoff'u · ServiceTrigger **cron**
> sonraki tetiği. Scheduler yalnız `armed` + `dueAt <= now()` satırlarını **Postgres'te claim eder** (`FOR UPDATE SKIP LOCKED`) → aynı TX'te
> `timerFired` olayı yazar → `resume.v1` yayınlar. Süreç günlerce beklerken **hiçbir worker kaynak tutmaz**; uyanma bu tablodan gelir.
>
> **`SchedulerJob` ile fark:** [`../organization-settings/scheduler-job.md`](../organization-settings/scheduler-job.md) = organizasyon-düzeyi
> **cron'lu arka plan fonksiyonları** (`functionName`, bakım/toplu iş); `WorkflowTimer` = **süreç-örneği düzeyinde** tek-atımlık uyandırma. İkisi karışmaz.

## 1. Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | bigint | PK | Timer kimliği. `timerFired` olayının `messageId`'si = `timer:{id}` (idempotency). |
| `organizationId` | int | (denormalize) | RLS Pattern B v2. |
| `kind` | [`WorkflowTimerKind`](../enums/workflow-timer-kind.md) | — | `stepTimer` · `taskTimeout` · `retry` · `serviceTriggerCron`. |
| `status` | [`WorkflowTimerStatus`](../enums/workflow-timer-status.md) | — | `armed` · `fired` · `deferred` · `cancelled`. |
| `processInstanceId` | int? | FK → ProcessInstance.id | Bağlı süreç. **`serviceTriggerCron`'da null** (servis-global). |
| `processStepInstanceId` | int? | FK → ProcessStepInstance.id | Timer'ı kuran adım çalıştırması (`taskTimeout`: bekleyen insan adımı · `retry`: hatalı adım · `stepTimer`: `timerStart`'ı koşan ya da Timer adımının kendisi). |
| `processStepId` | int? | FK → ProcessStep.id | **Uygulanacak** adım: `stepTimer` → Timer adımı (`selectedTimerProcessStepId` ya da kendisi); `taskTimeout` → bekleyen insan adımı; `retry` → yeniden koşacak adım. |
| `serviceTriggerId` | int? | FK → ServiceTrigger.id | **Yalnız `serviceTriggerCron`**. |
| `dueAt` | datetime | — | Uyanma zamanı (**UTC**). Kurulum anında hesaplanır (§3); `deferred`'da ileri alınır. |
| `armedAt` | datetime | — | Kurulum zamanı. |
| `firedAt` | datetime? | — | Uygulandığı an (`status = fired`). |
| `cancelledAt` | datetime? | — | İptal anı. |
| `cancelReason` | string? | — | `actionTaken` (aksiyon alındı, timeout gereksiz) · `timerEnd` · `processEnded` · `processCancelled` · `triggerDisabled` · `rearmed` (yeniden kuruldu). |
| `deferCount` | int | — | Kaç kez `deferred` edildi (süreç `running` olduğu için uygulanamadı). İzleme/alarm. |
| `attempt` | int? | — | **Yalnız `retry`**: bu timer dolunca koşacak deneme numarası (`WorkflowProjection.attempt + 1`). |
| `payload` | JSONB? | — | Türe özel küçük bilgi: `taskTimeout` → `{ timeoutActionCode, notify: bool }` · `stepTimer` → `{ armedBy: "timerStart" \| "stepEntry" }` · `serviceTriggerCron` → `{ cronExpression, timezone, scheduledFor }`. |
| `messageId` | string? | — | Kurulumu tetikleyen olayın idempotency anahtarı (aynı olay iki kez işlenirse **ikinci timer kurulmaz**; UNIQUE partial). |

## 2. Kurulum · iptal · uygulama (özet; ayrıntı → scheduler §2–§4)
| `kind` | Kurulur | İptal edilir | Dolunca |
|---|---|---|---|
| `stepTimer` | Timer adımına girilince (**askıya alınır**, `waitReason=timer`) **veya** `timerStart` koşunca (süreç ilerlemeye devam eder) | `timerEnd` · süreç bitti/iptal · aynı Timer için yeniden `timerStart` (`rearmed`) | Timer adımının **`default`** aksiyonu → hedef adım. Süreç başka adımda **bekliyorsa** o bekleme kapatılır (preemption) |
| `taskTimeout` | İnsan adımı `suspended` olurken (`settings.timeout.timeoutActive=true`) | O adımda **aksiyon alınınca** · süreç bitti/iptal | Timeout bildirimi (varsa) + **timeout aksiyonu** ile ilerleme (eskalasyon hedefi) |
| `retry` | `stepFailed(retryable=true)` yazılırken (`nextRetryAt`) | Admin `cancel`/`skip` · süreç iptal | Aynı adım `attempt+1` ile yeniden (`stepStarted`) |
| `serviceTriggerCron` | Trigger oluşturulup/aktifleşince → **ilk** sonraki tetik; her tetikten sonra **bir sonraki** | Trigger `active=false`/silindi | Hedef servis `processStart` → **yeni ana `ProcessInstance`**; yeni satır kurulur |

> **Uygulama kuralı (R14):** `stepTimer`/`taskTimeout` yalnız süreç **`waiting`** iken uygulanır; süreç o anda `running` ise (otomatik zincir koşuyor)
> **`deferred`** → `dueAt = now() + 30s`; süreç `done`/`cancelled` olmuşsa → `cancelled(processEnded)`. Böylece **tek aktif kol** kuralı bozulmaz.

## 3. `dueAt` hesabı
- **`stepTimer` / `taskTimeout`:** `ProcessStepTimerSettings.workStyle`'a göre (→ [`../service-settings/jsonTemplateModels/process-step-settings/timer.md`](../service-settings/jsonTemplateModels/process-step-settings/timer.md)):
  `workCalendar` → organizasyonun `WorkingSchedule` + `VacationDay` ile iş-saati ilerletme · `normalCalendar` → takvim günü + `workTimeSelection` + erteleme ·
  `fixedDateTime` → verilen an ± erteleme. **Kurulum anında hesaplanır ve sabitlenir** (takvim sonradan değişse timer yeniden hesaplanmaz → plan Q16).
- **`retry`:** `now() + backoff(attempt)` (→ errors §2).
- **`serviceTriggerCron`:** `cronExpression`'ın **scheduler saat diliminde** bir sonraki eşleşmesi (→ scheduler §5; TZ/DST → plan Q15).

## 4. İndeksler · RLS
| Nesne | Tanım | Ne için |
|---|---|---|
| PK | `id` | |
| B-tree (partial) | (`dueAt`) `WHERE status IN ('armed','deferred')` | **claim taraması** — küçük, sıcak |
| B-tree | (`processInstanceId`, `status`) | süreç bitince/aksiyon alınınca toplu iptal |
| UNIQUE (partial) | (`serviceTriggerId`) `WHERE status = 'armed' AND kind = 'serviceTriggerCron'` | trigger başına **tek** bekleyen tetik |
| UNIQUE (partial) | (`processStepInstanceId`, `kind`) `WHERE status = 'armed'` | aynı adım çalıştırması için aynı türden tek `armed` |
| UNIQUE (partial) | (`messageId`) `WHERE messageId IS NOT NULL` | kurulum idempotency |
| RLS | `organizationId` | Pattern B v2 (cron satırında da dolu — trigger'ın org'u) |

## 5. İlişkiler
- **N – 1** → `ProcessInstance` (`processInstanceId`), `ProcessStepInstance` (`processStepInstanceId`), `ProcessStep` (`processStepId`), `ServiceTrigger` (`serviceTriggerId`).
- **Üretir** → `WorkflowEvent(timerFired)` (`payload.workflowTimerId = id`).

## 6. Notlar / açık noktalar
- **Neden tek tablo (dört tür):** hepsi "bir anda bir şey yap" kaydıdır; tek claim döngüsü, tek indeks, tek izleme metriği (`now() - dueAt` p95 = scheduler gecikmesi).
- **Lider seçimi gerekmez (R7):** claim `FOR UPDATE SKIP LOCKED` ile yapılır → N scheduler kopyası **aynı timer'ı iki kez alamaz**; scheduler **yatay ölçeklenir**.
  Advisory lock yalnız singleton **housekeeping** işleri için (→ scheduler §7).
- **Saklama:** `fired`/`cancelled` satırlar 30 gün sonra silinir (→ retention §6).
- **Açık:** DST/TZ (Q15) · takvim değişince yeniden hesap (Q16) · `deferred` üst sınırı (kaç kez / ne kadar) (Q14).

*Oluşturma: 2026-08-31.*
