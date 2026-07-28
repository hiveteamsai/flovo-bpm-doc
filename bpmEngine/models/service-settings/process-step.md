# Model — ProcessStep (süreç adımı)

> **Durum:** 🟡 TASLAK (gözden geçirilecek)
> **Amaç:** İş akışındaki bir **düğüm/kutu**. Adımlar aksiyonlarla bağlanarak süreci oluşturur.
> **Davranış/kullanım + adım kataloğu (22 tip):** → `../../service-settings/process-step.md`
> **Tipe-özel ayar modellerinin (§3) ham kaynağı + taşıma kararları:** → [`../../research/current-flovo-bpm-engine/step-type-settings-and-enums.md`](../../research/current-flovo-bpm-engine/step-type-settings-and-enums.md)

## 1. Ortak alanlar (her adımda)
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Adım ID'si. |
| `organizationId` | int | FK → Organization.id | Kiracı. |
| `serviceId` | int | FK → Service | Bağlı servis. |
| `code` | string | benzersiz | Adımın kodu. |
| `stepType` | ProcessStepType | — | **Adım tipi ayrımlayıcısı** — `settings`'in nasıl yorumlanacağını belirler (→ [`../enums/process-step-type.md`](../enums/process-step-type.md)). |
| `settings` | jsonb | — | **Tipe-özel ayarlar** (`ProcessStep…Settings`). Şekli **`stepType`**'a göre değişir; şemalar **§3**'te. `ProcessStep` satırında **JSONB** kolon olarak tutulur (→ §2). |
| `definition` | string | — | Adımın adı/tanımı. |
| `translationCode` | string? | çeviri anahtarı | **Çeviri eşleşme anahtarı** (→ [`../organization-settings/translation.md`](../organization-settings/translation.md) `code`). `null` = çeviri **es geçilir**, doğrudan `definition` kullanılır. |
| `icon` | string | — | Adım ikonu. |
| `order` | int | — | Sıralama (sürükle-bırak). |
| `environmentRestriction` | string | — | Ortam kısıtı. _(Alan formatı açık → [`../../todo.md`](../../todo.md) "Ortam modeli".)_ |
| `hideInHistory` | bool | — | Süreç geçmişinde gizle. |
| `skipIfPreApproved` | bool | — | Önceden onaylanmışsa adımı atla. |
| `skipIfUserProcessStarter` | bool | — | Başlatan kullanıcıysa adımı atla. |
| `skipWithThisProcessStepActionId` | int | FK → ProcessStepAction | Atlamada **otomatik tetiklenecek aksiyon** — adıma bağlı **`ProcessStepAction`**'ı işaret eder (Action **şablonuna** değil; kopya modeliyle uyumlu). `skipIfPreApproved` ile birlikte kullanılır (davranış → `../../service-settings/process-step.md` §2). |

## 2. Tipe-özel ayarların depolanması — `settings` (JSONB)

**Karar (🟢):** Tipe-özel ayarlar, `ProcessStep` tablosunda **tek bir `settings` JSONB kolonunda** (gömülü) tutulur; adım
tipi başına **ayrı alt-tablo/model açılmaz**. İçeriğin şekli **`stepType`** (ProcessStepType) ayrımlayıcısına göre yorumlanır.
Aşağıdaki §3 modelleri, her `stepType` için bu JSONB'nin **şemasıdır**.

**Neden JSONB (özet):**
- **Config/tasarım verisi** — düşük hacim (servis başına ~onlarca adım); ayar **değerine göre sorgulanmaz** (adım **id ile** yüklenir).
- **22 tipin heterojen şeması** + **genişletilebilir** katalog → wide/sparse tablo veya tip-başına tablo her yeni tipte şema göçü ister; JSONB'de **göç yok**.
- İç içe/tekrarlı yapılar (`headers`, `conditions`, `recipients`…) doğal olarak **doküman**.
- Yığın zaten **PostgreSQL/JSONB** (→ [`../../tech-stack/postgresql.md`](../../tech-stack/postgresql.md)); yeni teknoloji gerekmez.

**Bütünlük & kurallar:**
- `settings` içindeki **referans id'ler** (`targetPropertyId` · `propertyId` · `selectedTimerProcessStepId` · `organizationUserGroupId` …)
  DB FK'siyle değil, **uygulama katmanında** doğrulanır (kaydetme anında + **tip başına JSON Schema**). Referanslanan bir varlık
  silinmeden önce "bunu kullanan adım var mı?" denetimi uygulama tarafındadır.
- Sürecin **topolojisi** (hangi adıma gidilir) `settings`'te **değil**, ilişkisel **`ProcessStepAction.targetProcessStepId`**'dedir
  → graf bütünlüğü JSONB'den **bağımsız**; JSONB yalnız her düğümün **yaprak konfigürasyonunu** taşır.
- **Ortak alanlar** (§1) tipli kolon kalır; yalnız tipe-özel kısım JSONB'dedir. `settings` düşük hacimli ve **bütün olarak**
  okunduğundan ayrı 1-1 tabloya gerek yoktur (aynı satırda kolon).

**`stepType` → ayar modeli (§3) haritası:**

| `stepType` | Ayar modeli | Bölüm |
|---|---|---|
| `httpRequest` | `ProcessStepHttpRequestSettings` | §3.1 |
| `flovoAi` | `ProcessStepFlovoAiSettings` | §3.2 |
| `valueAssignment` | `ProcessStepValueAssignmentSettings` | §3.3 |
| `comparison` | `ProcessStepComparisonSettings` | §3.4 |
| `switch` | `ProcessStepSwitchSettings` | §3.5 |
| `notification` | `ProcessStepNotificationSettings` | §3.6 |
| `timer` · `timerStart` · `timerEnd` | `ProcessStepTimerSettings` | §3.7 |
| `customIdCreator` | `ProcessStepCustomIdCreatorSettings` | §3.8 |
| `instanceCreator` | `ProcessStepInstanceCreatorSettings` | §3.9 |
| `user` | `ProcessStepUserSettings` | §3.10 |
| `userGroup` | `ProcessStepUserGroupSettings` | §3.11 |
| `parentInstanceUser` | `ProcessStepParentInstanceUserSettings` | §3.17 |
| `processEnd` | `ProcessStepProcessEndSettings` | §3.12 |
| `processing` | `ProcessStepProcessingSettings` | §3.13 |
| `processStart` | `ProcessStepProcessStartSettings` | §3.14 |
| `instanceDeleter` | `ProcessStepInstanceDeleterSettings` | §3.15 |
| `triggerProcessStep` · `formRedirect` · `subProcessStart` · `subProcessEnd` | (ayarsız / sonra detaylanacak) | §3.16 |

## 3. Adım-tipi ayar modelleri (`settings` şemaları)
> Her tablo, ilgili `stepType` için `settings` JSONB'sinin **alan-düzeyi şemasıdır**. Değer-kaynağı olan alanlar
> **ValueAssignType** ailesini kullanır (sabit / hesaplama / form property). Aksiyon-yönlendirme (true/false/default/case)
> `settings`'te değil, `ProcessStepAction` tarafındadır.

### 3.1 HTTP Request — `ProcessStepHttpRequestSettings` (`stepType = httpRequest`)
Dış endpoint'e HTTP isteği atan otomatik adım (davranış → `../../service-settings/process-step.md §3.2`).

| Alan | Tip | Açıklama |
|---|---|---|
| `endpoint` | string | İstek atılacak URL. |
| `method` | HttpMethod | HTTP metodu (→ [`../enums/http-method.md`](../enums/http-method.md): `get`/`post`/`put`/`delete`). |
| `templateParameters` | DynamicParameter[] | URL şablon/path parametreleri. |
| `queryParameters` | DynamicParameter[] | Query string parametreleri. |
| `headers` | DynamicParameter[] | İstek başlıkları. |
| `body` | DynamicParameter[] | Gövde parametreleri. |
| `async` | bool | `true` ise sonuç beklenmez; doğrudan `default` aksiyonla ilerlenir. |

**`DynamicParameter` (alt-model):**
| Alan | Tip | Açıklama |
|---|---|---|
| `name` | string | Parametre adı. |
| `value` | ValueAssignType-değeri | Değer kaynağı: `fixedValue` (sabit) / `fromCalculation` (hesaplama) / `propertyValue` (form property) + ilgili değer (→ [`../enums/value-assign-type.md`](../enums/value-assign-type.md)). |

> Not: Çalışma-zamanında hesaplanıp gönderilecek değer için ayrı bir yardımcı alan (`parameterValue`) kullanılır; bu **ayar**
> değildir (kaydedilen `settings`'e girmez).

### 3.2 Flovo AI — `ProcessStepFlovoAiSettings` (`stepType = flovoAi`)
Seçili Flovo AI'ı çalıştırıp parametre üreten otomatik adım (davranış → `§3.3`).

| Alan | Tip | Açıklama |
|---|---|---|
| `selectedAi` | string/enum | Kullanılacak AI (ör. Masraf · Fatura · Kredi Kartı Ekstresi). _(Kanonik set → netleşecek.)_ |
| `aiSettings` | object | Seçilen AI'a **özel** ayarlar (AI'ya göre değişen serbest yapı). |
| `fileSourceType` | enum (`thumbnail`/`fileProperty`) | AI'ın işleyeceği dosyanın kaynağı. _(Enum adayı — netleşince ayrı enum olabilir.)_ |
| `fileSourcePropertyId` | int? | `fileProperty` ise dosyayı taşıyan file property. |

### 3.3 Değer Atama — `ProcessStepValueAssignmentSettings` (`stepType = valueAssignment`)
Bir property'ye veya alt-servise sabit/hesaplanan değer atar (davranış → `§3.4`).

| Alan | Tip | Açıklama |
|---|---|---|
| `valueAssignType` | ValueAssignType | Değer kaynağı — bu adımda geçerli **alt-küme**: `fixedValue`/`propertyValue`/`fromCalculation` (→ [`../enums/value-assign-type.md`](../enums/value-assign-type.md); `fromDataSet`/`search`/`httpRequest` yalnız iş kuralı `assignValueToProperty` içindir, JSON Schema ile kısıtlanır). |
| `fixedValue` | string | Sabit değer (`valueAssignType = fixedValue`). |
| `expression` | string | Değeri üreten ifade (`valueAssignType = fromCalculation`). |
| `useDisplay` | bool | Görüntü (display) değerini kullan. |
| `targetPropertyId` | int | Hedef property (değerin yazılacağı alan). |
| `propertyId` | int | Kaynak property (`valueAssignType = propertyValue`). |
| `useAssociatedService` | bool | Atamayı **alt-servis** kayıtlarına yap. |
| `associatedServiceId` | int? | Hedef alt-servis (`useAssociatedService = true`). |
| `targetInstancesPropertyId` | int? | Hedef alt-servis kayıt(lar) property'si. |

### 3.4 Karşılaştırma — `ProcessStepComparisonSettings` (`stepType = comparison`)
Koşullara göre `true`/`false` iki dallı yönlendirme (davranış → `§3.13`).

| Alan | Tip | Açıklama |
|---|---|---|
| `conditions` | ComparisonCondition[] | Koşul listesi (iç içe gruplanabilir). |
| `conditionType` | BusinessRuleConditionType | Koşulların birleşimi (→ [`../enums/business-rule-condition-type.md`](../enums/business-rule-condition-type.md): `and`/`or`). |

**`ComparisonCondition` (alt-model, recursive):**
| Alan | Tip | Açıklama |
|---|---|---|
| `referenceValue` | değer | Karşılaştırılacak referans (alan/sabit/ifade). |
| `criterionType` | CriterionType | Operatör (→ [`../enums/criterion-type.md`](../enums/criterion-type.md): `equals`/`greaterThan`…). |
| `valueToCompare` | değer | Karşılaştırma değeri. |
| `children` | ComparisonCondition[] | İç içe koşul grubu (gruplama). |

> `true`/`false` dalları `ProcessStepAction` (aynı kodlu aksiyonlar) ile yönlendirilir; `settings`'te tutulmaz.

### 3.5 Switch — `ProcessStepSwitchSettings` (`stepType = switch`)
Seçili alanın değerine göre dallanma (davranış → `§3.14`).

| Alan | Tip | Açıklama |
|---|---|---|
| `propertyId` | int | Değerine bakılacak alan. |

> **Eşleşme doğrudan aksiyon koduyla:** Alanın **değeri ne ise, o `code`'a sahip** `ProcessStepAction` tetiklenir; ayrı
> `cases`/eşleme listesi tutulmaz. Eşleşme yoksa **`default`** kodlu aksiyon çalışır (default zorunlu).

### 3.6 Bildirim — `ProcessStepNotificationSettings` (`stepType = notification`)
Mail/Push/Toast bildirim gönderir (davranış → `§3.6`).

| Alan | Tip | Açıklama |
|---|---|---|
| `messages` | SendNotificationMessages | Kanal + dinamik dil listesi + parametreler. |
| `recipients` | SendNotificationUsers[] | Bir veya birden fazla alıcı bloğu. |

**`SendNotificationMessages` (alt-model):**
| Alan | Tip | Açıklama |
|---|---|---|
| `channels` | NotificationChannel[] | Gönderilecek kanallar (→ [`../enums/notification-channel.md`](../enums/notification-channel.md): `mail`/`push`/`toast`). |
| `items` | NotificationMessageItem[] | Dil-başına başlık/mesaj (dinamik liste). |
| `parameters` | DynamicParameter[] | (Push/Toast) çalışma-zamanı parametreleri (`DynamicParameter` → §3.1); UI'da gösterilmez. Mail'de yok. |

**`NotificationMessageItem` (alt-model):** `languageCode` (string) · `title` (string) · `text` (string).

**`SendNotificationUsers` (alt-model):**
| Alan | Tip | Açıklama |
|---|---|---|
| `recipientType` | NotificationRecipientType | `user` / `userGroup` / `takeUsersWhoTookActionBefore` (→ [`../enums/notification-recipient-type.md`](../enums/notification-recipient-type.md)). |
| `userSelection` | NotificationUserSelection? | `recipientType = user` ise. |
| `userGroupIds` | int[]? | `recipientType = userGroup` ise. |
| `addToCc` | bool | Alıcıyı CC'ye ekle. |

**`NotificationUserSelection` (alt-model):**
| Alan | Tip | Açıklama |
|---|---|---|
| `userType` | NotificationUserType | `processStarter`/`fixedUser`/`variableUsers`/`formProperty` (→ [`../enums/notification-user-type.md`](../enums/notification-user-type.md)). |
| `fixedUserIds` | int[]? | `fixedUser` ise. |
| `variableUserProcessStepIds` | int[]? | `variableUsers` ise. |
| `propertyId` | int? | `formProperty` ise. |

### 3.7 Timer ailesi — `ProcessStepTimerSettings` (`stepType = timer` · `timerStart` · `timerEnd`)
Zamanlayıcı; ayrıca Kullanıcı/Kullanıcı Grubu adımlarının **timeout** ayarında da aynı yapı gömülü kullanılır (davranış → `§3.7`).

| Alan | Tip | Açıklama |
|---|---|---|
| `timeoutActive` | bool | Zamanlayıcı/timeout aktif mi. |
| `workStyle` | TimerCalculationType | Süre hesap stili (→ [`../enums/timer-calculation-type.md`](../enums/timer-calculation-type.md): `workCalendar`/`normalCalendar`/`fixedDateTime`). |
| `workCalendarSchedule` | TimerWorkSchedule? | `workCalendar` bloğu. |
| `normalCalendarSchedule` | TimerNormalSchedule? | `normalCalendar` bloğu. |
| `fixedDateTimeSchedule` | TimerFixedSchedule? | `fixedDateTime` bloğu. |
| `timeoutNotificationActive` | bool | Süre dolunca bildirim gönderilsin mi. |
| `timeoutNotification` | SendNotificationMessages? | Gönderilecek bildirim (§3.6 mesaj modeli). |
| `selectedTimerProcessStepId` | int? | **Timer Start/End** için: başlatılacak/sonlandırılacak Timer adımı. |

**Alt-modeller:**
- **`TimerWorkSchedule`:** `value` (string) — çalışma takvimine göre süre.
- **`TimerNormalSchedule`:** `day` (string) · `workTimeSelection` (WorkTimeSelection → [`../enums/work-time-selection.md`](../enums/work-time-selection.md)) · `postponing` (bool) · `timeAdjustmentOption` (TimeAdjustmentOption → [`../enums/time-adjustment-option.md`](../enums/time-adjustment-option.md)) · `postponingHour` (string).
- **`TimerFixedSchedule`:** `dateTime` (string) · `postponing` (bool) · `timeAdjustmentOption` (TimeAdjustmentOption) · `postponingHour` (string).

### 3.8 Custom ID Creator — `ProcessStepCustomIdCreatorSettings` (`stepType = customIdCreator`)
Özel formatlı benzersiz ID üretip bir property'ye yazar (davranış → `§3.11`).

| Alan | Tip | Açıklama |
|---|---|---|
| `customId` | string | ID format şablonu (ön ek + sıra no + tarih…). |
| `targetPropertyId` | int | Üretilen ID'nin yazılacağı property. |
| `createWithBarcode` | bool | Barkod ile oluştur. |
| `targetFilePropertyId` | int? | Barkod görselinin yazılacağı file property. |

### 3.9 Instance Creator — `ProcessStepInstanceCreatorSettings` (`stepType = instanceCreator`)
Yeni form/instance üretir; init değerler aksiyondan gelen `parameters` ile eşlenir (davranış → `§3.12`).

| Alan | Tip | Açıklama |
|---|---|---|
| `targetServiceId` | int | Oluşturulacak form/servis. |
| `initValues` | InstanceInitValue[] | Başlangıç değer eşlemeleri. |
| `thumbnailParameterName` | string? | Thumbnail url'sini taşıyan parametre. |

**`InstanceInitValue` (alt-model):** `targetPropertyId` (int) · `parameterName` (string — kaynak `parameters` anahtarı).
> _(Detay sonra genişletilecek → `../../todo.md`.)_

### 3.10 Kullanıcı — `ProcessStepUserSettings` (`stepType = user`)
Tek kullanıcının onayına giden human-task adım (davranış → `§3.15`). _(Kaynak DTO: `ProcessStepTypeUser`.)_

| Alan | Tip | Açıklama |
|---|---|---|
| `userType` | ProcessStepUserType | Kullanıcı belirleme yöntemi (→ [`../enums/process-step-user-type.md`](../enums/process-step-user-type.md)). |
| `fixedUserId` | int? | `fixedUser` ise sabit kullanıcı. |
| `userAdministratorSourceProcessStepId` | int? | `usersManager` ise: bu adımda **son onay veren**in yöneticisi aksiyon sahibi olur. |
| `departmentManagerDepartmentId` | int? | `departmentManager` ise hedef departman. |
| `variableUserPropertyId` | int? | `variableUser` ise kullanıcıyı taşıyan form property. |
| `processViewProfileId` | int | Aksiyonu alacak kullanıcının göreceği görüntüleme profili. |
| `sendNotificationOnStep` | SendNotificationMessages? | Adıma girildiğinde bildirim kısayolu. |
| `timeout` | ProcessStepTimerSettings? | Adıma girildiğinde otomatik timeout (§3.7 yapısı). |

### 3.11 Kullanıcı Grubu — `ProcessStepUserGroupSettings` (`stepType = userGroup`)
Birden fazla kullanıcıya iletilen, biri/hepsi onaylayan human-task adım (davranış → `§3.16`). _(Kaynak DTO: `ProcessStepTypeUserGroup`.)_

| Alan | Tip | Açıklama |
|---|---|---|
| `userGroupType` | ProcessStepUserGroupType | Grup belirleme yöntemi (→ [`../enums/process-step-user-group-type.md`](../enums/process-step-user-group-type.md)). |
| `organizationUserGroupId` | int? | `fixedUserGroup` ise sabit grup. |
| `dynamicUserListPropertyId` | int? | `dynamicUserList`/`dynamicUserGroup` ise listeyi taşıyan form property. |
| `groupApproval` | bool | `true`: aksiyon alabilen **tüm** kullanıcılar onaylayınca ilerler; `false`: **bir** kişi yeter. |
| `processViewProfileId` | int | Onaya gidecek kullanıcıların göreceği görüntüleme profili. |
| `sendNotificationOnStep` | SendNotificationMessages? | Adıma girildiğinde bildirim kısayolu. |
| `timeout` | ProcessStepTimerSettings? | Adıma girildiğinde otomatik timeout. |

### 3.12 Süreç Bitişi — `ProcessStepProcessEndSettings` (`stepType = processEnd`)
Sürecin son adımı (davranış → `§3.17`).

| Alan | Tip | Açıklama |
|---|---|---|
| `processViewProfileId` | int | Bitişte görüntüleme profili. |
| `organizationUserGroupIds` | int[] | Bitiş sonrası erişebilecek gruplar. |

### 3.13 Processing — `ProcessStepProcessingSettings` (`stepType = processing`)
Forma döner ama beklemez; `default` ile otomatik ilerler (davranış → `§3.18`).

| Alan | Tip | Açıklama |
|---|---|---|
| `showLoading` | bool | `true` ise form detayına giriş/değer görüntüleme engellenir (kullanıcı "yükleniyor" görür). |

### 3.14 Süreç Başlangıcı — `ProcessStepProcessStartSettings` (`stepType = processStart`)
Ana sürecin giriş düğümü; **kimlerin süreci başlatabileceğini** kısıtlar (davranış → `§3.1`).

| Alan | Tip | Açıklama |
|---|---|---|
| `userGroupId` | int? | Süreci başlatabilecek **kullanıcı grubu** (FK → UserGroup). **Null** → **herkes** başlangıç aksiyonlarını görüntüleyebilir ve süreci başlatabilir; **dolu** → **yalnız o gruptaki** kişiler başlatabilir. |

### 3.15 Instance Deleter — `ProcessStepInstanceDeleterSettings` (`stepType = instanceDeleter`)
Formu (ve seçime göre ilişkili formları) siler (davranış → `§3.10`).

| Alan | Tip | Açıklama |
|---|---|---|
| `deleteMode` | InstanceDeleteMode | Silme davranışı (→ [`../enums/instance-delete-mode.md`](../enums/instance-delete-mode.md)). |

**`InstanceDeleteMode` seçenekleri:**
- **`withRelated`** — *formu ve ilişkili formları sil:* sürecin instance'ı **ve** ilişkili instance'lar `deleted = true` yapılır.
- **`unlinkRelated`** — *formu sil, ilişkili formların ilişkisini kaldır:* sürecin instance'ı `deleted = true` yapılır;
  `AssociatedInstance` kayıtları **silinir** (ilişki kaldırılır); **ilişkili instance'ların `deleted` durumuna dokunulmaz**.

### 3.16 Ayarsız / sonra detaylanacak adımlar
| `stepType` | Durum |
|---|---|
| `triggerProcessStep` | Tetiklenecek alt-servis/adım seçimi; detay **sonra** → `../../todo.md`. |
| `formRedirect` | Karşılaştırma + açılacak var-olan form; detay **sonra**. |
| `subProcessStart` | **Ayara ihtiyaç yok** — ayrı özelliği yok; tetikleme kaynağı webhook / iç tetikleme (davranış → `§3.20`). |
| `subProcessEnd` | **Ayara ihtiyaç yok** — alt sürecin çıkış düğümü; kol burada sonlanır (davranış → `§3.21`; Süreç Bitişi'nin aksine bitiş-sonrası erişim ayarı yoktur). |

### 3.17 Üst Form Kullanıcı — `ProcessStepParentInstanceUserSettings` (`stepType = parentInstanceUser`)
Aksiyon-onayına giden human-task adım; **atananları ve görüntüleme profilini üst formdan (parent instance) devralır**
(davranış → `../../service-settings/process-step.md §3.22`).

| Alan | Tip | Açıklama |
|---|---|---|
| `parentServiceId` | int | **Üst formun servisi** — ilişkiyi kuran alanın bulunduğu servis. |
| `associatedPropertyId` | int | Üst formdaki **ilişki alanı** — yalnız `AssociatedInstance` bağlantısı kuran alanlar (**Form List** veya `isAssociatedCombobox` **Combobox**). **Bu servisi hedefleyen** alanlarla sınırlıdır (Form List `childServiceId` = bu servis / Combobox `associatedServiceId` = bu servis). |

> **Bu adımda `processViewProfileId` ve aksiyon-bekleyen (atama) alanı YOKTUR** — ikisi de üst formdan çözülür:
> görüntüleme profili **`code` eşleşmesiyle** (aynı kodlu profil yoksa alt-servisin `isDefault` profili), atananlar ise
> üst formun **güncel `InstanceAwaitingUser`** kümesinden (öneri: **okuma-zamanı** çözümü — kopyalama-vs-anlık kararı →
> `../../todo.md`). Kenar durumlar (üst form bulunamaz / otomatik adımda / çok eşleşme / Süreç Bitişi) → `../../todo.md`.

## İlişkiler
- **N – 1** → `Organization` (`organizationId`), `Service` (`serviceId`).
- **1 – N** ← `ProcessStepAction` (`processStepId`); ayrıca `ProcessStepAction.targetProcessStepId` → bu model (graf topolojisi).
- `settings` içindeki referans id'ler (`propertyId`, `organizationUserGroupId`, `selectedTimerProcessStepId` …) **mantıksal**
  referanstır; DB FK'si yoktur, uygulama katmanında doğrulanır (§2).

## Notlar / açık noktalar
- **Depolama kararı — ÇÖZÜLDÜ (JSONB):** tipe-özel ayarlar `ProcessStep.settings` JSONB kolonunda gömülü tutulur; ayrı
  alt-tablo/model açılmaz (§2). Tip başına şema §3'te; doğrulama uygulama katmanında (tip başına JSON Schema).
- `default action` kavramı; Timer yaşam döngüsü; Süreç Bitişi re-open; human-task ailesi ortak modeli; adım seti
  genişletilebilirliği; `instanceDeleter`/`triggerProcessStep`/`formRedirect`/`subProcessStart` ayar detayları → `../../todo.md`.
- `environmentRestriction` alan formatı (enum/string) "Ortam modeli" ile netleşecek → `../../todo.md`.

*Oluşturma: 2026-07-02. Güncelleme: 2026-07-16 — `settings` JSONB kararı + §3 tip-tip ayar modelleri.*
