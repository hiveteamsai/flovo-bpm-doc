# Model — Department (Departman — organizasyon ayarı)

> **Durum:** 🟡 TASLAK
> **Amaç:** Organizasyonun **hiyerarşik birim** yapısı. BPM'de **"departman yöneticisi"** atamalarında kullanılır.

## Alanlar
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Departman ID'si. |
| `organizationId` | int | FK → `organization.md` | Sahibi organizasyon. |
| `code` | string | — | Departman kodu. |
| `definition` | string | — | Departman adı. |
| `translationCode` | string? | çeviri anahtarı | **Çeviri eşleşme anahtarı** (→ [`translation.md`](./translation.md) `code`). `null` = çeviri **es geçilir**, doğrudan `definition` kullanılır. |
| `managerUserId` | int? | FK → `user.md` | **Departman yöneticisi** (BPM onay merci; opsiyonel). |
| `parentDepartmentId` | int? | FK → Department | Üst departman (hiyerarşi, self-ref). |
| `costCenterId` | int | FK → `cost-center.md` | Bağlı masraf merkezi. |
| `active` | bool | — | Aktif/pasif — **null olamaz**, varsayılan `true`. `false` = frontend'de **görünür/düzenlenebilir** ama BPM işlemede kullanılmaz. |
| `deleted` | bool | — | Soft-delete — **null olamaz**, varsayılan `false`. `true` = frontend'de **gizli/aktarılmaz/salt** + BPM işlemede kullanılmaz. |
| `synchronizationStatus` | bool | — | Senkron durumu. |
| `companyIds` | List\<int\> | FK → `company.md` (N–N) | İlişkili şirketler. |

### Alt model — DepartmentQualificationValue
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Kayıt ID'si. |
| `departmentId` | int | FK → Department | Bağlı departman. |
| `qualificationId` | int | FK → `additional-qualification.md` | Ek nitelik. |
| `stringValue` | string? | — | `valueType=string` ise değer burada. |
| `doubleValue` | double? | — | `valueType=double` ise değer burada. |
| `datetimeValue` | datetime? | — | `valueType=dateTime` ise değer burada. |
| `comboboxItemId` | int? | FK → `additional-qualification.md` (QualificationItem) | `valueType=combobox` ise **seçilen öğe**. |
| `comboboxTranslationCode` | string? | çeviri anahtarı | Seçilen öğenin **kopya `translationCode`**'u (çeviri; `null` ise `comboboxDefinition` doğrudan kullanılır). |
| `comboboxDefinition` | string? | — | Seçilen öğenin **kopya `definition`**'ı. |

## Benzersizlik
> `(organizationId, code)` **benzersiz** — aynı organizasyonda aynı `code`'lu iki kayıt olamaz. **`deleted=true` kayıtlar kontrole dahil değildir** (soft-delete edilenler bu kontrolde sayılmaz).

## İlişkiler
- **N – 1** → `Organization`, `User` (`managerUserId`), `CostCenter`, `Department` (`parentDepartmentId`, self-ref).
- **N – N** → `Company` (`companyIds`).
- **1 – N** ← `User` (`departmentId`).
- **Ek nitelikler:** `AdditionalQualification` (`RelationalType=departments`).

*Oluşturma: 2026-07-03.*
