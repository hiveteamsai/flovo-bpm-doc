# Enum — criterionType (operatör)

> **Kullanan model:** [`business-rule-condition.md`](../service-settings/business-rule-condition.md) (`criterionType`) · [`process-step.md`](../service-settings/process-step.md) (**Karşılaştırma** adımı — koşul operatörleri)
> **Amaç:** Bir koşulda iki değerin **hangi operatörle** karşılaştırılacağını belirler.

## Değerler
| Kod | Anlam (operatör) | Ne için |
|---|---|---|
| `equals` | `=` Eşit. | İki değerin eşitliğini denetlemek. |
| `notEquals` | `!=` Eşit değil. | Eşitsizlik denetimi. |
| `isEmpty` | boş. | Alanın doldurulmadığını denetlemek. |
| `isNotEmpty` | boş değil. | Alanın doldurulduğunu denetlemek. |
| `greaterThan` | `>` Büyük. | Sayısal/tarihsel büyüklük. |
| `greaterThanOrEqual` | `>=` Büyük veya eşit. | Alt sınır denetimi. |
| `lessThan` | `<` Küçük. | Sayısal/tarihsel küçüklük. |
| `lessThanOrEqual` | `<=` Küçük veya eşit. | Üst sınır denetimi. |
| `startsWith` | ile başlar. | Metin başlangıcını denetlemek. |
| `endsWith` | ile biter. | Metin sonunu denetlemek. |
| `contains` | içerir. | Alt dize varlığını denetlemek. |
| `notContains` | içermez. | Alt dize yokluğunu denetlemek. |

## Notlar
- Kodlar **camelCase** olarak normalize edildi (v0.7); operatör sembolü/Türkçe karşılığı "Anlam" sütunundadır.

*Oluşturma: 2026-07-10.*
