# Enum — ProcessStepUserGroupType

> **Kullanan model:** [`process-step.md`](../service-settings/process-step.md) — **Kullanıcı Grubu** adımı ayarı, alan `userGroupType`, tip **ProcessStepUserGroupType**
> **Amaç:** Kullanıcı Grubu (human task) adımında **grubun belirleme yöntemini** seçer.
> **Davranış:** → [`../../service-settings/process-step.md`](../../service-settings/process-step.md) §3.16.

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `fixedUserGroup` | Sabit kullanıcı grubu | Seçilen sabit grup (`userGroupId`). |
| `dynamicUserList` | Dinamik kullanıcı listesi | Formdaki bir property'deki (`dynamicUserListPropertyId`) **kullanıcılardan** oluşan liste. |
| `dynamicUserGroup` | Dinamik kullanıcı grubu | Formdaki bir property'deki (`dynamicUserListPropertyId`) **kullanıcı grubundan** oluşan liste. |

## Notlar
- Bu enum yalnız **grubun belirlenme yöntemini** seçer; grup formu beklerken **üyelerden biri** aksiyon alınca süreç ilerler
  _(grup-onay eşiği **yoktur** — tek üye yeterli; quorum/"hepsi onaylar" yok — kalıcı karar v0.32)_. Üyelik **dinamiktir**
  (`InstanceAwaitingUser.userGroupId` okuma-anı çözülür).
- **Kaynak:** current Flovo `ProcessSettingUserGroupType` →
  [`../../research/current-flovo-bpm-engine/step-type-settings-and-enums.md`](../../research/current-flovo-bpm-engine/step-type-settings-and-enums.md) §3.

*Oluşturma: 2026-07-16.*
