# Enum — WorkflowTimerKind

> **Kullanan model:** [`../processInstances/workflow-timer.md`](../processInstances/workflow-timer.md) — alan `kind`, tip **WorkflowTimerKind**
> **Amaç:** Bir `WorkflowTimer` kaydının **hangi mekanizma adına** kurulduğunu belirtir; scheduler süre dolunca türe göre farklı
> uyandırma uygular (→ [`../../architectures/engine-runtime/engine-runtime-scheduler.md`](../../architectures/engine-runtime/engine-runtime-scheduler.md) §3–§4).
> **Durum:** 📝 TASLAK v0.44 — onay bekliyor.

## Değerler
| Değer | Anlam | Kim kurar | Dolunca ne olur |
|---|---|---|---|
| `stepTimer` | **Timer** adımı (§3.7) süresi | Timer adımına girilince **veya** `timerStart` (§3.8) ile | Timer adımının `default` aksiyonu tetiklenir → hedef adım |
| `taskTimeout` | İnsan-görev adımının **timeout** bloğu (§3.15 / §3.16 / §3.22) | İnsan adımına girilip askıya alınırken | Timeout bildirimi + timeout aksiyonuyla ilerleme (eskalasyon = hedef adım) |
| `retry` | Geçici hata sonrası **yeniden deneme** (backoff) | Worker `stepFailed(retryable)` yazarken | Aynı adım yeniden koşar (`attempt + 1`) |
| `serviceTriggerCron` | ServiceTrigger `timer` (cron) **sonraki tetik** | Trigger kaydedilir/aktifleşirken · her tetikten sonra bir sonraki | Hedef servisin `processStart`'ı ile **yeni ana süreç** başlar; sonraki tetik için yeni kayıt |

## Notlar
- `serviceTriggerCron` dışındaki türler bir **`processInstanceId`**'ye bağlıdır; `serviceTriggerCron` servis-globaldir (`processInstanceId = null`, `serviceTriggerId` dolu).
- Aynı adım çalıştırması (`processStepInstanceId`) için aynı türden **en fazla bir `armed`** timer bulunur (yeniden kurma = eskisini `cancelled` yap).

*Oluşturma: 2026-08-31.*
