# Enum — NotificationUserType

> **Kullanan model:** [`process-step.md`](../service-settings/process-step.md) — **Bildirim** adımı alıcı (kullanıcı) seçimi, tip **NotificationUserType**
> **Amaç:** Bildirim alıcısı **kullanıcı** olduğunda ([`notification-recipient-type.md`](./notification-recipient-type.md) = `user`),
> kullanıcının **belirleme yöntemini** seçer.
> **Davranış:** → [`../../service-settings/process-step.md`](../../service-settings/process-step.md) §3.6.

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `processStarter` | Süreci başlatan | Bildirim, süreci başlatan kullanıcıya. |
| `fixedUser` | Sabit kullanıcı(lar) | Seçilen sabit kullanıcı listesi (`fixedUserIds`). |
| `variableUsers` | Değişken kullanıcılar | Önceki adımlardan gelen kullanıcılar (`variableUserProcessStepIds`). |
| `formProperty` | Form property'sinden | Formdaki bir property'de (`propertyId`) seçili kullanıcı(lar). |

## Notlar
- `formProperty` değeri, eski `FormField` değerinin yeni adıdır (`field → property` normalizasyonu).
- **Kaynak:** current Flovo `NotificationStepTypeUserType` →
  [`../../research/current-flovo-bpm-engine/step-type-settings-and-enums.md`](../../research/current-flovo-bpm-engine/step-type-settings-and-enums.md) §4.

*Oluşturma: 2026-07-16.*
