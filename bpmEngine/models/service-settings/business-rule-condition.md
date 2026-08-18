# Model — BusinessRuleCondition (iş kuralı koşulu)

> **Durum:** 🟡 TASLAK — `BusinessRule` ile birlikte **en son** kesinleşecek (→ `../../todo.md`).
> **Amaç:** İki değerin bir **operatörle** karşılaştırılması. Koşullar **iç içe (recursive)** gruplanabilir (`and`/`or`).
> **Davranış/kullanım:** → `../../service-settings/business-rule.md` §4

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Koşul ID'si. |
| `businessRuleId` | int | FK → BusinessRule.id | Bağlı kural. |
| `parentConditionId` | int? | FK → BusinessRuleCondition.id | İç içe (recursive) üst koşul; `null` = kök. |
| `referenceValue` | BusinessRuleConditionCompareType | — | Referans değer (sol taraf); tipi [`../enums/business-rule-condition-compare-type.md`](../enums/business-rule-condition-compare-type.md). |
| `valueToCompare` | BusinessRuleConditionCompareType | — | Karşılaştırılacak değer (sağ taraf); tipi [`../enums/business-rule-condition-compare-type.md`](../enums/business-rule-condition-compare-type.md). |
| `criterionType` | CriterionType | — | Operatör (aşağıda) — [`../enums/criterion-type.md`](../enums/criterion-type.md). |
| `isConditionList` | bool | — | İç içe koşul grubu mu. |
| `businessRuleConditionType` | BusinessRuleConditionType | — | Alt grup birleştirme — [`../enums/business-rule-condition-type.md`](../enums/business-rule-condition-type.md): `and` (VE) / `or` (VEYA). |
| `businessRuleConditions` | List\<BusinessRuleCondition\> | — | İç içe koşullar (recursive). |

### `criterionType` (operatörler — bu modeldeki rol)
Enum tanımı → [`../enums/criterion-type.md`](../enums/criterion-type.md). Bu modelde iki değerin karşılaştırma operatörünü belirler
(kod → sembol/anlam): `equals` (=) · `notEquals` (!=) · `isEmpty` (boş) · `isNotEmpty` (boş değil) · `greaterThan` (>) ·
`greaterThanOrEqual` (>=) · `lessThan` (<) · `lessThanOrEqual` (<=) · `startsWith` (ile başlar) · `endsWith` (ile biter) ·
`contains` (içerir) · `notContains` (içermez).

### `BusinessRuleConditionCompareType` (karşılaştırma değer tipleri — bu modeldeki rol)
Enum tanımı → [`../enums/business-rule-condition-compare-type.md`](../enums/business-rule-condition-compare-type.md). Bu modelde `referenceValue`/`valueToCompare`'in neyi ifade ettiğini belirler:
`propertyValue` · `viewProfile` (aktif profil) · `fixedValue` · `fromCalculation` (expression).

## İlişkiler
- **N – 1** → `BusinessRule` (`businessRuleId`), `BusinessRuleCondition` (`parentConditionId`, recursive).

## Notlar / açık noktalar
- `id`/`businessRuleId`/`parentConditionId` DB modeli için **eklendi** (kaynak dokümanda gömülü/recursive anlatılıyor); yapı iş kuralı fazında teyit edilecek.

*Oluşturma: 2026-07-02.*
