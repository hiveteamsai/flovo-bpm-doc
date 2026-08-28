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
| **ActionType** (aksiyon türü) | `action.md` (`actionType`) · `process-step-action.md` | `manual` · `eventForm` · `takePhoto` · `selectFile` · `scanBarcode` · `webhook` · `autoAction` · `delete` | [`action-type.md`](./action-type.md) |
| **ActionDisplayType** | `action.md` (`actionDisplayType`) | `invisible` · `everywhere` · `onlyFormDetail` · `onlyFastApprove` | [`action-display-type.md`](./action-display-type.md) |
| **BusinessRuleActionType** (iş kuralı aksiyonu) | `business-rule.md` (`businessRuleActionType`) | `setViewForProperties` · `applyValidation` · `showMessage` · `assignValueToProperty` · `fillDataSource` · `assignValueToPropertyAttribute` · `setStyle` | [`business-rule-action-type.md`](./business-rule-action-type.md) |
| **BusinessRuleRuntimeType** | `business-rule.md` (`businessRuleRuntimeType`) | `always` · `firstOpening` · `whenChanging` | [`business-rule-runtime-type.md`](./business-rule-runtime-type.md) |
| **BusinessRuleConditionType** | `business-rule.md` · `business-rule-condition.md` · `process-step.md` (Karşılaştırma) | `and` (VE) · `or` (VEYA) | [`business-rule-condition-type.md`](./business-rule-condition-type.md) |
| **ValueAssignType** (değer kaynağı) | `business-rule.md` (`assignValueToProperty` — 6 değer) · `process-step.md` (Değer Atama `valueAssignType` — 3-değer alt-küme) | `fixedValue` · `propertyValue` · `fromCalculation` · `fromDataSet` · `search` · `httpRequest` | [`value-assign-type.md`](./value-assign-type.md) |
| **CriterionType** (operatör) | `business-rule-condition.md` (`criterionType`) · `process-step.md` (Karşılaştırma) | `equals` · `notEquals` · `isEmpty` · `isNotEmpty` · `greaterThan` · `greaterThanOrEqual` · `lessThan` · `lessThanOrEqual` · `startsWith` · `endsWith` · `contains` · `notContains` · `containsAny` · `containsAll` | [`criterion-type.md`](./criterion-type.md) |
| **BusinessRuleConditionCompareType** | `business-rule-condition.md` (`referenceValue`/`valueToCompare` tipi) | `propertyValue` · `viewProfile` · `fixedValue` · `fromCalculation` | [`business-rule-condition-compare-type.md`](./business-rule-condition-compare-type.md) |
| **FillDataSourceType** | `jsonTemplateModels/business-rule/fill-data-source.md` (`fillDataSourceType`) | `organizationData` · `userData` · `serviceInstances` · `httpRequest` | [`fill-data-source-type.md`](./fill-data-source-type.md) |
| **UserDataSourceType** | `jsonTemplateModels/business-rule/fill-data-source-user.md` (`userDataSourceType`) | `creditCards` · `companies` · `costCenters` | [`user-data-source-type.md`](./user-data-source-type.md) |
| **SortDirection** | `jsonTemplateModels/business-rule/assign-value-from-dataset.md` (`sortType`) | `none` · `asc` · `desc` | [`sort-direction.md`](./sort-direction.md) |
| **PropertyAttributeType** | `jsonTemplateModels/business-rule/assign-value-to-property-attribute.md` (`propertyAttributeType`) | `minDate` · `maxDate` · `helperText` · `sideText` · `addNewEnabled` | [`property-attribute-type.md`](./property-attribute-type.md) |
| **OrganizationDataSourceType** | `jsonTemplateModels/business-rule/fill-data-source-organization.md` (`organizationDataSourceType`) | `professions` · `departments` · `companies` · `costCenters` · `users` · `creditCards` · `workerLevels` · `userGroups` · `positions` · `workingSchedules` | [`organization-data-source-type.md`](./organization-data-source-type.md) |
| **OrganizationParameter** | `jsonTemplateModels/business-rule/fill-data-source-parameter.md` (`parameter`) | `company` · `name` · `code` · `userCode` · `additionalQualification` · `professionCode` | [`organization-parameter.md`](./organization-parameter.md) |
| **SubTextType** | `jsonTemplateModels/business-rule/fill-data-source-organization.md` · `…-user.md` (`subTextType`) | `code` · `username` · `department` · `profession` · `ref1` · `ref2` | [`sub-text-type.md`](./sub-text-type.md) |
| **ValueTypeOfList** | `jsonTemplateModels/business-rule/business-rule-condition-compare-value.md` (`valueTypeOfList`) | `defaultValue` · `value` · `display` | [`value-type-of-list.md`](./value-type-of-list.md) |
| **RelationalType** | `additional-qualification.md` (`relationalType`) | `users` · `departments` · `professions` · `costCenters` · `workerLevels` | [`relational-type.md`](./relational-type.md) |
| **QualificationValueType** | `additional-qualification.md` (`valueType`) | `string` · `double` · `dateTime` · `combobox` | [`qualification-value-type.md`](./qualification-value-type.md) |
| **SyncStatus** (harici senkron durumu) | org-ayarı text-entity'leri (`synchronizationStatus`) — `company`·`department`·`cost-center`·`credit-card`·`position`·`profession`·`user`·`worker-level`·`vacation-day` | `synced` · `pending` · `error` | [`sync-status.md`](./sync-status.md) |
| **FormType** | `service.md` (`formType`) | `form` · `parameter` · `eventForm` | [`form-type.md`](./form-type.md) |
| **ServiceTriggerType** (tetikleyici olay) | `service-trigger.md` (`serviceTriggerType`) | `timer` · `whenAddedAssociate` · `whenRemoveAssociate` | [`service-trigger-type.md`](./service-trigger-type.md) |
| **PropertyType** (kontrol tipi) | `property.md` (`propertyType`) | 18 kontrol tipi (`textbox` · `combobox` · `file` · `formList` …) | [`property-type.md`](./property-type.md) |
| **KeyboardType** | `property.md` (`keyboardType` — Textbox/Phone) | `default`·`plain`·`text`·`numeric`·`email`·`url`·`telephone` | [`keyboard-type.md`](./keyboard-type.md) |
| **BarcodeFormat** | `property.md` (`barcodeFormat` — Barcode) | `aztec`·`code39`·`ean13`·`code128`·`dataMatrix`·`qr`·`pdf417`… (10) | [`barcode-format.md`](./barcode-format.md) |
| **TextAlignment** | `property-settings/text.md` (`text` statik alan `settings.textAlignment`) | `left`·`center`·`right` | [`text-alignment.md`](./text-alignment.md) |
| **ReflectionMode** | `property.md` (`reflectionMode` — parentProperty/userInfo/flowInfo) | `snapshot` · `live` · `materialized` (materialized yalnız parentProperty) | [`reflection-mode.md`](./reflection-mode.md) |
| **ReflectionPropagation** | `property.md` (`reflectionPropagation` — parentProperty + `materialized`) | `async` · `sync` | [`reflection-propagation.md`](./reflection-propagation.md) |
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
- **İş kuralı DTO ailesi enum'ları (v0.34):** `FillDataSourceType` · `UserDataSourceType` · `SortDirection` ·
  `PropertyAttributeType` · **`OrganizationDataSourceType`** · **`OrganizationParameter`** · **`SubTextType`** · **`ValueTypeOfList`**
  (BusinessRule aksiyon konfig ailesi → [`../service-settings/jsonTemplateModels/business-rule/index.md`](../service-settings/jsonTemplateModels/business-rule/index.md)).
  **`PropertyAttributeType` ≠ `PropertyType`:** ilki alan **özniteliği** (minDate/helperText…), ikincisi **kontrol tipi**dir.
  `OrganizationDataSourceType`/`ValueTypeOfList` içinde eski **masraf-spesifik** değerler (ExpenseType/ExpenseCategory · expenseType*/categoryCode) **kapsam-dışı** (→ [`../../todo.md`](../../todo.md)).
- **`SyncStatus` — bool→enum tekleştirme (v0.36):** org-ayarı text-entity'lerinin `synchronizationStatus` alanı önceden bazı
  modellerde `bool`, bazılarında tanımsız "SyncStatus" idi; **tek tip = `SyncStatus` enum** (`synced`/`pending`/`error`) olarak
  hizalandı ve enum dosyası eklendi. Tüm ilgili modeller `[sync-status.md](./sync-status.md)`'e link verir.

*Oluşturma: 2026-07-10.*
