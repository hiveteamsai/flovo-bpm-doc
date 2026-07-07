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
| **Başlangıç / Bitiş** | Süreç Başlangıcı · **Alt Süreç Başlangıcı** · Süreç Bitişi |
| **İnsan görev (human task)** | Kullanıcı · Kullanıcı Grubu |
| **Otomatik / sistem** | HTTP Request · Flovo AI · Değer Atama · Karşılaştırma · Switch · Bildirim · Custom ID Creator · **Processing** (frontende form döner ama `default` ile otomatik ilerler → §3.18) |
| **Form & alt-servis** | Form Creator · Form Silme · Form Yönlendirme · Süreç Adımı Tetikleme |
| **Zamanlayıcı** | Timer · Timer Start · Timer End |

---

## 2. Adım Ortak Yapısı (her adımın temel alanları)
Tip-bağımsız: bu alanlar **her adımda** ortaktır; tipe özel ayarlar bunun üzerine gelir (§3 kataloğu).

| Alan | Tip | Açıklama |
|---|---|---|
| `code` | string | Adımın benzersiz kodu |
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
| `skipWithThisActionId` | int | Atlama yapılacak aksiyon ID'si |

### 2.1 — Adım ↔ Aksiyon ilişkisi
Her adıma bir veya birden fazla **aksiyon** tanımlanır; aksiyon, kontrolün bir sonraki adıma **nasıl geçeceğini** taşır.
Aksiyon türleri: **Manuel · withForm · Fotoğraf Çek · Dosya Seç · Barcode Tara · Webhook · Autoaction**
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

## 3. Adım Kataloğu (20 adım)
> Aşağıda her adımın **özeti** + (varsa) **detay ayarları** vardır. Sıra, kurucunun verdiği sıradır.
>
> **Tekrarlayan kavramlar:** **default action** (adımın varsayılan ilerleme aksiyonu) · **action modeli**
> (→ `process-step-action.md` §2) · **aksiyon alınabilir durum** (form atanan kullanıcı için işlem alınabilir hâle gelir =
> human task) · **alt servis** (form altındaki ilişkili süreç/form → `properties.md` §3.13 Form List).

### 3.1 — Süreç Başlangıcı
**Özet:** **Ana sürecin** başlama noktası (servis başına **1 zorunlu**). Altında yer alan **aksiyonların nasıl
başlatılabileceğini** ayarlamak için oluşturulur.
- **Manuel (frontend) başlatma:** Örn. altında bir **"Fotoğraf Çek"** aksiyonu var; bu aksiyonun **"aksiyon bekleyen
  formlar" listesi** sayfasında görünmesini istiyorsak, aksiyonu bu şekilde işaretleyerek frontend **manuel aksiyon
  görünümünü** aktif ederiz.
- **Dış (webhook) başlatma:** Süreç Başlangıcı **yalnız manuel değil**; altına eklenen bir **Webhook aksiyonu**
  (`process-step-action.md` §3.6) ile **uygulama dışından** da başlatılabilir — dış çağrı **yeni bir ana süreç çalıştırması
  (`WorkFlow`)** başlatır. Süreç Başlangıcı bir süreç adımı olduğundan bu aksiyon **ona bağlıdır**
  (`ProcessStepExecution.processStepId` sorunsuz atılır).
- Yani Süreç Başlangıcı, sürecin **nasıl başlatılacağını** (manuel **ve/veya** dış webhook) tanımlar. Altındaki aksiyon
  türleri → `process-step-action.md` §3.
> **Ayrım (anlam karmaşasını önle):** Hem **Süreç Başlangıcı** hem **§3.20 Alt Süreç Başlangıcı** dışarıdan **webhook** ile
> tetiklenebilir; **farkları:**
> - **Süreç Başlangıcı** = **ana süreci** başlatır (servis başına **1**); **manuel veya** webhook aksiyonu ile.
> - **Alt Süreç Başlangıcı** = ana süreçten **bağımsız bir alt süreci** başlatır (servis başına **N**; **manuel yok**;
>   webhook **veya** Süreç Adımı Tetikleme ile; insan-görev / süreç-bitişi **içermez**).

### 3.2 — HTTP Request
**Özet:** Bir dış endpoint'e (kullanıcının kendi sunucusu olabilir) HTTP isteği atan **otomatik** adım.

**Ayarlar:** `endpoint` (URL) · `method` (GET/POST/PUT/DELETE...) · `templateParameters` (URL şablon/path) ·
`queryParameters` · `headers` · `body` · `returns` (dönüş tipi/şeması) · `async` (bool).
**Parametre yapısı** (her parametre): `name` · `valueType` (sabit / form property'si / ifade) · `value`.

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
| `valueType` | enum | `FixedValue` (sabit) / `PropertyValue` (form property değeri) / `FromCalculation` (expression ile hesaplanan değer) |
| `fixedValue` | string | Sabit değer (`valueType=FixedValue`) |
| `expression` | string | Değeri üreten ifade (`valueType=FromCalculation`) |
| `useDisplay` | bool | Görüntü (display) değerini kullan |
| `targetPropertyId` | int | Hedef property (değerin yazılacağı alan) |
| `propertyId` | int | Kaynak property (`valueType=PropertyValue`) |

**Alt-servise değer atama:** `useRelatedService` (bool) · `relatedServiceId` (int) · `targetInstancesPropertyId`
(hedef alt-servis kayıt(lar) property'si).
> İki kapsam: **(a)** aynı formdaki property'ye, **(b)** alt-servis (Form List → `properties.md` §3.13) kayıtlarına.

### 3.5 — Süreç Adımı Tetikleme
**Özet:** Formda yer alan **alt servislerin** süreç adımlarını tetiklemek için kullanılır.
> _(Detay sonra eklenecek.)_

### 3.6 — Bildirim
**Özet:** **Mail, bildirim (push) veya toast** mesaj atmak için kullanılır. Statik kullanıcı(lar) seçilebilir; seçilen
kullanıcılara, girilen **dinamik mesaj** ile bildirim gönderilir.

**Kanallar (3 seçenek):** **Mail** · **Bildirim (Push)** · **Toast**. Başlık/mesaj **TR ve EN** ayrı girilir.

**Parametreler (yalnız Bildirim/Push ve Toast):** Bildirimle birlikte **`parameters`** gönderilebilir. Bu parametreler
**UI'da gösterilmez**; **çalışma zamanında veriyi güncellemek** için kullanılır (örn. `formId` + yeni alan değerleri →
frontend formu günceller). **Mail'de parametre yoktur.** _(örn. `../sampleProcess/expense`.)_

**Alıcılar:** Süreci başlatan · Sabit kullanıcı(lar) · Değişken kullanıcılar (önceki adımlardan) · Form property'sinden ·
Kullanıcı grubu · Daha önce aksiyon alanlar.
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

### 3.10 — Form Silme
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

### 3.12 — Form Creator
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
- **`conditionType`** — koşulların birleştirilmesi: **VE** (tümü) / **VEYA** (en az biri).
- **Operatörler:** `=` · `!=` · boş · boş değil · `>` · `>=` · `<` · `<=` · ile başlar · ile biter · içerir · içermez.

### 3.14 — Switch
**Özet:** Bir alan seçilir; o alandaki **değere göre** aksiyon tetiklenir. **Default aksiyon zorunludur**; eşleşen değer
yoksa default tetiklenir.

### 3.15 — Kullanıcı
**Özet:** İçinde **1 kullanıcı** seçilir; belirlenen kullanıcının **onayına** gider. Onaya giden kişi formu
**güncelleyebilir** ve form **aksiyon alınabilir** duruma gelir; seçili kullanıcı aksiyonlardan birini **manuel** tetikler.

**Kullanıcı belirleme yöntemi (`userType`):** Süreci başlatan · **Sabit kullanıcı** (`stableUserId`) · Kullanıcının
yöneticisi · Yönetici zinciri · Departman yöneticisi · Ünvana göre yönetici · **Değişken kullanıcı** (form property'sinden).

**Diğer ayarlar:** `processViewProfileId` (görüntüleme profili → `view-profile.md`) · adıma gelince **bildirim** · **timeout** (→ §3.7, `../flovo-bpm-engine.md` §6.2).

### 3.16 — Kullanıcı Grubu
**Özet:** **Birden fazla kullanıcıya** form, aksiyon alınabilir durumda iletilir; bunlardan **biri** manuel aksiyon alarak ilerletir.

**Grup belirleme yöntemi (`userGroupType`):** **Sabit kullanıcı grubu** (`organizationUserGroupId`) · **Dinamik kullanıcı
listesi** (form property'sinden) · **Dinamik kullanıcı grubu**.
**Diğer ayarlar:** `groupApproval` (hepsi mi / biri mi onaylasın) · görüntüleme profili · bildirim · timeout.

### 3.17 — Süreç Bitişi
**Özet:** Sürecin **son adımıdır**; kimsenin onayında beklemez, sürecin **bittiği** anlamına gelir. Yetkili kullanıcılar
altındaki aksiyonları **görüntüleyebilir** ve aksiyon alarak formu **önceki adımlara taşıyabilir**. Erişim:
**raporlardan** veya **daha önce aksiyon alınan form listesinden**.
**Ayarlar:** `processViewProfileId` (bitişte görüntüleme profili) · `organizationUserGroupIds` (bitiş sonrası erişebilecek gruplar).

### 3.18 — Processing
**Özet:** Form, **bir kullanıcıya** (Kullanıcı/Kullanıcı Grubu gibi) atanır; o kullanıcı bunu **"bu işlemin tamamlanmasını
bekleyenler"** listesinde görür. Form üzerinde **işlem alınamaz**.

**İlerleme (Kullanıcı/Kullanıcı Grubu'ndan farkı):** Bu adıma girildiğinde Kullanıcı/Kullanıcı Grubu gibi **frontende
form/response döner**; **fakat manuel aksiyon beklenmez** — adım **`default`** aksiyonuyla **otomatik ilerler** (motorda
otomatik adım gibi davranır → `../flovo-bpm-engine.md` §4.3 / §6.1).

**Ayar — `showLoading` (bool):** Bu adımdayken formun **detayına girilmesi** veya **alan değerlerinin görüntülenmesi**
istenmiyorsa **aktif edilir**; frontendde kullanıcı formu **"yükleniyor"** görür (giriş engellenir).
- **`true`** → form **loading** görünür (detay/değerler gizli). _(örn. `../sampleProcess/expense`.)_
- **`false`** → form **normal** görünür; genelde bir **durum güncellemesiyle** kullanıcıya güncel bilgi iletilir. _(örn. `../sampleProcess/integration`.)_

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
| Ne başlatır | **Ana süreç** (yeni `WorkFlow`) | **Bağımsız alt süreç** (yardımcı kol) |
| Nasıl başlar | Manuel (frontend) **veya** webhook aksiyonu | **Tetiklenerek** — webhook / Süreç Adımı Tetikleme (**manuel yok**) |
| Konum | Ana akış | Ana akıştan **bağımsız** alt akış |

**Nasıl tetiklenir (2 yol):**
1. **Dış — Webhook:** Uygulama dışından, **Flovo Customer API** ile tetiklenir (örn. müşteri sunucusu işini bitirince).
   "Kim tetikledi" → `ProcessStepExecution.atApiKeyId` (→ `../models/workFlows/process-step-execution.md`).
2. **İç — Süreç Adımı Tetikleme:** Başka bir sürecin **Süreç Adımı Tetikleme** (§3.5) adımı tarafından tetiklenir.

**Kısıtlar (alt süreç):**
- **Bağımsızlık:** Alt süreç ana sürecin **içinde yer almaz**; ana akıştan ayrık kurulur.
- **İçeremeyeceği adımlar:** **Kullanıcı (§3.15) · Kullanıcı Grubu (§3.16) · Processing (§3.18) · Süreç Bitişi (§3.17)** —
  insan-görev/bekleme veya "süreç sonu" içermez; kısa ömürlü, **otomatik ilerleyen** bir akıştır.
- Bir alt süreç kendi **tek** Alt Süreç Başlangıcı giriş düğümüyle başlar.

**Çalışma prensibi:**
- Adım **tetiklendiğinde**, kullanıcı eylemi beklenmeden **otomatik** olarak **`default`** aksiyonu çalışır ve **bir sonraki
  süreç adımına** ilerler.
- Tetikleme **girdisi bir `ActionTransfer` modelidir** (`parameters` · `changeList` · `action` → `process-step-action.md` §2).
  Bu girdi, **`default`** aksiyonu ile **bir sonraki adıma taşınır** (`changeList`, evrensel giriş kuralı gereği adım işini
  yapmadan **önce** forma uygulanır → `../flovo-bpm-engine.md` §4.2).
- **Yeni `WorkFlow` (bağımsız çalıştırma):** Tetiklenen alt süreç, ana süreçten **bağımsız, yeni bir `WorkFlow`** olarak
  çalışır; `WorkFlow.parentWorkFlowId`'ye **tetikleyen ana sürecin `WorkFlow` id'si** yazılır (→ `../models/workFlows/work-flow.md`).
> Örn. `../sampleProcess/createPdfAsync`: webhook `parameters: { pdfUrl }` ile `pdfReady` (Alt Süreç Başlangıcı) tetiklenir;
> **`default`**, `parameters: { formId, pdfUrl }`'i `notifyPdf` adımına taşır.

**Neden bu adım tipi (motor gerekçesi):** Webhook, önceden yalnızca bir **aksiyon** (`process-step-action.md` §3.6) olarak
modellendiğinden, süreçten bağımsız bir alt süreçte **bağlanacağı bir süreç adımı yoktu**; `ProcessStepExecution.processStepId`
**zorunlu** olduğu için yürütme kaydı doğru atılamıyordu. Alt Süreç Başlangıcı **bir süreç adımı** olduğundan, dışarıdan/başka
süreçten tetiklenen alt sürecin yürütmesi artık **geçerli `processStepId` ile** kaydedilir. Böylece webhook'u tutan aksiyon,
bu adıma bağlı **`default`** aksiyonuna dönüşür (örn. `../sampleProcess/createPdfAsync`).

**Ayarlar:** _(sonra detaylandırılacak — tetikleme kaynağı (webhook / iç tetikleme) · webhook güvenliği (secret/imza) +
idempotency → `process-step-action.md` §3.6 / `../flovo-customer-api.md`.)_

---

## 4. Açık Kararlar / Sorular
> **Açık sorular tek yerde:** Bu dokümanın açık kararları/soruları, tutarsızlığı önlemek için **yalnız** merkezi
> [`todo.md`](../todo.md) dosyasında toplanır (önceliklendirilmiş tüm-doküman listesi). İlgili maddeler orada `(process-step §..)`
> atfıyla bulunur; verilen kararlar bu dokümanın **gövdesinde** anlatılır.

> **Çözülenler (yerel karar log'u):**
- [x] **Alt Süreç Başlangıcı adım türü — ÇÖZÜLDÜ** (eski "Webhook/Triggered" açık sorusu): Bağımsız alt süreçlerin **giriş
  düğümü** için yeni **§3.20 Alt Süreç Başlangıcı** adımı eklendi. ("webhook" adı dar kaldığından — webhook **ve** Süreç Adımı
  Tetikleme (§3.5) ile tetiklenir.) Webhook'u tutan aksiyon artık bu adıma bağlı **`default`**'a dönüşür; Alt Süreç Başlangıcı
  bir **süreç adımı** olduğundan `ProcessStepExecution.processStepId` doğru atılır. **Ana süreç içinde** API ile ilerleme
  gerekiyorsa **Webhook aksiyonu** (`process-step-action.md` §3.6) kullanımı **korunur**. _(Örnek:
  `../sampleProcess/createPdfAsync/process.md` · `../models/workFlows/process-step-execution.md`.)_
- [x] **Alt süreç yürütmesinin runtime temsili — ÇÖZÜLDÜ:** Bağımsız alt süreç (Alt Süreç Başlangıcı ile başlayan) tetiklenince
  **ayrı, yeni bir `WorkFlow`** oluşur; **`WorkFlow.parentWorkFlowId`**'ye tetikleyen **ana sürecin `WorkFlow` id'si** yazılır
  (ana süreçlerde null). _(../models/workFlows/work-flow.md · process-step-execution.md · models.md)_

---

## 5. Notlar / Ham Düşünceler
> _(Buraya ham düşünceler; sonra yukarı işlenir.)_

---

*Oluşturma: 2026-06-26.*
