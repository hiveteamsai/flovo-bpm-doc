# Flovo BPM — Veri Modelleri (Şema Referansı) — İndeks

> **Durum:** 🟡 TASLAK — mevcut tasarım dokümanlarından **ilk çıkarım**; alanlar/tipler gözden geçirilecek.
> **Amaç:** `models/` ağacının **indeksi** — alt klasörlere yönlendirme (§1) + tüm modellerin **birbirleriyle ilişkileri**
> (§2/§3, tek yerde). Her modelin **alan-düzeyi ayrıntısı** kendi dosyasında, **klasör dizini** ise alt klasör `index.md`'lerindedir.
> Bu klasör **veri modeli/şema** odaklıdır; **davranış/kullanım** özellik dokümanlarındadır
> (`../organization-settings/`, `../service-settings/`, `../flovo-bpm-engine.md`).
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

## 1. Alt klasörler (dizin)

> Modeller **fiziksel olarak alt klasörlere** ayrılmıştır (özellik klasörleriyle hizalı). Her alt klasörün **kendi
> `index.md`'si** o klasördeki modelleri tek tek listeler; buradaki tablo yalnız **klasör düzeyinde** özet + yönlendirmedir.
> Model **ilişkileri** (klasörler arası) aşağıda §2/§3'te tek yerde tutulur.

| Klasör | İçerik (özet) | İndeks |
|---|---|---|
| **organization-settings/** | Kiracıya bağlı **yapısal veri** + **organizasyon havuzu** (eski "Account Settings"): Organization · Company · Department · Profession · Position · User · UserGroup · Translation · Style · Status · Action · CostCenter · WorkerLevel · CreditCard · AdditionalQualification · WorkingSchedule · VacationDay · ProcessTransfer · SchedulerJob. | [`organization-settings/index.md`](./organization-settings/index.md) |
| **service-settings/** | Bir **Solution/Service** altındaki tasarım modelleri: Solution · Service (`formType`) · ServiceTrigger · Property/PropertyItem · ProcessViewProfile ailesi · ProcessStep · ProcessStepAction · BusinessRule/BusinessRuleCondition. | [`service-settings/index.md`](./service-settings/index.md) |
| **processInstances/** | Ayarlardan üretilen **çalışma-zamanı (runtime)** kayıtları: ProcessInstance · ProcessStepInstance · Instance · InstanceAwaitingUser · AssociatedInstance. 🟢 TANIMLI. | [`processInstances/index.md`](./processInstances/index.md) |
| **enums/** | Modellerde kullanılan **enum tanımları** (kanonik değer listeleri; ör. `actionType`, `propertyType`, `formType`). | [`enums/index.md`](./enums/index.md) |

> **Not:** **Organization** kiracının kökü; **Solution · Service** service-settings kırılımının başladığı yerdir
> (fiziksel olarak `service-settings/` altında). **Organizasyon havuzu** (Translation/Style/Status/Action) organizasyona
> bağlıdır ve tüm servislerde kullanılır.

---

## 2. İlişki Haritası

```
Organization (id)
 ├─< Solution (organizationId)
 │    └─< Service (solutionId)
 │         ├─< ServiceTrigger       (serviceId; targetServiceId → Service, targetStarterProcessStepId → ProcessStep[timer:processStart | associate:subProcessStart], targetPropertyId → Property)
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
 └─< Instance (processInstanceId; serviceId → Service · creatorUserId → User · statusId → Status)
      └─< AssociatedInstance (instanceId → Instance · associatedInstanceId → Instance · associatedPropertyId → Property)
```

---

## 3. İlişki Tablosu
> Kapsam: **süreç hiyerarşisi + havuz + yetki** ilişkileri + **runtime (`processInstances/`)** (tablonun altında). Organizasyon-ayarı
> modellerinin (Company/User/Department… **arası**) FK'leri için ilgili model dosyalarının "İlişkiler" bölümlerine bakın.

| Kaynak | Alan | Hedef | Kardinalite | Not |
|---|---|---|---|---|
| Solution | `organizationId` | Organization.id | N–1 | |
| Service | `solutionId` | Solution.id | N–1 | organizasyon dolaylı (solution üzerinden) |
| ServiceTrigger | `serviceId` | Service.id | N–1 | kaynak servis (olay bunun instance'larında izlenir) |
| ServiceTrigger | `targetServiceId` | Service.id | N–1 | tetiklenecek hedef servis |
| ServiceTrigger | `targetStarterProcessStepId` | ProcessStep.id | N–1 | `timer` → `processStart`, associate → `subProcessStart`; **değişmez:** `ProcessStep(targetStarterProcessStepId).serviceId == targetServiceId` (hedef **adımın** servisi = hedef servis) **ve** `stepType == (timer ? processStart : subProcessStart)` |
| ServiceTrigger | `targetPropertyId` | Property.id | N–1 | izlenen ilişki alanı (associate tipi); null olabilir; `serviceId` ile aynı serviste |
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
| Translation | `code` | (kod eşleşmesi) | — | FK değil; kaynak modellerin **`translationCode`**'u + `languageCode` + `organizationId` ile çözülür (`translationCode=null` → çeviri es geçilir) |
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
| Instance | `creatorUserId` | User.id | N–1 | null olabilir (**`parameter`** tipi servis — sahipsiz veri-kaynağı; ayrıca **API/webhook başlatımlı `form`** — tek sahip yok, başlatan `ProcessInstance.createdByApiKeyId`) |
| Instance | `statusId` | Status.id | N–1 | formun mevcut durumu (havuz) |
| InstanceAwaitingUser | `processStepInstanceId` | ProcessStepInstance.id | N–1 | |
| InstanceAwaitingUser | `instanceId` | Instance.id | N–1 | |
| InstanceAwaitingUser | `userId` | User.id | N–1 | `userId` **veya** `userGroupId` (biri) |
| InstanceAwaitingUser | `userGroupId` | UserGroup.id | N–1 | |
| AssociatedInstance | `instanceId` · `associatedInstanceId` | Instance.id | N–1 | formlar arası ilişki |
| AssociatedInstance | `associatedPropertyId` | Property.id | N–1 | `associatedInstanceId`'nin formundaki property |

---

## 4. Henüz modellenmemiş / referans verilen varlıklar (açık)

| Varlık | Nerede geçiyor | Not |
|---|---|---|
| **ApiKey** (Customer API anahtarı) | `ProcessInstance.createdByApiKeyId`, `ProcessStepInstance.atApiKeyId` | API üzerinden başlatım/tetikleme kimliği (oluşturan `User` değilken "kim yaptı"). **Ad geçici**; Customer API erişim mekanizması kesinleşince doğrulanacak → `../todo.md`. |
| **ExpenseType / Currency / Tax** | Masraf süreçleri | Masraf tipi, para birimi, vergi — referans dokümanında **kapsam dışı**. _(Position/Staff artık modellendi → `organization-settings/position.md`.)_ |

> **Instance (doldurulmuş form) artık modellendi** → `processInstances/` (ProcessInstance · Instance · ProcessStepInstance · InstanceAwaitingUser ·
> AssociatedInstance). 🟢 TANIMLI — yalnız `Instance` **property value depolaması** açık (→ `../todo.md`).

> **Not:** **User** ve **UserGroup** artık modellendi (→ §1 "Organizasyon ayarları"). `userGroupId` /
> `actionDisplayAuthorizedUserGroupId` gibi BPM referansları `UserGroup`'a, kullanıcı atamaları `User`'a bağlanır.

---

## 5. Notlar
- **Enum'lar** artık **tek yerde** indekslenir → [`enums/index.md`](enums/index.md) (kanonik değer listeleri: `actionType`, `propertyType`, `businessRuleRuntimeType`, `criterionType`, `valueType`, `formType`...). Her model, kullandığı enum'a **buradan link** verir ve **o değerin o modeldeki rolünü** kendi içinde anlatır.
- **`Service.formType` (form/parameter/eventForm):** servisin davranışını belirler — **`form`** akış+onay+`Instance`
  (`creatorUserId` **genelde dolu ama zorunlu değil** — API/webhook başlatımında null olabilir, başlatan `createdByApiKeyId`;
  `InstanceAwaitingUser`); **`parameter`** onaysız veri-kaynağı (`Instance` oluşur, `creatorUserId`
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
  → Timer/zaman aşımı · **Department** → departman yöneticisi ataması · **Profession** → kullanıcı ünvanı + ek nitelik (`RelationalType=professions`) · **Position/Staff** → organizasyonel görev yeri +
  personel slotu (1 kadro ↔ 1 kullanıcı; kullanıcı pozisyonu `Staff.userId` üzerinden) · **CostCenter/CreditCard** → masraf.
- **Organizasyon ayarları — `active` / `deleted`:** `active` (eski `status`) + `deleted` bulunan master-veri modellerinde
  (Company · Department · Profession · Position · User · UserGroup · AdditionalQualification · CostCenter · WorkerLevel · WorkingSchedule · CreditCard) **BPM workflow motoru
  `deleted=true` VEYA `active=false` kayıtları kullanmaz** (ikisi de **not-null**: varsayılan `active=true`, `deleted=false`; yeni kayıtlar böyle oluşur). Fark: **`deleted=true`** frontend'de tamamen **gizli/aktarılmaz/salt**;
  **`active=false`** frontend'de **görünür + düzenlenebilir** (yalnız BPM veri işlemede dışlanır). _(VacationDay'de `active`/`code` yok; ProcessTransfer/SchedulerJob operasyon/altyapı — dokunulmadı.)_
- **`code` benzersizliği — `(organizationId, code)`:** aynı organizasyonda aynı `code`'lu iki kayıt olamaz.
  - **Yapısal org-ayarları (11):** Company·Department·Profession·Position·User·UserGroup·AdditionalQualification·CostCenter·WorkerLevel·WorkingSchedule·CreditCard — **`deleted=true` kayıtlar kontrole dahil edilmez**. _(User ayrıca `(organizationId, email)` · `(organizationId, phone)` benzersiz — aynı e-posta farklı org'larda olabilir; **`email`/`phone` nullable, null olanlar kontrole girmez, ancak ikisi birden null olamaz**. Position'ın `Staff` alt modeli `(positionId, code)` + `userId` benzersiz.)_
  - **Organizasyon havuzu:** **Status · Action** benzersiz; **Style** `code` doluysa (`organizationId=null` sistem tarafı da).
  - **İstisnalar:** **Translation** → `(organizationId, code, languageCode)`; **Organization** → `code` **global** benzersiz.
- **Çeviri anahtarı — `translationCode` (`string?`):** Çevrilebilir modeller çeviriye **iş kodlarıyla (`code`) değil**,
  ayrı bir **`translationCode`** alanıyla bağlanır (`Model.translationCode → Translation.code`). Gerekçe: `code`
  **model-içi** benzersiz (`(organizationId, code)`), çeviri ad-uzayı ise **organizasyon geneli** ve varlık ayrımı yok →
  Departman `"01"` ile Şirket `"01"` aynı çeviri satırına düşerdi. **`null` = çeviri es geçilir**, doğrudan `definition`
  kullanılır (çeviri **opt-in**). Alanı taşıyan **23 model/alt-model** + gerekçe → `../organization-settings/translation.md` §3.1.
  _(Taşımayanlar: `Style`·`User`·`Organization` — çevrilecek `definition` yok; `Translation` — anahtarın kendisi.)_
  **Snapshot kopyaları** anahtarı da kopyalar: `ProcessStepAction.translationCode` (Action'dan) ·
  `...QualificationValue.comboboxTranslationCode` (QualificationItem'dan).
- **Yetkilendirme:** `Organization.adminUserIds` (adminler — en az 1 aktif; tüm yetkiler + config'i düzenler) +
  **4 grup alanı** (`impersonationUserGroupId`·`organizationSettingsUserGroupId`·`serviceSettingsUserGroupId`·`viewAllReportsUserGroupId`;
  her biri **tek** `UserGroup`). Yetki **org-bazlı** (admin + grup) **dinamik** → `../organization-settings/permissions.md`.

---

*Oluşturma: 2026-07-02.*
