# Enum — NotificationRecipientType

> **Kullanan model:** [`process-step.md`](../service-settings/process-step.md) — **Bildirim** adımı alıcı tanımı, tip **NotificationRecipientType**
> **Amaç:** Bir bildirim **alıcı bloğunun** kimi hedeflediğini belirler; seçime göre alıcı farklı biçimde tespit edilir.
> **Davranış:** → [`../../service-settings/process-step.md`](../../service-settings/process-step.md) §3.6.

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `user` | Kullanıcı | Alıcı bir **kullanıcı** → [`notification-user-type.md`](./notification-user-type.md) ile tespit edilir. |
| `userGroup` | Kullanıcı grubu | Seçilen kullanıcı grubu/grupları (`userGroupIds`). |
| `takeUsersWhoTookActionBefore` | Daha önce aksiyon alanlar | Süreçte daha önce aksiyon almış kullanıcılara bildirim. |

## Notlar
- **Adım tipiyle karıştırma:** Bu enum bildirim **alıcı türüdür**; sürecin adım tipi olan
  [`process-step-type.md`](./process-step-type.md) (**ProcessStepType**) ile ilgisi yoktur. (Eski adı `ProcessSettingStepType`.)
- Bildirim alıcısı **kendi** seçim yöntemini kullanır; adım-atama enum'larından
  ([`process-step-user-type.md`](./process-step-user-type.md) / [`process-step-user-group-type.md`](./process-step-user-group-type.md)) **bağımsızdır**.
- **`takeUsersWhoTookActionBefore` buraya taşındı:** önceki ayrı `NotificationUserGroupType` enum'u **kaldırıldı**; grup
  tarafında tek gerçek seçim `userGroup` (`userGroupIds`) olduğundan her iki değeri de bu üst-düzey alıcı türüne toplandı.
- **Kaynak:** → [`../../research/current-flovo-bpm-engine/step-type-settings-and-enums.md`](../../research/current-flovo-bpm-engine/step-type-settings-and-enums.md) §4.

*Oluşturma: 2026-07-16.*
