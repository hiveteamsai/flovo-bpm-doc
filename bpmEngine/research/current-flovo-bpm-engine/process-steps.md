# Süreç Adımları (Process Steps) Dokümantasyonu

## Genel Bakış

Süreç adımları, Pratico uygulamasında bir iş akışının (workflow) tanımlanmasını ve yönetilmesini sağlayan temel yapıdır. Her servis (form) için bağımsız bir süreç akışı tanımlanabilir ve bu akış, adımlardan (step) ve aksiyonlardan (action) oluşur.

Süreç adımları `lib/Models/Settings/FlvSettings/ProcessStep/` dizininde model olarak, `lib/Pages/Settings/FlvSettings/ProcessStep/` dizininde ise UI bileşenleri olarak yer almaktadır.

---

## Süreç Adımı Tipleri (ProcessSettingStepType)

Uygulamada tanımlanabilen süreç adımı tipleri şunlardır:

| Index | Enum Değeri | Açıklama |
|-------|-------------|----------|
| 0 | `surecBaslangici` | Süreç Başlangıcı - Akışın başlangıç noktası |
| 1 | `kullanici` | Kullanıcı - Tek bir kullanıcıya atanacak onay adımı |
| 2 | `kullaniciGrubu` | Kullanıcı Grubu - Bir kullanıcı grubuna atanacak onay adımı |
| 3 | `atama` | Atama - Görev ataması yapılan adım |
| 4 | `function` | Function - Harici API çağrısı yapan adım |
| 5 | `surecBitisi` | Süreç Bitişi - Akışın bitiş noktası |
| 6 | `ebaIntegratedFlovoApp` | Eba Entegre - Eba ile entegre FBA platformu adımı |
| 7 | `compare` | Karşılaştırma - Koşula bağlı dallanma yapan adım |
| 8 | `notification` | Bildirim - Bildirim gönderen adım |
| 9 | `timerStart` | Timer Start - Zamanlayıcıyı başlatan adım |
| 10 | `timerEnd` | Timer End - Zamanlayıcıyı sonlandıran adım |
| 11 | `timer` | Timer - Zamanlayıcı tanımı yapılan adım |
| 12 | `stepCancellation` | Adım İptali - Önceki adımları iptal eden adım |
| 13 | `customIdCreator` | Custom Id Creator - Özel numara üreten adım |
| 14 | `valueAssignment` | Değer Atama - Form alanlarına değer atayan adım |

---

## Süreç Adımı Temel Yapısı (ProcessStepDto)

Her süreç adımı aşağıdaki ortak özelliklere sahiptir:

### Zorunlu Alanlar

| Alan | Tip | Açıklama |
|------|-----|----------|
| `code` | String | Adımın benzersiz kodu |
| `definition` | String | Adımın tanımı/adı |
| `environmentRestriction` | String | Ortam kısıtlaması (hangi ortamda çalışacağı) |

### Opsiyonel Alanlar

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Veritabanı ID'si |
| `accountId` | String | Hesap ID'si |
| `serviceId` | int | Bağlı olduğu servis ID'si |
| `icon` | String | Adımın ikonu (FontAwesome kodu) |
| `order` | int | Sıralama numarası (sürükle-bırak ile değiştirilebilir) |
| `hideInHistory` | bool | Süreç geçmişinde gizle |
| `skipIfPreApproved` | bool | Önceden onaylanmışsa adımı atla |
| `skipIfUserProcessStarter` | bool | Kullanıcı süreç başlatıcısıysa adımı atla |
| `skipWithThisActionId` | int | Bu aksiyon ile atlama yapılacak aksiyon ID'si |
| `selectModalItemDeactive` | bool | Modal seçim öğesini devre dışı bırak |
| `canSelectExpenses` | bool | Masraf seçimi yapılabilir mi |
| `useRelatedService` | bool | İlişkili servis kullan |
| `relatedServiceId` | int | İlişkili servis ID'si |
| `targetInstancesFieldId` | int | Hedef kayıt alanı ID'si |

---

## Adım Tipi Detayları

### 1. Kullanıcı Adımı (StepTypeUserDto)

Tek bir kullanıcıya atanan onay adımıdır. Kullanıcı belirleme yöntemleri:

#### Kullanıcı Tipleri (ProcessSettingUserType)

| Index | Enum | Açıklama |
|-------|------|----------|
| 0 | `surecBaslatan` | Süreci başlatan kullanıcı |
| 1 | `sabitKullanici` | Sabit olarak belirlenen kullanıcı |
| 2 | `kullanicininYoneticisi` | Kullanıcının yöneticisi |
| 3 | `yoneticiZinciri` | Yönetici zinciri |
| 4 | `departmanYoneticisi` | Departman yöneticisi |
| 5 | `unvanaGoreYonetici` | Ünvana göre yönetici |
| 6 | `degisgenKullanici` | Dinamik kullanıcı (form alanından belirlenen) |

#### Kullanıcı Adımı Özellikleri

| Alan | Tip | Açıklama |
|------|-----|----------|
| `userType` | ProcessSettingUserType | Kullanıcı belirleme yöntemi |
| `processViewProfileId` | int | Görüntüleme profili ID'si |
| `stableUserId` | int | Sabit kullanıcı ID'si |
| `managerChainConditionType` | int | Yönetici zinciri koşul tipi |
| `userAdministratorSourceProcessStepId` | int | Yönetici kaynağı adım ID'si |
| `departmanManagerDepartmantId` | int | Departman yöneticisi departman ID'si |
| `managerByDegreeSourceProcessStepId` | int | Ünvana göre yönetici kaynak adım ID'si |
| `managerByDegreeDegreeIds` | List\<int\> | Ünvan ID listesi |
| `dynamicUser` | WorkRuleConditionCompareValueDto | Dinamik kullanıcı koşul değeri |
| `sendNotificationOnStepDto` | SendNotificationOnStepDto | Adıma gelindiğinde gönderilecek bildirim |
| `stepTypeTimerDto` | StepTypeTimerDto | Zaman aşımı (timeout) ayarları |

---

### 2. Kullanıcı Grubu Adımı (StepTypeUserGroupDto)

Bir kullanıcı grubuna atanan onay adımıdır.

#### Kullanıcı Grubu Tipleri (ProcessSettingUserGroupType)

| Index | Enum | Açıklama |
|-------|------|----------|
| 0 | `sabitKullaniciGrubu` | Sabit kullanıcı grubu |
| 1 | `dinamikKullaniciListesi` | Dinamik kullanıcı listesi (form alanından) |
| 2 | `dinamikKullaniciGrubu` | Dinamik kullanıcı grubu |

#### Kullanıcı Grubu Adımı Özellikleri

| Alan | Tip | Açıklama |
|------|-----|----------|
| `userGroupType` | ProcessSettingUserGroupType | Grup belirleme yöntemi |
| `accountUserGroupId` | int | Kullanıcı grubu ID'si |
| `processViewProfileId` | int | Görüntüleme profili ID'si |
| `groupApproval` | bool | Grup onayı gerekli mi |
| `dynamicUserListFieldId` | int | Dinamik kullanıcı listesi alan ID'si |
| `sendNotificationOnStepDto` | SendNotificationOnStepDto | Adıma gelindiğinde bildirim |
| `stepTypeTimerDto` | StepTypeTimerDto | Zaman aşımı ayarları |

---

### 3. Function Adımı (StepTypeFunctionDto)

Harici bir API çağrısı yapan adımdır. RESTful HTTP istekleri gerçekleştirir.

| Alan | Tip | Açıklama |
|------|-----|----------|
| `method` | String | HTTP metodu (GET, POST, PUT, DELETE vb.) |
| `resource` | String | API endpoint URL'si |
| `returns` | String | Dönüş tipi |
| `templateParameters` | List\<StepTypeFunctionParameter\> | Template parametreleri |
| `queryParameters` | List\<StepTypeFunctionParameter\> | Query string parametreleri |
| `headers` | List\<StepTypeFunctionParameter\> | HTTP header'ları |
| `body` | List\<StepTypeFunctionParameter\> | Request body parametreleri |

#### Function Parametre Yapısı (StepTypeFunctionParameter)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `name` | String | Parametre adı |
| `degerTuru` | String | Değer türü (sabit, form alanı vb.) |
| `value` | String | Parametre değeri |

---

### 4. Karşılaştırma Adımı (StepTypeConditionDto)

Form alanlarındaki değerlere göre koşullu dallanma sağlar.

| Alan | Tip | Açıklama |
|------|-----|----------|
| `conditions` | List\<WorkRuleConditionDto\> | Koşul listesi |
| `conditionType` | KosulTuru | Koşul türü (VE/VEYA) |

#### Kriter Tipleri (CriteritionType)

Koşullarda kullanılabilecek karşılaştırma operatörleri:

| Index | Enum | Açıklama |
|-------|------|----------|
| 0 | `esittir` | Eşittir (=) |
| 1 | `esitDegildir` | Eşit değildir (!=) |
| 2 | `bos` | Boş |
| 3 | `bosDegil` | Boş değil |
| 4 | `dahaBuyuk` | Daha büyük (>) |
| 5 | `dahaBuyukVeyaEsit` | Daha büyük veya eşit (>=) |
| 6 | `dahaKucuk` | Daha küçük (<) |
| 7 | `dahaKucukVeyaEsit` | Daha küçük veya eşit (<=) |
| 8 | `ileBaslar` | İle başlar |
| 9 | `ileBiter` | İle biter |
| 10 | `icerir` | İçerir |
| 11 | `icermez` | İçermez |

---

### 5. Bildirim Adımı (StepTypeNotificationDto)

Belirli kullanıcılara veya gruplara bildirim gönderir.

| Alan | Tip | Açıklama |
|------|-----|----------|
| `sendNotificationOnStepDto` | SendNotificationOnStepDto | Bildirim içerik ayarları |
| `notificationStepTypesDtos` | List\<NotificationStepTypesDto\> | Bildirim alıcı tanımları |

#### Bildirim Alıcı Tipleri

**Kullanıcı Bazlı (NotificationStepTypeUserType):**

| Index | Enum | Açıklama |
|-------|------|----------|
| 0 | `ProcessStarter` | Süreç başlatıcısı |
| 1 | `FixedUser` | Sabit kullanıcılar |
| 2 | `VariableUsers` | Değişken kullanıcılar (önceki adımlardan) |
| 3 | `FormField` | Form alanından belirlenen kullanıcı |

**Grup Bazlı (NotificationStepTypeUserGroupType):**

| Index | Enum | Açıklama |
|-------|------|----------|
| 0 | `UserGroup` | Kullanıcı grubu |
| 1 | `TakeUsersWhoTakeActionBefore` | Daha önce aksiyon alan kullanıcılar |

---

### 6. Timer (Zamanlayıcı) Adımı (StepTypeTimerDto)

Zamanlama ve zaman aşımı mekanizmasını tanımlar. Kullanıcı ve kullanıcı grubu adımlarının timeout ayarlarında da bu yapı kullanılır.

| Alan | Tip | Açıklama |
|------|-----|----------|
| `timeoutActive` | bool | Zaman aşımı aktif mi |
| `workStyle` | WorkStyle | Çalışma takvimi tipi |
| `accordingToWorkSchedule` | AccordingToWorkSchedule | Çalışma takvimine göre ayarlar |
| `accordingToNormalSchedule` | AccordingToNormalSchedule | Normal takvime göre ayarlar |
| `accordingToFixedDateTime` | AccordingToFixedDateTime | Sabit zamana göre ayarlar |
| `timeoutNotificationActive` | bool | Zaman aşımı bildirimi aktif mi |
| `timeoutNotification` | SendNotificationOnStepDto | Zaman aşımı bildirim ayarları |

#### Çalışma Stili (WorkStyle)

| Index | Enum | Açıklama |
|-------|------|----------|
| 0 | `calismaTakvimineGore` | Çalışma takvimine göre |
| 1 | `normalTakvimeGore` | Normal takvime göre |
| 2 | `sabitZaman` | Sabit zaman |

#### Normal Takvim Ayarları (AccordingToNormalSchedule)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `day` | String | Gün değeri |
| `workTimeSelection` | WorkTimeSelection | Çalışma zamanı seçimi |
| `postPoning` | bool | Erteleme aktif mi |
| `timeAdjustmentOption` | TimeAdjustmentOption | Zaman ayarlama opsiyonu |
| `postPoningHour` | String | Erteleme saati |

#### Çalışma Zamanı Seçimi (WorkTimeSelection)

| Index | Enum | Açıklama |
|-------|------|----------|
| 0 | `calismaBaslangicinda` | Çalışma başlangıcında |
| 1 | `calismaBitiminde` | Çalışma bitiminde |

#### Zaman Ayarlama Opsiyonu (TimeAdjustmentOption)

| Index | Enum | Açıklama |
|-------|------|----------|
| 0 | `saatSonra` | Saat sonra |
| 1 | `saatOnce` | Saat önce |

---

### 7. Timer Start Adımı (StepTypeStartTimerDto)

Daha önce tanımlanmış bir zamanlayıcıyı başlatır.

| Alan | Tip | Açıklama |
|------|-----|----------|
| `selectedTimerProcessStepId` | int | Başlatılacak timer adımının ID'si |

---

### 8. Timer End Adımı (StepTypeEndTimerDto)

Çalışmakta olan bir zamanlayıcıyı sonlandırır.

| Alan | Tip | Açıklama |
|------|-----|----------|
| `selectedTimerProcessStepId` | int | Sonlandırılacak timer adımının ID'si |

---

### 9. Adım İptali (StepTypeStepCancellationDto)

Süreçteki bekleyen talepleri iptal eder.

| Alan | Tip | Açıklama |
|------|-----|----------|
| `cancellationType` | CancellationType | İptal tipi |
| `canceledProcessStepId` | int | İptal edilecek adımın ID'si |

#### İptal Tipleri (CancellationType)

| Index | Enum | Açıklama |
|-------|------|----------|
| 0 | `CancelAllRequests` | Tüm talepleri iptal et |
| 1 | `CancelStepRequest` | Belirli adımın talebini iptal et |

---

### 10. Custom ID Creator (StepTypeCustomIdCreatorDto)

Özel format ile benzersiz numara/ID üretir.

| Alan | Tip | Açıklama |
|------|-----|----------|
| `customId` | String | ID format şablonu |
| `targetPropertyId` | int | Hedef alan ID'si (üretilen ID'nin yazılacağı alan) |
| `createWithBarcode` | bool | Barkod ile oluştur |
| `targetFilePropertyId` | int | Hedef dosya alanı ID'si (barkod görseli) |

---

### 11. Süreç Bitişi Adımı (StepTypeEndDto)

Sürecin tamamlandığını belirten bitiş adımıdır.

| Alan | Tip | Açıklama |
|------|-----|----------|
| `processViewProfileDto` | ProcessViewProfileDto | Görüntüleme profili |
| `accountUserGroupDtos` | List\<AccountUserGroupDto\> | Bitiş sonrası erişim grubu |

---

### 12. Değer Atama Adımı (ProcessStepTargetFieldDto)

Form alanlarına otomatik değer atar.

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Kayıt ID'si |
| `processStepId` | int | Bağlı süreç adımı ID'si |
| `valueType` | ProcessStepTargetFieldValueType | Değer tipi |
| `fixedValue` | String | Sabit değer |
| `useDisplay` | bool | Görüntü değerini kullan |
| `targetFieldId` | int | Hedef alan ID'si |
| `targetField` | PropertyDto | Hedef alan tanımı |
| `fieldId` | int | Kaynak alan ID'si |
| `field` | PropertyDto | Kaynak alan tanımı |

#### Değer Tipi (ProcessStepTargetFieldValueType)

| Index | Enum | Açıklama |
|-------|------|----------|
| 0 | `FixedValue` | Sabit değer |
| 1 | `FormValue` | Form alanı değeri |

---

## Aksiyonlar (ProcessStepActionDto)

Her süreç adımına bir veya birden fazla aksiyon tanımlanabilir. Aksiyonlar, kullanıcının adımda yapabileceği eylemleri temsil eder.

### Aksiyon Özellikleri

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Aksiyon ID'si |
| `code` | String | Aksiyon kodu |
| `definition` | String | Aksiyon tanımı |
| `processStepId` | int | Bağlı adım ID'si |
| `icon` | String | Aksiyon ikonu |
| `actionType` | String | Aksiyon tipi (success, danger, warning vb.) |
| `action` | String | Aksiyon davranışı |
| `environmentRestriction` | String | Ortam kısıtlaması |
| `validation` | bool | Validasyon gerekli mi |
| `reasonRequired` | bool | Sebep girilmesi zorunlu mu |
| `stayOnPage` | bool | Aksiyondan sonra sayfada kal |
| `showHistory` | bool | Süreç geçmişini göster |
| `changeStatusId` | int | Durum değiştir (hedef durum ID'si) |
| `targetProcessStepId` | int | Hedef süreç adımı ID'si |
| `showInHistory` | bool | Süreç geçmişinde göster |
| `authorizationLevel` | int | Yetki seviyesi |
| `actionDisplayType` | ActionDisplayType | Aksiyon görüntüleme tipi |
| `actionDisplayAuthorizedUserGroupId` | int | Aksiyonu görüntüleyebilecek kullanıcı grubu |

### Aksiyon Davranışları (action)

| Değer | Açıklama |
|-------|----------|
| `fire-event` | Olay tetikle (varsayılan) |
| `new-instance` | Yeni kayıt oluştur |
| `new-instance-referenced` | Referanslı yeni kayıt oluştur |
| `new-instance-other` | Başka serviste yeni kayıt oluştur |
| `expform-new-instance-other` | Masraf formu - başka serviste yeni kayıt |
| `take-photo` | Fotoğraf çek |
| `expform-take-photo` | Masraf formu - fotoğraf çek |
| `select-file` | Dosya seç |
| `expform-select-file` | Masraf formu - dosya seç |
| `expform-add-exist-expense` | Mevcut masrafı ekle |
| `take-barcode` | Barkod oku |
| `manuel-barcode-input` | Manuel barkod girişi |
| `excel-export` | Excel'e aktar |
| `add-test-receipt` | Test fişi ekle |

---

## Bildirim Yapısı (SendNotificationOnStepDto)

Adıma gelindiğinde veya zaman aşımında gönderilecek bildirim ayarlarıdır. Çoklu dil desteği sunar (TR/EN).

| Alan | Tip | Açıklama |
|------|-----|----------|
| `isPushNotificationMustSend` | bool | Push bildirim gönderilecek mi |
| `isMailMustSend` | bool | E-posta gönderilecek mi |
| `pushNotificationTitle` | String | Push bildirim başlığı (TR) |
| `pushNotificationMessage` | String | Push bildirim mesajı (TR) |
| `mailTitle` | String | E-posta başlığı (TR) |
| `mailMessage` | String | E-posta mesajı (TR) |
| `pushNotificationTitleEn` | String | Push bildirim başlığı (EN) |
| `pushNotificationMessageEn` | String | Push bildirim mesajı (EN) |
| `mailTitleEn` | String | E-posta başlığı (EN) |
| `mailMessageEn` | String | E-posta mesajı (EN) |

### Bildirim Şablon Değişkenleri

Bildirim mesajlarında kullanılabilecek dinamik değişkenler:

| Değişken | Açıklama |
|----------|----------|
| `#ProcessCreator` | Süreci başlatan kullanıcı |
| `#ProcessState` | Süreç durumu |
| `#ProcessStartDate` | Süreç başlangıç tarihi |
| `#ServiceName` | Servis adı |

---

## Koşullar (ProcessStepConditionDto)

Süreç adımlarına eklenebilen koşullar, adımın ne zaman aktif olacağını belirler.

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Koşul ID'si |
| `processStepId` | int | Bağlı adım ID'si |
| `conditionType` | int | Koşul tipi |
| `value` | String | Koşul değeri (JSON formatında) |

### Koşul Türleri (ConditionType)

| Index | Enum | Açıklama |
|-------|------|----------|
| 0 | `titleValueLimit` | Başlık değer limiti |

---

## Görüntüleme Profili (ProcessSettingViewProfile)

Kullanıcı ve kullanıcı grubu adımlarında, adıma gelen kullanıcının formu hangi görünümde göreceğini belirler.

| Index | Enum | Açıklama |
|-------|------|----------|
| 0 | `varsayilan` | Varsayılan görüntüleme profili |

---

## API Endpoint'leri

Süreç adımları yönetimi için kullanılan API endpoint'leri:

| Endpoint | Açıklama |
|----------|----------|
| `GetProcessSteps` | Süreç adımlarını listele |
| `AddOrUpdateProcessStep` | Süreç adımı ekle/güncelle |
| `DeleteProcessStep/{id}` | Süreç adımı sil |
| `AddOrUpdateProcessActionList` | Süreç adım sıralamasını güncelle |
| `GetProcessActions` | Aksiyonları listele |
| `AddOrUpdateProcessAction` | Aksiyon ekle/güncelle |
| `GetProcessStatuses` | Durumları listele |
| `AddOrUpdateProcessStatus` | Durum ekle/güncelle |

### İstek Header'ları

Tüm API istekleri aşağıdaki header bilgilerini gerektirir:

| Header | Açıklama |
|--------|----------|
| `accountId` | Hesap ID'si |
| `solutionid` | Çözüm ID'si |
| `ServiceId` | Servis ID'si |

---

## Yardımcı Veriler (GetListProcessStepDto)

Süreç adımları sayfası yüklendiğinde backend'den gelen yardımcı veriler:

| Alan | Tip | Açıklama |
|------|-----|----------|
| `processStepDtos` | List\<ProcessStepDto\> | Mevcut süreç adımları |
| `accountProfessionDtos` | List\<AccountProfessionDto\> | Hesap ünvanları |
| `accountDepartmentDtos` | List\<AccountDepartmentDto\> | Hesap departmanları |
| `processActionDtos` | List\<ProcessActionDto\> | Tanımlı aksiyonlar |
| `statusDtos` | List\<ProcessStatusDto\> | Tanımlı durumlar |
| `processViewProfileDtos` | List\<ProcessViewProfileDto\> | Görüntüleme profilleri |
| `accountUserGroupDtos` | List\<AccountUserGroupDto\> | Kullanıcı grupları |
| `methods` | List\<String\> | HTTP metotları |
| `returns` | List\<String\> | Dönüş tipleri |
| `degerTuru` | List\<String\> | Değer türleri |
| `processStepExpressionKeys` | List\<String\> | Şablon ifade anahtarları |
| `fields` | List\<PropertyDto\> | Form alanları |
| `defaultProcessViewProfileId` | int | Varsayılan görüntüleme profili ID'si |

---

## İş Akışı Mantığı

### Süreç Akışı Nasıl Çalışır

1. **Başlangıç:** Süreç, `surecBaslangici` tipindeki adımdan başlar.
2. **İlerleme:** Her aksiyon, `targetProcessStepId` ile bir sonraki adımı belirler.
3. **Koşullu Dallanma:** `compare` tipindeki adımlar, form değerlerine göre farklı adımlara yönlendirir.
4. **Onay:** `kullanici` veya `kullaniciGrubu` adımları, kullanıcıdan onay bekler.
5. **Otomasyon:** `function`, `notification`, `valueAssignment`, `customIdCreator` gibi adımlar otomatik çalışır.
6. **Bitiş:** Süreç, `surecBitisi` tipindeki adıma ulaştığında tamamlanır.

### Atlama (Skip) Mekanizması

- **skipIfPreApproved:** Kayıt önceden onaylanmışsa adım atlanır.
- **skipIfUserProcessStarter:** Süreci başlatan kullanıcı bu adıma geliyorsa atlanır.
- **skipWithThisActionId:** Atlama yapılırken kullanılacak aksiyonun ID'si.

### Zaman Aşımı (Timeout) Mekanizması

Kullanıcı ve kullanıcı grubu adımlarında timeout tanımlanabilir:

1. **Çalışma Takvimine Göre:** İş günü ve çalışma saatleri dikkate alınarak süre hesaplanır.
2. **Normal Takvime Göre:** Takvim günleri üzerinden hesaplanır, erteleme seçeneği vardır.
3. **Sabit Zaman:** Belirli bir tarih/saat belirlenir.

Zaman aşımı gerçekleştiğinde opsiyonel olarak bildirim gönderilebilir.

### Sıralama

Süreç adımları `order` alanına göre sıralanır ve kullanıcı arayüzünde sürükle-bırak ile yeniden sıralanabilir. Sıralama değişikliği `AddOrUpdateProcessActionList` endpoint'i ile kaydedilir.

---

## Dosya Yapısı

```
lib/
├── Models/Settings/FlvSettings/ProcessStep/
│   ├── ProcessStepDto.dart                         # Ana süreç adımı modeli
│   ├── ProcessSettingStepType.dart                 # Adım tipleri enum'u
│   ├── ProcessStepActionDto.dart                   # Aksiyon modeli
│   ├── ProcessStepConditionDto.dart                # Koşul modeli
│   ├── ProcessStepConditionDatasDto.dart           # Koşul verileri
│   ├── ProcessStepConditionTitleValueLimitDto.dart # Başlık değer limiti koşulu
│   ├── ProcessStepTargetFieldDto.dart              # Hedef alan modeli (değer atama)
│   ├── GetListProcessStepDto.dart                  # Liste yanıt modeli
│   ├── GetProcessStepConditionDto.dart             # Koşul sorgulama modeli
│   ├── ProcessSettingViewProfile.dart              # Görüntüleme profili enum'u
│   ├── ConditionType.dart                          # Koşul tipi enum'u
│   ├── CriteritionType.dart                        # Kriter tipi enum'u
│   ├── StepTypeUserDto.dart                        # Kullanıcı adımı modeli
│   ├── StepTypeUserGroupDto.dart                   # Kullanıcı grubu adımı modeli
│   ├── StepTypeFunctionDto.dart                    # Function adımı modeli
│   ├── StepTypeConditionDto.dart                   # Karşılaştırma adımı modeli
│   ├── StepTypeNotificationDto.dart                # Bildirim adımı modeli
│   ├── StepTypeTimerDto.dart                       # Timer adımı modeli
│   ├── StepTypeStartTimerDto.dart                  # Timer başlatma modeli
│   ├── StepTypeEndTimerDto.dart                    # Timer sonlandırma modeli
│   ├── StepTypeEndDto.dart                         # Süreç bitişi modeli
│   ├── StepTypeStepCancellationDto.dart            # Adım iptali modeli
│   ├── StepTypeCustomIdCreatorDto.dart             # Custom ID modeli
│   └── SendNotificationOnStepDto.dart              # Bildirim içerik modeli
│
└── Pages/Settings/FlvSettings/ProcessStep/
    ├── ProcessStepSettingsPage.dart                 # Süreç adımları liste sayfası
    ├── ProcessStepDetailPage.dart                   # Süreç adımı detay sayfası
    ├── ProcessStepActionDeiltaPage.dart             # Aksiyon detay sayfası
    ├── ProcessStepConditionPage.dart                # Koşul sayfası
    ├── ProcessStepConditionComparableValuePage.dart # Koşul değeri sayfası
    └── StepTypeViews/
        ├── StepTypeUser.dart                        # Kullanıcı adımı görünümü
        ├── StepTypeUserGroup.dart                   # Kullanıcı grubu görünümü
        ├── StepTypeEndView.dart                     # Süreç bitişi görünümü
        ├── StepTypeTimerView.dart                   # Timer görünümü
        ├── StepTypeStepCancellation.dart            # Adım iptali görünümü
        ├── StepTypeCustomIdCreator.dart             # Custom ID görünümü
        ├── SendNotificationOnStepView.dart          # Bildirim ayarları görünümü
        ├── Function/
        │   ├── StepTypeFunction.dart                # Function adımı görünümü
        │   └── ParametersDetailPage.dart            # Parametre detay sayfası
        ├── Notification/
        │   ├── StepTypeNotification.dart            # Bildirim adımı görünümü
        │   └── StepTypeNotificationSelectionView.dart # Bildirim seçimi
        └── ValueAssignment/
            ├── StepTypeValueAssignment.dart          # Değer atama görünümü
            └── TargetAreasView.dart                  # Hedef alanları görünümü
```
