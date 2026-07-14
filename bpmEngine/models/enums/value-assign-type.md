# Enum — ValueAssignType

> **Kullanan model:** [`business-rule.md`](../service-settings/business-rule.md) (`assignValueToProperty` aksiyonu) · süreç adımı **Değer Atama** [`process-step.md`](../service-settings/process-step.md) — alan `valueType`, tip **ValueAssignType**
> **Amaç:** Bir alana atanacak değerin **nereden geleceğini** (kaynağını) belirler.

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `fixedValue` | Sabit, elle girilen değer. | Bilinen sabit bir değeri yazmak. |
| `propertyValue` | Başka bir alanın değeri. | Alandan alana değer taşımak/yansıtmak. |
| `fromCalculation` | Bir ifade/hesaplama sonucu. | Formül ile türetilen değer. |
| `fromDataSet` | Bir veri kümesinden çekilen değer. | Kayıtlı veri setinden değer getirmek. |
| `search` | Arama sonucu seçilen değer. | Kullanıcının aramayla bulduğu kaydı atamak. |
| `httpRequest` | Dış HTTP isteğinin dönüşü. | Entegrasyondan gelen değeri atamak. |

## Notlar
- **⚠️ Alan adı çakışması:** Süreç adımı Değer Atama'daki `valueType` **bu** enum'dur (**ValueAssignType**); [`additional-qualification.md`](../organization-settings/additional-qualification.md)'deki `valueType` ise [`qualification-value-type.md`](./qualification-value-type.md)'dir (**QualificationValueType** — farklı enum).

*Oluşturma: 2026-07-10.*
