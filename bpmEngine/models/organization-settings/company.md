# Model — Company (organizasyon ayarı)

> **Durum:** 🟡 TASLAK — eski uygulama DTO'sundan türetildi.
> **Kaynak DTO:** `../../research/current-flovo-bpm-engine/organizations/companies.md` (`AccountCompanyDto`).
> **Dönüşüm:** `account*`→`organization*`; `accountId` (string) → **`organizationId` (int)**; `kod`/`tanim`→`code`/`definition`.
> **Amaç:** Organizasyonun **tüzel kişiliklerini** (şirketler) temsil eder. Çok-şirketli organizasyonlar tek kiracı altında yönetilir.

## Alanlar
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Şirket ID'si. |
| `organizationId` | int | FK → `organization.md` | Sahibi organizasyon. |
| `code` | string | — | Şirket kodu. |
| `definition` | string | — | Şirket adı/tanımı. |
| `active` | bool | — | Aktif/pasif — **null olamaz**, varsayılan `true`. `false` = frontend'de **görünür/düzenlenebilir** ama BPM işlemede kullanılmaz. |
| `deleted` | bool | — | Soft-delete — **null olamaz**, varsayılan `false`. `true` = frontend'de **gizli/aktarılmaz/salt** + BPM işlemede kullanılmaz. |
| `isDefaultCompany` | bool | — | Varsayılan şirket mi (seçim yapılmazsa kullanılır). |
| `synchronizationStatus` | bool | — | Harici ERP/muhasebe ile senkron durumu. |

## Benzersizlik
> `(organizationId, code)` **benzersiz** — aynı organizasyonda aynı `code`'lu iki kayıt olamaz. **`deleted=true` kayıtlar kontrole dahil değildir** (soft-delete edilenler bu kontrolde sayılmaz).

## İlişkiler
- **N – 1** → `Organization` (`organizationId`).
- **N – N** ← `companyIds` ile bağlananlar: `Department`, `Profession`, `User`, `UserGroup`, `AdditionalQualification`.
- **N – 1** ← `companyId` (tekil) ile bağlananlar: `CostCenter`, `CreditCard`.

## Notlar
- Diğer bileşenlerin **şirket bağlantısının temelidir**. UI seçim listelerinde (`IOrganizationParameter`) veri kaynağı olarak kullanılır.

*Oluşturma: 2026-07-03.*
