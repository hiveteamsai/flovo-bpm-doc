# Model — BusinessRuleCondition (iş kuralı koşulu)

> **Durum:** 🟢 KARAR (v0.35) — **gömülü JSONB** (ayrı tablo değil): `BusinessRule.businessRuleConditions` alanının
> her düğümüdür. **PK/FK yok.**
> **Amaç:** İki değerin bir **operatörle** karşılaştırılması. Koşullar **iç içe (recursive)** gruplanabilir (`and`/`or`).
> **Davranış/kullanım:** → `../../service-settings/business-rule.md` §4

## Alanlar
> **Kalıcılık:** Bu düğüm **gömülü** taşınır (`BusinessRule.businessRuleConditions` JSONB ağacı içinde); `id`/`businessRuleId`/
> `parentConditionId` **yoktur** — hiyerarşi doğrudan `businessRuleConditions` iç-içeliğiyle kurulur.

| Alan | Tip | Açıklama / amaç |
|---|---|---|
| `referenceValue` | BusinessRuleConditionCompareValue | Referans değer (sol taraf) — **değer kaynağı DTO'su**: `compareType` + kaynağa göre alanlar (→ [`./dto/business-rule/shared/business-rule-condition-compare-value.md`](./dto/business-rule/shared/business-rule-condition-compare-value.md)). |
| `valueToCompare` | BusinessRuleConditionCompareValue | Karşılaştırılacak değer (sağ taraf) — aynı DTO. |
| `criterionType` | CriterionType | Operatör (aşağıda) — [`../enums/criterion-type.md`](../enums/criterion-type.md). |
| `isConditionList` | bool | İç içe koşul grubu mu. |
| `businessRuleConditionType` | BusinessRuleConditionType | Alt grup birleştirme — [`../enums/business-rule-condition-type.md`](../enums/business-rule-condition-type.md): `and` (VE) / `or` (VEYA). |
| `businessRuleConditions` | List\<BusinessRuleCondition\> | İç içe koşullar (recursive — gömülü). |

### `criterionType` (operatörler — bu modeldeki rol)
Enum tanımı → [`../enums/criterion-type.md`](../enums/criterion-type.md). Bu modelde iki değerin karşılaştırma operatörünü belirler
(kod → sembol/anlam): `equals` (=) · `notEquals` (!=) · `isEmpty` (boş) · `isNotEmpty` (boş değil) · `greaterThan` (>) ·
`greaterThanOrEqual` (>=) · `lessThan` (<) · `lessThanOrEqual` (<=) · `startsWith` (ile başlar) · `endsWith` (ile biter) ·
`contains` (içerir) · `notContains` (içermez) · `containsAny` (parçalardan biri) · `containsAll` (parçaların hepsi).

### Karşılaştırma değeri (`referenceValue` / `valueToCompare`)
Her iki taraf da bir **`BusinessRuleConditionCompareValue`** DTO'sudur (→ [`./dto/business-rule/shared/business-rule-condition-compare-value.md`](./dto/business-rule/shared/business-rule-condition-compare-value.md)):
**ayrımlayıcı `compareType`** (`propertyValue` · `viewProfile` (aktif profil) · `fixedValue` · `fromCalculation` →
[`../enums/business-rule-condition-compare-type.md`](../enums/business-rule-condition-compare-type.md)) + kaynağa göre **payload** (`propertyValue`/`fixedValue`/`fromCalculation` alt-objeleri; **discriminated union / oneOf** — yalnız biri dolu).

## İlişkiler
- **Gömülü** — `BusinessRule.businessRuleConditions` JSONB ağacının düğümü; kendi içinde recursive (`businessRuleConditions`). Ayrı tablo/FK yok.

## Notlar / açık noktalar
- **Koşul depolama = gömülü JSONB (KARAR v0.35):** koşul ağacı ayrı ilişkisel tabloda değil, `BusinessRule` içinde **JSONB** olarak
  taşınır (`configuration` ile tutarlı) — CRUD tek kayıt, runtime payload doğrudan. Önceki `id`/`businessRuleId`/`parentConditionId`
  (ilişkisel) alanları **düştü**. "Hangi kural X alanını kullanıyor" sorgusu **GIN index** ile karşılanır.
- **`referenceValue`/`valueToCompare`** ayrı DTO'dur (`BusinessRuleConditionCompareValue` — compareType + değer kaynağı; discriminated union).

*Oluşturma: 2026-07-02.*
