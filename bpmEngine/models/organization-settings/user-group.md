# Model — UserGroup (Kullanıcı Grubu — organizasyon ayarı)

> **Durum:** 🟡 TASLAK — eski uygulama DTO'sundan türetildi.
> **Kaynak DTO:** `../../research/current-flovo-bpm-engine/organizations/user-groups.md` (`AccountUserGroupDto`).
> **Dönüşüm:** `account*`→`organization*`; `accountId` (string) → **`organizationId` (int)**.
> **Amaç:** Birden fazla kullanıcıyı toplayan grup. BPM'de **grup onayı**, **bildirim hedefi**, **aksiyon görünürlük yetkisi**.

## Alanlar
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Grup ID'si. |
| `organizationId` | int | FK → `organization.md` | Sahibi organizasyon. |
| `code` | string | — | Grup kodu. |
| `definition` | string | — | Grup adı/tanımı. |
| `groupApprovalRequired` | bool | — | **Grup onayı gerekli mi?** Bu grup bir formu beklerken (`FormAwaitingUser.userGroupId`) `true` ise, onaylayan üyeler `UserGroupApprovedUser` tablosundan tespit edilir. |
| `active` | bool | — | Aktif/pasif — **null olamaz**, varsayılan `true`. `false` = frontend'de **görünür/düzenlenebilir** ama BPM işlemede kullanılmaz. |
| `deleted` | bool | — | Soft-delete — **null olamaz**, varsayılan `false`. `true` = frontend'de **gizli/aktarılmaz/salt** + BPM işlemede kullanılmaz. |
| `companyIds` | List\<int\> | FK → `company.md` (N–N) | İlişkili şirketler. |

### Alt model — UserGroupMember (grup üyesi)
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Üyelik kayıt ID'si. |
| `userGroupId` | int | FK → UserGroup | Bağlı grup. |
| `userId` | int | FK → `user.md` | Üye kullanıcı. |
| `companyId` | int | FK → `company.md` | Üyenin şirketi. |

## Benzersizlik
> `(organizationId, code)` **benzersiz** — aynı organizasyonda aynı `code`'lu iki kayıt olamaz. **`deleted=true` kayıtlar kontrole dahil değildir** (soft-delete edilenler bu kontrolde sayılmaz).

## İlişkiler
- **N – 1** → `Organization` · **N – N** → `Company`.
- **1 – N** ← `UserGroupMember` (`userGroupId`).
- **BPM kullanımı:** "Kullanıcı Grubu" adımı (grup onayı) · `ProcessStepAction.actionDisplayAuthorizedUserGroupId` · bildirim hedefi · rapor erişimi.
- **1 – N** ← `UserGroupApprovedUser` (dolaylı, `FormAwaitingUser` üzerinden) — yalnız `groupApprovalRequired=true` iken onaylayan üyeler tutulur → `../workFlows/user-group-approved-user.md`.

*Oluşturma: 2026-07-03.*
