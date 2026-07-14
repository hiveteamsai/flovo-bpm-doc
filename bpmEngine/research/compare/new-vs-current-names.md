# Yeni Flovo BPM vs Mevcut (Eski) Flovo — İsim Değişiklikleri

> **Amaç:** Yeni tasarımın **modellerinde** yapılan **isim değişikliklerini** tek yerde, taranabilir biçimde toplamak
> (model adları + alan adları). Gerekçe/davranış için → ilgili model/özellik dokümanı ve [`new-vs-current.md`](./new-vs-current.md).
>
> **Gösterim:**
> - **`eski` > `yeni`** — yeniden adlandırılan.
> - **`-- ad`** — kaldırılan (silinen).
> - **`ad ++`** — eklenen (yeni).
>
> **Not:** Yeni **runtime (`processInstances/`)** modellerinin bir kısmının eski uygulamada karşılığı vardır
> (ör. `ProcessStepInstance` ← `ServiceInstanceRequests`, §15.1); diğerleri yenidir. Kaynak (eski DTO'lar) → `../current-flovo-bpm-engine/`.
>
> **v0.7 — proje-içi ad netleştirmesi:** runtime & iş-kuralı model adları güncellendi (bu dosyada **yeni** sütun bunları
> yansıtır): `WorkFlow`>**`ProcessInstance`** · `ProcessStepExecution`>**`ProcessStepInstance`** · `Form`>**`Instance`** ·
> `RelatedForm`>**`RelatedInstance`** · `FormAwaitingUser`>**`InstanceAwaitingUser`** · `WorkRule`>**`BusinessRule`** ·
> `WorkRuleCondition`>**`BusinessRuleCondition`**; FK'ler: `workFlowId`>**`processInstanceId`** · `parentWorkFlowId`>**`parentProcessInstanceId`** ·
> `processStepExecutionId`>**`processStepInstanceId`** · `formId`>**`instanceId`** · `relatedFormId`>**`relatedInstanceId`** ·
> `formAwaitingUserId`>**`instanceAwaitingUserId`** · `workRuleId`>**`businessRuleId`**. Klasör `workFlows/`>**`processInstances/`**.

---

## 1. Kiracı / Kimlik (Account → Organization)
- `Account` (varlık) > **`Organization`**
- `accountId` (string) > **`organizationId`** (int, PK)
- `organizationCode` (string, dış referans) **++** _(eski `accountId` aslında **kod** niteliğindeydi)_
- `account*` > **`organization*`** (ör. `accountUserGroup*` > `organizationUserGroup*`, `accountRestriction` > `organizationRestriction`)
- `-- accountCompanyDtos` (ve benzeri UI-yardımcı koleksiyonlar — DB modeline alınmadı)
- **Organization eklenen alanları:** `code ++` · `name ++` · `defaultLang ++` · `logoUrl ++` · `idleTimeoutMinute ++`

---

## 2. Genel: `field` → `property`
- `...FieldId` > **`...PropertyId`**
- `fieldId` > **`propertyId`**
- `targetFieldId` > **`targetPropertyId`**
- `targetInstancesFieldId` > **`targetInstancesPropertyId`**
- `FieldValue` / `FormValue` > **`PropertyValue`**
- `PropertyDto` (alan) kavramı "field" > **"property"**

---

## 3. Aksiyon (`Action` / `ProcessStepAction`)
> ⚠️ **Kavram takası** (dikkat):
- `actionType` (renk/stil: success/danger…) > **`styleId`** (dinamik Style'a FK)
- `action` (davranış: fire-event…) > **`actionType`** (tür: `manual`/`eventForm`…)
- `reasonRequired` > **`eventForm`** (tür)
- `-- actionId` (ProcessStepAction'da **canlı FK yok**; alanlar bir kez kopyalanır)
- **Yeni türler:** `eventForm ++` · `webhook ++` · `autoAction ++`
- **Kaldırılan iş-bazlı custom davranışlar:** `-- fire-event` · `-- new-instance` · `-- new-instance-referenced` ·
  `-- new-instance-other` · `-- take-photo` · `-- select-file` · `-- take-barcode` · `-- manuel-barcode-input` ·
  `-- excel-export` · `-- expform-*` · `-- add-test-receipt`
- **↔ Korunan:** `targetProcessStepId` · `changeStatusId` · `authorizationLevel` · `actionDisplayAuthorizedUserGroupId` ·
  `showInHistory` · `environmentRestriction`

---

## 4. Durum (`Status`)
- `statusType` > **`styleId`** (yanlış adlandırılmıştı; aslında Style'a FK)
- `id ++` (PK) · `organizationId ++` (havuz)
- **↔ Korunan:** `code` · `definition` · `icon` · `changeStatusId`

---

## 5. Stil (`Style`) — YENİ KAVRAM
- Statik Bootstrap renk sınıfı (`actionType`) > **dinamik `Style` varlığı** (referansla seçim)
- **Alanlar:** `bgColor ++` · `fontColor ++` · `organizationId ++` (null = sistem stili)

---

## 6. Form Alanları (`Property`)
**Yeniden adlandırılan**
- `ModalList` > **`formList`** (Form List)
- `onAfterChange` > **`saveAndRefreshOnAfterChange`**
- `maximumNumberDecimalDigits` > **`maxDecimalDigits`**

**Birleştirilen (tür → tür/opsiyon)**
- `MaskedEntry` > **`textbox`** (maske) · `Entry` + `Editor` > **`textbox`** (`minLine`/`maxLine`) ·
  `NumericUpDown` > **`numericTextbox`** · `MultiSelect` > **`combobox`** · `DateTimePicker` > **`datepicker`** ·
  `Photo` / `ImageList` > **`file`**

**Kaldırılan**
- `-- DataGrid` · `-- DataGridControl` · `-- ObjectAccessController` · `-- TableFieldDisplayController`
- `-- propertyName` · `-- label` (→ `definition` ile duplicate; binding key **`code`** oldu)
- `-- precition` (→ `maxDecimalDigits` ile birleşti)
- `-- style` (property'de style alanı yok)
- `-- required` · `-- visible` · `-- enabled` (property'den çıkıp **görüntüleme profiline** taşındı)

**Eklenen**
- `userInfo ++` (User Info; `flowInfo`'dan ayrıldı)
- **`PropertyItem` alt modeli ++:** `id` · `propertyId` · `value` · `code ++` · `definition ++`
  (**`value` ↔ `code` ayrıldı**; `(propertyId, value)` benzersiz)

**Form List ayarları → görüntüleme profiline**
- `addNewEnabled` > **`activeStartActions`**
- `addFromExistingRecordsIsActive` > **`addFromExistingStatusIds`**
- `selectedEnable` > **`selectableVisible`** (profil-bazlı; eski `selectableModeActive` alan-düzeyiydi — kaldırıldı)
- `selectedEditable ++` (öneri; profil-bazlı)

---

## 7. Görüntüleme Profili (`ProcessViewProfile`)
- `processViewProfileFields` > **`processViewProfileProperty`**
- `ProcessViewProfileFieldDto` > **`ProcessViewProfilePropertyDto`**
- `fieldId` > **`propertyId`**
- **`ProcessViewProfilePropertySetting` ++** (key/value; profil-bazlı tipe-özel override)
- **DB anahtarları:** `id ++` · `serviceId ++` · `viewProfileId ++` · `propertyId ++`
- **Kaldırılan (rapor/eski alanlar):** `-- showOnDataGrid` · `-- isUserReport` · `-- userGroupId` (rapor) ·
  `-- showAsManager` · `-- showToEveryone` · `-- showOnListingPage` · `-- subFieldsViewProfiles` ·
  `-- deletableStatuses` · `-- cardViewProfile` · `-- childFieldsProcessViewProfileFieldDtos`

---

## 8. İş Kuralı (`BusinessRule`)
- `SetViewForFields` > **`setViewForProperties`**
- `AssignValueToField` > **`assignValueToProperty`**
- `assignValueToPropertyField` > **`assignValueToPropertyAttribute`** _(⚠️ teyit)_
- `FieldValue` / `FormValue` > **`PropertyValue`**
- `Function` (değer kaynağı) > **`httpRequest`**
- `-- FromEba` (değer kaynağı — Eba kaldırıldı)
- **↔ Korunan:** `changeViewProfile` · `applyValidation` · `showMessage` · `fillDataSource` · `setStyle`

---

## 9. Süreç Adımı (`ProcessStep`)
**Yeniden adlandırılan**
- `Function` > **`HTTP Request`** (+ `async ++`)
- (Değer Atama) `valueType = FormValue` > **`PropertyValue`** · `targetFieldId` > **`targetPropertyId`** · `fieldId` > **`propertyId`**

**Eklenen adımlar**
- `Flovo AI ++` · `Switch ++` · `Processing ++` · `Instance Creator ++` · `Instance Deleter ++` · `Form Yönlendirme ++` · `Süreç Adımı Tetikleme ++`
- (Değer kaynağı) `fromCalculation ++` (+ `expression ++`)

**Kaldırılan adımlar / alanlar**
- `-- Adım İptali` (`stepCancellation`)
- `-- Eba Entegre` (`ebaIntegratedFlovoApp`)
- `-- atama` (eski enum'da tanımlı ama kullanılmayan ölü değer)
- `-- selectModalItemDeactive` · `-- canSelectExpenses` (→ Form List konusu)

---

## 10. Çeviri (`Translation`)
- `-- tr` · `-- en` · `-- de` (kolon-başına-dil kaldırıldı)
- `languageCode ++` · `definition ++` (**kayıt-başına-dil**)
- Benzersizlik: `(organizationId, code, languageCode)`

---

## 11. Organizasyon Ayarları (yapısal veri — 13 model)
> Eski **"Account Settings"** DTO'ları → yeni DB modelleri.

**Model adı**
- `Title` / `Ünvan` > **`Profession`** (model · FK'ler · enum değeri)
- `AccountUserGroupDto` > **`UserGroup`** _(ve diğer `Account*Dto` > `*` karşılıkları)_

**Alan (Türkçe → İngilizce)**
- `kod` > **`code`**
- `tanim` > **`definition`**
- `departmanYoneticiUserId` > **`managerUserId`**
- `unvanId` > **`professionId`**
- `selectedCompanyIds` > **`companyIds`** (List\<int\>)
- string FK'ler > **int FK'ler**

**Kaldırılan**
- `-- UserExpenseLimit` (aktif kullanılmıyor)
- `-- WorkingSchedule.explanation`

---

## 12. Master-veri Yaşam Döngüsü & Yetki
**Yaşam döngüsü**
- `status` (bool) > **`active`**
- `deleted ++` (soft-delete; `active` + `deleted` ikisi de not-null)
- Benzersizlik `(organizationId, code) ++` (`deleted=true` hariç)

**Kullanıcı (`User`)**
- `-- userName` > **`email ++`** (giriş) + **`phone ++`**
- Benzersizlik: `(organizationId, email) ++` · `(organizationId, phone) ++`

**Yetkilendirme**
- `-- User.authorizationLevel` (kullanıcı bazında sayısal — kaldırıldı)
- `Organization.adminUserIds ++` (en az 1 aktif admin)
- `impersonationUserGroupId ++` · `organizationSettingsUserGroupId ++` · `serviceSettingsUserGroupId ++` · `viewAllReportsUserGroupId ++`
  (her biri tek `UserGroup`)

---

## 13. Ek Nitelik (`AdditionalQualification`)
- `RelationalSetting` > **`RelationalType`**
- `QualificationValueType ++` (enum: `String` · `Double` · `DateTime` · `Combobox`)
- `valueType ++` (alan)
- (Değer modelleri) tek `value` > **typed sütunlar**: `stringValue ++` · `doubleValue ++` · `datetimeValue ++`
- `comboboxItemId ++` (FK) · `comboboxCode ++` · `comboboxDefinition ++` (seçilen öğenin kopyası)
- **`QualificationItem` alt modeli ++** (combobox seçenekleri; `PropertyItem`'dan türetildi ama `Property`'siz;
  `additionalQualificationId`)

---

## 14. Kullanıcı Grubu (`UserGroup`)
- `groupApprovalRequired ++` (grup onayı gerekli mi? — bkz. `../../models/processInstances/user-group-approved-user.md`)

---

## 15. İş Akışı / Runtime Modelleri (`processInstances/`)
> Motorun **çalışma-zamanı** kayıtları. Bir kısmının eski uygulamada karşılığı vardır (aşağıda eşlendi); diğerleri yeni.

### 15.1 ProcessStepInstance (eski: `ServiceInstanceRequests`)
- `ServiceInstanceRequests` > **`ProcessStepInstance`** (model)
- `RequestDate` > **`executionDate`**
- `responsaDate` > **`actionTriggerDate`**
- `InstanceId` > **`instanceId`**
- `ProxyApproverUserId` > **`atDelegateUserId`**
- `-- Description`
- `-- IsItSkipped`
- `-- SentBack`
- `-- IsItCanceled`
- `-- UserId`
- `processInstanceId ++`
- `atUserId ++`
- `atApiKeyId ++`
- `processStepActionParameter ++`
- **↔ Korunan (casing normalize):** `Id` > `id` · `ProcessStepId` > `processStepId` · `ProcessStepActionId` > `processStepActionId`

### 15.2 Instance (eski: `ServiceInstances`)
- `ServiceInstances` > **`Instance`** (model)
- `UserId` > **`creatorUserId`**
- `ProcessStatusId` > **`statusId`**
- `-- acountId`
- `-- StateId`
- `-- ParentInstanceId`
- `-- isTest`
- `-- ProcessStepId`
- `createdDate ++`
- `processInstanceId ++`
- **↔ Korunan:** `Id` > `id` · `ServiceId` > `serviceId` · `delete` (soft-delete; org-ayarı modellerindeki `deleted` ile aynı amaç, farklı ad)

### 15.3 Diğer runtime modelleri — YENİ (eski karşılığı yok)
> Bu 4 model tamamen yenidir; eski uygulamada birebir karşılığı yoktur.
- `ProcessInstance ++` · `InstanceAwaitingUser ++` · `UserGroupApprovedUser ++` · `RelatedInstance ++`
- **Alan adı normalizasyonu (taslak görsel → proje kuralı):** `Id` > `id` · `FormId` > `instanceId` · `ProcessStepId` > `processStepId`
  (PK `id`, FK `...Id` camelCase) · `FormAwaitingUser-Id` > `instanceAwaitingUserId`

---

*Oluşturma: 2026-07-06 · Güncelleme: 2026-07-10 (v0.7 — runtime & iş-kuralı model adları: ProcessInstance · ProcessStepInstance · Instance · RelatedInstance · InstanceAwaitingUser · BusinessRule). Kaynak: `new-vs-current.md` + `../../models/` + depo kökü `commitNotes/`.*
