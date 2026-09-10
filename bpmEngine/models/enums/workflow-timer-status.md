# Enum — WorkflowTimerStatus

> **Kullanan model:** [`../processInstances/workflow-timer.md`](../processInstances/workflow-timer.md) — alan `status`, tip **WorkflowTimerStatus**
> **Amaç:** Bir zamanlayıcı kaydının yaşam döngüsü konumu. Scheduler yalnız `armed` kayıtları tarar (→ [`../../architectures/engine-runtime/engine-runtime-scheduler.md`](../../architectures/engine-runtime/engine-runtime-scheduler.md) §1).
> **Durum:** 📝 TASLAK v0.44 — onay bekliyor.

## Değerler
| Değer | Anlam | Geçiş |
|---|---|---|
| `armed` | Kurulu — `dueAt` bekleniyor | oluşturulunca |
| `fired` | Süre doldu ve **uygulandı** (`timerFired` olayı yazıldı) | `armed → fired` (scheduler claim + aynı TX'te olay) |
| `deferred` | Süre doldu ama süreç o anda **uygulanamaz** durumda (`running`) → kısa süre sonra yeniden denenecek (`dueAt` ileri alınır, `deferCount++`) | `armed → deferred → armed` |
| `cancelled` | Kuruluyken **iptal** edildi (aksiyon alındı → timeout gereksiz · `timerEnd` · süreç bitti/iptal · trigger pasifleşti) | `armed | deferred → cancelled` |

## Notlar
- `fired` ve `cancelled` **terminal**dir; yeni kurulum = **yeni satır** (geçmiş korunur, saklama → [`../../architectures/engine-runtime/engine-runtime-retention.md`](../../architectures/engine-runtime/engine-runtime-retention.md)).
- `deferred` fiilen `armed`'ın alt hâlidir; ayrı değer tutulmasının nedeni **izleme** (kaç kez ertelendi → uzun süre `running` kalan süreç alarmı).

*Oluşturma: 2026-08-31.*
