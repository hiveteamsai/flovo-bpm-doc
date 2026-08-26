# DTO — ApplyValidation (aksiyon konfigi)

> **Tür:** **DTO** — **DB tablosu değildir.** `businessRuleActionType == applyValidation` iken
> `BusinessRule.configuration` **JSONB** gövdesinin şeklidir.
> **Amaç:** Koşullu validasyon — sağlanmazsa kullanıcıya hata/uyarı mesajı; kaydetmeyi/aksiyonu bloklayabilir.
> **Davranış/kullanım:** → [`../../../../../service-settings/business-rule.md`](../../../../../service-settings/business-rule.md) §3

## Alanlar
| Alan | Tip | Ne için |
|---|---|---|
| `message` | AssignValue | Validasyon **mesajı** — yalnız `fixedValue` veya `fromCalculation` (→ [`assign-value.md`](../shared/assign-value.md)). |
| `canPassValidation` | bool | `true`: **uyarı** (kullanıcı devam edebilir); `false`: **engelleyici** (kaydetme/aksiyon bloklanır). |
| `showAsPopup` | bool | Mesaj **popup** olarak da gösterilsin. |
| `withFormList` | bool | `true`: validasyon **Form List** satırları üzerinde **satır-bazlı** çalışır. |
| `formListPropertyId` | int? (FK → Property) | `withFormList` ise hedef **Form List** alanı. |
| `formListRowCondition` | BusinessRuleCondition? | Her Form List satırında **ayrıca** değerlendirilecek koşul (→ [`../../../business-rule-condition.md`](../../../business-rule-condition.md)). |

## Notlar
- Koşul **düzelince** ilgili validasyon girdisi **otomatik kalkar** (kural-bazlı durumsal yönetim).
- **Eski `ModalList` → `formList`** (→ `new-vs-current-names.md` §6/§8): `withFormList` = Form List satır-bazlı; `formListPropertyId` = Form List alanı; `formListRowCondition` = satır koşulu. _(Eski Flutter: `withModal`/`modalProperty`/`withModalCondition`.)_

*Oluşturma: 2026-08-26.*
