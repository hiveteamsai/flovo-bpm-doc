# DTO — ShowMessage (aksiyon konfigi)

> **Tür:** **DTO** — **DB tablosu değildir.** `businessRuleActionType == showMessage` iken
> `BusinessRule.configuration` **JSONB** gövdesinin şeklidir.
> **Amaç:** Koşul sağlanınca kullanıcıya **bilgi/uyarı mesajı** (başlık + gövde) gösterir.
> **Davranış/kullanım:** → [`../../../../../service-settings/business-rule.md`](../../../../../service-settings/business-rule.md) §3

## Alanlar
| Alan | Tip | Ne için |
|---|---|---|
| `title` | AssignValue | Dialog **başlığı** (`fixedValue`/`fromCalculation`); boş kalırsa varsayılan "Bilgilendirme" (→ [`assign-value.md`](../shared/assign-value.md)). |
| `message` | AssignValue | Dialog **mesajı** (`fixedValue`/`fromCalculation`). |

## Notlar
- **Durum tutmaz:** koşul her sağlandığında dialog yeniden gösterilir; pratikte kural yalnız koşul alanı değişince tetiklendiği için alan değişimi başına bir kez görünür. "Bir kez göster" mekanizması → iş-kuralı fazında değerlendirilecek *(→ [`../../../../../todo.md`](../../../../../todo.md))*.

*Oluşturma: 2026-08-26.*
