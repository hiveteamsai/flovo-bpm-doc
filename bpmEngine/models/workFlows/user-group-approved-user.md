# Model — UserGroupApprovedUser (grup onayında onaylayan kullanıcı)

> **Durum:** 🟢 TANIMLI
> **Eski karşılığı:** yok — **yeni model**.
> **Amaç:** Bir form bir **kullanıcı grubunun** onayını beklerken (`FormAwaitingUser.userGroupId` dolu **ve** o grubun
> `UserGroup.groupApprovalRequired = true` olduğunda), gruptaki **hangi kullanıcının** ne zaman onayladığını tutar.
> **Tek amaç:** Grup onayında onaylayanları tespit etmek — **başka hiçbir amaçla kullanılmaz**.

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Onay kaydı ID'si. |
| `formAwaitingUserId` | int | FK → FormAwaitingUser.id | Hangi grup-bekleme kaydına ait onay. |
| `userId` | int | FK → User.id | Onaylayan kullanıcı (grubun üyesi). |
| `approvedDate` | datetime | — | Onay zamanı. |

## İlişkiler
- **N – 1** → `FormAwaitingUser` (`formAwaitingUserId`), `User` (`userId`).

## Nasıl çalışır (grup onayı)
- Bir `FormAwaitingUser` kaydı **gruba** aitse (`userGroupId` dolu) **ve** o grubun `UserGroup.groupApprovalRequired = true`
  ise, gruptan onay veren her kullanıcı için buraya bir kayıt eklenir (`formAwaitingUserId` + `userId` + `approvedDate`).
- Onayı **kimlerin** verdiği bu tablodan tespit edilir. Grup onayı gerekli değilse (`groupApprovalRequired = false`) bu
  tablo kullanılmaz.

## Notlar / açık noktalar
- Onayın **tamamlanma eşiği** (**hepsi mi / biri mi**) Kullanıcı Grubu adımının **`groupApproval`** ayarına göre
  değerlendirilir → `../../service-settings/process-step.md` §3.16.
- **Açık soru (adlandırma/yetki çakışması):** adım-düzeyi **`groupApproval`** (hepsi/biri — eşik) ile
  **`UserGroup.groupApprovalRequired`** (bool — grup onayı gerekli mi) arasındaki ilişki/sınır netleştirilmeli → `../../todo.md`.

*Oluşturma: 2026-07-06.*
