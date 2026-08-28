# Process Step Settings — `comparison` (Karşılaştırma)

> **stepType:** `comparison` · **Adım:** girilen koşulları değerlendiren **otomatik** adım; sonuç **doğruysa `true`**,
> **sağlanmıyorsa `false`** aksiyonuyla ilerler (IF benzeri iki dallı).
> **Davranış:** → [`../../../../service-settings/process-step.md`](../../../../service-settings/process-step.md) §3.13 · **Model (§3):** [`../../process-step.md`](../../process-step.md) §3.4 · **İndeks:** [`index.md`](./index.md).
> **Depolama:** `ProcessStep.settings` (JSONB), ayrımlayıcı `stepType`.

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `conditions` | `ComparisonCondition[]` | evet | — | Değerlendirilecek koşul(lar) — her düğüm ya bir **yaprak** (referans değer + operatör + karşılaştırılan değer) ya da alt koşulları toplayan bir **grup** (`children`). İç içe (recursive) gruplanabilir (§2). En az bir koşul gerekir. |
| `conditionType` | [`BusinessRuleConditionType`](../../../enums/business-rule-condition-type.md) | hayır | `and` | Kök seviyedeki `conditions` düğümlerinin birleştirilme mantığı — `and` (tümü sağlanmalı) · `or` (en az biri sağlanmalı). |

> **Akış yönlendirme `settings`'te DEĞİL:** `true`/`false` dalları ayrı alanda tutulmaz; koşul sonucuna göre **aynı kodlu**
> (`true` veya `false`) [`ProcessStepAction`](../../process-step-action.md) tetiklenir (`targetProcessStepId` orada). Böylece
> hedef adımlar bu `settings`'ten bağımsızdır.

## 2. Alt-model — `ComparisonCondition` (recursive)
Koşul ağacının bir düğümü. **Yaprak düğüm** iki değeri bir operatörle karşılaştırır (`referenceValue` / `criterionType` /
`valueToCompare`). **Grup düğüm** ise `children` ile alt koşulları taşır (gruplama/parantezleme). Düğüm kendini içerdiğinden
ağaç istenildiği kadar derinleşebilir.

| Alan | Tip | Zorunlu | Açıklama |
|---|---|---|---|
| `referenceValue` | `ValueAssignType`-değeri | koşullu | Karşılaştırmanın **sol tarafı** (referans). Değer **kaynağı**: `fixedValue` (sabit) · `propertyValue` (form alanından) · `fromCalculation` (ifade) → [`../../../enums/value-assign-type.md`](../../../enums/value-assign-type.md). **Yaprak** düğümde zorunlu. |
| `criterionType` | [`CriterionType`](../../../enums/criterion-type.md) | koşullu | Operatör (`equals`·`greaterThan`·`contains`…). **Yaprak** düğümde zorunlu. |
| `valueToCompare` | `ValueAssignType`-değeri | koşullu | Karşılaştırmanın **sağ tarafı**. `referenceValue` ile aynı değer-kaynağı yapısı. `isEmpty`/`isNotEmpty` operatörlerinde **kullanılmaz**. |
| `children` | `ComparisonCondition[]` | koşullu | **Grup** düğümde alt koşullar (iç içe). Doluysa düğüm gruptur; `referenceValue`/`criterionType`/`valueToCompare` alanları o düğümde beklenmez. |

> **Yaprak ⟷ grup:** Bir düğümde ya `referenceValue`+`criterionType`(+`valueToCompare`) ya da `children` bulunur — ikisi birden
> değil. Grup düğümünün alt koşullarının **and/or** birleşimi bu modelde kök `conditionType` ile hizalanır; düğüm-başına ayrı
> birleştirici (iş kuralındaki `businessRuleConditionType` gibi) **taşınmaz** → gerekirse genişletme [`../../../../todo.md`](../../../../todo.md).

> Not: Çalışma-zamanında hesaplanan **koşul sonucu** (`true`/`false`) **ayar değildir**, kaydedilen `settings`'e girmez.

## 3. Ortak alanlar (settings'te değil — `ProcessStep` kolonu)
`code`·`stepType`·`definition`·`order`·`showInHistory`·`skip*`·`environmentRestriction` → [`../../process-step.md`](../../process-step.md) §1.

## 4. JSON Schema
```json
{
  "$id": "process-step-settings/comparison",
  "type": "object",
  "additionalProperties": false,
  "required": ["conditions"],
  "properties": {
    "conditions":    { "type": "array", "minItems": 1, "items": { "$ref": "#/$defs/comparisonCondition" } },
    "conditionType": { "enum": ["and", "or"], "default": "and" }
  },
  "$defs": {
    "comparisonCondition": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "referenceValue": { "type": "object" },
        "criterionType":  { "enum": ["equals", "notEquals", "isEmpty", "isNotEmpty", "greaterThan", "greaterThanOrEqual", "lessThan", "lessThanOrEqual", "startsWith", "endsWith", "contains", "notContains", "containsAny", "containsAll"] },
        "valueToCompare": { "type": "object" },
        "children":       { "type": "array", "items": { "$ref": "#/$defs/comparisonCondition" } }
      }
    }
  }
}
```
> Not: `referenceValue`/`valueToCompare`'ın tam şeması **ValueAssignType** discriminated-union'ıdır (`fixedValue`/`propertyValue`/`fromCalculation`); ortak tanım → [`../../../enums/value-assign-type.md`](../../../enums/value-assign-type.md). Yaprak/grup ayrımı (yaprakta `referenceValue`+`criterionType`, grupta `children`), `propertyValue.propertyId` referansları ve `isEmpty`/`isNotEmpty`'de `valueToCompare` gereksizliği **uygulama-katmanı** doğrulamasıdır.

## 5. Örnek
```json
{
  "conditionType": "and",
  "conditions": [
    {
      "referenceValue": { "valueAssignType": "propertyValue", "propertyValue": { "propertyId": 42 } },
      "criterionType": "greaterThan",
      "valueToCompare": { "valueAssignType": "fixedValue", "fixedValue": { "value": "1000" } }
    },
    {
      "children": [
        {
          "referenceValue": { "valueAssignType": "propertyValue", "propertyValue": { "propertyId": 7 } },
          "criterionType": "equals",
          "valueToCompare": { "valueAssignType": "fixedValue", "fixedValue": { "value": "approved" } }
        },
        {
          "referenceValue": { "valueAssignType": "propertyValue", "propertyValue": { "propertyId": 9 } },
          "criterionType": "isNotEmpty"
        }
      ]
    }
  ]
}
```

*Oluşturma: 2026-08-28.*
