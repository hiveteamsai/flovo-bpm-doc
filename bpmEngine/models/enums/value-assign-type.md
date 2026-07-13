# Enum — ValueAssignType (değer kaynağı)

> **Kullanan model:** [`business-rule.md`](../service-settings/business-rule.md) (`AssignValueToProperty` aksiyonu) · süreç adımı **Değer Atama** [`process-step.md`](../service-settings/process-step.md) (`valueType`)
> **Amaç:** Bir alana atanacak değerin **nereden geleceğini** (kaynağını) belirler.

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `FixedValue` | Sabit, elle girilen değer. | Bilinen sabit bir değeri yazmak. |
| `PropertyValue` | Başka bir alanın değeri. | Alandan alana değer taşımak/yansıtmak. |
| `FromCalculation` | Bir ifade/hesaplama sonucu. | Formül ile türetilen değer. |
| `FromDataSet` | Bir veri kümesinden çekilen değer. | Kayıtlı veri setinden değer getirmek. |
| `Search` | Arama sonucu seçilen değer. | Kullanıcının aramayla bulduğu kaydı atamak. |
| `HttpRequest` | Dış HTTP isteğinin dönüşü. | Entegrasyondan gelen değeri atamak. |

## Notlar
- **⚠️ Alan adı çakışması:** Süreç adımı Değer Atama'daki `valueType` **bu** enum'dur; [`additional-qualification.md`](../organization-settings/additional-qualification.md)'deki `valueType` ise [`qualification-value-type.md`](./qualification-value-type.md)'dir (farklı enum).

*Oluşturma: 2026-07-10.*
