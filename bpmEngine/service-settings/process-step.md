# Flovo — Süreç Adımları (Process Steps) Tasarımı

> **Durum:** 🟢 DETAYLANIYOR — adım kataloğu + ortak yapı tanımlı; bazı yeni adımların detayı doldurulacak.
> **Amaç:** Flovo BPM motorunun **adım tipleri katalogunu** tanımlamak — "hangi süreç adımı **tipleri** var?"
> (Bir adımın **içinde** ne yapıldığı → `process-step-action.md`; adımların **nasıl çalıştırıldığı** → `../flovo-bpm-engine.md`.)
>
> **Terim:** Bir **süreç adımı (process step)** = iş akışındaki bir düğüm/kutu. Adımlar bağlanarak süreci oluşturur.

---

## 0. Adım Nedir?
> _(Doldurulacak: bir "süreç adımı"nın tanımı, girdisi/çıktısı, görsel temsili.)_

---

## 1. Adım Taksonomisi (kategoriler)
| Kategori | Flovo adımları |
|---|---|
| **Başlangıç / Bitiş** | Süreç Başlangıcı · **Alt Süreç Başlangıcı** · Süreç Bitişi · **Alt Süreç Bitişi** |
| **İnsan görev (human task)** | Kullanıcı · Kullanıcı Grubu · **Üst Form Kullanıcı** (atananları/görüntülemeyi **üst formdan** devralır → §3.22) |
| **Otomatik / sistem** | HTTP Request · Flovo AI · Değer Atama · Karşılaştırma · Switch · Bildirim · Custom ID Creator · **Processing** (`default` kodlu `autoAction` varsa otomatik ilerler, yoksa bekler → §3.18) |
| **Form & alt-servis** | Instance Creator · Instance Deleter · Form Yönlendirme · Süreç Adımı Tetikleme |
| **Zamanlayıcı** | Timer · Timer Start · Timer End |

---

## 2. Adım Ortak Yapısı (her adımın temel alanları)
Tip-bağımsız: bu alanlar **her adımda** ortaktır; tipe özel ayarlar bunun üzerine gelir (§3 kataloğu).

| Alan | Tip | Açıklama |
|---|---|---|
| `code` | string | Adımın benzersiz kodu |
| `stepType` | ProcessStepType | **Adım tipi ayrımlayıcısı** — tipe-özel ayarların (§3) nasıl yorumlanacağını belirler (→ `../models/enums/process-step-type.md`) |
| `settings` | jsonb | **Tipe-özel ayarlar** — şekli `stepType`'a göre değişir (§3); modelde `ProcessStep` satırında **JSONB** kolon (→ `../models/service-settings/process-step.md` §2/§3) |
| `definition` | string | Adımın adı/tanımı |
| `environmentRestriction` | string | Ortam kısıtlaması |
| `id` | int | Veritabanı ID'si |
| `organizationId` | int | Organizasyon ID'si (FK → `../organization-settings/organization.md` `id`) |
| `serviceId` | int | Bağlı servis ID'si |
| `icon` | string | Adım ikonu |
| `order` | int | Sıralama (sürükle-bırak) |
| `hideInHistory` | bool | Süreç geçmişinde gizle |
| `skipIfPreApproved` | bool | Önceden onaylanmışsa adımı atla |
| `skipIfUserProcessStarter` | bool | Başlatan kullanıcıysa adımı atla |
| `skipWithThisProcessStepActionId` | int | Atlamada **otomatik tetiklenecek `ProcessStepAction`** (adıma bağlı aksiyon) |

> **Adım atlama (`skipIfPreApproved` · `skipWithThisProcessStepActionId`):** **Kullanıcı (§3.15) / Kullanıcı Grubu (§3.16)**
> adımlarında geçerlidir. **`skipIfPreApproved`** aktifken, bu adımdan **önce son onayı veren kişi** ile bu adımda **aksiyon
> alacak kişi aynıysa**, süreç **döngüye girmesin** diye adım kullanıcıya sunulmadan **otomatik ilerletilir**: bunun için
> **`skipWithThisProcessStepActionId`**'deki **`ProcessStepAction`** otomatik tetiklenir (Action **şablonuna** değil, adıma
> bağlı aksiyona işaret eder). _(Benzer: `skipIfUserProcessStarter` — aksiyonu alacak kişi süreci **başlatan** kullanıcıysa atlar.)_

### 2.1 — Adım ↔ Aksiyon ilişkisi
Her adıma bir veya birden fazla **aksiyon** tanımlanır; aksiyon, kontrolün bir sonraki adıma **nasıl geçeceğini** taşır.
Aksiyon türleri: **`manual` · `eventForm` · `takePhoto` · `selectFile` · `scanBarcode` · `webhook` · `autoAction`**
(→ `process-step-action.md` §3). Detay → `process-step-action.md` / `../organization-settings/action.md`.

### 2.2 — Detay şablonu (her adım tipini tarif ederken)
```
### <Adım Adı>
- **Amaç:**
- **Girdi:** (ne alır)
- **Çıktı:** (ne üretir; kaç çıkış dalı)
- **Yapabildiği aksiyonlar:** (→ process-step-action.md)
- **Ayarlar:**
```

---

## 3. Adım Kataloğu (22 adım)
> Aşağıda her adımın **özeti** + (varsa) **detay ayarları** vardır. Sıra, kurucunun verdiği sıradır.
>
> **Tekrarlayan kavramlar:** **default action** (adımın varsayılan ilerleme aksiyonu) · **action modeli**
> (→ `process-step-action.md` §2) · **aksiyon alınabilir durum** (form atanan kullanıcı için işlem alınabilir hâle gelir =
> human task) · **alt servis** (form altındaki ilişkili süreç/form → `properties.md` §3.13 Form List).
>
> **`default action` hangi adımlarda var?** **Her adımda değildir.** İşini yapıp **tek yolla** ilerleyen otomatik
> adımlarda bulunur: **Değer Atama · HTTP Request** (response'ta `action` dönmezse / `async`) **· Processing** (koşullu: `default autoAction` varsa; yoksa bekler → §3.18) **· Bildirim ·
> Timer Start / Timer End · Custom ID Creator** vb. **Birden fazla çıkışı** olan adımlarda ise ilerleme aksiyonu
> **adıma-özel / dinamik** belirlenir: **Karşılaştırma** → koşul `true` ise `true`, değilse `false` aksiyonu · **Switch** →
> seçilen alanın değerine **eşleşen `code`'lu** aksiyon (eşleşme yoksa **default**). _(Motor tarafı → `../flovo-bpm-engine.md` §4.3.)_

### 3.1 — Süreç Başlangıcı
**Özet:** **Ana sürecin** başlama noktası (servis başına **1 zorunlu**). Altında yer alan **aksiyonların nasıl
başlatılabileceğini** ayarlamak için oluşturulur.
- **Manuel (frontend) başlatma:** Örn. altında bir **`takePhoto` (Fotoğraf Çek)** aksiyonu var; bu aksiyonun **"aksiyon bekleyen
  formlar" listesi** sayfasında görünmesini istiyorsak, aksiyonu bu şekilde işaretleyerek frontend **manuel aksiyon
  görünümünü** aktif ederiz.
- **Dış (webhook) başlatma:** Süreç Başlangıcı **yalnız manuel değil**; altına eklenen bir **Webhook aksiyonu**
  (`process-step-action.md` §3.6) ile **uygulama dışından** da başlatılabilir — dış çağrı **yeni bir ana süreç çalıştırması
  (`ProcessInstance`)** başlatır. Süreç Başlangıcı bir süreç adımı olduğundan bu aksiyon **ona bağlıdır**
  (`ProcessStepInstance.processStepId` sorunsuz atılır).
- Yani Süreç Başlangıcı, sürecin **nasıl başlatılacağını** (manuel **ve/veya** dış webhook) tanımlar. Altındaki aksiyon
  türleri → `process-step-action.md` §3.
- **Kim başlatabilir (`userGroupId` kısıtı):** Süreç Başlangıcı, **manuel başlatmayı** bir kullanıcı grubuna kısıtlayabilir
  (`userGroupId` → `../models/service-settings/process-step.md` §3.14). **Görünürlük = tetikleme yetkisi:** `userGroupId`
  **boş** → **herkes** başlangıç aksiyonlarını **görür ve** başlatır; **dolu** → **yalnız o gruptaki** kullanıcılar **görür ve**
  başlatır, **grup dışı kullanıcı bu aksiyonları görmez** (ayrı "görür ama tetikleyemez" durumu yoktur). **Webhook / Customer
  API** başlatımı bu kısıttan **etkilenmez** — kullanıcı değil **`ApiKey`** ile kimliklendirilir; dış erişim yetkisi ayrı
  katmandadır (→ `../flovo-customer-api.md`).
> **Ayrım (anlam karmaşasını önle):** Hem **Süreç Başlangıcı** hem **§3.20 Alt Süreç Başlangıcı** dışarıdan **webhook** ile
> tetiklenebilir; **farkları:**
> - **Süreç Başlangıcı** = **ana süreci** başlatır (servis başına **1**); **manuel veya** webhook aksiyonu ile.
> - **Alt Süreç Başlangıcı** = ana süreçten **bağımsız bir alt süreci** başlatır (servis başına **N**; **manuel yok**;
>   webhook **veya** Süreç Adımı Tetikleme ile; insan-görev / süreç-bitişi **içermez**).

### 3.2 — HTTP Request
**Özet:** Bir dış endpoint'e (kullanıcının kendi sunucusu olabilir) HTTP isteği atan **otomatik** adım.

**Ayarlar:** `endpoint` (URL) · `method` (**HttpMethod**: GET/POST/PUT/DELETE → [`../models/enums/http-method.md`](../models/enums/http-method.md)) · `templateParameters` (URL şablon/path) ·
`queryParameters` · `headers` · `body` · `async` (bool).
**Parametre yapısı** (`DynamicParameter`, her parametre): `name` · `value` (değer kaynağı **ValueAssignType**: sabit / form property / hesaplama).

**Çalışma:**
1. Adım tetiklendiğinde, ayarlardaki her alan **yapılandırıldığı gibi** istek atılır.
2. İstek sonucunda geriye bir **action modeli** beklenir.
3. **Dönen `action` doluysa:** bu adımda yer alan **aynı koda sahip** aksiyon, response'tan dönen `parameters` ve
   `changeList` ile süreci ilerletir.
4. **Dönen `action` boşsa:** **`default`** kodlu aksiyon ile devam eder.

**Async modu (`async = true`):** İstek atılır **ama** sonuç **beklenmez**; doğrudan **`default`** aksiyonla devam edilir.
> Örn. senkron: `../sampleProcess/createPdf` · async: `../sampleProcess/createPdfAsync`, `../sampleProcess/integration`.

### 3.3 — Flovo AI
**Özet:** Flovo'nun geliştirdiği AI'ları çalıştıran **otomatik** adım; sonucu **parametre** olarak sonraki adıma taşır.

**Ayarlar:**
- Geliştirilmiş **AI listesi**nden kullanılacak AI seçilir; seçilen AI'a **özel ayarlar** açılır.
- AI'ın işleyeceği **dosyanın kaynağı**: formun **thumbnail** dosyası **veya** bir **file alanı** (→ `properties.md` §3.8).

**Çalışma:** Adım tetiklendiğinde AI çalışır, **parametre üretir**.
- **Başarılı** → **`default`** aksiyon (parametreyi taşıyarak).
- **Hata** → **`onFail`** aksiyonu (→ `../flovo-bpm-engine.md` §7).

**Başlangıçta planlanan AI'lar:** **Masraf · Fatura · Kredi Kartı Ekstresi** (üçü de parametre olarak dosya alır).
> Örn. `../sampleProcess/expense`.

### 3.4 — Değer Atama
**Özet:** Formdaki bir **property'ye veya** formun altındaki **alt servislere**; **statik** ya da **hesaplayarak**
değer atamak için kullanılır.

**Veri modeli (atama tanımı):**
| Alan | Tip | Açıklama |
|---|---|---|
| `valueAssignType` | ValueAssignType | Değer kaynağı — Değer Atama'da geçerli **alt-küme**: `fixedValue` (sabit) / `propertyValue` (form property değeri) / `fromCalculation` (expression ile hesaplanan değer). _(Enum'un `fromDataSet`/`search`/`httpRequest` değerleri yalnız iş kuralı `assignValueToProperty` içindir; bu adımda geçersiz — JSON Schema ile kısıtlanır.)_ |
| `fixedValue` | string | Sabit değer (`valueAssignType=fixedValue`) |
| `expression` | string | Değeri üreten ifade (`valueAssignType=fromCalculation`) |
| `useDisplay` | bool | Görüntü (display) değerini kullan |
| `targetPropertyId` | int | Hedef property (değerin yazılacağı alan) |
| `propertyId` | int | Kaynak property (`valueAssignType=propertyValue`) |

**Alt-servise değer atama:** `useAssociatedService` (bool) · `associatedServiceId` (int) · `targetInstancesPropertyId`
(hedef alt-servis kayıt(lar) property'si).
> İki kapsam: **(a)** aynı formdaki property'ye, **(b)** alt-servis (Form List → `properties.md` §3.13) kayıtlarına.

### 3.5 — Süreç Adımı Tetikleme
**Özet:** Formda yer alan **alt servislerin** süreç adımlarını tetiklemek için kullanılır.
> _(Detay sonra eklenecek.)_

### 3.6 — Bildirim
**Özet:** **Mail, bildirim (push) veya toast** mesaj atmak için kullanılır. Statik kullanıcı(lar) seçilebilir; seçilen
kullanıcılara, girilen **dinamik mesaj** ile bildirim gönderilir.

**Kanallar (3 seçenek):** **Mail** · **Bildirim (Push)** · **Toast** (→ [`../models/enums/notification-channel.md`](../models/enums/notification-channel.md)). Başlık/mesaj **dil-başına** (dinamik `{languageCode, text}` listesi) girilir.

**Parametreler (yalnız Bildirim/Push ve Toast):** Bildirimle birlikte **`parameters`** gönderilebilir. Bu parametreler
**UI'da gösterilmez**; **çalışma zamanında veriyi güncellemek** için kullanılır (örn. `instanceId` + yeni alan değerleri →
frontend formu günceller). **Mail'de parametre yoktur.** _(örn. `../sampleProcess/expense`.)_

**Alıcılar:** Süreci başlatan · Sabit kullanıcı(lar) · Değişken kullanıcılar (önceki adımlardan) · Form property'sinden ·
Kullanıcı grubu · Daha önce aksiyon alanlar. Her alıcı, **birincil alıcı** yerine **CC** (bilgi) olarak da eklenebilir
(`addToCc` → mail/bildirim kopyası; ana muhatap değil).
**Dinamik mesaj değişkenleri:** `#ProcessCreator` · `#ProcessState` · `#ProcessStartDate` · `#ServiceName` (+ form property'leri).

**İlerleme:** Bildirimi atar ve **`default`** aksiyonla ilerler.

### 3.7 — Timer
**Özet:** **Süreçten bağımsız** olarak oluşturulur. İçinde **dinamik süre** belirlenir (cron benzeri). Süre dolunca
**`default`** aksiyonla ilerler.

**Süre hesabı (3 stil):**
- **Çalışma takvimine göre** — iş günü + çalışma saatleri.
- **Normal takvime göre** — takvim günleri; **erteleme** opsiyonu (saat önce/sonra).
- **Sabit zaman** — belirli tarih/saat.

**Zaman aşımı bildirimi:** süre dolduğunda bildirim gönderilebilir.
> Aynı zaman-aşımı yapısı **Kullanıcı / Kullanıcı Grubu** adımlarının **timeout** ayarında da kullanılır (→ §3.15 / §3.16, `../flovo-bpm-engine.md` §6.2).

### 3.8 — Timer Start
**Özet:** Bir timer seçilir ve o timer'ın süresini **başlatır** (`selectedTimerProcessStepId`). İşini yapıp **`default`** ile ilerler.

### 3.9 — Timer End
**Özet:** Bir timer seçilir ve **daha önce başlatılmış** olanı **sonlandırır** (`selectedTimerProcessStepId`). İşini yapıp **`default`** ile ilerler.

### 3.10 — Instance Deleter
**Özet:** Formu siler (örn. `deleted` durumuna çeker).
> _(Detay sonra eklenecek.)_

### 3.11 — Custom ID Creator
**Özet:** Özel formatlı **benzersiz numara/ID** üretir ve bir property'ye yazar.
| Ayar | Açıklama |
|---|---|
| `customId` | ID format şablonu (örn. ön ek + sıra no + tarih) |
| `targetPropertyId` | Üretilen ID'nin yazılacağı **property** |
| `createWithBarcode` | Barkod ile oluştur (bool) |
| `targetFilePropertyId` | Barkod görselinin yazılacağı **file property** |

### 3.12 — Instance Creator
**Özet:** Form id'si, alanları vb. oluşturur (yeni form üretir).

**Ayar — başlangıç (init) değerleri:** oluşturulacak forma **init değerler** girilebilir:
- bir **alana (property) karşılık gelen değer**, veya **thumbnail url**.
- Atanacak değer, **aksiyondan gelen `parameters`** ile **eşleştirilerek** ayarlanır.
- Form oluşturulurken gelen `parameters` ile **alanlara initial değer atanarak** form üretilir.
> Örn. `../sampleProcess/scanBarcode` (barcode init) · `../sampleProcess/expense` (thumbnail url).

### 3.13 — Karşılaştırma
**Özet:** Girilen **koşullara göre** aksiyon tetikler. Koşullar **doğruysa `true`**, **sağlanmıyorsa `false`** aksiyonunu
tetikler (IF benzeri iki dallı).
- **`conditions`** — koşul listesi (referans değer · operatör · karşılaştırılan değer; **iç içe** gruplanabilir).
- **`conditionType`** — koşulların birleştirilmesi: **`and`** (VE, tümü) / **`or`** (VEYA, en az biri).
- **Operatörler (`criterionType`):** `equals` · `notEquals` · `isEmpty` · `isNotEmpty` · `greaterThan` · `greaterThanOrEqual` · `lessThan` · `lessThanOrEqual` · `startsWith` · `endsWith` · `contains` · `notContains` (→ `../models/enums/criterion-type.md`).

### 3.14 — Switch
**Özet:** Bir alan seçilir; o alandaki **değere göre** aksiyon tetiklenir. **Default aksiyon zorunludur**; eşleşen değer
yoksa default tetiklenir.

### 3.15 — Kullanıcı
**Özet:** İçinde **1 kullanıcı** seçilir; belirlenen kullanıcının **onayına** gider. Onaya giden kişi formu
**güncelleyebilir** ve form **aksiyon alınabilir** duruma gelir; seçili kullanıcı aksiyonlardan birini **manuel** tetikler.

**Kullanıcı belirleme yöntemi (`userType` → [`../models/enums/process-step-user-type.md`](../models/enums/process-step-user-type.md)):**
Süreci başlatan · **Sabit kullanıcı** (`fixedUserId`) · **Kullanıcının yöneticisi** · Departman yöneticisi ·
**Değişken kullanıcı** (form property'sinden). _(Eski "yönetici zinciri" ve "ünvana göre yönetici" kaldırıldı — aktif değildi.)_

> **"Kullanıcının yöneticisi" — hangi kullanıcının?** Bu yöntem seçildiğinde yönetici, **kaynak bir süreç adımında son
> onayı veren** kişiye göre belirlenir (`userAdministratorSourceProcessStepId` → o adımda **son aksiyonu alan** kullanıcının
> yöneticisi bu adımın sahibi olur). Böylece "yönetici" muğlak kalmaz, belirli bir adımın onaylayanına bağlanır.

**Diğer ayarlar:** `processViewProfileId` (görüntüleme profili → `view-profile.md`) · adıma gelince **bildirim** · **timeout** (→ §3.7, `../flovo-bpm-engine.md` §6.2).

### 3.16 — Kullanıcı Grubu
**Özet:** **Birden fazla kullanıcıya** form, aksiyon alınabilir durumda iletilir; bunlardan **biri** manuel aksiyon alarak ilerletir.

**Grup belirleme yöntemi (`userGroupType`):** **Sabit kullanıcı grubu** (`userGroupId`) · **Dinamik kullanıcı
listesi** (form property'sinden) · **Dinamik kullanıcı grubu**.
**Diğer ayarlar:** görüntüleme profili · bildirim · timeout.
> _(İlk fazda **grup "hepsi onaylar" eşiği yok**: gruba iletilen formda **bir** üye aksiyon alınca süreç ilerler.)_

### 3.17 — Süreç Bitişi
**Özet:** Sürecin **son adımıdır**; kimsenin onayında beklemez, sürecin **bittiği** anlamına gelir.

**İstisna — yetkili geri-taşıma (re-open):** Bu adıma da **aksiyonlar bağlanabilir**; istisna durumlar için, **yalnız
yetkili kullanıcı grupları** (`userGroupIds`) bu aksiyonları **görüntüleyip tetikleyebilir**. Bir aksiyon
tetiklendiğinde süreç kapanmış sayılmaz — aksiyonun **`targetProcessStepId`**'sindeki **farklı bir süreç adımına**
ilerler. Bu, **aynı `ProcessInstance` üzerinde** yeniden başlatmadır (yeni çalıştırma **açılmaz**).
> **Örnek:** Süreç Bitişi'ne **"ters kayıt"** aksiyonu eklenir; hedefi (**`targetProcessStepId`**) **muhasebe** adımıdır.
> Yetkili grup bu aksiyonu görüp tetiklediğinde süreç **muhasebe** adımına ilerler.

**Erişim:** **raporlardan** veya **daha önce aksiyon alınan form listesinden**.
**Ayarlar:** `processViewProfileId` (bitişte görüntüleme profili) · `userGroupIds` (bitiş sonrası erişip
geri-taşıma aksiyonu **alabilecek** gruplar).
> Motor tarafı: BİTİŞ düğümü yürütme döngüsünü sonlandırır; geri-taşıma, yetkilinin **manuel aksiyonu** ile aynı instance'ta
> **yeniden başlar** (→ `../flovo-bpm-engine.md` §4.4).

### 3.18 — Processing
**Özet:** Form, **bir kullanıcıya** (Kullanıcı/Kullanıcı Grubu gibi) atanır; o kullanıcı bunu **"bu işlemin tamamlanmasını
bekleyenler"** listesinde görür. Form üzerinde **işlem alınamaz**.

**İlerleme (opsiyonel otomatik ilerleme):** Bu adıma girildiğinde Kullanıcı/Kullanıcı Grubu gibi **frontende form/response döner.**
Otomatik ilerleme **opsiyoneldir**:
- Adımda **`default` kodlu, `actionType = autoAction`** bir aksiyon **varsa** → manuel aksiyon beklenmeden onunla **otomatik ilerler**
  (motorda otomatik adım gibi davranır; ör. `../sampleProcess/expense` — loading gösterip AI adımına ilerler).
- **Yoksa** → süreç bu adımda **bekler**; ilerleme, adıma tanımlı bir **webhook** (veya başka) aksiyonun dışarıdan tetiklenmesiyle
  olur (ör. `../sampleProcess/integration` — aktarım sonucunu webhook ile bekler).
_(→ `../flovo-bpm-engine.md` §4.3 / §6.1.)_

**Ayar — `showLoading` (bool):** Bu adımdayken formun **detayına girilmesi** veya **alan değerlerinin görüntülenmesi**
istenmiyorsa **aktif edilir**; frontendde kullanıcı formu **"yükleniyor"** görür (giriş engellenir).
- **`true`** → form **loading** görünür (detay/değerler gizli). _(örn. `../sampleProcess/expense`.)_
- **`false`** → form **normal** görünür; genelde bir **durum güncellemesiyle** kullanıcıya güncel bilgi iletilir. _(örn. `../sampleProcess/integration`.)_

> **Processing'in kendine özel bir "durum değişimi" yoktur.** Durum (status), her adımda olduğu gibi **aksiyon ilerlerken**
> (aksiyonun `changeStatusId`'si) değişir — **adımın içinde** değil. `false` seçeneğindeki "güncel bilgi", adıma
> **girişini sağlayan** (Processing'e ilerleten) aksiyonun `changeStatusId`'siyle iletilir; Processing adımında ayrı bir status alanı tutulmaz.

### 3.19 — Form Yönlendirme
**Özet:** Form **create edilmeden önce**, belli bir **karşılaştırma/işlem** yapılıp **farklı, var olan bir formun**
açılması istendiğinde kullanılır.
> Örn. `../sampleProcess/scanBarcode` (barkodla var olan formu açma).

### 3.20 — Alt Süreç Başlangıcı
**Özet:** Ana süreçten **bağımsız**, aynı servise hizmet eden fakat ana akışın içinde yer **almayan** bir **alt sürecin
başlangıç/giriş düğümü**. Kısa ömürlü, tek bir işi yapıp kapanan yardımcı akışlar içindir (örn. dışarıda hazırlanan bir
PDF geldiğinde bildirim gönderen kol). **Servis başına birden fazla** olabilir.

**Süreç Başlangıcı'ndan (§3.1) farkı:**
| | Süreç Başlangıcı (§3.1) | Alt Süreç Başlangıcı (§3.20) |
|---|---|---|
| Servis başına | **1 zorunlu** | **N (opsiyonel)** |
| Ne başlatır | **Ana süreç** (yeni `ProcessInstance`) | **Bağımsız alt süreç** (yardımcı kol) |
| Nasıl başlar | Manuel (frontend) **veya** webhook aksiyonu | **Tetiklenerek** — webhook / Süreç Adımı Tetikleme (**manuel yok**) |
| Konum | Ana akış | Ana akıştan **bağımsız** alt akış |

**Nasıl tetiklenir (3 yol):**
1. **Dış — Webhook:** Uygulama dışından, **Flovo Customer API** ile tetiklenir (örn. müşteri sunucusu işini bitirince).
   "Kim tetikledi" → `ProcessStepInstance.atApiKeyId` (→ `../models/processInstances/process-step-instance.md`).
2. **İç — Süreç Adımı Tetikleme:** Başka bir sürecin **Süreç Adımı Tetikleme** (§3.5) adımı tarafından tetiklenir.
3. **Otomatik — ServiceTrigger (associate):** Servisin ilişki alanı (Form List / `isAssociatedCombobox` Combobox) değişince
   `whenAddedAssociate`/`whenRemoveAssociate` trigger'ı, **hedef instance'ın** `subProcessStart`'ını **akış-dışı** otomatik
   çalıştırır (→ `../models/service-settings/service-trigger.md`).

**Kısıtlar (alt süreç):**
- **Bağımsızlık:** Alt süreç ana sürecin **içinde yer almaz**; ana akıştan ayrık kurulur.
- **İçeremeyeceği adımlar:** **Kullanıcı (§3.15) · Kullanıcı Grubu (§3.16) · Processing (§3.18) · Süreç Bitişi (§3.17)** —
  insan-görev/bekleme veya (ana süreç) "süreç sonu" içermez; kısa ömürlü, **otomatik ilerleyen** bir akıştır.
- Bir alt süreç kendi **tek** Alt Süreç Başlangıcı giriş düğümüyle başlar ve **Alt Süreç Bitişi (§3.21)** ile sonlanır
  (ana sürecin Süreç Bitişi'nin alt-süreç karşılığı).

**Çalışma prensibi:**
- Adım **tetiklendiğinde**, kullanıcı eylemi beklenmeden **otomatik** olarak **`default`** aksiyonu çalışır ve **bir sonraki
  süreç adımına** ilerler.
- Tetikleme **girdisi bir `ActionTransfer` modelidir** (`parameters` · `changeList` · `action` → `process-step-action.md` §2).
  Bu girdi, **`default`** aksiyonu ile **bir sonraki adıma taşınır** (`changeList`, evrensel giriş kuralı gereği adım işini
  yapmadan **önce** forma uygulanır → `../flovo-bpm-engine.md` §4.2).
- **Yeni `ProcessInstance` (bağımsız çalıştırma):** Tetiklenen alt süreç **yeni bir `ProcessInstance`** olarak
  çalışır (yeni **Instance/form kaydı** oluşmaz); `ProcessInstance.parentProcessInstanceId`'ye alt sürecin koştuğu **hedef/host instance'ın ana `ProcessInstance` id'si** yazılır (**tetikleyen** süreç değil; instance'a bağ bu zincirle **dolaylı**dır) (→ `../models/processInstances/process-instance.md`).
> Örn. `../sampleProcess/createPdfAsync`: webhook `parameters: { pdfUrl }` ile `pdfReady` (Alt Süreç Başlangıcı) tetiklenir;
> **`default`**, `parameters: { instanceId, pdfUrl }`'i `notifyPdf` adımına taşır.

**Neden bu adım tipi (motor gerekçesi):** Webhook, önceden yalnızca bir **aksiyon** (`process-step-action.md` §3.6) olarak
modellendiğinden, süreçten bağımsız bir alt süreçte **bağlanacağı bir süreç adımı yoktu**; `ProcessStepInstance.processStepId`
**zorunlu** olduğu için yürütme kaydı doğru atılamıyordu. Alt Süreç Başlangıcı **bir süreç adımı** olduğundan, dışarıdan/başka
süreçten tetiklenen alt sürecin yürütmesi artık **geçerli `processStepId` ile** kaydedilir. Böylece webhook'u tutan aksiyon,
bu adıma bağlı **`default`** aksiyonuna dönüşür (örn. `../sampleProcess/createPdfAsync`).

**Ayarlar:** _(sonra detaylandırılacak — tetikleme kaynağı (webhook / iç tetikleme) · webhook güvenliği (secret/imza) +
idempotency → `process-step-action.md` §3.6 / `../flovo-customer-api.md`.)_

### 3.21 — Alt Süreç Bitişi
**Özet:** Bir **alt sürecin son adımıdır** — ana sürecin **Süreç Bitişi (§3.17)**'nin alt-süreç karşılığı. Alt süreç
kısa ömürlü ve otomatik ilerlediğinden, kolun **açık bir bitiş düğümüyle** sonlanmasını sağlar: motor bu adıma
ulaştığında alt süreç yürütmesi **sonlanır** (yürütme döngüsünün çıkış düğümü → `../flovo-bpm-engine.md` §4.4).

**Süreç Bitişi'nden (§3.17) farkı:** Alt süreç bağımsız ve yardımcı bir koldur; **kimseyi onayda bekletmez** ve
**geri-taşıma / re-open** yoktur. Bu yüzden Süreç Bitişi'nin bitiş-sonrası erişim ayarları (`processViewProfileId` /
`userGroupIds`) **burada yoktur** — Alt Süreç Bitişi **ayarsızdır**.

**Neden ayrı adım tipi:** Alt Süreç Başlangıcı (§3.20) alt sürecin girişini açık bir süreç adımı yaptı; simetrik
biçimde Alt Süreç Bitişi de **çıkışı** açık bir düğüm yapar. Böylece "aksiyonu olmayan otomatik adımın kolu ima yoluyla
bitirmesi" belirsizliği ortadan kalkar; her alt süreç kolunun **tanımlı bir sonu** olur.

**Ayarlar:** — (**ayarsız**; alt süreç bu adımda sonlanır).

### 3.22 — Üst Form Kullanıcı (Parent Instance User)
**Özet:** Kullanıcı / Kullanıcı Grubu'na benzer, **aksiyon-onayına giden** bir insan-görev adımı; farkı: **atananları
(aksiyon bekleyenler) ve görüntüleme profilini kendi ayarında tutmaz — bunları bağlı olduğu üst formdan (parent instance)
devralır.** Bir formun altında çalışan **yardımcı/alt-servisler** içindir: alt-servis, üst formla **paralel ilerletilmeye
çalışılmadan** (senkronizasyon + performans yükü olmadan) üst formun **güncel** aksiyon-alabilenlerine ve görünümüne
**bağlanır**.

**Neden bu adım (motor gerekçesi):** Bir ana form (örn. **masraf formu**) Form List ile alt-servis kayıtları (örn. **masraf**)
barındırır. Ana form süreçte ilerledikçe (yönetici → muhasebe …) alt-servis kayıtları üzerinde de **aynı kişilerin** düzenleme/
aksiyon alabilmesi istenir. Alt-servisin sürecini ana forma **paralel ilerletmek** (her adımda ikisini de senkron tutmak)
hem **sync** hem **performans** açısından pahalıdır. Bu adım, alt-servis kaydını üst formun **o anki** görünümüne/atananlarına
**bağlar** — kopyalamaz, **anlık çözer**.

**Ayarlar:**
| Ayar | Açıklama |
|---|---|
| `parentServiceId` | **Üst formun servisi** — ilişkiyi kuran alanın bulunduğu servis (örn. *masraf formu*). |
| `associatedPropertyId` | Üst formdaki **ilişki alanı** — yalnız `AssociatedInstance` bağlantısı kuran alanlar seçilebilir: **Form List** veya **Combobox (`isAssociatedCombobox`)**. |

> **Seçilebilir alan filtresi:** Yalnız **bu servisi hedefleyen** ilişki alanları listelenir — Form List `childServiceId` =
> bu servis, **veya** Combobox `associatedServiceId` = bu servis. Böylece seçilen alan, üst formdan **bu** alt-servise işaret eder.

> **Bu adımda YOKTUR:** `processViewProfileId` (görüntüleme profili) **seçimi** ve **aksiyon bekleyenler** (atama) seçimi —
> ikisi de üst formdan devralınır (aşağıdaki çalışma).

**Çalışma (runtime):**
1. Alt-servis kaydı (Instance) bu adıma girer.
2. **Üst form tespiti:** `AssociatedInstance` içinde `instanceId = <bu instance>` **ve** `associatedPropertyId =
   <settings.associatedPropertyId>` olan kayıt bulunur; **`associatedInstanceId` = üst form (parent instance)**'dur.
   _(Model yönü: ilişkiyi kuran alan üst formun içindedir → `associatedInstanceId` üst forma denk gelir →
   `../models/processInstances/associated-instance.md`.)_
3. **Görüntüleme profili (code ile eşleşme):** Üst formun **o anki aktif adımının** görüntüleme profilinin `code`'u alınır;
   **bu alt-servis içinde aynı `code`'a sahip** `ProcessViewProfile` kullanılır. Aynı kodlu profil **yoksa** alt-servisin
   **`isDefault = true`** profili kullanılır (→ `view-profile.md`).
4. **Aksiyon bekleyenler (anlık devralma):** Üst formun **güncel `InstanceAwaitingUser`** kümesi bu alt-servis kaydının
   aksiyon-alabilenleri olur. _(Öneri: bu küme **kopyalanmaz**, **okuma-zamanında** üst form üzerinden çözülür — senkronizasyon
   yükünü önlemek bu adımın asıl amacıdır; kopyalama-vs-anlık kararı → `../todo.md`.)_
5. Devralınan kullanıcı(lar) alt-servis kaydını **code-eşleşen profil** ile görür/düzenler ve **alt-servisin kendi
   aksiyonlarını** alır; aksiyon alındığında alt-servis **kendi sürecinde** ilerler (yalnız görünüm + atananlar devralınır;
   veri/aksiyon/ilerleme alt-servisin kendisinindir).

> **Not (kenar durumlar → `../todo.md`):** üst formda **eşleşen kayıt bulunamazsa** (henüz bağlanmamış / bağ kaldırılmış),
> üst form **otomatik bir adımda** olup aksiyon bekleyeni yokken, **birden fazla üst form** eşleştiğinde ve üst form
> **Süreç Bitişi**'ne ulaştığında bu adımın davranışı **açık** (→ Tier 2 "Üst Form Kullanıcı — kenar durumlar").

---

## 4. Açık Kararlar / Sorular
> **Açık sorular tek yerde:** Bu dokümanın açık kararları/soruları, tutarsızlığı önlemek için **yalnız** merkezi
> [`todo.md`](../todo.md) dosyasında toplanır (önceliklendirilmiş tüm-doküman listesi). İlgili maddeler orada `(process-step §..)`
> atfıyla bulunur; verilen kararlar bu dokümanın **gövdesinde** anlatılır.

> **Çözülenler (yerel karar log'u):**
- [x] **Alt Süreç Başlangıcı adım türü — ÇÖZÜLDÜ** (eski "Webhook/Triggered" açık sorusu): Bağımsız alt süreçlerin **giriş
  düğümü** için yeni **§3.20 Alt Süreç Başlangıcı** adımı eklendi. ("webhook" adı dar kaldığından — webhook **ve** Süreç Adımı
  Tetikleme (§3.5) ile tetiklenir.) Webhook'u tutan aksiyon artık bu adıma bağlı **`default`**'a dönüşür; Alt Süreç Başlangıcı
  bir **süreç adımı** olduğundan `ProcessStepInstance.processStepId` doğru atılır. **Ana süreç içinde** API ile ilerleme
  gerekiyorsa **Webhook aksiyonu** (`process-step-action.md` §3.6) kullanımı **korunur**. _(Örnek:
  `../sampleProcess/createPdfAsync/process.md` · `../models/processInstances/process-step-instance.md`.)_
- [x] **Alt süreç yürütmesinin runtime temsili — ÇÖZÜLDÜ:** Bağımsız alt süreç (Alt Süreç Başlangıcı ile başlayan) tetiklenince
  **ayrı, yeni bir `ProcessInstance`** oluşur (yeni **Instance/form kaydı** oluşmaz); **`ProcessInstance.parentProcessInstanceId`**'ye alt sürecin koştuğu
  **hedef/host instance'ın ana `ProcessInstance` id'si** yazılır (**tetikleyen** süreç değil; ana süreçlerde null). Instance'a bağ `parentProcessInstanceId`
  zinciriyle **dolaylı**dır (`ProcessInstance`'a ayrı `instance` alanı eklenmez). _(../models/processInstances/process-instance.md · process-step-instance.md · index.md)_

---

## 5. Notlar / Ham Düşünceler
> _(Buraya ham düşünceler; sonra yukarı işlenir.)_

---

*Oluşturma: 2026-06-26.*
