# Flovo BPM — Enum'lar (İndeks)

> **Durum:** 🟡 TASLAK — model dokümanlarından çıkarıldı; değer setleri gözden geçirilecek.
> **Amaç:** Modellerde kullanılan **tüm enum'ların tek yerde** indekslenmesi. Her enum'un **değer-düzeyi tanımı**
> (değer → anlam → ne için) kendi dosyasındadır. İlgili model dokümanı, kullandığı enum'a **buradan link** verir ve
> **o değerin o modeldeki görevini** kendi içinde anlatır.
>
> **Adlandırma:** Enum **tip adı** PascalCase (`ActionType`, `ControlType` …); enum **değerleri** camelCase
> (`manual`, `fixedValue` …). Modeldeki **alan adı** camelCase kalır (`actionType`, `valueType` …).
>
> **Kural:** Enum tanımı (kanonik değer listesi + genel anlam) **bu klasörde**; enum'un **bir modeldeki bağlamsal
> rolü** ilgili **model dokümanında**.

---

## Enum dizini

| Enum (tip) | Kullanan model (`alan`) | Değerler (özet) | Dosya |
|---|---|---|---|
| **ActionType** (aksiyon türü) | `action.md` (`actionType`) · `process-step-action.md` | `manual` · `eventForm` · `takePhoto` · `selectFile` · `scanBarcode` · `webhook` · `autoAction` | [`action-type.md`](./action-type.md) |
| **ActionDisplayType** | `action.md` (`actionDisplayType`) | `invisible` · `everywhere` · `onlyFormDetail` · `onlyFastApprove` | [`action-display-type.md`](./action-display-type.md) |
| **BusinessRuleActionType** (iş kuralı aksiyonu) | `business-rule.md` (`businessRuleActionType`) | `setViewForProperties` · `changeViewProfile` · `applyValidation` · `showMessage` · `assignValueToProperty` · `fillDataSource` · `assignValueToPropertyAttribute` · `setStyle` | [`business-rule-action-type.md`](./business-rule-action-type.md) |
| **BusinessRuleRuntimeType** | `business-rule.md` (`businessRuleRuntimeType`) | `always` · `firstOpening` · `whenChanging` | [`business-rule-runtime-type.md`](./business-rule-runtime-type.md) |
| **BusinessRuleConditionType** | `business-rule.md` · `business-rule-condition.md` · `process-step.md` (Karşılaştırma) | `and` (VE) · `or` (VEYA) | [`business-rule-condition-type.md`](./business-rule-condition-type.md) |
| **ValueAssignType** (değer kaynağı) | `business-rule.md` (`assignValueToProperty`) · `process-step.md` (Değer Atama `valueType`) | `fixedValue` · `propertyValue` · `fromCalculation` · `fromDataSet` · `search` · `httpRequest` | [`value-assign-type.md`](./value-assign-type.md) |
| **CriterionType** (operatör) | `business-rule-condition.md` (`criterionType`) · `process-step.md` (Karşılaştırma) | `equals` · `notEquals` · `isEmpty` · `isNotEmpty` · `greaterThan` · `greaterThanOrEqual` · `lessThan` · `lessThanOrEqual` · `startsWith` · `endsWith` · `contains` · `notContains` | [`criterion-type.md`](./criterion-type.md) |
| **BusinessRuleConditionCompareType** | `business-rule-condition.md` (`referenceValue`/`valueToCompare` tipi) | `propertyValue` · `viewProfile` · `fixedValue` · `fromCalculate` | [`business-rule-condition-compare-type.md`](./business-rule-condition-compare-type.md) |
| **RelationalType** | `additional-qualification.md` (`relationalType`) | `users` · `departments` · `professions` · `costCenters` · `workerLevels` | [`relational-type.md`](./relational-type.md) |
| **QualificationValueType** | `additional-qualification.md` (`valueType`) | `string` · `double` · `dateTime` · `combobox` | [`qualification-value-type.md`](./qualification-value-type.md) |
| **FormType** | `service.md` (`formType`) | `form` · `parameter` · `eventForm` | [`form-type.md`](./form-type.md) |
| **ControlType** (propertyType) | `property.md` (`controlTypeId`) | 19 kontrol tipi (`textbox` · `combobox` · `file` · `formList` …) | [`control-type.md`](./control-type.md) |
| **KeyboardType** | `property.md` (`keyboardType` — Textbox/Phone) | _(kaynakta sayılmadı — netleşecek)_ | [`keyboard-type.md`](./keyboard-type.md) |
| **BarcodeFormat** | `property.md` (`barcodeFormat` — Barcode) | _(kaynakta sayılmadı — netleşecek)_ | [`barcode-format.md`](./barcode-format.md) |

---

## Notlar

- **`actionType` çakışması giderildi (v0.7):** Önceden hem Action hem BusinessRule alanı `actionType` adını taşıyordu.
  Karışmayı önlemek için BusinessRule tarafı **`businessRuleActionType`** olarak yeniden adlandırıldı:
  **`Action.actionType`** (tip **ActionType** — tetiklenme türü, `manual`/`webhook`…) ↔ **`BusinessRule.businessRuleActionType`**
  (tip **BusinessRuleActionType** — frontend etkisi, `setViewForProperties`/`assignValueToProperty`…). Ayrı varlıklar, ayrı adlar.
- **`valueType` iki bağlamda:** `AdditionalQualification.valueType` → tip **QualificationValueType**; süreç adımı
  **Değer Atama** `valueType` → tip **ValueAssignType** (değer kaynağı). Aynı alan adı, farklı enum.
- Değer setleri model/özellik dokümanlarından çıkarıldı; kesinleşmemiş olanlar dosyalarında işaretlidir.

*Oluşturma: 2026-07-10.*
