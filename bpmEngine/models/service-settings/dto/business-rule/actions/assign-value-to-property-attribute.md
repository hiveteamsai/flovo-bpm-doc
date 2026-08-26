# DTO — AssignValueToPropertyAttribute (aksiyon konfigi)

> **Tür:** **DTO** — **DB tablosu değildir.** `businessRuleActionType == assignValueToPropertyAttribute` iken
> `BusinessRule.configuration` **JSONB** gövdesinin şeklidir.
> **Amaç:** Bir alanın **değerine değil**, bir **öznitelik/metadata**'sına (ör. minDate, helperText) koşula göre değer yazar.
> **Davranış/kullanım:** → [`../../../../../service-settings/business-rule.md`](../../../../../service-settings/business-rule.md) §3 · öznitelik → [`../../../../enums/property-attribute-type.md`](../../../../enums/property-attribute-type.md)

## Alanlar
| Alan | Tip | Ne için |
|---|---|---|
| `propertyId` | int (FK → Property) | Hedef alan. |
| `propertyAttributeType` | PropertyAttributeType | Değiştirilecek **öznitelik** (`minDate`/`maxDate`/`helperText`/`sideText`/`addNewEnabled`). |
| `value` | AssignValue | Özniteliğe atanacak **değer** (→ [`assign-value.md`](../shared/assign-value.md)). |

## Notlar
- Örnek: `BITIS_TARIHI.minDate ← #BASLANGIC_TARIHI` — bitiş, başlangıçtan önce seçilemez.

*Oluşturma: 2026-08-26.*
