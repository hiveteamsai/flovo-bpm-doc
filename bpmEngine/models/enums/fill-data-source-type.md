# Enum — FillDataSourceType

> **Kullanan model:** [`../service-settings/jsonTemplateModels/business-rule/actions/fill-data-source.md`](../service-settings/jsonTemplateModels/business-rule/actions/fill-data-source.md) (`fillDataSource` aksiyon konfigi) — alan `fillDataSourceType`
> **Amaç:** İş kuralı **`fillDataSource`** aksiyonunun besleyeceği veri kaynağının **türünü** belirler.
> **Davranış/kullanım:** → [`../../service-settings/business-rule.md`](../../service-settings/business-rule.md) §3

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `organizationData` | **Organizasyon verisi** (departman · şirket · masraf-merkezi · unvan · pozisyon · kademe · çalışma-takvimi · kullanıcı-grubu · kullanıcı …). | Kurumsal master-veriden seçenek listesi üretmek. |
| `userData` | **Oturum kullanıcısının** verisi (kredi kartı · şirket · masraf-merkezi). | Kullanıcıya özel seçenekler. |
| `serviceInstances` | **Başka bir servisin instance'ları** (kayıtları); durum kodlarıyla filtrelenebilir. | Kayıt-tabanlı dinamik liste (eski "veri seti" kavramının karşılığı). |
| `httpRequest` | **Dış HTTP isteğinin** dönüşü. | Entegrasyon / dış-API kaynağı. |

## Notlar
- **Eski `FromEba` kaldırıldı** (→ [`../../research/compare/new-vs-current-names.md`](../../research/compare/new-vs-current-names.md) §8); dış kaynak artık **`httpRequest`** ile.
- **`serviceInstances`** kaynağının sorgu şekli → [`../service-settings/jsonTemplateModels/business-rule/data-source/assign-value-from-dataset.md`](../service-settings/jsonTemplateModels/business-rule/data-source/assign-value-from-dataset.md).
- **`organizationData` alt-kaynak** v0.34'te **gerçek koddan modellendi:** [`OrganizationDataSourceType`](./organization-data-source-type.md) (10 kaynak) + [`fill-data-source-organization.md`](../service-settings/jsonTemplateModels/business-rule/data-source/fill-data-source-organization.md). Masraf-spesifik tipler (ExpenseType/ExpenseCategory) **kapsam-dışı** → [`../../todo.md`](../../todo.md).

*Oluşturma: 2026-08-26.*
