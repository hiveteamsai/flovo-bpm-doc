# Enum — WorkTimeSelection

> **Kullanan model:** [`process-step.md`](../service-settings/process-step.md) — **Timer** normal-takvim ayar bloğu, alan `workTimeSelection`, tip **WorkTimeSelection**
> **Amaç:** Normal takvime göre süre hesabında, referans anın **çalışma gününün başı mı yoksa sonu mu** olacağını belirler.
> **Davranış:** → [`../../service-settings/process-step.md`](../../service-settings/process-step.md) §3.7.

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `atWorkStart` | Çalışma başlangıcında | Referans an = çalışma gününün başlangıcı. |
| `atWorkEnd` | Çalışma bitiminde | Referans an = çalışma gününün bitişi. |

## Notlar
- [`timer-calculation-type.md`](./timer-calculation-type.md) `normalCalendar` ile birlikte kullanılır.
- **Kaynak:** → [`../../research/current-flovo-bpm-engine/step-type-settings-and-enums.md`](../../research/current-flovo-bpm-engine/step-type-settings-and-enums.md) §5.

*Oluşturma: 2026-07-16.*
