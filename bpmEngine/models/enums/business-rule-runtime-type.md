# Enum — BusinessRuleRuntimeType

> **Kullanan model:** [`business-rule.md`](../service-settings/business-rule.md) — alan `businessRuleRuntimeType`, tip **BusinessRuleRuntimeType**
> **Amaç:** Kuralın form yaşam döngüsünde **ne zaman değerlendirileceğini** belirler.

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `always` | Her değişiklikte ve açılışta sürekli değerlendirilir. | Sürekli geçerli olması gereken kurallar. |
| `firstOpening` | Yalnız form ilk açıldığında bir kez değerlendirilir. | Başlangıç durumunu kurmak (ör. varsayılan görünüm). |
| `whenChanging` | Yalnız izlenen alan(lar) değişince değerlendirilir. | Alan değişimine tepki veren kurallar. |

*Oluşturma: 2026-07-10.*
