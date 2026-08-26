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
| `referenceValue` | BusinessRuleConditionCompareValue | — | Referans değer (sol taraf) — **değer kaynağı DTO'su** (JSONB): `compareType` + kaynağa göre alanlar (→ [`./dto/business-rule/shared/business-rule-condition-compare-value.md`](./dto/business-rule/shared/business-rule-condition-compare-value.md)). |
| `valueToCompare` | BusinessRuleConditionCompareValue | — | Karşılaştırılacak değer (sağ taraf) — aynı DTO. |
| `criterionType` | CriterionType | — | Operatör (aşağıda) — [`../enums/criterion-type.md`](../enums/criterion-type.md). |
| `isConditionList` | bool | — | İç içe koşul grubu mu. |
| `businessRuleConditionType` | BusinessRuleConditionType | — | Alt grup birleştirme — [`../enums/business-rule-condition-type.md`](../enums/business-rule-condition-type.md): `and` (VE) / `or` (VEYA). |
| `businessRuleConditions` | List\<BusinessRuleCondition\> | — | İç içe koşullar (recursive). |

### `criterionType` (operatörler — bu modeldeki rol)
Enum tanımı → [`../enums/criterion-type.md`](../enums/criterion-type.md). Bu modelde iki değerin karşılaştırma operatörünü belirler
(kod → sembol/anlam): `equals` (=) · `notEquals` (!=) · `isEmpty` (boş) · `isNotEmpty` (boş değil) · `greaterThan` (>) ·
`greaterThanOrEqual` (>=) · `lessThan` (<) · `lessThanOrEqual` (<=) · `startsWith` (ile başlar) · `endsWith` (ile biter) ·
`contains` (içerir) · `notContains` (içermez).

### Karşılaştırma değeri (`referenceValue` / `valueToCompare`)
Her iki taraf da bir **`BusinessRuleConditionCompareValue`** DTO'sudur (→ [`./dto/business-rule/shared/business-rule-condition-compare-value.md`](./dto/business-rule/shared/business-rule-condition-compare-value.md)):
**ayrımlayıcı `compareType`** (`propertyValue` · `viewProfile` (aktif profil) · `fixedValue` · `fromCalculation` →
[`../enums/business-rule-condition-compare-type.md`](../enums/business-rule-condition-compare-type.md)) + kaynağa göre **payload** (`propertyValue`/`fixedValue`/`fromCalculation` alt-objeleri; **discriminated union / oneOf** — yalnız biri dolu).

## İlişkiler
- **N – 1** → `BusinessRule` (`businessRuleId`), `BusinessRuleCondition` (`parentConditionId`, recursive).

## Notlar / açık noktalar
- `id`/`businessRuleId`/`parentConditionId` DB modeli için **eklendi** (kaynak dokümanda gömülü/recursive anlatılıyor); yapı iş kuralı fazında teyit edilecek.
- **`referenceValue`/`valueToCompare` ayrı DTO'ya çıkarıldı (v0.34, gerçek kod: `WorkRuleConditionCompareValueDto`):** düz enum değil,
  **`BusinessRuleConditionCompareValue`** (compareType + değer kaynağı alanları) — JSONB kolon olarak saklanır.

*Oluşturma: 2026-07-02.*
