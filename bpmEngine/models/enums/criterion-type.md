# Enum — CriterionType

> **Kullanan model:** [`business-rule-condition.md`](../service-settings/business-rule-condition.md) (alan `criterionType`, tip **CriterionType**) · [`process-step.md`](../service-settings/process-step.md) (**Karşılaştırma** adımı — koşul operatörleri)
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
| `containsAny` | virgülle ayrılmış parçalardan **herhangi biri** değerde geçer. | **Çoklu-değer** (multi-select combobox / liste) koşulu. |
| `containsAll` | parçaların **hepsi** değerde geçer. | Çoklu-değer koşulu. |

## Notlar
- Kodlar **camelCase** olarak normalize edildi (v0.7); operatör sembolü/Türkçe karşılığı "Anlam" sütunundadır.
- **`containsAny`/`containsAll` (v0.35):** çoklu-değer (virgüllü) karşılaştırma; sağ değer parçalara bölünür, sol değerde **herhangi biri/hepsi** aranır.

*Oluşturma: 2026-07-10.*
