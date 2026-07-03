# Model — Department (Departman — organizasyon ayarı)

> **Durum:** 🟡 TASLAK — eski uygulama DTO'sundan türetildi.
> **Kaynak DTO:** `../../research/current-flovo-bpm-engine/organizations/departments.md` (`AccountDepartmentDto`).
> **Dönüşüm:** `account*`→`organization*`; `accountId` (string) → **`organizationId` (int)**; `departmanAdi`/`departmanKodu`
> → `definition`/`code`; `departmanYoneticiUserId`→`managerUserId`; `ustDepartmentId`→`parentDepartmentId`.
> **Amaç:** Organizasyonun **hiyerarşik birim** yapısı. BPM'de **"departman yöneticisi"** atamalarında kullanılır.

## Alanlar
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Departman ID'si. |
| `organizationId` | int | FK → `organization.md` | Sahibi organizasyon. |
| `code` | string | — | Departman kodu. |
| `definition` | string | — | Departman adı. |
| `managerUserId` | int (null olabilir) | FK → `user.md` | **Departman yöneticisi** (BPM onay merci; opsiyonel). |
| `parentDepartmentId` | int (null olabilir) | FK → Department | Üst departman (hiyerarşi, self-ref). |
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
| `stringValue` | string (null olabilir) | — | `valueType=String` ise değer burada. |
| `doubleValue` | double (null olabilir) | — | `valueType=Double` ise değer burada. |
| `datetimeValue` | datetime (null olabilir) | — | `valueType=DateTime` ise değer burada. |
| `comboboxItemId` | int (null olabilir) | FK → `additional-qualification.md` (QualificationItem) | `valueType=Combobox` ise **seçilen öğe**. |
| `comboboxCode` | string (null olabilir) | — | Seçilen öğenin **kopya `code`**'u (çeviri). |
| `comboboxDefinition` | string (null olabilir) | — | Seçilen öğenin **kopya `definition`**'ı. |

## Benzersizlik
> `(organizationId, code)` **benzersiz** — aynı organizasyonda aynı `code`'lu iki kayıt olamaz. **`deleted=true` kayıtlar kontrole dahil değildir** (soft-delete edilenler bu kontrolde sayılmaz).

## İlişkiler
- **N – 1** → `Organization`, `User` (`managerUserId`), `CostCenter`, `Department` (`parentDepartmentId`, self-ref).
- **N – N** → `Company` (`companyIds`).
- **1 – N** ← `User` (`departmentId`).
- **Ek nitelikler:** `AdditionalQualification` (`RelationalType=Departments`).

*Oluşturma: 2026-07-03.*
