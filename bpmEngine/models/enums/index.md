# Flovo BPM — Enum'lar (İndeks)

> **Durum:** 🟡 TASLAK — model dokümanlarından çıkarıldı; değer setleri gözden geçirilecek.
> **Amaç:** Modellerde kullanılan **tüm enum'ların tek yerde** indekslenmesi. Her enum'un **değer-düzeyi tanımı**
> (değer → anlam → ne için) kendi dosyasındadır. İlgili model dokümanı, kullandığı enum'a **buradan link** verir ve
> **o değerin o modeldeki görevini** kendi içinde anlatır.
>
> **Adlandırma:** Enum **tip adı** PascalCase (`ActionType`, `PropertyType` …); enum **değerleri** camelCase
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
| **BusinessRuleActionType** (iş kuralı aksiyonu) | `business-rule.md` (`businessRuleActionType`) | `setViewForProperties` · `applyValidation` · `showMessage` · `assignValueToProperty` · `fillDataSource` · `assignValueToPropertyAttribute` · `setStyle` | [`business-rule-action-type.md`](./business-rule-action-type.md) |
| **BusinessRuleRuntimeType** | `business-rule.md` (`businessRuleRuntimeType`) | `always` · `firstOpening` · `whenChanging` | [`business-rule-runtime-type.md`](./business-rule-runtime-type.md) |
| **BusinessRuleConditionType** | `business-rule.md` · `business-rule-condition.md` · `process-step.md` (Karşılaştırma) | `and` (VE) · `or` (VEYA) | [`business-rule-condition-type.md`](./business-rule-condition-type.md) |
| **ValueAssignType** (değer kaynağı) | `business-rule.md` (`assignValueToProperty` — 6 değer) · `process-step.md` (Değer Atama `valueAssignType` — 3-değer alt-küme) | `fixedValue` · `propertyValue` · `fromCalculation` · `fromDataSet` · `search` · `httpRequest` | [`value-assign-type.md`](./value-assign-type.md) |
| **CriterionType** (operatör) | `business-rule-condition.md` (`criterionType`) · `process-step.md` (Karşılaştırma) | `equals` · `notEquals` · `isEmpty` · `isNotEmpty` · `greaterThan` · `greaterThanOrEqual` · `lessThan` · `lessThanOrEqual` · `startsWith` · `endsWith` · `contains` · `notContains` | [`criterion-type.md`](./criterion-type.md) |
| **BusinessRuleConditionCompareType** | `business-rule-condition.md` (`referenceValue`/`valueToCompare` tipi) | `propertyValue` · `viewProfile` · `fixedValue` · `fromCalculate` | [`business-rule-condition-compare-type.md`](./business-rule-condition-compare-type.md) |
| **RelationalType** | `additional-qualification.md` (`relationalType`) | `users` · `departments` · `professions` · `costCenters` · `workerLevels` | [`relational-type.md`](./relational-type.md) |
| **QualificationValueType** | `additional-qualification.md` (`valueType`) | `string` · `double` · `dateTime` · `combobox` | [`qualification-value-type.md`](./qualification-value-type.md) |
| **FormType** | `service.md` (`formType`) | `form` · `parameter` · `eventForm` | [`form-type.md`](./form-type.md) |
| **ServiceTriggerType** (tetikleyici olay) | `service-trigger.md` (`serviceTriggerType`) | `timer` · `whenAddedAssociate` · `whenRemoveAssociate` | [`service-trigger-type.md`](./service-trigger-type.md) |
| **PropertyType** (kontrol tipi) | `property.md` (`propertyType`) | 18 kontrol tipi (`textbox` · `combobox` · `file` · `formList` …) | [`property-type.md`](./property-type.md) |
| **KeyboardType** | `property.md` (`keyboardType` — Textbox/Phone) | `default`·`plain`·`text`·`numeric`·`email`·`url`·`telephone` | [`keyboard-type.md`](./keyboard-type.md) |
| **BarcodeFormat** | `property.md` (`barcodeFormat` — Barcode) | `aztec`·`code39`·`ean13`·`code128`·`dataMatrix`·`qr`·`pdf417`… (10) | [`barcode-format.md`](./barcode-format.md) |
| **ProcessStepType** (adım tipi) | `process-step.md` (`stepType`) | 22 adım: `processStart`·`httpRequest`·`user`·`userGroup`·`parentInstanceUser`·`notification`·`timer`… `subProcessStart`·`subProcessEnd` | [`process-step-type.md`](./process-step-type.md) |
| **ProcessStepUserType** | `process-step.md` (Kullanıcı `userType`) | `processStarter`·`fixedUser`·`usersManager`·`departmentManager`·`variableUser` | [`process-step-user-type.md`](./process-step-user-type.md) |
| **ProcessStepUserGroupType** | `process-step.md` (Kul. Grubu `userGroupType`) | `fixedUserGroup`·`dynamicUserList`·`dynamicUserGroup` | [`process-step-user-group-type.md`](./process-step-user-group-type.md) |
| **NotificationChannel** | `process-step.md` (Bildirim kanalı) | `mail`·`push`·`toast` | [`notification-channel.md`](./notification-channel.md) |
| **NotificationRecipientType** | `process-step.md` (Bildirim alıcı türü) | `user`·`userGroup`·`takeUsersWhoTookActionBefore` | [`notification-recipient-type.md`](./notification-recipient-type.md) |
| **NotificationUserType** | `process-step.md` (Bildirim alıcı-kullanıcı) | `processStarter`·`fixedUser`·`variableUsers`·`formProperty` | [`notification-user-type.md`](./notification-user-type.md) |
| **TimerCalculationType** | `process-step.md` (Timer/timeout `workStyle`) | `workCalendar`·`normalCalendar`·`fixedDateTime` | [`timer-calculation-type.md`](./timer-calculation-type.md) |
| **WorkTimeSelection** | `process-step.md` (Timer normal-takvim) | `atWorkStart`·`atWorkEnd` | [`work-time-selection.md`](./work-time-selection.md) |
| **TimeAdjustmentOption** | `process-step.md` (Timer erteleme) | `hoursAfter`·`hoursBefore` | [`time-adjustment-option.md`](./time-adjustment-option.md) |
| **HttpMethod** | `process-step.md` (HTTP Request `method`) | `get`·`post`·`put`·`delete` | [`http-method.md`](./http-method.md) |
| **InstanceDeleteMode** | `process-step.md` (Instance Deleter `deleteMode`) | `withRelated`·`unlinkRelated` | [`instance-delete-mode.md`](./instance-delete-mode.md) |

---

## Notlar

- **`actionType` çakışması giderildi (v0.7):** Önceden hem Action hem BusinessRule alanı `actionType` adını taşıyordu.
  Karışmayı önlemek için BusinessRule tarafı **`businessRuleActionType`** olarak yeniden adlandırıldı:
  **`Action.actionType`** (tip **ActionType** — tetiklenme türü, `manual`/`webhook`…) ↔ **`BusinessRule.businessRuleActionType`**
  (tip **BusinessRuleActionType** — frontend etkisi, `setViewForProperties`/`assignValueToProperty`…). Ayrı varlıklar, ayrı adlar.
- **`valueType` ↔ `valueAssignType` ayrıştırıldı (v0.18):** `AdditionalQualification.valueType` → tip **QualificationValueType**;
  süreç adımı **Değer Atama** alanı **`valueAssignType`** → tip **ValueAssignType** (değer kaynağı). Alan adları **farklı** — çakışma giderildi.
- Değer setleri model/özellik dokümanlarından çıkarıldı; kesinleşmemiş olanlar dosyalarında işaretlidir.
- **Süreç adımı tipe-özel enum'ları (2026-07-16):** **ProcessStepType** (adım ayrımlayıcısı) + Kullanıcı/Grup
  (`ProcessStepUserType`, `ProcessStepUserGroupType`), Bildirim (`NotificationChannel`, `NotificationRecipientType`,
  `NotificationUserType`), Timer (`TimerCalculationType`, `WorkTimeSelection`,
  `TimeAdjustmentOption`) · `HttpMethod` · `InstanceDeleteMode` eklendi; **KeyboardType** & **BarcodeFormat** placeholder'ları dolduruldu.
  Kaynak: [`../../research/current-flovo-bpm-engine/step-type-settings-and-enums.md`](../../research/current-flovo-bpm-engine/step-type-settings-and-enums.md).
- **`NotificationRecipientType` ≠ `ProcessStepType`:** ilki bildirim **alıcı türü** (`user`/`userGroup`), ikincisi sürecin
  **adım tipi**dir; adları benzemez, karıştırılmamalı (eski `ProcessSettingStepType`).

*Oluşturma: 2026-07-10.*
