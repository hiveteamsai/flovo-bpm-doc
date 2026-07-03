# Model — CostCenter (Masraf Merkezi — organizasyon ayarı)

> **Durum:** 🟡 TASLAK — eski uygulama DTO'sundan türetildi.
> **Kaynak DTO:** `../../research/current-flovo-bpm-engine/organizations/expense-center.md` (`AccountCostCenterDto`).
> **Dönüşüm:** `account*`→`organization*`; `accountId` (string) → **`organizationId` (int)**; `kod`/`tanim`→`code`/`definition`;
> `accountCompanyId`→`companyId`.
> **Amaç:** Maliyet takibi yapılan muhasebesel birim (Cost Center). Masraf/harcama süreçlerinde maliyet yansıtma birimi.

## Alanlar
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Masraf merkezi ID'si. |
| `organizationId` | int | FK → `organization.md` | Sahibi organizasyon. |
| `companyId` | int | FK → `company.md` | Bağlı şirket. |
| `code` | string | — | Kod. |
| `definition` | string | — | Ad/tanım. |
| `active` | bool | — | Aktif/pasif — **null olamaz**, varsayılan `true`. `false` = frontend'de **görünür/düzenlenebilir** ama BPM işlemede kullanılmaz. |
| `deleted` | bool | — | Soft-delete — **null olamaz**, varsayılan `false`. `true` = frontend'de **gizli/aktarılmaz/salt** + BPM işlemede kullanılmaz. |
| `synchronizationStatus` | bool | — | Senkron durumu. |

### Alt model — CostCenterQualificationValue
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Kayıt ID'si. |
| `costCenterId` | int | FK → CostCenter | Bağlı masraf merkezi. |
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
- **N – 1** → `Organization`, `Company` (`companyId`).
- **1 – N** ← `Department` (`costCenterId`), `User` (`costCenterId`).
- **Ek nitelikler:** `AdditionalQualification` (`RelationalType=CostCenters`).

*Oluşturma: 2026-07-03.*
