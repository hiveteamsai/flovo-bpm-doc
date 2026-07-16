# Enum — TimeAdjustmentOption

> **Kullanan model:** [`process-step.md`](../service-settings/process-step.md) — **Timer** normal/sabit ayar bloğu (erteleme), alan `timeAdjustmentOption`, tip **TimeAdjustmentOption**
> **Amaç:** Erteleme (postponing) yönünü belirler — hesaplanan zamandan **saat önce mi, saat sonra mı** olacağı.
> **Davranış:** → [`../../service-settings/process-step.md`](../../service-settings/process-step.md) §3.7.

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `hoursAfter` | Saat sonra | Hesaplanan zamana `postponingHour` kadar **eklenir**. |
| `hoursBefore` | Saat önce | Hesaplanan zamandan `postponingHour` kadar **çıkarılır**. |

## Notlar
- Yalnız erteleme (`postponing = true`) etkinken anlamlıdır; miktar `postponingHour` alanındadır.
- **Kaynak:** → [`../../research/current-flovo-bpm-engine/step-type-settings-and-enums.md`](../../research/current-flovo-bpm-engine/step-type-settings-and-enums.md) §5.

*Oluşturma: 2026-07-16.*
