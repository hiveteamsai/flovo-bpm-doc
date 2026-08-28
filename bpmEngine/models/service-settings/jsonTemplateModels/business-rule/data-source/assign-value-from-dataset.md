# DTO — AssignValueFromDataSet

> **Tür:** **DTO** — **DB tablosu değildir.** `AssignValue` (`fromDataSet`) veya `fillDataSource` (`serviceInstances`)
> içinde, `BusinessRule.configuration` **JSONB** gövdesinde iç-içe yaşar.
> **Amaç:** **Başka bir servisin instance'larından** (kayıtlarından) **tek değer** (→ `AssignValue`) veya **değer listesi**
> (→ `fillDataSource`) çekme sorgusu.
> **Davranış/kullanım:** → [`../../../../../service-settings/business-rule.md`](../../../../../service-settings/business-rule.md) §3 · kaynak enum → [`../../../../enums/fill-data-source-type.md`](../../../../enums/fill-data-source-type.md)

## Alanlar
| Alan | Tip | Ne için |
|---|---|---|
| `serviceId` | int (FK → Service) | Kayıtları çekilecek **kaynak servis** (eski "veri seti"nin yeni karşılığı). |
| `parameters` | List\<AssignValueFromDataSetParameter\> | Satır **filtreleri** (→ [`assign-value-from-dataset-parameter.md`](./assign-value-from-dataset-parameter.md)). |
| `valuePropertyId` | int (FK → Property) | **Değer** olarak alınacak kolon (kaynak servisin alanı). |
| `displayPropertyId` | int? (FK → Property) | **Görünen metin** olarak alınacak kolon (liste doldururken). |
| `statusIds` | List\<int\>? (FK → Status) | Yalnız bu **durumlardaki** kayıtlar. |
| `lazyLoading` | bool | `true`: veri **çalışma-anında** sunucudan çekilir. `false`: serviste **gömülü** gelen kayıtlar kullanılır. |
| `cacheDeactive` | bool | `true` ise lazy isteğin istemci cache'i kapatılır. |
| `searchActive` | bool | `true` + `lazyLoading`: liste çekilmez, **arama sunucu tarafında** yapılır (büyük veri için). |
| `sortPropertyId` | int? (FK → Property) | **Sıralama** kolonu. |
| `sortType` | SortDirection | Sıralama yönü (`none`/`asc`/`desc` → [`../../../../enums/sort-direction.md`](../../../../enums/sort-direction.md)). |

## Notlar
- **Tek değer** (`AssignValue.fromDataSet`): tüm parametre koşullarını sağlayan **ilk** kayıttan `valuePropertyId` okunur.
- **Liste** (`fillDataSource.serviceInstances`): eşleşen kayıtlar `{value: valuePropertyId, display: displayPropertyId}` öğelerine çevrilir.
- Sıralama yalnız `sortType != none` **ve** `sortPropertyId` dolu iken uygulanır.
- **Eski `dataSetName` (string) → `serviceId` (FK):** "veri seti" kavramı yeni motorda **başka servisin instance'ları** olarak modellenir; durum filtresi `recordProcessStatusCodes` (string) → **`statusIds`** (FK → Status).

*Oluşturma: 2026-08-26.*
