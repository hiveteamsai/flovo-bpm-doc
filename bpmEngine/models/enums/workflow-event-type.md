# Enum — WorkflowEventType

> **Kullanan model:** [`../processInstances/workflow-event.md`](../processInstances/workflow-event.md) — alan `eventType`, tip **WorkflowEventType**
> **Amaç:** Bir `ProcessInstance`'ın yürütme günlüğündeki (`workflow_events`) **geçiş türünü** belirtir. Her değer, motorun
> state machine'inde (→ [`../../engine-runtime.md`](../../engine-runtime.md) §1) **bir kenara** karşılık gelir; payload şekli
> değer-başına tanımlıdır (→ `workflow-event.md` §2).
> **Durum:** 📝 TASLAK v0.44 — onay bekliyor (→ [`../../engine-runtime-plan.md`](../../engine-runtime-plan.md)).

## Değerler
| Değer | Anlam | Ne zaman yazılır | `executionState` etkisi |
|---|---|---|---|
| `startRequested` | Süreç başlatıldı | `processStart` / `subProcessStart` / ServiceTrigger (associate · cron) ile yeni `ProcessInstance` açıldığında — **ilk olay (version 1)**. | `new` |
| `stepStarted` | Adım koşmaya başladı | Worker bir **otomatik** adımı çalıştırmaya başlarken, **yan etki üretmeden önce** (deneme sayacı burada artar). | `running` |
| `stepCompleted` | Otomatik adım bitti, aksiyon seçildi | Adım işini yaptı; sonuç bir aksiyon koduna eşlendi; sonraki adım için `step_ready` dispatch edildi. | `running` |
| `stepSkipped` | Adım atlandı | `skipIfPreApproved` / `skipIfUserProcessStarter` ile insan adımı **beklenmeden** `skipWithThisProcessStepActionId` tetiklendi. | `running` |
| `suspended` | Süreç askıya alındı | İnsan adımı (Kullanıcı / Grup / Üst Form Kullanıcı) · `autoAction`'sız Processing · Timer beklemesi · **retry beklemesi**; `InstanceAwaitingUser` senkronlandı, worker serbest. | `waiting` (+ `WorkflowProjection.waitReason`) |
| `actionTaken` | Dış aksiyon alındı | Kullanıcı / API / webhook bir aksiyon tetikledi (`POST …/actions/{code}`); aktör doğrulandı, `ActionTransfer` taşındı. | `running` |
| `timerFired` | Zamanlayıcı doldu | `WorkflowTimer` (adım timer'ı · insan-görev timeout · retry) süresi dolup scheduler tarafından **uygulandığında**. | `running` |
| `stepFailed` | Adım hata verdi | Bir denemede hata (sınıf + deneme + varsa sonraki retry zamanı payload'da). Retry edilecekse ardından `suspended(retry)`; edilmeyecekse `onFail` ya da `failed`. | — (retry → `waiting`, onFail → `running`) |
| `failed` | Süreç dead-letter | `onFail` yok / retry tükendi / tasarım hatası → süreç motor tarafından **durduruldu**; admin kurtarması bekler. | `failed` |
| `recovered` | Kurtarma uygulandı | Admin `failed` süreçte **retry** (aynı adım yeniden) veya **skip** (seçilen aksiyonla ilerlet) uyguladı. | `running` |
| `cancelled` | Süreç iptal edildi | Admin `failed`/`waiting` süreci **iptal** etti (BİTİŞ düğümüne ulaşılmadı). | `cancelled` |
| `ended` | Süreç bitti | Süreç Bitişi / Alt Süreç Bitişi düğümüne ulaşıldı **veya** terminal otomatik adım kolu bitirdi. | `done` |

## Notlar
- **Geçiş kuralları (hangi olay hangisinden sonra gelebilir):** `startRequested → stepStarted | suspended` · `stepStarted → stepCompleted | stepFailed | suspended` ·
  `stepCompleted → stepStarted | suspended | ended` · `suspended → actionTaken | timerFired | cancelled` · `actionTaken | timerFired | stepSkipped | recovered → stepStarted | suspended | ended` ·
  `stepFailed → suspended(retry) | stepStarted(onFail hedefi) | failed` · `failed → recovered | cancelled`. Kural dışı geçiş = motor hatası (yazılmaz, alarm).
- **`stepStarted` neden ayrı olay:** worker yan etki (HTTP çağrısı) **ürettikten sonra** çökerse redelivery aynı adımı ikinci kez koşar;
  `stepStarted` var + `stepCompleted` yok = **şüpheli (in-doubt)** deneme → adım tipine göre güvenli-tekrar / hata (→ [`../../engine-runtime-errors.md`](../../engine-runtime-errors.md) §3).
- **`retryScheduled` ayrı değer değildir:** retry bilgisi `stepFailed.payload.nextRetryAt` + ardından gelen `suspended(waitReason=retry)` ile ifade edilir.
- **Realtime/NATS eşlemesi:** `stepCompleted → step_completed.v1` · `suspended → suspended.v1` · `failed → failed.v1`; `step_ready`/`resume` **job**'ları olay değil, olayın `dispatch`'idir (→ `workflow-event.md` §3).

*Oluşturma: 2026-08-31.*
