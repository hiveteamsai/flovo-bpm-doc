# Enum — ProcessStepUserType

> **Kullanan model:** [`process-step.md`](../service-settings/process-step.md) — **Kullanıcı** adımı ayarı, alan `userType`, tip **ProcessStepUserType**
> **Amaç:** Kullanıcı (human task) adımında **aksiyonu alacak kullanıcının belirleme yöntemini** seçer.
> **Davranış:** → [`../../service-settings/process-step.md`](../../service-settings/process-step.md) §3.15.

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `processStarter` | Süreci başlatan | Aksiyon, süreci başlatan kullanıcıya gider. |
| `fixedUser` | Sabit kullanıcı | Seçilen sabit kullanıcı (`fixedUserId`). |
| `usersManager` | Kullanıcının yöneticisi | Hedef adımda (`userAdministratorSourceProcessStepId`) **en son onay veren** kullanıcının yöneticisi. |
| `departmentManager` | Departman yöneticisi | Seçilen departmanın (`departmentManagerDepartmentId`) yöneticisi. |
| `variableUser` | Değişken kullanıcı | Formdaki bir property'den gelen kullanıcı (değişken atama). |

## Notlar
- **Kaldırılan değerler:** eski `managerChain` (yönetici zinciri) ve `managerByTitle` (ünvana göre yönetici) —
  mevcut projede aktif çalışmadığından **çıkarıldı**; ilgili ayar alanları da kaldırıldı.
- **Kaynak/karar:** current Flovo `ProcessSettingUserType` →
  [`../../research/current-flovo-bpm-engine/step-type-settings-and-enums.md`](../../research/current-flovo-bpm-engine/step-type-settings-and-enums.md) §2.

*Oluşturma: 2026-07-16.*
