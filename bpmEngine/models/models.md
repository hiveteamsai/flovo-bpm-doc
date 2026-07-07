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

**`Organization → Solution → Service → {Property · ProcessViewProfile · ProcessStep · WorkRule}`**

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
> (**Solution · Service** + servise bağlı modeller). Bu indeks (`models.md`) kökte kalır.

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
| **Service** | [`service.md`](./service-settings/service.md) | İş sürecinin/formun tamamı (solution altında). |
| **Property** | [`property.md`](./service-settings/property.md) | Form alanı (kontrol tipiyle render edilir). |
| **PropertyItem** | [`property-item.md`](./service-settings/property-item.md) | Seçim alanının statik seçeneği. |
| **ProcessViewProfile** | [`view-profile.md`](./service-settings/view-profile.md) | Formun adım-bazlı görünümü. |
| **ProcessViewProfileProperty** | [`view-profile-property.md`](./service-settings/view-profile-property.md) | Profildeki tek alan yapılandırması. |
| **ProcessViewProfilePropertySetting** | [`view-profile-property-setting.md`](./service-settings/view-profile-property-setting.md) | Alanın profil-bazlı tipe-özel override'ı (key/value). |
| **ProcessStep** | [`process-step.md`](./service-settings/process-step.md) | Süreç adımı (akıştaki düğüm). |
| **ProcessStepAction** | [`process-step-action.md`](./service-settings/process-step-action.md) | Aksiyonun adıma bağlanması (binding). |
| **WorkRule** | [`work-rule.md`](./service-settings/work-rule.md) | Frontend realtime form davranışı. 🟡 en son şekillenecek. |
| **WorkRuleCondition** | [`work-rule-condition.md`](./service-settings/work-rule-condition.md) | İş kuralı koşulu (recursive). 🟡 en son. |

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

### İş akışı / çalıştırma (runtime — `workFlows/`)
> 🟢 **TANIMLI** — ayarlardan (`Service`/`ProcessStep`/`Property`…) motor tarafından üretilen **çalışma-zamanı**
> kayıtları. 6 modelin alanları netleşti. _(Açık: `Form` **property value depolaması** sonraya bırakıldı → `../todo.md`.)_

| Model | Dosya | Kısa açıklama |
|---|---|---|
| **WorkFlow** | [`work-flow.md`](./workFlows/work-flow.md) | Bir servis sürecinin çalıştırma örneği. |
| **ProcessStepExecution** | [`process-step-execution.md`](./workFlows/process-step-execution.md) | Tek bir adımın çalıştırılması (aksiyon/tetikleyici/zaman). |
| **Form** | [`form.md`](./workFlows/form.md) | Doldurulmuş form / süreç örneği; mevcut `statusId`. |
| **FormAwaitingUser** | [`form-awaiting-user.md`](./workFlows/form-awaiting-user.md) | Formu bekleyen kullanıcı/grup (onay kuyruğu). |
| **UserGroupApprovedUser** | [`user-group-approved-user.md`](./workFlows/user-group-approved-user.md) | Grup onayında onaylayan üye + zamanı. |
| **RelatedForm** | [`related-form.md`](./workFlows/related-form.md) | Formlar arası ilişki (property boyutuyla). |

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
 │         └─< WorkRule             (serviceId; +organizationId = izolasyon)
 │                  └─< WorkRuleCondition (workRuleId, recursive)
 │
 └── Organizasyon havuzu (organizationId) — servis modellerinde kullanılır:
      ├─< Translation (null = ortak/Flovo)
      ├─< Style       (null = sistem) ─────> Action.styleId · Status.styleId
      ├─< Action                     ┄┄┄┄> (ProcessStepAction'a bir kez kopyalanır — canlı FK yok)
      └─< Status                     ─────> ProcessStepAction.changeStatusId
```

**İş akışı / çalıştırma (runtime — `workFlows/`):** ayarlardan üretilen instance/execution verisi.

```
WorkFlow (id; createdByUserId → User · createdByApiKeyId → ApiKey[geçici] · serviceId → Service · parentWorkFlowId → WorkFlow[self, alt süreç])
 ├─< ProcessStepExecution (workFlowId; formId → Form · processStepId → ProcessStep ·
 │        │                 processStepActionId → ProcessStepAction · atUserId/atDelegateUserId → User · atApiKeyId → ApiKey[geçici])
 │        └─< FormAwaitingUser (processStepExecutionId; formId → Form · userId → User · userGroupId → UserGroup)
 │                 └─< UserGroupApprovedUser (formAwaitingUserId; userId → User)   # yalnız grup onayı
 └─< Form (workFlowId; serviceId → Service · creatorUserId → User · statusId → Status)
      └─< RelatedForm (formId → Form · relatedFormId → Form · relatedPropertyId → Property)
```

---

## 3. İlişki Tablosu
> Kapsam: **süreç hiyerarşisi + havuz + yetki** ilişkileri + **runtime (`workFlows/`)** (tablonun altında). Organizasyon-ayarı
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
| WorkRule | `serviceId` | Service.id | N–1 | asıl kapsayıcı |
| WorkRule | `organizationId` | Organization.id | N–1 | kiracı/izolasyon (denormalize) |
| WorkRule | `activeViewProfiles` | ProcessViewProfile.id | N–N | yalnız bu profillerde çalış |
| WorkRuleCondition | `workRuleId` | WorkRule.id | N–1 | |
| WorkRuleCondition | `parentConditionId` | WorkRuleCondition.id | N–1 | iç içe (recursive) |
| Translation | `code` | (kod eşleşmesi) | — | FK değil; `code` + `languageCode` + `organizationId` ile çözülür |
| **— İş akışı / çalıştırma (runtime — `workFlows/`) —** | | | | |
| WorkFlow | `createdByUserId` | User.id | N–1 | null olabilir (kullanıcı **ya da** API) |
| WorkFlow | `createdByApiKeyId` | ApiKey | N–1 | null olabilir; **ApiKey geçici** |
| WorkFlow | `serviceId` | Service.id | N–1 | |
| WorkFlow | `parentWorkFlowId` | WorkFlow.id | N–1 | **self**; null olabilir (alt süreç → ana süreç akışı; ana süreçte null) |
| ProcessStepExecution | `workFlowId` | WorkFlow.id | N–1 | |
| ProcessStepExecution | `formId` | Form.id | N–1 | null olabilir (form yönlendirme) |
| ProcessStepExecution | `processStepId` | ProcessStep.id | N–1 | |
| ProcessStepExecution | `processStepActionId` | ProcessStepAction.id | N–1 | aksiyon tetiklenince dolar |
| ProcessStepExecution | `atUserId` · `atDelegateUserId` | User.id | N–1 | tetikleyen · vekaleten onaylayan |
| ProcessStepExecution | `atApiKeyId` | ApiKey | N–1 | null olabilir; **ApiKey geçici** |
| Form | `workFlowId` | WorkFlow.id | N–1 | |
| Form | `serviceId` | Service.id | N–1 | |
| Form | `creatorUserId` | User.id | N–1 | |
| Form | `statusId` | Status.id | N–1 | formun mevcut durumu (havuz) |
| FormAwaitingUser | `processStepExecutionId` | ProcessStepExecution.id | N–1 | |
| FormAwaitingUser | `formId` | Form.id | N–1 | |
| FormAwaitingUser | `userId` | User.id | N–1 | `userId` **veya** `userGroupId` (biri) |
| FormAwaitingUser | `userGroupId` | UserGroup.id | N–1 | |
| UserGroupApprovedUser | `formAwaitingUserId` | FormAwaitingUser.id | N–1 | yalnız grup onayı |
| UserGroupApprovedUser | `userId` | User.id | N–1 | onaylayan üye |
| RelatedForm | `formId` · `relatedFormId` | Form.id | N–1 | formlar arası ilişki |
| RelatedForm | `relatedPropertyId` | Property.id | N–1 | `relatedFormId`'nin formundaki property |

---

## 4. Henüz modellenmemiş / referans verilen varlıklar (açık)

| Varlık | Nerede geçiyor | Not |
|---|---|---|
| **ApiKey** (Customer API anahtarı) | `WorkFlow.createdByApiKeyId`, `ProcessStepExecution.atApiKeyId` | API üzerinden başlatım/tetikleme kimliği (oluşturan `User` değilken "kim yaptı"). **Ad geçici**; Customer API erişim mekanizması kesinleşince doğrulanacak → `../todo.md`. |
| **ExpenseType / Currency / Position / Tax** | Masraf süreçleri | Masraf tipi, para birimi, pozisyon, vergi — referans dokümanında **kapsam dışı**. |

> **Form / Instance artık modellendi** → `workFlows/` (WorkFlow · Form · ProcessStepExecution · FormAwaitingUser ·
> UserGroupApprovedUser · RelatedForm). 🟢 TANIMLI — yalnız `Form` **property value depolaması** açık (→ `../todo.md`).

> **Not:** **User** ve **UserGroup** artık modellendi (→ §1 "Organizasyon ayarları"). `organizationUserGroupId` /
> `actionDisplayAuthorizedUserGroupId` gibi BPM referansları `UserGroup`'a, kullanıcı atamaları `User`'a bağlanır.

---

## 5. Notlar
- **Enum'lar** ilgili model dosyasında listelenir (`actionType`, `controlTypeId`, `workRuleRuntimeType`, `criterionType`, `valueType`...).
- **Organizasyon havuzu** (Translation/Style/Status/Action) `organization-settings/`'a; **servise bağlı** modeller `service-settings/`'ya karşılık gelir.
- **ProcessStep / WorkRule** asıl kapsayıcısı **Service**'tir; `organizationId` kiracı izolasyonu için denormalize edilmiş referanstır (gözden geçirilebilir → `../todo.md`).
- **Style tüketicileri:** yalnız **Action** ve **Status** (`styleId`). Form alanları bu Style varlığını kullanmaz.
- **Action → ProcessStepAction:** canlı bağ (FK) **yoktur**. Adıma aksiyon eklenirken Action alanları
  (`code`/`definition`/`icon`/`styleId`/`actionType`) **bir kez kopyalanır**; sonrasında iki taraf **bağımsızdır**
  (Action değişince mevcut binding'ler güncellenmez). Bu yüzden `ProcessStepAction`'da `actionId` **tutulmaz**.
- **Profil-bazlı alan override'ı:** `ProcessViewProfilePropertySetting` (`viewProfilePropertyId` + `key`/`value`),
  `propertyType`'a göre yorumlanan bir **dictionary**'dir; `Property` varsayılanını profil düzeyinde ezer (Form List:
  `activeStartActions`, `addFromExistingStatusIds`). Key kataloğu → `service-settings/view-profile-property.md`.
- **WorkRule / WorkRuleCondition** frontend'de çalışır; **en son** kesinleşecek (→ `../todo.md`).
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
