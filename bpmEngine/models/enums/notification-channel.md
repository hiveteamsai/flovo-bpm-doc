# Enum — NotificationChannel

> **Kullanan model:** [`process-step.md`](../service-settings/process-step.md) — **Bildirim** adımı (ve adım-içi bildirim kısayolu), tip **NotificationChannel**
> **Amaç:** Bir bildirimin **hangi kanaldan** gönderileceğini belirler. Kanallar **dinamik** bir yapıda tutulur —
> aynı bildirimde birden fazla kanal seçilebilir.
> **Davranış:** → [`../../service-settings/process-step.md`](../../service-settings/process-step.md) §3.6.

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `mail` | E-posta | E-posta bildirimi. **Parametre taşımaz.** |
| `push` | Push bildirimi | Mobil/masaüstü push. **`parameters`** taşıyabilir (UI'da gösterilmez; çalışma-zamanı veri güncelleme). |
| `toast` | Toast | Uygulama içi anlık mesaj. **`parameters`** taşıyabilir. |

## Notlar
- Başlık/mesaj metinleri **dinamik dil listesinde** (`{ languageCode, text }`) tutulur — sabit TR/EN alan çiftlerinin yerine.
- **Kaynak/karar:** current Flovo'da kanallar iki bool (`isMailMustSend`/`isPushNotificationMustSend`) idi; **Toast eklenip**
  dinamik kanal + enum yapısına dönüştürüldü →
  [`../../research/current-flovo-bpm-engine/step-type-settings-and-enums.md`](../../research/current-flovo-bpm-engine/step-type-settings-and-enums.md) §4.

*Oluşturma: 2026-07-16.*
