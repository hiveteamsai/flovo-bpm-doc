# Enum — businessRuleConditionType (BusinessRule / BusinessRuleCondition)

> **Kullanan model:** [`business-rule.md`](../service-settings/business-rule.md) · [`business-rule-condition.md`](../service-settings/business-rule-condition.md) (`businessRuleConditionType`) · [`process-step.md`](../service-settings/process-step.md) (**Karşılaştırma** adımı — `conditionType`)
> **Amaç:** Bir koşul grubundaki alt koşulların **mantıksal birleştirme** biçimini belirler.

## Değerler
| Kod | Anlam | Ne için |
|---|---|---|
| `and` | VE — grubun **tüm** alt koşulları sağlanmalı. | Birden çok koşulun aynı anda geçerli olması gereken durumlar. |
| `or` | VEYA — grubun **en az bir** alt koşulu sağlanmalı. | Alternatif koşullardan herhangi biri geçerliyse tetiklenme. |

## Notlar
- Koşullar iç içe (recursive) gruplanabildiğinden bu tür **grup düzeyinde** uygulanır (`isConditionList` = true olan düğümde).
- Kodlar **camelCase** olarak normalize edildi (v0.7); Türkçe karşılığı (VE/VEYA) "Anlam" sütunundadır.

*Oluşturma: 2026-07-10.*
