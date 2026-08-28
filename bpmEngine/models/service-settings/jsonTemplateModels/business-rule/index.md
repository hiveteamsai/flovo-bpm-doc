# İş Kuralı DTO'ları — İndeks

> **Amaç:** İş kuralı (`BusinessRule`) **aksiyon konfigürasyonu** ailesi — `BusinessRule.configuration` **JSONB** alanının
> `businessRuleActionType`'a göre aldığı **alt-şemalar** ve bunların paylaştığı ortak alt-modeller.
>
> **Tür:** Hepsi **DB tablosu değildir** (genel kural → [`../index.md`](../index.md)); yalnız JSONB gövdesinde taşınır/saklanır.
> **Davranış/kullanım:** → [`../../../../service-settings/business-rule.md`](../../../../service-settings/business-rule.md).

## Ağaç
```
business-rule/
├── actions/        → 7 aksiyon konfigi (businessRuleActionType → configuration şeması)
├── shared/         → ortak yapı taşları (değer çözümleme · görünüm · koşul-değeri)
└── data-source/    → veri kaynağı sorgu/filtre modelleri (dataset + fillDataSource kaynakları)
```

## [`actions/`](./actions/index.md) — Aksiyon konfigleri
`businessRuleActionType`'a karşılık gelen `configuration` şemaları.

| Döküman | Aksiyon tipi |
|---|---|
| [`set-view-for-properties.md`](./actions/set-view-for-properties.md) | `setViewForProperties` — visible/enabled/required. |
| [`apply-validation.md`](./actions/apply-validation.md) | `applyValidation` — koşullu validasyon. |
| [`show-message.md`](./actions/show-message.md) | `showMessage` — başlık + gövde dialog. |
| [`assign-value-to-property.md`](./actions/assign-value-to-property.md) | `assignValueToProperty` — alan **değerine** atama. |
| [`fill-data-source.md`](./actions/fill-data-source.md) | `fillDataSource` — seçim alanının veri kaynağı. |
| [`assign-value-to-property-attribute.md`](./actions/assign-value-to-property-attribute.md) | `assignValueToPropertyAttribute` — alan **özniteliğine** atama. |
| [`set-style.md`](./actions/set-style.md) | `setStyle` — tekil görünüm niteliği. |

## [`shared/`](./shared/index.md) — Ortak yapı taşları
Birden çok yerde kullanılan temel modeller.

| Döküman | Özet |
|---|---|
| [`assign-value.md`](./shared/assign-value.md) | **Merkezi değer-çözümleme** (`AssignValue`) — her değer noktasında (`ValueAssignType` ayrımlayıcısı + oneOf payload). |
| [`property-appearance.md`](./shared/property-appearance.md) | Alan görünüm bayrakları (`visible`/`enabled`/`required`) — `setViewForProperties` içinde. |
| [`business-rule-condition-compare-value.md`](./shared/business-rule-condition-compare-value.md) | Koşul tarafı (`referenceValue`/`valueToCompare`) değer kaynağı DTO'su. |

## [`data-source/`](./data-source/index.md) — Veri kaynağı modelleri
`fillDataSource` ve `fromDataSet` kaynaklarının sorgu/filtre şekilleri.

| Döküman | Özet |
|---|---|
| [`assign-value-from-dataset.md`](./data-source/assign-value-from-dataset.md) | Başka servisin instance'larından değer/liste sorgusu. |
| [`assign-value-from-dataset-parameter.md`](./data-source/assign-value-from-dataset-parameter.md) | Yukarıdaki sorgunun satır filtresi. |
| [`fill-data-source-organization.md`](./data-source/fill-data-source-organization.md) | `organizationData` kaynağı (kurum master-verisi). |
| [`fill-data-source-user.md`](./data-source/fill-data-source-user.md) | `userData` kaynağı (oturum kullanıcısının verisi). |
| [`fill-data-source-parameter.md`](./data-source/fill-data-source-parameter.md) | org/user kaynaklarının **ortak** satır filtresi. |

## Notlar
- **Discriminated union konvansiyonu (SOLID — v0.34):** `AssignValue` (shared) · `BusinessRuleConditionCompareValue` (shared) ·
  `FillDataSource` (actions) üçü de **ayrımlayıcı + oneOf payload** kullanır — her tip **yalnız kendi alt-yapısını** taşır (ISP);
  yeni tip mevcut payload'ları **bozmaz** (OCP). Yeni bir aksiyon/kaynak eklerken bu deseni izleyin.
- **`organizationData`** kaynağı v0.34'te **gerçek koddan modellendi** (`OrganizationDataSourceType` + `OrganizationParameter` + `SubTextType`). Açık: `search` değer kaynağı + masraf-spesifik tipler → [`../../../../todo.md`](../../../../todo.md).
- İlgili enum'lar: [`value-assign-type.md`](../../../enums/value-assign-type.md) · [`fill-data-source-type.md`](../../../enums/fill-data-source-type.md) · [`organization-data-source-type.md`](../../../enums/organization-data-source-type.md) · [`user-data-source-type.md`](../../../enums/user-data-source-type.md) · [`organization-parameter.md`](../../../enums/organization-parameter.md) · [`sub-text-type.md`](../../../enums/sub-text-type.md) · [`sort-direction.md`](../../../enums/sort-direction.md) · [`property-attribute-type.md`](../../../enums/property-attribute-type.md) · [`value-type-of-list.md`](../../../enums/value-type-of-list.md) · [`criterion-type.md`](../../../enums/criterion-type.md) · [`business-rule-condition-compare-type.md`](../../../enums/business-rule-condition-compare-type.md).

*Oluşturma: 2026-08-26.*
