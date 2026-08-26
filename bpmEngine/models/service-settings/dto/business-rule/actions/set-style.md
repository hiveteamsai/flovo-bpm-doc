# DTO — SetStyle (aksiyon konfigi)

> **Tür:** **DTO** — **DB tablosu değildir.** `businessRuleActionType == setStyle` iken
> `BusinessRule.configuration` **JSONB** gövdesinin şeklidir.
> **Amaç:** Bir alanın/öğenin **tekil görünüm niteliklerini** (ör. `fontSize`, `titleColor`) koşula göre değiştirir.
> **Davranış/kullanım:** → [`../../../../../service-settings/business-rule.md`](../../../../../service-settings/business-rule.md) §3

## Alanlar
| Alan | Tip | Ne için |
|---|---|---|
| `propertyId` | int (FK → Property) | Hedef alan (**Form List** olabilir). |
| `formListPropertyId` | int? (FK → Property) | Form List içinde stillenecek **alt alan**; boşsa **satırın kendisi** stillenir. |
| `formListRowCondition` | BusinessRuleCondition? | Her Form List satırında değerlendirilecek koşul (→ [`../../../business-rule-condition.md`](../../../business-rule-condition.md)). |
| `style` | görünüm-niteliği objesi | Uygulanacak **tekil nitelikler** (ör. `fontSize`, `titleColor`). |
| `clearIfConditionNotTrue` | bool | Koşul sağlanmazsa stil **temizlensin**. |

## Notlar
- **`style.md` Style varlığını SEÇMEZ:** [`../../../../organization-settings/style.md`](../../../../organization-settings/style.md) referansla seçilen bir varlıktır; `setStyle` ise daha **spesifik, tekil** nitelik değişimidir. `style` objesinin kesin şeması → iş-kuralı fazında netleşecek *(→ [`../../../../../todo.md`](../../../../../todo.md))*.
- **Eski `ModalList` → `formList`** (→ `new-vs-current-names.md` §6).

*Oluşturma: 2026-08-26.*
