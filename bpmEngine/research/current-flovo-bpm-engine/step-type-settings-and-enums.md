# Mevcut Flovo — Adım Tipine Özel Ayar Modelleri & Enum'lar (ham referans + taşıma notları)

> **Durum:** 🟡 REFERANS (ham) — gözden geçirilecek, kararlar işlenmedi.
> **Amaç:** Mevcut (eski) Flovo'daki **adım-tipine-özel ayar DTO'ları** + **enum tanımlarının** ham dökümü ve bunların
> **yeni projeye taşınmasına dair kararlar**. Yeni projedeki iki boşluğu besler: `service-settings/process-step.md §2`
> (tipe-özel ayarlar) ve [`../../models/enums/`](../../models/enums/index.md) (eksik/boş enum'lar).
> **Kaynak:** Mevcut Flovo Flutter projesi (`Pratico.Apps`) — Dart DTO/enum tanımları.
> **Kullanım:** Bu dosya **referans + karar taslağıdır**; **ana model/enum dokümanları henüz güncellenMEDİ** — bu dosya
> onaylandıktan sonra işlenecek.
> **Not (CLAUDE.md md.4/5):** Ham eski-app tanımları + "eski ad → yeni ad" eşlemesi **yalnız burada (research)** tutulur;
> yeni tasarım dokümanlarına "eski adı…" ifadeleri konmaz.

## İşaretler

| İşaret | Anlam | İşaret | Anlam |
|---|---|---|---|
| 🔤 | enum | ❌ | kaldırılacak |
| 🧩 | DTO / model | ✏️ | değişecek / sadeleşecek |
| 🔁 | yeniden adlandırılacak | ➕ | eklenecek |
| 🟢 | karar net | ❓ | açık / netleşecek |

> **Adlandırma hedefi (🟢 onaylandı):** enum **tip adı** İngilizce **PascalCase**, enum **değeri** İngilizce **camelCase**;
> model **alan adı** camelCase — eski **`field`** adları **`property`**'ye çevrilir. Aşağıdaki ham tanımlar eski projeden
> geldiği için bu kurala **uymuyor**; "Taşıma kararı" satırları normalize edilmiş hedefi verir.

---

## 1. 🔤 ProcessStepType — adım tipi ayrımlayıcısı

**Mevcut durum:** Yeni projede ne enum ne de `ProcessStep.stepType` alanı var; adım tipleri yalnız
`service-settings/process-step.md §3`'te başlık olarak duruyor.

**Taşıma kararı (🟢):** `ProcessStep` modelindeki **21 adım tipine** göre isimlendirilmiş bir **`ProcessStepType`** enum'u
oluşturulacak; `ProcessStep` modeline `stepType: ProcessStepType` ayrımlayıcı alanı eklenecek. Değerler `§3` kataloğundan
türetilir (öneri, camelCase):

```
processStart · httpRequest · flovoAi · valueAssignment · triggerProcessStep · notification ·
timer · timerStart · timerEnd · instanceDeleter · customIdCreator · instanceCreator ·
comparison · switch · user · userGroup · processEnd · processing · formRedirect · subProcessStart
```

> 🟢 **Onaylandı** — `ProcessStepType` adı ve yaklaşımı uygun. Değer adları `§3` başlıklarıyla birebir eşlenerek kesinleşir.

---

## 2. 🧩 Kullanıcı adımı — `ProcessStepUserType` + `ProcessStepTypeUser`

### 2.1 🔤 Enum (mevcut)

```dart
enum ProcessSettingUserType {
  surecBaslatan, sabitKullanici, kullanicininYoneticisi,
  yoneticiZinciri, departmanYoneticisi, unvanaGoreYonetici, degisgenKullanici
}
```

### 2.2 🧩 DTO (mevcut) — alan-alan

```dart
class StepTypeUserDto {
  ProcessSettingUserType? userType;
  int?  processViewProfileId;
  int?  managerChainConditionType;
  int?  userAdministratorSourceProcessStepId;
  int?  departmanManagerDepartmantId;
  int?  managerByDegreeSourceProcessStepId;
  List<int>? managerByDegreeDegreeIds;
  int?  stableUserId;
  WorkRuleConditionCompareValueDto? dynamicUser;
  SendNotificationOnStepDto?        sendNotificationOnStepDto;
  StepTypeTimerDto                  stepTypeTimerDto;
}
```

| Alan | Ne işe yarıyor | Karar |
|---|---|---|
| `userType` | Aksiyonu alacak kullanıcının **belirleme yöntemi** (yukarıdaki enum). | 🔁 tip `ProcessStepUserType` olacak |
| `processViewProfileId` | Aksiyonu alacak kullanıcının formu **hangi görüntüleme profiliyle** göreceği. | 🟢 kalır |
| `managerChainConditionType` | "Yönetici zinciri" yöntemine ait ayar. | ❌ kaldırılacak |
| `userAdministratorSourceProcessStepId` | **"Kullanıcının yöneticisi"** yönteminde kullanılır. Bu alandaki **süreç adımını hedef alır:** akışta **o adımda en son onay veren** kullanıcının **yöneticisi** kim ise aksiyon sahibi o olur. | 🟢 kalır |
| `departmanManagerDepartmantId` | "Departman yöneticisi" yönteminde **hangi departmanın** yöneticisine gideceği. | 🟢 kalır *(yazım: `departmentManagerDepartmentId`)* |
| `managerByDegreeSourceProcessStepId` | "Ünvana göre yönetici" yöntemine ait kaynak adım. | ❌ kaldırılacak |
| `managerByDegreeDegreeIds` | "Ünvana göre yönetici" yöntemine ait ünvan listesi. | ❌ kaldırılacak |
| `stableUserId` | **Sabit kullanıcı** yönteminde seçilen kullanıcının id'si. | 🔁 **`fixedUserId`** olacak |
| `dynamicUser` | **Değişken kullanıcı** yöntemi. Şu an iş-kuralı modeliyle (sabit kullanıcı / form alanı / hesaplama) yönetiliyor; pratikte hep **form alanı** seçilip "o alandaki kullanıcı kimse ona git" olarak kullanılıyor. | ✏️ **sadeleşecek:** ağır iş-kuralı modeli kaldırılıp — Kullanıcı Grubu'ndaki gibi — doğrudan **form property id** alan bir alana indirgenecek |
| `sendNotificationOnStepDto` | Adıma **girildiğinde bildirim** gönderme kısayolu. | 🟢 kalır (bkz. §4 — SendNotificationMessages) |
| `stepTypeTimerDto` | Adıma **girildiğinde otomatik timer/timeout** başlatma. | 🟢 kalır (bkz. §5 — zamanlayıcı bloğu) |

### 2.3 Taşıma kararları

- 🔁 `ProcessSettingUserType` → **`ProcessStepUserType`**
- 🔁 `StepTypeUserDto` → **`ProcessStepTypeUser`**
- ❌ **Enum değerleri `yoneticiZinciri` ve `unvanaGoreYonetici` kaldırılacak** (mevcut projede aktif çalışmayan özellikler).
- ❌ Kaldırılan bu iki değere bağlı DTO alanları da kaldırılacak: `managerChainConditionType`,
  `managerByDegreeSourceProcessStepId`, `managerByDegreeDegreeIds`.
- ✏️ Kalan enum değer adları proje dokümanlarına uygun (camelCase/İngilizce) normalize edilecek.
- **Kalan enum (kaldırmalar sonrası, 5 değer):** `surecBaslatan · sabitKullanici · kullanicininYoneticisi ·
  departmanYoneticisi · degisgenKullanici` → normalize önerisi: `processStarter · fixedUser · usersManager ·
  departmentManager · variableUser`.

---

## 3. 🧩 Kullanıcı Grubu adımı — `ProcessStepUserGroupType` + `ProcessStepTypeUserGroup`

### 3.1 🔤 Enum + 🧩 DTO (mevcut)

```dart
enum ProcessSettingUserGroupType { sabitKullaniciGrubu, dinamikKullaniciListesi, dinamikKullaniciGrubu }

class StepTypeUserGroupDto {
  ProcessSettingUserGroupType? userGroupType;
  int?  accountUserGroupId;
  int?  processViewProfileId;
  bool? groupApproval;
  SendNotificationOnStepDto? sendNotificationOnStepDto;
  StepTypeTimerDto           stepTypeTimerDto;
  int?  dynamicUserListFieldId;
}
```

| Alan | Ne işe yarıyor | Karar |
|---|---|---|
| `userGroupType` | Grubun **belirleme yöntemi** (sabit grup / dinamik liste / dinamik grup). | 🔁 tip `ProcessStepUserGroupType` |
| `accountUserGroupId` | **Sabit kullanıcı grubu** yönteminde seçilen grup. | 🟢 **`organizationUserGroupId`** olacak (`account*→organization*` normalizasyonu) |
| `processViewProfileId` | Onaya gidecek kullanıcıların göreceği görüntüleme profili. | 🟢 kalır |
| `groupApproval` | Grup onay davranışı. **`true`:** aksiyon alabilen **tüm** kullanıcılar onaylayınca süreç ilerler. **`false`:** gruptaki **bir** kişinin onayı yeterli. | 🟢 **bool kalır** |
| `sendNotificationOnStepDto` | Adıma girildiğinde bildirim kısayolu. | 🟢 kalır (§4) |
| `stepTypeTimerDto` | Adıma girildiğinde otomatik timer/timeout. | 🟢 kalır (§5) |
| `dynamicUserListFieldId` | **Dinamik liste/grup** yönteminde, listeyi formdaki **property'den** (o alandaki kullanıcı/kullanıcı grupları) belirleme alanı. | 🟢 kalır; ✏️ **`dynamicUserListPropertyId`** (`field→property`) |

> 🟢 **İsimlendirme onaylandı:** `ProcessSettingUserGroupType → ProcessStepUserGroupType`,
> `StepTypeUserGroupDto → ProcessStepTypeUserGroup`.

---

## 4. 🧩 Bildirim adımı — `ProcessStepSendNotification`

### 4.1 🧩 Sınıf hiyerarşisi (mevcut)

```dart
class StepTypeNotificationDto {
  SendNotificationOnStepDto?       sendNotificationOnStepDto;
  List<NotificationStepTypesDto>?  notificationStepTypesDtos;
}

// Bildirim MESAJLARI (Push + Mail, TR + EN sabit alanlar)
class SendNotificationOnStepDto {
  bool?   isPushNotificationMustSend;
  bool?   isMailMustSend;
  String? pushNotificationTitle;    String? pushNotificationMessage;
  String? mailTitle;                String? mailMessage;
  String? pushNotificationTitleEn;  String? pushNotificationMessageEn;
  String? mailTitleEn;              String? mailMessageEn;
}

// Bildirim ALICILARI (kullanıcı veya kullanıcı-grubu bazlı)
class NotificationStepTypesDto {
  ProcessSettingStepType?        stepType;              // alıcı türü: user | userGroup (→ NotificationRecipientType)
  UserStepTypeNotification?      userStepTypeNotification;
  UserGroupStepTypeNotification? userGroupStepTypeNotification;
  bool?                          addToCc;
}

class UserStepTypeNotification {
  NotificationStepTypeUserType? userType;
  List<int>? fixedUserIds;
  List<int>? variableUserProcessStepIds;
  int?       propertyId;
}
enum NotificationStepTypeUserType { ProcessStarter, FixedUser, VariableUsers, FormField }

class UserGroupStepTypeNotification {
  NotificationStepTypeUserGroupType? userGroupType;
  List<int>? userGroupIds;
}
enum NotificationStepTypeUserGroupType { UserGroup, TakeUsersWhoTakeActionBefore }
```

### 4.2 Taşıma kararları

- 🔁 `StepTypeNotificationDto` → **`ProcessStepSendNotification`**
- 🔁 `SendNotificationOnStepDto` → **`SendNotificationMessages`**
- 🔁 `NotificationStepTypesDto` → **`SendNotificationUsers`**
- 🔁 Kalan sınıf/enum adları (`UserStepTypeNotification`, `NotificationStepTypeUserType`, …) projeye uygun normalize edilecek.
- ✏️ **`NotificationUserGroupType` kaldırıldı:** iki değeri (`userGroup`, `takeUsersWhoTookActionBefore`) üst-düzey
  **`NotificationRecipientType`**'a taşındı → `{user, userGroup, takeUsersWhoTookActionBefore}`. Grup tarafında tek gerçek
  seçim `userGroupIds` olduğundan ayrı alt-enum gereksizdi.
- ✏️ **Mesajlar dinamik listeye dönecek:** Şu anki sabit `...Title/...Message` + `...TitleEn/...MessageEn` alanları yerine,
  her öğesi **`{ languageCode, text }`** olan bir **dil listesi** olacak (çok-dil desteği sabit TR/EN'e bağlı kalmadan genişler).
- ✏️➕ **Kanallar dinamikleşecek + `NotificationChannel` enum'u:** mevcut yapı sabit **Push + Mail** (iki bool). Yeni projede
  kanallar **dinamik** yapıya dönecek ve **`NotificationChannel {mail, push, toast}`** enum'uyla temsil edilecek (**Toast** eklendi).
- ➕ **Parametre alanları** eklenecek: Push/Toast bildirimiyle birlikte gönderilen `parameters`
  (UI'da gösterilmez; çalışma zamanında formu güncelleme için — `service-settings/process-step.md §3.6`).

> **Önemli — `SendNotificationMessages` çok yerde yeniden kullanılıyor:** aynı mesaj DTO'su §2 (Kullanıcı),
> §3 (Kullanıcı Grubu), §5 (Timer `timeoutNotification`) ve bu bölümde (Bildirim adımı) ortak. Yukarıdaki
> "dinamik liste + toast + parametre" değişikliği **bu dört kullanım yerinin hepsini** etkiler.

> 🟢 **`SendNotificationUsers.stepType` netleşti — alıcı türü `NotificationRecipientType {user, userGroup, takeUsersWhoTookActionBefore}`:**
> **`user`** → alıcı `UserStepTypeNotification` (→ `NotificationUserType`) ile; **`userGroup`** → doğrudan `userGroupIds`;
> **`takeUsersWhoTookActionBefore`** → daha önce aksiyon almış kullanıcılar. §1'deki `ProcessStepType` ile karışmaması için bu adla
> ayrıştırıldı (21 adım tipiyle ilgisi yok). Ayrı `NotificationUserGroupType` **kaldırıldı** (değerleri buraya toplandı); bildirim
> alıcısı adım-atama enum'larından **ayrıdır**.

---

## 5. 🧩 Zamanlayıcı ortak bloğu — `ProcessStepTypeTimer` (Timer + adım timeout'u)

> Bu blok hem **Timer / Timer Start / Timer End** adımlarının, hem de **Kullanıcı & Kullanıcı Grubu** adımlarındaki
> **timeout** özelliğinin ortak yapısıdır (§2/§3'teki `stepTypeTimerDto`).

### 5.1 🧩 DTO + 🔤 enum (mevcut)

```dart
class StepTypeTimerDto {
  bool?      timeoutActive;
  WorkStyle? workStyle;
  AccordingToWorkSchedule?   accordingToWorkSchedule;
  AccordingToNormalSchedule? accordingToNormalSchedule;
  AccordingToFixedDateTime?  accordingToFixedDateTime;
  bool?      timeoutNotificationActive;
  SendNotificationOnStepDto? timeoutNotification;
}

enum WorkStyle { calismaTakvimineGore, normalTakvimeGore, sabitZaman }
enum WorkTimeSelection    { calismaBaslangicinda, calismaBitiminde }   // çalışma başlangıcında / bitiminde
enum TimeAdjustmentOption { saatSonra, saatOnce }                       // saat sonra / saat önce

class AccordingToWorkSchedule   { String? value; }
class AccordingToNormalSchedule { String? day; WorkTimeSelection? workTimeSelection;
                                  bool? postPoning; TimeAdjustmentOption? timeAdjustmentOption; String? postPoningHour; }
class AccordingToFixedDateTime  { String? dateTime;
                                  bool? postPoning; TimeAdjustmentOption? timeAdjustmentOption; String? postPoningHour; }
```

| Alan | Ne işe yarıyor |
|---|---|
| `timeoutActive` | Zaman aşımı/zamanlayıcı aktif mi. |
| `workStyle` | Süre hesaplama stili — **`WorkStyle`** enum (çalışma takvimine göre / normal takvime göre / sabit zaman). |
| `accordingToWorkSchedule` / `accordingToNormalSchedule` / `accordingToFixedDateTime` | Seçilen stile karşılık gelen **ayar bloğu** (üçünden biri dolu). |
| `timeoutNotificationActive` + `timeoutNotification` | Süre dolunca **bildirim** gönderilsin mi + gönderilecek mesaj (bkz. §4 `SendNotificationMessages`). |

### 5.2 Taşıma kararları

- 🟢 İsimlendirme onaylandı: **`StepTypeTimerDto → ProcessStepTypeTimer`**, **`WorkStyle → TimerCalculationType`**
  ({workCalendar, normalCalendar, fixedDateTime}). ✏️ Yazım: `postPoning/postPoningHour → postponing/postponingHour`.
- 🟢 **`WorkTimeSelection` ve `TimeAdjustmentOption` değerleri netleşti** (yukarıda). Normalize önerisi:
  `WorkTimeSelection {atWorkStart, atWorkEnd}` · `TimeAdjustmentOption {hoursAfter, hoursBefore}`.
- 🟢 Yapı korunur: 1 stil enum'u + stile karşılık gelen 3 ayar bloğu + opsiyonel timeout bildirimi.

---

## 6. 🔤 Property enum'ları — `KeyboardType` & `BarcodeFormat`

> Bunlar adım ayarı değil; yeni projedeki **boş (placeholder) enum'ları** doldurur → `models/enums/keyboard-type.md`,
> `models/enums/barcode-format.md` (`property.md` Textbox/Phone ve Barcode kontrolleri).

```dart
enum KeyboardType { Default, Plain, Text, Numeric, Email, Url, Telephone }

enum BarcodeFormat {
  aztec, code39, code93, ean8, ean13, code128, dataMatrix, qr, interleaved2of5, pdf417
}
```

- 🟢 **KeyboardType** ve **BarcodeFormat** artık değer setleriyle **doldu** (eski placeholder'lar kapanacak).
- ✏️ Değerler camelCase'e normalize edilecek (`Default→default_/plain…`; `qr`/`ean13` zaten uygun).

---

## 7. 🧩 HTTP Request adımı (eski ad: **Function**) — `StepTypeFunctionDto`

### 7.1 🧩 DTO (mevcut)

```dart
class StepTypeFunctionDto {
  String? method;
  String? resource;                              // ≈ yeni projedeki "endpoint"
  String? returns;
  List<StepTypeFunctionParameter>? templateParameters;
  List<StepTypeFunctionParameter>? queryParameters;
  List<StepTypeFunctionParameter>? headers;
  List<StepTypeFunctionParameter>? body;
}

class StepTypeFunctionParameter {
  String? name;
  String? degerTuru;   // "değer türü": backend'den gelen liste; değerler: sabit değer, form alanı
  String? value;
}

// İş kuralı tarafındaki muadili (referans — daha eksiksiz):
class FunctionParameterItem {
  String?              name;
  AssignValueToFieldDto? value;   // enum: sabit değer / hesaplayarak / form alanı → değeri buna göre üretir
  dynamic              parameterValue;  // ayarda kullanılmaz; iş kuralı çalışınca hesaplanan ve
                                        // HTTP request'te gönderilecek değer burada tutulur (yardımcı alan)
}
```

### 7.2 Taşıma kararları

- 🔁 **Adım yeni adı: HTTP Request** (eski "Function").
- 🟢 **`resource → endpoint`** — terim yeni tasarımdaki `endpoint` ile birleşti.
- ✏️ **`method` bir enum olacak:** şu an `String`; **`HttpMethod {get, post, put, delete}`** (GET/POST/PUT/DELETE) enum'u üretilecek.
- ✏️ **Parametre modeli iş-kuralındakiyle hizalanacak:** Mevcut `StepTypeFunctionParameter` **eksik** (Function adımı gerçek
  HTTP request atacak şekilde çalışmadığından). Yerine iş kuralı tarafındaki **`FunctionParameterItem`** benzeri yapı
  kullanılacak: değer, **`AssignValueToFieldDto`** ile — içindeki enum **{ sabit değer, hesaplayarak, form alanı }** —
  belirlenir. Yani `degerTuru: String` yerine **tipli değer-kaynağı enum'u**.
- ➕ **Not:** Yeni tasarımda `async` (bool) alanı da var (`process-step.md §3.2`); ham dökümde yok — yeni projede eklenen.

> **Bağ:** `AssignValueToFieldDto`'nun değer-kaynağı enum'u, `models/enums/value-assign-type.md` (**ValueAssignType**:
> `fixedValue`/`propertyValue`/`fromCalculation`…) ile aynı ailedendir — HTTP parametre değer-kaynağı burada birleştirilebilir.

---

## 8. ❓ environmentRestriction (açık konu)

- Mevcut modellerde `environmentRestriction` her yerde `string`; "ortam kısıtı".
- **Karar:** Bu konu **açık konulara** (`todo.md`) eklenecek ve **daha sonra detaylı incelenecek** (enum mu, format mı, kapsam ne).

---

## 9. 🔁 Yeniden adlandırma haritası (özet)

| Eski (mevcut Flovo) | Yeni (bu proje) | Tür | Not |
|---|---|---|---|
| `ProcessSettingUserType` | `ProcessStepUserType` | 🔤 | 2 değer kaldırıldı |
| `StepTypeUserDto` | `ProcessStepTypeUser` | 🧩 | kaldırılan alanlar var |
| `ProcessSettingUserGroupType` | `ProcessStepUserGroupType` | 🔤 | 🟢 onaylandı |
| `StepTypeUserGroupDto` | `ProcessStepTypeUserGroup` | 🧩 | 🟢 onaylandı; `accountUserGroupId→organizationUserGroupId` |
| `StepTypeNotificationDto` | `ProcessStepSendNotification` | 🧩 | |
| `SendNotificationOnStepDto` | `SendNotificationMessages` | 🧩 | mesajlar dinamik liste; toast + parametre eklenecek |
| `NotificationStepTypesDto` | `SendNotificationUsers` | 🧩 | |
| `ProcessSettingStepType` (+ `…UserGroupType`) | `NotificationRecipientType` | 🔤 | 🟢 `{user, userGroup, takeUsersWhoTookActionBefore}` — alıcı türü; ayrı grup-enum'u foldlandı |
| `StepTypeTimerDto` | `ProcessStepTypeTimer` | 🧩 | 🟢 onaylandı |
| `WorkStyle` | `TimerCalculationType` | 🔤 | 🟢 onaylandı |
| `StepTypeFunctionDto` | (HTTP Request adım ayarı) | 🧩 | `method→HttpMethod` enum; parametre modeli iş-kuralına hizalanır |
| — | `ProcessStepType` | 🔤 | yeni; §3'teki 21 adımdan |
| — | `HttpMethod` | 🔤 | yeni; GET/POST/PUT/DELETE |
| — | `NotificationChannel` | 🔤 | yeni; `{mail, push, toast}` (Push/Mail bool'ları + Toast → dinamik kanal) |
| `WorkTimeSelection` | `WorkTimeSelection` | 🔤 | değerler netleşti → `{atWorkStart, atWorkEnd}` |
| `TimeAdjustmentOption` | `TimeAdjustmentOption` | 🔤 | değerler netleşti → `{hoursAfter, hoursBefore}` |
| `KeyboardType` | `KeyboardType` | 🔤 | değerler dolduruldu |
| `BarcodeFormat` | `BarcodeFormat` | 🔤 | değerler dolduruldu |

---

## 10. 🔎 İnceleme — kalan açık nokta

> Önceki inceleme maddeleri **karara bağlandı** ve dosyaya işlendi; bu başlıktan kaldırıldı. Kalan tek açık konu:

- **`environmentRestriction`** — `string` "ortam kısıtı"; enum/format/kapsam kararı **ertelendi** → `todo.md`'ye açık
  konu olarak eklenip **daha sonra detaylı incelenecek** (§8).

> **Ana modele (`models/enums/` + `service-settings/process-step.md §2`) geçerken uygulanacak — kararlar net, mekanik:**
> enum tip adları **İngilizce PascalCase** · enum değerleri **İngilizce camelCase** · **`field → property`** ·
> yazım düzeltmeleri (`degisgen→variable`, `departmant→department`, `postPoning→postponing`) · `resource → endpoint` ·
> `method → HttpMethod` · bildirim kanalları → dinamik + `NotificationChannel`.

---

*Kaynak: mevcut Flovo (`Pratico.Apps`) DTO/enum tanımları. Oluşturma: 2026-07-16 — ham nottan revize.*
