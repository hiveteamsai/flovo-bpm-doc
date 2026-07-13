# Flovo BPM — Veri Modelleri (Şema Referansı)

> **Durum:** 🟡 TASLAK — mevcut tasarım dokümanlarından **ilk çıkarım**; alanlar/tipler gözden geçirilecek.
> **Amaç:** Tüm veri modellerinin **tek yerde** kısa tanımı + **birbirleriyle ilişkileri**. Her modelin **alan-düzeyi
> ayrıntısı** kendi dosyasındadır. Bu klasör **veri modeli/şema** odaklıdır; **davranış/kullanım** özellik
> dokümanlarındadır (`organization-settings/`, `service-settings/`, `flovo-bpm-engine.md`).
>
> **Anahtar kuralı:** Her modelin birincil anahtarı **`id`** (int). Yabancı anahtarlar **`...Id`** (örn. `serviceId`,
> `styleId`). Kiracı kimliği **`organizationId`** (int); dış referanslarda **`organizationCode`** (string) kullanılır.

---

## 0. Hiyerarşi (özet)

**`Organization → Solution → Service → {Property · ProcessViewProfile · ProcessStep · BusinessRule}`**

- **Organization** = kiracının kendisi.
- **Solution** = organizasyona bağlı; **servisleri gruplayan** tanım. Bir organizasyonda birden çok solution olabilir.
- **Service** = bir solution altında oluşturulur; **kendi ayarlarını** (property/görüntüleme profili/süreç adımı/iş
  kuralı) barındırır.
- **Organizasyon havuzu** (`Translation`, `Style`, `Status`, `Action`) = organizasyona bağlıdır; o organizasyonun
  **tüm servislerinde** kullanılabilir.
- **ProcessStepAction** = bir **ProcessStep**'e bağlıdır.

---

## 1. Modeller (dizin)

> **Fiziksel yerleşim (özellik klasörleriyle hizalı):** modeller iki alt klasöre ayrıldı — **`organization-settings/`**
> (Organization + Organizasyon havuzu + **organizasyon ayarları/yapısal veri**) ve **`service-settings/`**
> (**Solution · Service** + servise bağlı modeller). Ayrıca **`enums/`** — modellerde kullanılan **enum tanımlarının**
> (kanonik değer listeleri) tek yerde indekslendiği alt klasör (→ [`enums/enums.md`](enums/enums.md)). Bu indeks (`models.md`) kökte kalır.

### Kiracı & hiyerarşi
| Model | Dosya | Kısa açıklama |
|---|---|---|
| **Organization** | [`organization.md`](./organization-settings/organization.md) | Kiracı (tenant). En üst kapsayıcı. |

> **Solution** ve **Service** — service-settings kırılımının **başladığı** yer olduğu için fiziksel olarak
> **`service-settings/`** altındadır (aşağıdaki "Servis hiyerarşisi & servise bağlı" bölümü).

### Organizasyon havuzu (organizasyona bağlı — servislerde kullanılır)
| Model | Dosya | Kısa açıklama |
|---|---|---|
| **Translation** | [`translation.md`](./organization-settings/translation.md) | `code`-bazlı çok dilli metinler (ortak + organizasyon). |
| **Style** | [`style.md`](./organization-settings/style.md) | Renk/görünüm varlığı (bg + font). |
| **Status** | [`status.md`](./organization-settings/status.md) | Kaydın aşaması (etiket). |
| **Action** | [`action.md`](./organization-settings/action.md) | Aksiyon **şablonu** (ActionDto); adıma eklenince kopyalanır. |

### Servis hiyerarşisi & servise bağlı (`service-settings/`)
| Model | Dosya | Kısa açıklama |
|---|---|---|
| **Solution** | [`solution.md`](./service-settings/solution.md) | Servisleri gruplayan tanım (organizasyona bağlı). |
| **Service** | [`service.md`](./service-settings/service.md) | İş sürecinin/formun tamamı (solution altında). **`formType`**: form/parameter/eventForm. |
| **Property** | [`property.md`](./service-settings/property.md) | Form alanı (kontrol tipiyle render edilir). |
| **PropertyItem** | [`property-item.md`](./service-settings/property-item.md) | Seçim alanının statik seçeneği. |
| **ProcessViewProfile** | [`view-profile.md`](./service-settings/view-profile.md) | Formun adım-bazlı görünümü. |
| **ProcessViewProfileProperty** | [`view-profile-property.md`](./service-settings/view-profile-property.md) | Profildeki tek alan yapılandırması. |
| **ProcessViewProfilePropertySetting** | [`view-profile-property-setting.md`](./service-settings/view-profile-property-setting.md) | Alanın profil-bazlı tipe-özel override'ı (key/value). |
| **ProcessStep** | [`process-step.md`](./service-settings/process-step.md) | Süreç adımı (akıştaki düğüm). |
| **ProcessStepAction** | [`process-step-action.md`](./service-settings/process-step-action.md) | Aksiyonun adıma bağlanması (binding). |
| **BusinessRule** | [`business-rule.md`](./service-settings/business-rule.md) | Frontend realtime form davranışı. 🟡 en son şekillenecek. |
| **BusinessRuleCondition** | [`business-rule-condition.md`](./service-settings/business-rule-condition.md) | İş kuralı koşulu (recursive). 🟡 en son. |

### Organizasyon ayarları (yapısal veri — `organization-settings/`; eski "Account Settings" DTO'ları)
| Model | Dosya | Kısa açıklama |
|---|---|---|
| **Company** | [`company.md`](./organization-settings/company.md) | Tüzel kişilik (şirket); çok-şirket temeli. |
| **Department** | [`department.md`](./organization-settings/department.md) | Hiyerarşik birim; departman yöneticisi. |
| **Profession** | [`profession.md`](./organization-settings/profession.md) | Görev/meslek (eski "Ünvan/Title"). |
| **User** | [`user.md`](./organization-settings/user.md) | Kişi; BPM onay merci temeli. |
| **UserGroup** | [`user-group.md`](./organization-settings/user-group.md) | Kullanıcı topluluğu (grup onayı/bildirim/aksiyon yetkisi). |
| **AdditionalQualification** | [`additional-qualification.md`](./organization-settings/additional-qualification.md) | Dinamik/özel alanlar (+ RelationalType · QualificationValueType · **QualificationItem** alt modeli — combobox). |
| **CostCenter** | [`cost-center.md`](./organization-settings/cost-center.md) | Masraf merkezi. |
| **WorkerLevel** | [`worker-level.md`](./organization-settings/worker-level.md) | Çalışan seviyesi. |
| **WorkingSchedule** | [`working-schedule.md`](./organization-settings/working-schedule.md) | Haftalık çalışma takvimi (Timer temeli). |
| **VacationDay** | [`vacation-day.md`](./organization-settings/vacation-day.md) | Tatil günleri. |
| **CreditCard** | [`credit-card.md`](./organization-settings/credit-card.md) | Kurumsal kart. |
| **ProcessTransfer** | [`process-transfer.md`](./organization-settings/process-transfer.md) | Görev devri (operasyon). |
| **SchedulerJob** | [`scheduler-job.md`](./organization-settings/scheduler-job.md) | Cron arka plan görevi (+ log). |

### İş akışı / çalıştırma (runtime — `processInstances/`)
> 🟢 **TANIMLI** — ayarlardan (`Service`/`ProcessStep`/`Property`…) motor tarafından üretilen **çalışma-zamanı**
> kayıtları. 6 modelin alanları netleşti. _(Açık: `Instance` **property value depolaması** sonraya bırakıldı → `../todo.md`.)_

| Model | Dosya | Kısa açıklama |
|---|---|---|
| **ProcessInstance** | [`process-instance.md`](./processInstances/process-instance.md) | Bir servis sürecinin çalıştırma örneği. |
| **ProcessStepInstance** | [`process-step-instance.md`](./processInstances/process-step-instance.md) | Tek bir adımın çalıştırılması (aksiyon/tetikleyici/zaman). |
| **Instance** | [`instance.md`](./processInstances/instance.md) | Doldurulmuş form / süreç örneği; mevcut `statusId`. |
| **InstanceAwaitingUser** | [`instance-awaiting-user.md`](./processInstances/instance-awaiting-user.md) | Formu bekleyen kullanıcı/grup (onay kuyruğu). |
| **UserGroupApprovedUser** | [`user-group-approved-user.md`](./processInstances/user-group-approved-user.md) | Grup onayında onaylayan üye + zamanı. |
| **RelatedInstance** | [`related-instance.md`](./processInstances/related-instance.md) | Formlar arası ilişki (property boyutuyla). |

---

## 2. İlişki Haritası

```
Organization (id)
 ├─< Solution (organizationId)
 │    └─< Service (solutionId)
 │         ├─< Property             (serviceId) ──< PropertyItem  (propertyId; (propertyId,value) benzersiz)
 │         ├─< ProcessViewProfile   (serviceId)
 │         │        └─< ProcessViewProfileProperty (viewProfileId, propertyId → Property)
 │         │                 └─< ProcessViewProfilePropertySetting (viewProfilePropertyId; key/value — propertyType'a göre)
 │         ├─< ProcessStep          (serviceId; +organizationId = izolasyon)
 │         │        └─< ProcessStepAction (processStepId,
 │         │                               targetProcessStepId → ProcessStep,
 │         │                               changeStatusId      → Status)
 │         └─< BusinessRule             (serviceId; +organizationId = izolasyon)
 │                  └─< BusinessRuleCondition (businessRuleId, recursive)
 │
 └── Organizasyon havuzu (organizationId) — servis modellerinde kullanılır:
      ├─< Translation (null = ortak/Flovo)
      ├─< Style       (null = sistem) ─────> Action.styleId · Status.styleId
      ├─< Action                     ┄┄┄┄> (ProcessStepAction'a bir kez kopyalanır — canlı FK yok)
      └─< Status                     ─────> ProcessStepAction.changeStatusId
```

**İş akışı / çalıştırma (runtime — `processInstances/`):** ayarlardan üretilen instance/execution verisi.

```
ProcessInstance (id; createdByUserId → User · createdByApiKeyId → ApiKey[geçici] · serviceId → Service · parentProcessInstanceId → ProcessInstance[self, alt süreç])
 ├─< ProcessStepInstance (processInstanceId; instanceId → Instance · processStepId → ProcessStep ·
 │        │                 processStepActionId → ProcessStepAction · atUserId/atDelegateUserId → User · atApiKeyId → ApiKey[geçici])
 │        └─< InstanceAwaitingUser (processStepInstanceId; instanceId → Instance · userId → User · userGroupId → UserGroup)
 │                 └─< UserGroupApprovedUser (instanceAwaitingUserId; userId → User)   # yalnız grup onayı
 └─< Instance (processInstanceId; serviceId → Service · creatorUserId → User · statusId → Status)
      └─< RelatedInstance (instanceId → Instance · relatedInstanceId → Instance · relatedPropertyId → Property)
```

---

## 3. İlişki Tablosu
> Kapsam: **süreç hiyerarşisi + havuz + yetki** ilişkileri + **runtime (`processInstances/`)** (tablonun altında). Organizasyon-ayarı
> modellerinin (Company/User/Department… **arası**) FK'leri için ilgili model dosyalarının "İlişkiler" bölümlerine bakın.

| Kaynak | Alan | Hedef | Kardinalite | Not |
|---|---|---|---|---|
| Solution | `organizationId` | Organization.id | N–1 | |
| Service | `solutionId` | Solution.id | N–1 | organizasyon dolaylı (solution üzerinden) |
| Translation | `organizationId` | Organization.id | N–1 | `null` = ortak (Flovo) |
| Style | `organizationId` | Organization.id | N–1 | `null` = sistem stili (salt-okunur) |
| Action | `organizationId` | Organization.id | N–1 | organizasyon havuzu |
| Action | `styleId` | Style.id | N–1 | |
| Status | `organizationId` | Organization.id | N–1 | organizasyon havuzu |
| Status | `styleId` | Style.id | N–1 | |
| Organization | `adminUserIds` | User.id | N–N | organizasyon adminleri |
| Organization | `*UserGroupId` (4 alan) | UserGroup.id | N–1 | grup-bazlı yetkiler (impersonation / orgSettings / serviceSettings / viewAllReports) |
| Property | `serviceId` | Service.id | N–1 | |
| PropertyItem | `propertyId` | Property.id | N–1 | `(propertyId, value)` benzersiz |
| ProcessViewProfile | `serviceId` | Service.id | N–1 | |
| ProcessViewProfileProperty | `viewProfileId` | ProcessViewProfile.id | N–1 | |
| ProcessViewProfileProperty | `propertyId` | Property.id | N–1 | |
| ProcessViewProfilePropertySetting | `viewProfilePropertyId` | ProcessViewProfileProperty.id | N–1 | profil-bazlı alan override (key/value) |
| ProcessStep | `serviceId` | Service.id | N–1 | asıl kapsayıcı |
| ProcessStep | `organizationId` | Organization.id | N–1 | kiracı/izolasyon (denormalize) |
| ProcessStepAction | `processStepId` | ProcessStep.id | N–1 | binding'in ait olduğu adım |
| ProcessStepAction | `targetProcessStepId` | ProcessStep.id | N–1 | ilerlenecek hedef adım |
| ProcessStepAction | `changeStatusId` | Status.id | N–1 | aksiyon sonrası durum |
| BusinessRule | `serviceId` | Service.id | N–1 | asıl kapsayıcı |
| BusinessRule | `organizationId` | Organization.id | N–1 | kiracı/izolasyon (denormalize) |
| BusinessRule | `activeViewProfiles` | ProcessViewProfile.id | N–N | yalnız bu profillerde çalış |
| BusinessRuleCondition | `businessRuleId` | BusinessRule.id | N–1 | |
| BusinessRuleCondition | `parentConditionId` | BusinessRuleCondition.id | N–1 | iç içe (recursive) |
| Translation | `code` | (kod eşleşmesi) | — | FK değil; `code` + `languageCode` + `organizationId` ile çözülür |
| **— İş akışı / çalıştırma (runtime — `processInstances/`) —** | | | | |
| ProcessInstance | `createdByUserId` | User.id | N–1 | null olabilir (kullanıcı **ya da** API) |
| ProcessInstance | `createdByApiKeyId` | ApiKey | N–1 | null olabilir; **ApiKey geçici** |
| ProcessInstance | `serviceId` | Service.id | N–1 | |
| ProcessInstance | `parentProcessInstanceId` | ProcessInstance.id | N–1 | **self**; null olabilir (alt süreç → ana süreç akışı; ana süreçte null) |
| ProcessStepInstance | `processInstanceId` | ProcessInstance.id | N–1 | |
| ProcessStepInstance | `instanceId` | Instance.id | N–1 | null olabilir (form yönlendirme) |
| ProcessStepInstance | `processStepId` | ProcessStep.id | N–1 | |
| ProcessStepInstance | `processStepActionId` | ProcessStepAction.id | N–1 | aksiyon tetiklenince dolar |
| ProcessStepInstance | `atUserId` · `atDelegateUserId` | User.id | N–1 | tetikleyen · vekaleten onaylayan |
| ProcessStepInstance | `atApiKeyId` | ApiKey | N–1 | null olabilir; **ApiKey geçici** |
| Instance | `processInstanceId` | ProcessInstance.id | N–1 | |
| Instance | `serviceId` | Service.id | N–1 | |
| Instance | `creatorUserId` | User.id | N–1 | null olabilir (**`parameter`** tipi servis — sahipsiz veri-kaynağı) |
| Instance | `statusId` | Status.id | N–1 | formun mevcut durumu (havuz) |
| InstanceAwaitingUser | `processStepInstanceId` | ProcessStepInstance.id | N–1 | |
| InstanceAwaitingUser | `instanceId` | Instance.id | N–1 | |
| InstanceAwaitingUser | `userId` | User.id | N–1 | `userId` **veya** `userGroupId` (biri) |
| InstanceAwaitingUser | `userGroupId` | UserGroup.id | N–1 | |
| UserGroupApprovedUser | `instanceAwaitingUserId` | InstanceAwaitingUser.id | N–1 | yalnız grup onayı |
| UserGroupApprovedUser | `userId` | User.id | N–1 | onaylayan üye |
| RelatedInstance | `instanceId` · `relatedInstanceId` | Instance.id | N–1 | formlar arası ilişki |
| RelatedInstance | `relatedPropertyId` | Property.id | N–1 | `relatedInstanceId`'nin formundaki property |

---

## 4. Henüz modellenmemiş / referans verilen varlıklar (açık)

| Varlık | Nerede geçiyor | Not |
|---|---|---|
| **ApiKey** (Customer API anahtarı) | `ProcessInstance.createdByApiKeyId`, `ProcessStepInstance.atApiKeyId` | API üzerinden başlatım/tetikleme kimliği (oluşturan `User` değilken "kim yaptı"). **Ad geçici**; Customer API erişim mekanizması kesinleşince doğrulanacak → `../todo.md`. |
| **ExpenseType / Currency / Position / Tax** | Masraf süreçleri | Masraf tipi, para birimi, pozisyon, vergi — referans dokümanında **kapsam dışı**. |

> **Instance (doldurulmuş form) artık modellendi** → `processInstances/` (ProcessInstance · Instance · ProcessStepInstance · InstanceAwaitingUser ·
> UserGroupApprovedUser · RelatedInstance). 🟢 TANIMLI — yalnız `Instance` **property value depolaması** açık (→ `../todo.md`).

> **Not:** **User** ve **UserGroup** artık modellendi (→ §1 "Organizasyon ayarları"). `organizationUserGroupId` /
> `actionDisplayAuthorizedUserGroupId` gibi BPM referansları `UserGroup`'a, kullanıcı atamaları `User`'a bağlanır.

---

## 5. Notlar
- **Enum'lar** artık **tek yerde** indekslenir → [`enums/enums.md`](enums/enums.md) (kanonik değer listeleri: `actionType`, `controlTypeId`, `businessRuleRuntimeType`, `criterionType`, `valueType`, `formType`...). Her model, kullandığı enum'a **buradan link** verir ve **o değerin o modeldeki rolünü** kendi içinde anlatır.
- **`Service.formType` (form/parameter/eventForm):** servisin davranışını belirler — **`form`** akış+onay+sahipli `Instance`
  (`creatorUserId` dolu, `InstanceAwaitingUser`); **`parameter`** onaysız veri-kaynağı (`Instance` oluşur, `creatorUserId`
  **null**, `InstanceAwaitingUser`'a bakılmaz); **`eventForm`** akışsız/`Instance`'sız (pop-up viewprofile → `parameters`;
  `eventForm` actionType ile). Ayrıntı → `service-settings/service.md`.
- **Organizasyon havuzu** (Translation/Style/Status/Action) `organization-settings/`'a; **servise bağlı** modeller `service-settings/`'ya karşılık gelir.
- **ProcessStep / BusinessRule** asıl kapsayıcısı **Service**'tir; `organizationId` kiracı izolasyonu için denormalize edilmiş referanstır (gözden geçirilebilir → `../todo.md`).
- **Style tüketicileri:** yalnız **Action** ve **Status** (`styleId`). Form alanları bu Style varlığını kullanmaz.
- **Action → ProcessStepAction:** canlı bağ (FK) **yoktur**. Adıma aksiyon eklenirken Action alanları
  (`code`/`definition`/`icon`/`styleId`/`actionType`) **bir kez kopyalanır**; sonrasında iki taraf **bağımsızdır**
  (Action değişince mevcut binding'ler güncellenmez). Bu yüzden `ProcessStepAction`'da `actionId` **tutulmaz**.
- **Profil-bazlı alan override'ı:** `ProcessViewProfilePropertySetting` (`viewProfilePropertyId` + `key`/`value`),
  `propertyType`'a göre yorumlanan bir **dictionary**'dir; `Property` varsayılanını profil düzeyinde ezer (Form List:
  `activeStartActions`, `addFromExistingStatusIds`, `selectableVisible`). Key kataloğu → `service-settings/view-profile-property.md`.
- **BusinessRule / BusinessRuleCondition** frontend'de çalışır; **en son** kesinleşecek (→ `../todo.md`).
- **Organizasyon ayarları (yapısal veri):** eski "Account Settings" DTO'larından türetildi; tümü **`organizationId` (int)**
  ile kiracıya bağlı (`accountId` string→int; `account*`→`organization*`; Türkçe alanlar İngilizceye normalize; **Title→Profession**).
  **Company** ve **User** merkez düğümlerdir. BPM tüketimi: **User/UserGroup** → onay merci/atama · **WorkingSchedule+VacationDay**
  → Timer/zaman aşımı · **Department/Profession** → yönetici atama tipleri · **CostCenter/CreditCard** → masraf.
- **Organizasyon ayarları — `active` / `deleted`:** `active` (eski `status`) + `deleted` bulunan master-veri modellerinde
  (Company · Department · Profession · User · UserGroup · AdditionalQualification · CostCenter · WorkerLevel · WorkingSchedule · CreditCard) **BPM workflow motoru
  `deleted=true` VEYA `active=false` kayıtları kullanmaz** (ikisi de **not-null**: varsayılan `active=true`, `deleted=false`; yeni kayıtlar böyle oluşur). Fark: **`deleted=true`** frontend'de tamamen **gizli/aktarılmaz/salt**;
  **`active=false`** frontend'de **görünür + düzenlenebilir** (yalnız BPM veri işlemede dışlanır). _(VacationDay'de `active`/`code` yok; ProcessTransfer/SchedulerJob operasyon/altyapı — dokunulmadı.)_
- **`code` benzersizliği — `(organizationId, code)`:** aynı organizasyonda aynı `code`'lu iki kayıt olamaz.
  - **Yapısal org-ayarları (10):** Company·Department·Profession·User·UserGroup·AdditionalQualification·CostCenter·WorkerLevel·WorkingSchedule·CreditCard — **`deleted=true` kayıtlar kontrole dahil edilmez**. _(User ayrıca `(organizationId, email)` · `(organizationId, phone)` benzersiz — aynı e-posta farklı org'larda olabilir.)_
  - **Organizasyon havuzu:** **Status · Action** benzersiz; **Style** `code` doluysa (`organizationId=null` sistem tarafı da).
  - **İstisnalar:** **Translation** → `(organizationId, code, languageCode)`; **Organization** → `code` **global** benzersiz.
- **Yetkilendirme:** `Organization.adminUserIds` (adminler — en az 1 aktif; tüm yetkiler + config'i düzenler) +
  **4 grup alanı** (`impersonationUserGroupId`·`organizationSettingsUserGroupId`·`serviceSettingsUserGroupId`·`viewAllReportsUserGroupId`;
  her biri **tek** `UserGroup`). Eski `User.authorizationLevel` **kaldırıldı** → `../organization-settings/permissions.md`.

---

*Oluşturma: 2026-07-02.*
