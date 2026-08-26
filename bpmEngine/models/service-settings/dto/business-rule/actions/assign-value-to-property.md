# DTO — AssignValueToProperty (aksiyon konfigi)

> **Tür:** **DTO** — **DB tablosu değildir.** `businessRuleActionType == assignValueToProperty` iken
> `BusinessRule.configuration` **JSONB** gövdesinin şeklidir.
> **Amaç:** Bir alanın **değerine** koşula göre otomatik değer atar.
> **Davranış/kullanım:** → [`../../../../../service-settings/business-rule.md`](../../../../../service-settings/business-rule.md) §3.1

## Alanlar
| Alan | Tip | Ne için |
|---|---|---|
| `propertyId` | int (FK → Property) | Değer **atanacak** alan. |
| `value` | AssignValue | Atanacak değerin **kaynağı** (→ [`assign-value.md`](../shared/assign-value.md)). |
| `clearIfConditionNotTrue` | bool | Koşul **sağlanmazsa** hedef alan **temizlensin**. |

## Notlar
- Değer atama, hedef kontrol "değişti" derse **zincirleme** yeni bir kural turu tetikler (→ [`../../../../../service-settings/business-rule.md`](../../../../../service-settings/business-rule.md) §5).
- Asenkron kaynaklar (`fromDataSet` lazy · `httpRequest` · async `fromCalculation`) için atama, istek tamamlanınca yapılır.
- **Eski `childField` (DataGrid) **taşınmadı**** (DataGrid kaldırıldı).

*Oluşturma: 2026-08-26.*
