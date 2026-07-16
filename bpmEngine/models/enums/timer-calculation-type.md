# Enum — TimerCalculationType

> **Kullanan model:** [`process-step.md`](../service-settings/process-step.md) — **Timer** ailesi + Kullanıcı/Kullanıcı Grubu adımlarının **timeout** ayarı, alan `workStyle`, tip **TimerCalculationType**
> **Amaç:** Bir zamanlayıcının/timeout'un **süresinin nasıl hesaplanacağını** belirler. Seçilen değere göre ilgili
> ayar bloğu (çalışma takvimi / normal takvim / sabit zaman) doldurulur.
> **Davranış:** → [`../../service-settings/process-step.md`](../../service-settings/process-step.md) §3.7 (+ §3.15/§3.16 timeout).

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `workCalendar` | Çalışma takvimine göre | İş günü + çalışma saatleri (WorkingSchedule) üzerinden hesap. |
| `normalCalendar` | Normal takvime göre | Takvim günleri; erteleme opsiyonu ([`time-adjustment-option.md`](./time-adjustment-option.md)) alabilir. |
| `fixedDateTime` | Sabit zaman | Belirli bir tarih/saat. |

## Notlar
- Eski ad **WorkStyle**. `normalCalendar` bloğu ayrıca [`work-time-selection.md`](./work-time-selection.md) (çalışma başı/sonu)
  ve [`time-adjustment-option.md`](./time-adjustment-option.md) (saat önce/sonra) kullanır.
- **Kaynak:** → [`../../research/current-flovo-bpm-engine/step-type-settings-and-enums.md`](../../research/current-flovo-bpm-engine/step-type-settings-and-enums.md) §5.

*Oluşturma: 2026-07-16.*
