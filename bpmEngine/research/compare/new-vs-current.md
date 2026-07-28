# Yeni Flovo BPM vs Mevcut (Eski) Flovo — Farklar

> **Amaç:** Mevcut (eski) Flovo BPM tarafı ile **yeni proje tasarımı** arasındaki farkları tek yerde toplamak —
> **neler eklendi, neler çıkarıldı, neler yeniden adlandırıldı / taşındı** — ve sonda **başarılı/başarısız değerlendirmesi.**
>
> **Kaynak:** Tasarım dokümanları (`../../flovo-bpm-engine.md`, `../../service-settings/*`, `../../organization-settings/*`) ·
> Mevcut proje referansı → `../current-flovo-bpm-engine/`.
>
> **Not:** Bu **canlı özet**tir; her maddenin gerekçesi/detayı ilgili tasarım dosyasındadır. Çakışınca **ilgili doküman esastır.**

---

## 0. Özet — En Büyük Değişiklikler
| # | Değişiklik | Eski | Yeni |
|---|---|---|---|
| 1 | **Aksiyon seçimi + yönlendirme** | Örtük seçim + `targetProcessStepId` | **Aksiyon kodu** aksiyonu seçer (`default`/`onFail`/`true`-`false`/switch); **`targetProcessStepId` korunur** ve adıma yönlendirir |
| 2 | **Adımlar arası veri** | Örtük/server-driven | **Explicit `parameters` · `changeList` · `action`** modeli |
| 3 | **İş kuralı katmanı** | Motorla iç içe | **Frontend realtime katman**; motoru doğrudan etkilemez |
| 4 | **Renk/stil** | Statik Bootstrap (`actionType`) | **Dinamik Style** varlığı (ayrı yönetim) |
| 5 | **Aksiyon türleri** | İş-bazlı custom (`expform-*`, `new-instance*`...) | **Sade genel türler** (`manual`/`eventForm`/`takePhoto`/...) |
| 6 | **Aksiyon tanımı** | Tek DTO | **ActionDto = şablon** + adıma kopyalanan binding |
| 7 | **Adlandırma** | "field" | **"property"** (`...FieldId → ...PropertyId`) |
| 8 | **Raporlar** | View-profile içinde | **Ayrıldı** (ayrı özellik) |
| 9 | **Şişman modeller** | PropertyDto ~60 alan | **İnce çekirdek + tipe-özel ayar** |
| 10 | **Eba entegrasyonu** | Var (`ebaIntegratedFlovoApp`, `FromEba`) | **Tamamen kaldırıldı** |
| 11 | **Çeviri (i18n)** | Dağınık/örtük | **`code`-bazlı çeviri motoru** (ortak+organizasyon; **kayıt-başına-dil**: `languageCode`+`definition`) + **ayrı `translationCode` anahtarı** (iş kodu ≠ çeviri anahtarı) |
| 12 | **Organizasyon (kiracı)** | **Account** (`accountId`) + `solutionid` başlıkları | **Organization** (`organizationId` **int**) varlığı (`defaultLang`, `idleTimeoutMinute`, `logoUrl`) |
| 13 | **Seçim öğesi** | `propertyItems` (değer=metin) | **`PropertyItem`** — `translationCode` (çeviri) ile `value` **ayrıldı** |
| 14 | **Hiyerarşi & havuz** | account/solution/service başlıkları | **Organization → Solution → Service**; Action/Status/Style/Translation = **organizasyon havuzu** (`organizationId`) |
| 15 | **Profil-bazlı alan override** | Alan ayarları profilden bağımsız | **`ProcessViewProfilePropertySetting`** (key/value) — Form List ayarları görüntüleme profiline göre |
| 16 | **Organizasyon ayarları (yapısal)** | "Account Settings" DTO'ları (`accountId` string) | **13 DB modeli** (Company/User/Department/Profession…) — `organizationId` **int**; **Title→Profession**; typed/combobox ek nitelik |
| 17 | **Yetkilendirme** | Kullanıcı bazında **sayısal `authorizationLevel`** (dinamik değil) | **Org-bazlı**: `adminUserIds` + grup-bazlı yetkiler (kullanıcı yerine geçme · org/servis ayarları erişimi · tüm raporlar) |
| 18 | **Master-veri yaşam döngüsü** | `status` (bool) | **`active` + `deleted`** (soft-delete); `(organizationId, code)` **benzersiz** |
| 19 | **İş akışı / çalıştırma (runtime)** | `ServiceInstances` · `ServiceInstanceRequests` (+ dağınık alanlar) | **`processInstances/` 5 model**: `ProcessInstance` · `ProcessStepInstance` · `Instance` · `InstanceAwaitingUser` · `AssociatedInstance` |
| 20 | **Adım tipe-özel ayarlar** | Adım DTO'suna gömülü düz alanlar | **`settings` (JSONB)** + **`stepType`** ayrımlayıcı + tip-tip ayar modelleri (§3) + adım-tipi **enum'ları** (ProcessStepType, HttpMethod, TimerCalculationType, NotificationChannel…) |
| 21 | **Çeviri anahtarı** | Çeviri **iş kodu (`code`) ile** eşleşir → farklı varlıkların kodları (Departman "01" ↔ Şirket "01") **aynı çeviri satırına çakışır** | **Ayrı, nullable `translationCode`** (23 model/alt-model); `code` yalnız iş kodu. **`null` = çeviri es geçilir → `definition`** (opt-in) |

---

## 1. Motor / Mimari (`../../flovo-bpm-engine.md`)
**➕ Eklendi**
- **Aksiyon-kodu tabanlı aksiyon seçimi:** adım sonucu → **kod** (`default`/`onFail`/`true`/`false`/switch) → o kodlu aksiyon; seçilen aksiyonun **`targetProcessStepId`**'si sonraki adıma yönlendirir.
- **`parameters` / `changeList` / `action`** veri aktarım modeli (niyetli/explicit).
- **changeList evrensel giriş kuralı:** her adım, işini yapmadan ÖNCE changeList'i forma uygular.
- **İki-katman ayrımı:** form-mantığı (frontend realtime) ↔ akış-mantığı (motor).
- **ActionDto = yeniden kullanılabilir aksiyon şablonu** kavramı.

**➖ Çıkarıldı / değişti**
- "Her şey backend / ince istemci" yaklaşımı yeniden değerlendirildi (iş kuralları frontend'e taşındı).

**↔ Korundu**
- Servis / Solution / **Organization** çok-kiracılık modeli (`organizationId`/`solutionId`/`serviceId`) — model korundu, **Account → Organization** olarak yeniden adlandırıldı. _(Eski `accountId` aslında **kod** niteliğindeydi → yeni **`organizationCode`** (string); yeni **`organizationId`** ise int primary key'dir.)_
- Tasarım-zamanı 6-alan sırası (property → profil → kural → aksiyon → durum → adım).
- Aksiyonun **`targetProcessStepId`**'si (aksiyon çalışınca hangi adıma ilerleneceği) — **korunur**; üstüne **aksiyon-kodu seçimi** formalize edildi.

---

## 2. Süreç Adımları (`../../service-settings/process-step.md`)
Mevcut **15 adım tipi** (biri, `atama`, enum'da tanımlı ama **kullanılmayan**) → yeni **22 adım** (korunan + yeni;
çıkarılan: **Adım İptali** · **Eba Entegre** · kullanılmayan **`atama`**).

**➕ Eklenen (mevcutta yok)**
- **Flovo AI** · **Switch** · **Processing** · **Instance Creator** · **Instance Deleter** · **Form Yönlendirme** · **Süreç Adımı Tetikleme** ·
  **Alt Süreç Başlangıcı** (bağımsız alt sürecin **giriş düğümü**; webhook **veya** Süreç Adımı Tetikleme ile tetiklenir → §11 not) ·
  **Alt Süreç Bitişi** (bağımsız alt sürecin **çıkış düğümü**; Süreç Bitişi'nin alt-süreç karşılığı) ·
  **Üst Form Kullanıcı** (`parentInstanceUser` — alt-servis kaydını **üst formun** güncel atananlarına/`code`-eşleşen görüntüleme
  profiline **anlık** bağlayan human-task adımı; alt-servisi paralel ilerletmenin senkron/performans yükünü çözer → §3.22)

**➖ Çıkarılan**
- **Adım İptali** (`stepCancellation`) — kaldırıldı.
- **Eba Entegre** (`ebaIntegratedFlovoApp`) — kaldırıldı.
- **`atama`** — eski `ProcessStepType` enum'unda **tanımlı ama hiçbir yerde kullanılmayan / aktif olmayan** ölü bir değerdi
  (gerçek bir adım davranışı yoktu); bu yüzden yeni tasarıma **taşınmadı** (işlevsel bir kayıp değil).
  > ⚠️ Bu, form alanlarına **değer** yazan **Değer Atama** (`valueAssignment`) ile **karıştırılmamalı** — o ayrı ve **korunur** (aşağı bkz.).

**↔ Korunan (adım — dikkat)**
- **Değer Atama** (`valueAssignment`) → yeni **§3.4 Değer Atama** olarak **korunur** (property'ye / alt-servise değer atama).

**✏️ Yeniden adlandırılan**
- **Function → HTTP Request** (+ yeni `async` ayarı; query/template/header/body parametreleri explicit). **`resource → endpoint`**,
  **`method` (string) → `HttpMethod` enum**, `returns` **kaldırıldı**, parametreler **`DynamicParameter`** (Bildirim ile ortak alt-model).
- **Adım ayar alanları:** (Kullanıcı) `stableUserId → fixedUserId`; (Kullanıcı Grubu) `accountUserGroupId → organizationUserGroupId`,
  `dynamicUserListFieldId → dynamicUserListPropertyId`; (Timer) `WorkStyle → TimerCalculationType`.

**🔧 Adım ortak yapısı (`ProcessStepDto`) değişiklikleri**
- **Kaldırıldı:** `selectModalItemDeactive`, `canSelectExpenses` → görüntüleme/seçim profili konusu (Form List).
- **Taşındı → Değer Atama:** `useRelatedService` (→ **`useAssociatedService`**), `relatedServiceId` (→ **`associatedServiceId`**), `targetInstancesFieldId` (→ `targetInstancesPropertyId`).
- **Değer Atama:** alan `valueType` → **`valueAssignType`** (tip ValueAssignType); değer `FormValue` → **`PropertyValue`**; `targetFieldId`→`targetPropertyId`, `fieldId`→`propertyId`; ayrıca **`fromCalculation`** (+`expression`) değer kaynağı eklendi.

**🧩 Tipe-özel ayarların modellenmesi (yeni)**
- **`stepType` (ProcessStepType) + `settings` (JSONB):** Tipe-özel ayarlar `ProcessStep.settings` JSONB kolonunda **gömülü**
  (ayrı alt-tablo yok); şekli `stepType`'a göre yorumlanır. Tip-tip ayar modelleri → `../../models/service-settings/process-step.md` §3.
- **Yeni adım-tipi enum'ları:** `ProcessStepType` (21) · `HttpMethod` · `ProcessStepUserType` · `ProcessStepUserGroupType` ·
  `NotificationChannel` · `NotificationRecipientType` · `NotificationUserType` · `TimerCalculationType` · `WorkTimeSelection` ·
  `TimeAdjustmentOption` · `InstanceDeleteMode`; ayrıca `KeyboardType`/`BarcodeFormat` placeholder'ları dolduruldu. → `../../models/enums/index.md`.
- **Bildirim:** sabit TR/EN mesaj alanları → **dinamik dil listesi** (`{languageCode, text}`); **Toast** kanalı eklendi; `parameters` → `DynamicParameter[]`;
  alıcılar `NotificationRecipientType` (`user`/`userGroup`/`takeUsersWhoTookActionBefore`; ayrı `NotificationUserGroupType` **foldlandı**).
- **Kullanıcı:** userType'tan `managerChain` (yönetici zinciri) ve `managerByTitle` (ünvana göre yönetici) **kaldırıldı** (aktif değildi).
- **Switch:** ayrı `cases`/eşleme listesi yok — **alan değeri = aksiyon kodu** (eşleşme yoksa `default`).
- **Instance Deleter:** `deleteMode` (`InstanceDeleteMode`: `withRelated` / `unlinkRelated`).
- **Süreç Başlangıcı:** `userGroupId` (nullable) — **null = herkes** başlatabilir, **dolu = yalnız o grup**.

---

## 3. Aksiyonlar (`../../organization-settings/action.md` + `../../service-settings/process-step-action.md`)
**➕ Eklendi**
- **ActionDto = aksiyon şablonu** (ayrı doküman); adıma eklenince `code`/`definition`/`icon`/`styleId`/`actionType` **bir kez kopyalanır** (canlı bağ/FK yok — `actionId` tutulmaz; iki taraf bağımsız).
- **Sade actionType kataloğu:** **`manual` · `eventForm` · `takePhoto` · `selectFile` · `scanBarcode` · `webhook` · `autoAction`**.
- **`eventForm`** (reasonRequired'ın yerini alır) · **`webhook`** · **`autoAction`** (yeni türler).
- **`parameters`/`changeList`/`action`** aktarım modeli.

**➖ Çıkarıldı**
- `reasonRequired` → **eventForm** karşılıyor.
- **Custom per-job davranışları:** `fire-event`, `new-instance` / `-referenced` / `-other`, `take-photo`, `select-file`,
  `take-barcode`, `manuel-barcode-input`, `excel-export`, `expform-*`, `add-test-receipt` → genel türlere / başka mekanizmalara taşındı:
  - `new-instance*` → **Instance Creator** adımı + **Form List** `activeStartActions` (profil override)
  - `expform-add-exist-expense` → **Form List** `addFromExistingStatusIds` (profil override)
  - `excel-export` → **raporlama** (ayrı özellik)
  - `add-test-receipt` → kaldırıldı

**✏️ Yeniden adlandırılan (DİKKAT — kavram takası)**
| Eski alan | Eski anlam | Yeni |
|---|---|---|
| `actionType` (ProcessActionDto) | renk/stil (success/danger…) | **`styleId`** (dinamik Style varlığına FK) |
| `action` (ProcessStepActionDto) | davranış (fire-event…) | **`actionType`** (tür: `manual`/`eventForm`…) |

**↔ Korundu (binding'de):** **`targetProcessStepId`** (hedef adım), `changeStatusId`, `authorizationLevel`, `actionDisplayAuthorizedUserGroupId`, `showInHistory`, `environmentRestriction`.

---

## 4. Form Alanları (`../../service-settings/properties.md`)
Mevcut **30 ControlType** → yeni **19 alan** (16 founder + **3 mevcuttan korunan**; bazıları birleştirildi/çıkarıldı).

**➕ Eklendi**
- **İnce çekirdek + tipe-özel ayar** ayrımı (şişman ~60 alanlık `PropertyDto` sadeleştirildi).
- **`required`/`visible`/`enabled` property'den çıkarıldı → görüntüleme profiline** (alan = ne olduğu, profil = nasıl göründüğü).
- **User Info** alanı netleştirildi (Flow Info'dan ayrıldı).
- **`PropertyItem` modeli** (§2.6): `id` · `propertyId` · `value` · `translationCode` · `definition`. **`value` ↔
  `translationCode` ayrıldı** — farklı comboboxlar aynı `value`'yu (0/1/2/3) kullanabildiği için **çeviri eşleşmesi
  `translationCode` ile** yapılır; `(propertyId, value)` benzersiz. _(Bu ayrım sonradan **tüm çevrilebilir modellerin
  standardı** oldu → §9.)_

**➖ Çıkarıldı**
- **DataGrid / DataGridControl** — kaldırıldı.
- **`ObjectAccessController` · `TableFieldDisplayController`** — kaldırıldı.
- **Property'den `style` alanı** — property'de style alanı yok; görünüm style ile değişmiyor.
- **`propertyName` · `label`** — `definition` ile duplicate; **binding key `code`** oldu.
- **`precition`** (Numeric) — `maxDecimalDigits` ile birleşti.

**↔ Mevcuttan korunan (ayarları belgelendi)**
- `GroupByTaxReceiptController` · `KeyValueListControl` · `ImageAreaSelector` (§3.17–§3.19) — davranış+ayarları kaynaktan çıkarıldı.

**✏️ Yeniden adlandırılan**
- **ModalList → `formList`** (Form List; alt-servis alanı; **`combobox` değil**).
- **`onAfterChange` → `saveAndRefreshOnAfterChange`** (anlam netleşti: değer değişince kaydet+formu yenile).
- **`maximumNumberDecimalDigits` → `maxDecimalDigits`** (Numeric; `precition` ile birleşik).

**🔗 Birleştirilen (alanın opsiyonu olarak)**
- `MaskedEntry` → **`textbox`** (maske) · **`Entry` + `Editor` → `textbox`** (`minLine`/`maxLine`; ayrı çok-satır alanı yok) ·
  `NumericUpDown` → **`numericTextbox`** · `MultiSelect` → **`combobox`** · `DateTimePicker` → **`datepicker`** ·
  `Photo` / `ImageList` → **`file`** · `DataGrid` görünümü → (kaldırıldı).

**🔧 Görünüm alanlarının kapsamı daraltıldı**
- `headerText` — artık **her alanda değil**; yalnız **pop-up açan alanlarda** (`combobox`/`datepicker`/`timePicker`) pop-up başlığı.
- `fontSize`·`iconSize`·`isBold`·`textAlignment`·`stiky` — çekirdekten çıkıp **`text` (statik başlık)** alanına özel oldu.

**🔀 Form List ayarları → görüntüleme profiline (yeni)**
- `addNewEnabled` → **`activeStartActions`** (list; `childService` başlangıç aksiyonlarından seçim; **boş=oluşturma yok**) ·
  `addFromExistingRecordsIsActive` → **`addFromExistingStatusIds`** (list; hangi durumdaki formlar) — ikisi de **profil-bazlı**
  (`ProcessViewProfilePropertySetting`).
- `selectedEnable` → **`selectableVisible`** (Form List **profil-bazlı**; tik/seçim görünürlüğü) · öneri `selectedEditable` (profil-bazlı tik düzenlenebilirliği). _(Eski alan-düzeyi `selectableModeActive` kaldırıldı.)_

---

## 5. Görüntüleme Profilleri (`../../service-settings/view-profile.md`)
**➕ Eklendi**
- **`ProcessViewProfilePropertySetting`** (key/value) — alanın **tipe-özel** görünüm/davranış ayarlarını **profil bazında**
  override eder (`propertyType`'a göre dictionary). Örn. Form List: `activeStartActions`, `addFromExistingStatusIds`, `selectableVisible`, `selectedEditable`.
- Profil ve profil-alan modellerine **DB anahtarları** netleştirildi (`id`, `serviceId`, `viewProfileId`, `propertyId`).

**➖ Çıkarıldı**
- **Raporlar ayrıldı:** `showOnDataGrid` + rapor objesi (`isUserReport`, `userGroupId`, `showAsManager`, `showToEveryone`).
- `ProcessViewProfilePropertyDto`'dan: `showOnListingPage`, `subFieldsViewProfiles`, `deletableStatuses`,
  `cardViewProfile`, `childFieldsProcessViewProfileFieldDtos`.

**✏️ Yeniden adlandırılan**
- `processViewProfileFields` → **`processViewProfileProperty`** · `ProcessViewProfileFieldDto` → **`ProcessViewProfilePropertyDto`** · `fieldId` → **`propertyId`**

---

## 6. İş Kuralları (`../../service-settings/business-rule.md`)
**🔧 Konumlandırma:** İş kuralları = **frontend realtime katman** (motoru doğrudan etkilemez) — netleştirildi.

**➖ Çıkarıldı:** `FromEba` (değer kaynağı) — Eba kaldırıldı.

**✏️ Yeniden adlandırılan**
| Eski | Yeni |
|---|---|
| `SetViewForFields` | `setViewForProperties` |
| `AssignValueToField` | `assignValueToProperty` |
| `assignValueToPropertyField` | `assignValueToPropertyAttribute` |
| `FieldValue` / `FormValue` | `PropertyValue` |
| `Function` (değer kaynağı) | `httpRequest` |

**↔ Korundu:** `applyValidation`, `showMessage`, `fillDataSource`, `setStyle`, runtime tipleri (always/firstOpening/whenChanging), recursive koşullar.
**🗑️ Kaldırıldı (yeni):** `changeViewProfile` (v0.18) — çalışma-zamanı profil değiştirme iş-kuralı aksiyonu tasarımdan çıkarıldı; profil süreç adımına `processViewProfileId` ile bağlanır, koşullu görünürlük `setViewForProperties` ile yapılır.

---

## 7. Durumlar (`../../organization-settings/status.md`)
**✏️ Yeniden adlandırılan:** `statusType` → **`styleId`** (yanlış adlandırılmıştı; aslında Style'a FK).
**🔧 Renk:** `definition` metni + `icon` rengi Style'ın **`fontColor`**'ından gelir (`bgColor` = etiket arka planı).
**➕ DB anahtarları:** `id` (PK) + `organizationId` (havuz).
**↔ Korundu:** `code`, `definition`, `icon`; aksiyonla durum değişimi (`changeStatusId`).

---

## 8. Stiller (`../../organization-settings/style.md`) — YENİ KAVRAM
**➕ Eklendi:** **Dinamik Style yönetimi** — sistem stilleri (`organizationId=null`, read-only) + organizasyon stilleri (bg/font); **çapraz-kesen** (aksiyon ✓ · durum ✓ · **alan ✗** — form alanları Style **kullanmaz**). Referans **`styleId`** FK ile; `fontColor` = metin+ikon rengi.
**➖ Değişti:** Statik Bootstrap renk sınıfları (`actionType`) → **dinamik Style varlığı** (referansla seçim).

---

## 9. Çeviri & Organizasyon (YENİ) — `../../organization-settings/translation.md` · `../../organization-settings/organization.md`
**➕ Çeviri motoru** (yeni yapı)
- **`code`-bazlı** çeviri: model `id`·`code`·`organizationId`·**`languageCode`·`definition`** — **kayıt-başına-dil**
  (`tr`/`en`/`de` kolonları yok); `(organizationId, code, languageCode)` benzersiz.
- **İki katman:** ortak (Flovo, `organizationId=null`, salt-okunur) + organizasyon çevirileri (kendi kayıtlarını günceller).
- **Çözümleme:** `translationCode` yoksa (`null`) tabloya **gidilmez** → `definition`; `definition` = organizasyonun
  `defaultLang` metni → dil eşleşince yine **gidilmez**; farklıysa `translationCode`+**`languageCode`**+`organizationId`
  (override) → +`null` (ortak) → yoksa/boşsa **`definition`** fallback.

**➕ Çeviri anahtarı `translationCode` — iş kodu ≠ çeviri anahtarı** (23 model/alt-model)
- **Sorun:** Çeviri ad-uzayı **organizasyon geneli** (`(organizationId, code, languageCode)`) ve **varlık ayrımı yok**;
  modellerin `code`'u ise yalnız **model-içi** benzersiz (`(organizationId, code)`). İş kodu doğrudan anahtar olsaydı
  **Departman `"01"` ile Şirket `"01"` aynı çeviri satırına düşerdi** (departman adı şirket adının çevirisini gösterirdi).
- **Çözüm:** Her çevrilebilir modelde **ayrı, nullable `translationCode`** (`Model.translationCode → Translation.code`);
  `code` yalnız **iş/tanımlayıcı** rolünde kalır. **`null` = çeviri es geçilir** → `definition` (çeviri **opt-in**).
  Aynı anahtarı veren iki kayıt çeviriyi **bilinçli paylaşabilir**.
- **Emsal:** `PropertyItem` bunu zaten yapıyordu (`code` ≠ `value`); standart **tüm modellere** yayıldı ve isimler
  `translationCode`'a çekildi.
- **Snapshot'lar anahtarı da kopyalar:** `ProcessStepAction.translationCode` (Action'dan) ·
  `...QualificationValue.comboboxTranslationCode` (QualificationItem'dan).
- **Taşımayanlar:** `Style`·`User`·`Organization` (çevrilecek `definition` yok) · `Translation` (anahtarın kendisi).

**➕ Organizasyon (tenant) varlığı**
- Model (başlangıç): `id`·`code`·`name`·`defaultLang`·`logoUrl`·`idleTimeoutMinute`.
- `code` benzersiz + dış referans anahtarı; `idleTimeoutMinute` (0=disable); `defaultLang` sabit dil seti (`tr`/`en`/`de`).

**➕ Hiyerarşi & havuz (yeni)**
- **Organization → Solution → Service** hiyerarşisi netleşti (**Solution** ve **Service** ayrı model). `organizationId`
  **int** PK; dış referans `organizationCode` (string).
- **Action / Status / Style / Translation** = **organizasyon havuzu** (`organizationId`); o organizasyonun tüm
  servislerinde kullanılır (Service'e bağlı **değil**).

---

## 10. Organizasyon Ayarları (yapısal veri) — YENİ MODELLER (`../../models/organization-settings/`)
Eski uygulamanın **"Account Settings"** DTO'ları (`../current-flovo-bpm-engine/organizations/`) yeni **DB modellerine** dönüştürüldü.

**➕ Modellenen (13):** Company · Department · **Profession** (eski "Ünvan/Title") · User · UserGroup · AdditionalQualification ·
CostCenter · WorkerLevel · WorkingSchedule · VacationDay · CreditCard · ProcessTransfer · SchedulerJob.

**✏️ Dönüşüm kuralları**
- **Account → Organization:** `account*`→`organization*`; **`accountId` (string) → `organizationId` (int)** — her modelde.
- **Türkçe → İngilizce alan:** `kod`/`tanim`→`code`/`definition`; `departmanYoneticiUserId`→`managerUserId`; `unvanId`→`professionId`;
  string FK'ler → int; `selectedCompanyIds`→`companyIds` (List\<int\>).
- **Title → Profession** (model adı · FK'ler · enum değeri).
- UI-yardımcı koleksiyonlar (`accountCompanyDtos` vb.) DB modeline alınmadı; `id` PK + FK'ler eklendi; `User` org bağlantıları
  **nullable**, `UserExpenseLimit` **kaldırıldı** (aktif değil).

**🔧 Master-veri ortak alanları (yeni)**
- **`active` + `deleted`** (soft-delete) — eski `status`(bool) → **`active`**; ikisi de **not-null** (vars. `active=true`, `deleted=false`).
  BPM workflow motoru **`deleted=true` VEYA `active=false`** kayıtları **kullanmaz**; `deleted=true` frontend'de gizli/salt, `active=false` görünür+düzenlenebilir.
- **`(organizationId, code)` benzersiz** (`deleted=true` hariç) — **11 master model** (User dahil) + havuz Status/Action/Style. İstisna: Translation `(…, languageCode)`; Organization `code` global. _(→ `models/index.md` yapısal org-ayarları listesi.)_
- **User:** `userName` → **`email`** (giriş) + **`phone`**; benzersizlik `(organizationId, code/email/phone)` (aynı e-posta farklı org'larda olabilir); `UserExpenseLimit` kaldırıldı.
  **`email`/`phone` ikisi de nullable** ama **en az biri dolu** olmak zorunda (CHECK) — kullanıcı e-posta ile, telefon ile veya ikisiyle tanımlanabilir;
  null olanlar benzersizlik kontrolüne girmez. `profilePhoto`/`employmentStartDate` **nullable**. **Sosyal medya alanları** (`facebook`/`instagram`/`linkedin`/`twitter`) **kaldırıldı** — yeni uygulamada yok.

**🔐 Yetkilendirme (yeni)**
- Eski **kullanıcı bazında sayısal `User.authorizationLevel`** (dinamik ayarlanamıyordu) **kaldırıldı**.
- **Org-bazlı**: `Organization.adminUserIds` (**en az 1 aktif** admin; tüm yetkiler + yetki config'ini düzenleyen tek grup) + **4 grup alanı**
  (`impersonationUserGroupId` · `organizationSettingsUserGroupId` · `serviceSettingsUserGroupId` · `viewAllReportsUserGroupId`; her biri tek `UserGroup`).
  Detay → `../../organization-settings/permissions.md`.

**🔧 Ek Nitelik (AdditionalQualification) — yeniden yapılandırıldı**
- `RelationalSetting` → **`RelationalType`** (Users/Departments/Professions/CostCenters/WorkerLevels).
- **`QualificationValueType`** enum: `String` · `Double` · `DateTime` · **`Combobox`**.
- Değer alt modelleri: tek `value` → **typed sütunlar** (`stringValue`/`doubleValue`/`datetimeValue`) + combobox
  (`comboboxItemId` + kopya `comboboxTranslationCode`/`comboboxDefinition`).
- **QualificationItem** alt modeli (combobox seçenekleri) — `PropertyItem`'dan türetildi ama **`Property`'siz** (`additionalQualificationId`).

**➕ Pozisyon/Kadro modellendi:** `Position` (+ `Staff` alt modeli; 1 kadro ↔ 1 kullanıcı) → `models/organization-settings/position.md`.
**➖ Kapsam dışı (referans dokümanı):** para birimi, vergi oranları (ExpenseType/Currency/Tax) — modellenmedi.

**↔ BPM tüketimi:** User/UserGroup → onay merci/atama · WorkingSchedule+VacationDay → Timer/zaman aşımı ·
Department/Profession → yönetici atama tipleri · CostCenter/CreditCard → masraf.

---

## 11. İş Akışı / Runtime Modelleri (`../../models/processInstances/`) — YENİ KATMAN
Motorun **çalışma-zamanı** kayıtları (ayarlardan üretilen instance/execution verisi). 5 model; **tam isim eşlemesi** →
[`new-vs-current-names.md §15`](./new-vs-current-names.md).

**✏️ Eski modelden yeniden adlandırılan**
- `ServiceInstanceRequests` → **`ProcessStepInstance`** (adım çalıştırma kaydı): `RequestDate`→`executionDate` ·
  `responsaDate`→`actionTriggerDate` · `InstanceId`→`instanceId` · `ProxyApproverUserId`→`atDelegateUserId`;
  **çıkarılan** `Description`/`IsItSkipped`/`SentBack`/`IsItCanceled`/`UserId`; **eklenen** `processInstanceId`/`atUserId`/`atApiKeyId`/`processStepActionParameter`.
- `ServiceInstances` → **`Instance`** (doldurulmuş form / süreç örneği): `UserId`→`creatorUserId` · `ProcessStatusId`→`statusId`;
  **çıkarılan** `acountId`/`StateId`/`ParentInstanceId`/`isTest`/`ProcessStepId`; **eklenen** `createdDate`/`processInstanceId`.

**➕ Tamamen yeni (eski karşılığı yok)**
- **`ProcessInstance`** — bir servis sürecinin çalıştırma örneği (başlatan `createdByUserId` **veya** `createdByApiKeyId`;
  **`parentProcessInstanceId`** self-link ile alt süreç → ana süreç bağı).
- **`InstanceAwaitingUser`** — form üzerinde **atanan/aksiyon alabilecek** kullanıcı-grup kümesi; maliyet için doğrudan tutulur
  (aksiyon alabilecekleri `ProcessStepInstance` filtrelemeden bu tablodan tespit) ve adım geçişlerinde **sync** (eklenir/silinir).
- **`AssociatedInstance`** — formlar arası ilişki (property boyutuyla; `associatedPropertyId`, `associatedInstanceId`'nin formundaki alan).

**✅ Çözülen açık konu:** Webhook bir **aksiyon** olduğundan bağımsız alt süreçte bağlanacağı adım yoktu
(`ProcessStepInstance.processStepId` zorunlu). Çözüm: yeni **Alt Süreç Başlangıcı** süreç adımı (→
`../../service-settings/process-step.md` §3.20) — bağımsız alt sürecin **giriş düğümü**; webhook **veya** Süreç Adımı Tetikleme
ile tetiklenir, webhook aksiyonu bu adıma bağlı **`default`**'a dönüşür. Alt süreç ana süreçten **bağımsız, yeni bir `ProcessInstance`**
olarak çalışır; **`ProcessInstance.parentProcessInstanceId`** ile ana sürece bağlanır.

---

## 12. Genel Adlandırma Kuralı
> **Tüm isim değişikliklerinin** (model + alan) taranabilir tam listesi ayrı dosyada: [`new-vs-current-names.md`](./new-vs-current-names.md)
> (`eski > yeni` · `-- silinen` · `eklenen ++`).
- **field → property** (her yerde): `...FieldId` → `...PropertyId`, `fieldId`→`propertyId`, `FieldValue`/`FormValue`→`PropertyValue`.
- **Account → Organization**: `accountId`→`organizationId`, `accountUserGroup*`→`organizationUserGroup*`, `accountRestriction`→`organizationRestriction`.
- **function → HTTP Request** · **ModalList → `formList`** · **statusType → styleId** · **(aksiyon) actionType → styleId** + **(aksiyon) action → actionType** · **onAfterChange → saveAndRefreshOnAfterChange**.
- **Çeviri:** `tr`/`en`/`de` kolonları → **`languageCode` + `definition`** (kayıt-başına-dil). **Form List:** `addNewEnabled`→`activeStartActions`, `addFromExistingRecordsIsActive`→`addFromExistingStatusIds`, `selectedEnable`→`selectableVisible` (profil-bazlı).
- **Organizasyon ayarları:** **Title → Profession** · `RelationalSetting → RelationalType` · `account*`→`organization*` · `accountId`(string)→`organizationId`(int) · `kod`/`tanim`→`code`/`definition`.
- **Master-veri & yetki:** `status`(bool) → **`active`** (+ `deleted`) · `User.userName` → `email`/`phone` · `User.authorizationLevel` **kaldırıldı** (→ org-bazlı yetki).

---

## 13. Başarılı / Başarısız Değerlendirme (mevcut projeye göre)

### ✅ Başarılı (mevcuda göre net iyileşme)
- **Açık veri sözleşmesi:** `parameters`/`changeList`/`action` ile adımlar arası akış **örtük server-driven**'dan çıkıp okunur/öngörülebilir hale geldi.
- **İki-katman ayrımı** (form-mantığı ↔ akış-mantığı): iş kuralları frontend realtime'a çekilerek motor sadeleşti; sorumluluklar netleşti.
- **ActionDto şablon + Style varlığı:** tekrar eden aksiyon/renk tanımları tek yerden yönetilir; statik Bootstrap bağımlılığı kalktı.
- **İnce çekirdek + tipe-özel ayar:** ~60 alanlık şişman `PropertyDto` sadeleşti; performans + self-servis kolaylaştı.
- **Ölü ağırlığın atılması:** Eba entegrasyonu, `add-test-receipt`, iş-bazlı custom aksiyonlar, çift ondalık alanı (`precition`), `UserExpenseLimit` ve **kullanıcı sosyal medya alanları** (`facebook`/`instagram`/`linkedin`/`twitter`) temizlendi.
- **i18n motoru:** `code`↔`definition` ayrımı + `definition`=varsayılan dil kısa-devresi hem tutarlı hem performanslı (çoğu kullanıcı sorgusuz).
- **Aksiyon-kodu + `targetProcessStepId` iki katmanı:** "hangi aksiyon" ile "hangi adım" ayrımı net formalize edildi.
- **Kararlar netleşti:** Action→ProcessStepAction **bağımsız kopya** (FK yok); Form List ayarları **profil-bazlı override** (B2); Translation **kayıt-başına-dil**; kapsam kararı (havuz ↔ servis) çözüldü.
- **Organizasyon altyapısı modellendi:** eski Account Settings (kullanıcı/departman/ünvan/şirket/takvim…) **13 DB modeline** dönüştürüldü (account→organization, **Title→Profession**, typed+combobox ek nitelik değerleri).
- **Yetki modeli modernize edildi:** sabit **sayısal `authorizationLevel`** → **dinamik org-bazlı** (admin + kullanıcı grubu bazlı yetkiler); ayrıca master-verilerde `active`/`deleted` (soft-delete) ve `(organizationId, code)` benzersizlik standardı.
- **Runtime/instance katmanı modellendi:** eski dağınık `ServiceInstances`/`ServiceInstanceRequests` → **`processInstances/` 5 model** (ProcessInstance · ProcessStepInstance · Instance · InstanceAwaitingUser · AssociatedInstance); aksiyon-alabilenler ayrı tablo (maliyet), formlar-arası ilişki netleşti;
  bağımsız alt süreçler ayrı `ProcessInstance` (**`parentProcessInstanceId`** ile ana sürece bağlı).

### ⚠️ Başarısız / riskli / henüz eksik
- **Form List alt-servis görünümü:** davranış ayarları artık **profil-bazlı override** (B2) ile yönetiliyor; ancak alt-servisin **görüntülenecek alanları / kart görünümü** (`subFieldsViewProfiles`/`cardViewProfile` karşılığı) hâlâ açık.
- **`definition` = varsayılan dil kırılganlığı:** Bir organizasyon `defaultLang`'ini sonradan değiştirirse eski `definition`'lar yanlış dilde kalır; bu bir **veri-giriş kuralı** olarak garanti edilmeli (çeviri motorunun zayıf noktası).
- **Motor iç mekaniği hâlâ yazılmadı:** `flovo-bpm-engine.md`'de yürütme durumu/kalıcılık, bekleme-noktası serileştirme, hata katmanları, döngü/join **placeholder**; mevcut projede de netti değildi — devralınan boşluk.
- **`changeList` öğe yapısı belirsiz** (alan id + değer + tip?) — açık soru.
- **İsim çakışması (çözüldü, v0.7):** `actionType` (ActionDto tür) ↔ BusinessRule etki tipi — karışmayı önlemek için BusinessRule tarafı **`businessRuleActionType`** olarak yeniden adlandırıldı.
- **İki-katman tekrarı:** değer atama & karşılaştırma hem adımda hem iş kuralında var — sınır netleşmeli.
- **`ProcessStep`/`BusinessRule` denormalize `organizationId`:** asıl kapsayıcı `serviceId` iken kiracı için ayrıca `organizationId` tutulması — gözden geçirilecek.

---

## 14. Açık / Karara Bağlı Konular
> **Açık sorular tek yerde:** Bu karşılaştırmadan doğan açık kararlar/sorular, tutarsızlığı önlemek için **yalnız** merkezi
> [`todo.md`](../../todo.md) dosyasında toplanır (önceliklendirilmiş tüm-doküman listesi; ilgili maddeler kaynak doküman
> atıflarıyla bulunur). Bu bölüm artık ayrı bir açık-soru listesi tutmaz.

---

*Güncelleme: 2026-07-10 · Tasarım dokümanları ile `../current-flovo-bpm-engine/` karşılaştırılarak derlendi (Alt Süreç Başlangıcı adımı eklendi; v0.7 — runtime & iş-kuralı model adları güncellendi: WorkFlow→ProcessInstance · ProcessStepExecution→ProcessStepInstance · Form→Instance · RelatedForm→RelatedInstance · FormAwaitingUser→InstanceAwaitingUser · WorkRule→BusinessRule). · 2026-07-16 (v0.12 — adım tipe-özel ayarlar JSONB `settings` + adım-tipi enum'ları + alan yeniden adlandırmaları: resource→endpoint · method→HttpMethod · stableUserId→fixedUserId · WorkStyle→TimerCalculationType · Function param→DynamicParameter) · 2026-07-17 (v0.13 — ayrı çeviri anahtarı `translationCode`: §0/§9/§10) · 2026-07-24 (v0.15 — Alt Süreç Bitişi adımı → 21 adım/ProcessStepType; `controlTypeId`→`propertyType`; master model sayısı 11) · 2026-07-24 (v0.17 — `RelatedInstance`→`AssociatedInstance` model + `relatedInstanceId`→`associatedInstanceId` · `relatedPropertyId`→`associatedPropertyId`) · 2026-07-27 (v0.18 — iş-kuralı aksiyonu `changeViewProfile` **kaldırıldı** (§6); combobox'a `isAssociatedCombobox`/`associatedServiceId` eklendi; Değer Atama alanı `valueType`→**`valueAssignType`** (§9); Action'dan `defaultAction` (bool) **kaldırıldı**; `assignValueToPropertyAttribute` adı **teyit** edildi). · 2026-07-28 (v0.20 — **Üst Form Kullanıcı** (`parentInstanceUser`) insan-görev adımı eklendi: alt-servisi üst formun atananlarına/`code`-eşleşen profiline anlık bağlar → **21 → 22 adım**). · 2026-07-28 (v0.21 — `imageAreaSelector` alan tipi **kaldırıldı** (19→18); **grup onayı özelliği kaldırıldı** — `groupApproval`/`UserGroup.groupApprovalRequired`/`UserGroupApprovedUser` silindi, runtime 6→5 model).*
