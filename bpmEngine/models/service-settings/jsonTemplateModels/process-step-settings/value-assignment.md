# Process Step Settings — `valueAssignment` (Değer Atama)

> **stepType:** `valueAssignment` · **Adım:** bir form property'sine **veya** formun altındaki alt-servis kayıtlarına **sabit / kaynak-alandan / hesaplanan** değer yazan **otomatik** adım; işini yapıp `default` aksiyonla ilerler.
> **Davranış:** → [`../../../../service-settings/process-step.md`](../../../../service-settings/process-step.md) §3.4 · **Model (§3):** [`../../process-step.md`](../../process-step.md) §3.3 · **İndeks:** [`index.md`](./index.md).
> **Depolama:** `ProcessStep.settings` (JSONB), ayrımlayıcı `stepType`.

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `valueAssignType` | [`ValueAssignType`](../../../enums/value-assign-type.md) | evet | — | Atanacak değerin **kaynağı**. Bu adımda geçerli **alt-küme** yalnız üç değer: `fixedValue` (sabit) · `propertyValue` (başka bir form alanının değeri) · `fromCalculation` (ifadeyle hesaplanan). Enum'un `fromDataSet`/`search`/`httpRequest` değerleri **yalnız iş kuralı** `assignValueToProperty` içindir; burada **geçersiz** (JSON Schema `enum` ile kısıtlanır). |
| `fixedValue` | string | koşullu | — | Yazılacak **sabit** değer (`valueAssignType = fixedValue` iken). |
| `expression` | string | koşullu | — | Değeri üreten **ifade** (`valueAssignType = fromCalculation` iken); form alanlarına (`#ALAN`) ve operatörlere dayanan hesaplama. |
| `useDisplay` | bool | hayır | `false` | Kaynak alanın **görüntü (display)** değerini kullan. Ham değer yerine kullanıcıya görünen metni taşımak için (ör. Combobox'ta id yerine seçili öğenin etiketi). |
| `targetPropertyId` | int | evet | — | Değerin **yazılacağı** hedef property. `useAssociatedService = false` iken **bu formdaki** alan; `true` iken **alt-servis kayıtlarındaki** alandır. **`settings` içi referans id** (§3). |
| `propertyId` | int | koşullu | — | **Kaynak** property (`valueAssignType = propertyValue` iken değeri okunacak alan). **`settings` içi referans id** (§3). |
| `useAssociatedService` | bool | hayır | `false` | Atama kapsamı: `false` → **aynı formdaki** property; `true` → formun altındaki **alt-servis (Form List)** kayıtlarına yazılır (→ [`../property-settings/form-list.md`](../property-settings/form-list.md)). |
| `associatedServiceId` | int? | koşullu | — | `useAssociatedService = true` iken **hedef alt-servis**. **`settings` içi referans id** (§3). |
| `targetInstancesPropertyId` | int? | koşullu | — | `useAssociatedService = true` iken, alt-servis kayıt(lar)ını taşıyan **Form List property'si** — değerin hangi bağlı kayıtlara yazılacağını belirler. **`settings` içi referans id** (§3). |

> **Akış yönlendirme `settings`'te DEĞİL:** Atama tamamlanınca **`default`** kodlu `ProcessStepAction` tetiklenir → [`../../process-step-action.md`](../../process-step-action.md).

## 2. Alt-model
- Yok. Alanlar `settings` kök nesnesinde **düz** (flat) tutulur; ValueAssignType burada **ayrı bir `value` nesnesi değil**, doğrudan `valueAssignType` + eşlik eden alan (`fixedValue`/`expression`/`propertyId`) olarak modellenir.

## 3. Ortak alanlar (settings'te değil — `ProcessStep` kolonu)
`code`·`stepType`·`definition`·`order`·`showInHistory`·`skip*`·`environmentRestriction` → [`../../process-step.md`](../../process-step.md) §1.
`settings` içindeki referans id'ler (`targetPropertyId`·`propertyId`·`associatedServiceId`·`targetInstancesPropertyId`) **DB FK'si değildir** → uygulama-katmanı doğrulaması + silme koruması (→ [`../../../../todo.md`](../../../../todo.md)).

## 4. JSON Schema
```json
{
  "$id": "process-step-settings/valueAssignment",
  "type": "object",
  "additionalProperties": false,
  "required": ["valueAssignType", "targetPropertyId"],
  "properties": {
    "valueAssignType": { "enum": ["fixedValue", "propertyValue", "fromCalculation"] },
    "fixedValue":  { "type": "string" },
    "expression":  { "type": "string" },
    "useDisplay":  { "type": "boolean", "default": false },
    "targetPropertyId": { "type": "integer" },
    "propertyId":  { "type": "integer" },
    "useAssociatedService": { "type": "boolean", "default": false },
    "associatedServiceId": { "type": "integer" },
    "targetInstancesPropertyId": { "type": "integer" }
  },
  "allOf": [
    {
      "if":   { "properties": { "valueAssignType": { "const": "fixedValue" } }, "required": ["valueAssignType"] },
      "then": { "required": ["fixedValue"] }
    },
    {
      "if":   { "properties": { "valueAssignType": { "const": "propertyValue" } }, "required": ["valueAssignType"] },
      "then": { "required": ["propertyId"] }
    },
    {
      "if":   { "properties": { "valueAssignType": { "const": "fromCalculation" } }, "required": ["valueAssignType"] },
      "then": { "required": ["expression"] }
    },
    {
      "if":   { "properties": { "useAssociatedService": { "const": true } }, "required": ["useAssociatedService"] },
      "then": { "required": ["associatedServiceId", "targetInstancesPropertyId"] }
    }
  ]
}
```
> Not: `valueAssignType` enum'u bilerek **3 değere** daraltıldı (`fromDataSet`/`search`/`httpRequest` yalnız iş kuralı bağlamında geçerlidir → [`value-assign-type.md`](../../../enums/value-assign-type.md)). Referans id'lerin (`targetPropertyId`/`propertyId`/…) varlığı ve tip uyumu **uygulama-katmanı** doğrulamasıdır.

## 5. Örnek
```json
{
  "valueAssignType": "fromCalculation",
  "expression": "#TUTAR * #KUR",
  "targetPropertyId": 42,
  "useAssociatedService": false
}
```
```json
{
  "valueAssignType": "propertyValue",
  "propertyId": 18,
  "useDisplay": true,
  "targetPropertyId": 55,
  "useAssociatedService": true,
  "associatedServiceId": 12,
  "targetInstancesPropertyId": 30
}
```

*Oluşturma: 2026-08-28.*
