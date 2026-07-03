# Model — WorkRuleCondition (iş kuralı koşulu)

> **Durum:** 🟡 TASLAK — `WorkRule` ile birlikte **en son** kesinleşecek (→ `../todo.md`).
> **Amaç:** İki değerin bir **operatörle** karşılaştırılması. Koşullar **iç içe (recursive)** gruplanabilir (VE/VEYA).
> **Davranış/kullanım:** → `../servis-ayarlari/work-rule.md` §4

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Koşul ID'si. |
| `workRuleId` | int | FK → WorkRule.id | Bağlı kural. |
| `parentConditionId` | int (null olabilir) | FK → WorkRuleCondition.id | İç içe (recursive) üst koşul; `null` = kök. |
| `referenceValue` | — | — | Referans değer (sol taraf); tipi `WorkRuleConditionCompareType`. |
| `valueToCompare` | — | — | Karşılaştırılacak değer (sağ taraf). |
| `criterionType` | enum | — | Operatör (aşağıda). |
| `isConditionList` | bool | — | İç içe koşul grubu mu. |
| `workRuleConditionType` | enum | — | Alt grup birleştirme: VE / VEYA. |
| `workRuleConditions` | List\<WorkRuleCondition\> | — | İç içe koşullar (recursive). |

### `criterionType` (operatörler)
`=` · `!=` · boş · boş değil · `>` · `>=` · `<` · `<=` · ile başlar · ile biter · içerir · içermez.

### `WorkRuleConditionCompareType` (karşılaştırma değer tipleri)
`PropertyValue` · `ViewProfile` (aktif profil) · `FixedValue` · `FromCalculate` (expression).

## İlişkiler
- **N – 1** → `WorkRule` (`workRuleId`), `WorkRuleCondition` (`parentConditionId`, recursive).

## Notlar / açık noktalar
- `id`/`workRuleId`/`parentConditionId` DB modeli için **eklendi** (kaynak dokümanda gömülü/recursive anlatılıyor); yapı iş kuralı fazında teyit edilecek.

*Oluşturma: 2026-07-02.*
