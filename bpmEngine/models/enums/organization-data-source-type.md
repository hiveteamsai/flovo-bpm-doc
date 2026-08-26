# Enum — OrganizationDataSourceType

> **Kullanan model:** [`../service-settings/dto/business-rule/data-source/fill-data-source-organization.md`](../service-settings/dto/business-rule/data-source/fill-data-source-organization.md) — alan `organizationDataSourceType`
> **Amaç:** `fillDataSource` `organizationData` kaynağında, **hangi kurum master-verisinden** seçim listesi üretileceğini belirler.

## Nedir?
Organizasyon master-verisinden (departman, şirket, masraf merkezi, kullanıcı…) bir seçim listesi doldururken **kaynağı** seçer.
Her kaynak, yalnız **belirli** `OrganizationParameter`'larla filtrelenebilir (aşağıdaki tablo).

## Değerler
| Değer | Kaynak | Seçilebilir filtreler (`OrganizationParameter`) |
|---|---|---|
| `professions` | Unvanlar (→ Profession) | `name` · `code` · `company` |
| `departments` | Departmanlar (→ Department) | `name` · `code` · `company` |
| `companies` | Şirketler (→ Company) | `name` · `code` |
| `costCenters` | Masraf merkezleri (→ CostCenter) | `name` · `code` · `company` |
| `users` | Kullanıcılar (→ User) | `name` · `code` · `company` · `userCode` · `additionalQualification` · `professionCode` |
| `creditCards` | Kredi kartları (→ CreditCard) | `name` · `code` · `company` · `userCode` |
| `workerLevels` | Kademeler (→ WorkerLevel) | `name` · `code` |
| `userGroups` | Kullanıcı grupları (→ UserGroup) | `name` · `code` · `company` |
| `positions` | Pozisyonlar (→ Position) | `name` · `code` · `company` |
| `workingSchedules` | Çalışma takvimleri (→ WorkingSchedule) | `name` · `code` |

## Notlar
- **Eski isim eşlemeleri:** `Tiers` → **`workerLevels`** · `FromUserGroupData` → **`userGroups`** (yeni motor org modelleriyle hizalandı).
- **Kapsam-dışı bırakılan (masraf çekirdek modeli yok):** eski `ExpenseType` · `ExpenseCategory` **taşınmadı** — yeni motorda karşılık gelen
  model yok. Masraf varlıkları modellenirse eklenir → [`../../todo.md`](../../todo.md) ("Kapsam-dışı varlıklar").
- **`users`** kaynağı ağ kullanıcı listesinden beslenir; `company` filtresi için `fill-data-source.md` `companyId` de kullanılabilir.

*Oluşturma: 2026-08-26.*
