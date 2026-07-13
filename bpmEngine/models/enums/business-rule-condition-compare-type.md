# Enum — BusinessRuleConditionCompareType

> **Kullanan model:** [`business-rule-condition.md`](../service-settings/business-rule-condition.md) (`referenceValue` / `valueToCompare` tipi)
> **Amaç:** Bir koşulda karşılaştırılan **değerin tipini/kaynağını** belirler (sol/sağ taraf ne ifade ediyor).

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `PropertyValue` | Bir alanın değeri. | Alanın anlık değerini karşılaştırmaya sokmak. |
| `ViewProfile` | Aktif görüntüleme profili. | Hangi profilin aktif olduğuna göre koşullamak. |
| `FixedValue` | Sabit değer. | Bilinen sabitle karşılaştırmak. |
| `FromCalculate` | İfade/hesaplama sonucu. | Türetilen değerle karşılaştırmak. |

*Oluşturma: 2026-07-10.*
