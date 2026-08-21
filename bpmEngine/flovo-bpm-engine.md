# Flovo BPM Motoru — Çalışma Prensibi (Tasarım Dokümanı)

> **Durum:** 🟢 DETAYLANIYOR — temel kavramlar / çalışma prensibi / yürütme algoritması dolduruldu; **§3 veri modeli = koleksiyon-tabanlı (v0.30)**; bazı bölümler (§2.2, §7, §8, §10, §11) founder/teknik girdi bekliyor.
> **Amaç:** Yeni Flovo'nun **BPM motorunun** nasıl çalışacağını (mimari + yürütme prensibi) tanımlamak.
> Bu doküman "hangi adımlar var" değil (→ `service-settings/process-step.md`), "adımlar ne yapar" değil (→ `service-settings/process-step-action.md`);
> **"motor bu adımları nasıl çalıştırır"** sorusunu cevaplar.
>
> **Referanslar:** n8n motoru nasıl çalışır → `research/n8n/n8n-motor-nasil-calisir.md` ·
> n8n adım envanteri → `research/n8n/n8n-surec-adimlari-analizi.md`
>
> **Not:** Bu klasördeki içerik bir karar/ürün tanımıdır; n8n dosyaları yalnızca **referans/ilham**tır.

---

## 0. Özet (bir paragraf)
Flovo BPM motoru, **süreç adımlarından** oluşan bir akışı, adımdan adıma **aksiyon (action)** ile ilerleterek
yürütür. Her adım, **kontrol kendisine geldiğinde** kendi işini yapar; işini bitirince **ürettiği parametreleri**
ilerleyeceği **aksiyon ile birlikte** bir sonraki adıma taşır (→ `service-settings/process-step-action.md` §2 veri aktarım modeli).
Adımlar iki türdür: **otomatik (sistem) adımları** (HTTP Request, Switch, Karşılaştırma, Flovo AI, Değer Atama,
Timer...) işlerini yapıp **uygun aksiyonla kendiliğinden** ilerler; **insan-tetiklemeli (human task) adımları**
(Kullanıcı, Kullanıcı Grubu, Üst Form Kullanıcı) süreci **durdurur**, formu atanan kullanıcıların **aksiyonuna** bırakır.

---

## 1. Temel Kavramlar ve Bileşenler
> Bir servis hangi **temel kavram ve bileşenlerden** oluşur, bunlar nasıl ilişkilenir.

### 1.1 — Temel Kavramlar
- **Servis (Service / Form):** Motorun temel birimi; **bir iş sürecinin tamamı** (örn. İzin Talebi, Satın Alma,
  Masraf Formu). Her servisin kendi **property'leri, süreç adımları, aksiyonları, durumları, iş kuralları ve
  görüntüleme profilleri** vardır. Servisin **davranış türü** **`formType`** ile belirlenir: **`form`** (akış+onay+sahipli
  `Instance`) · **`parameter`** (onaysız veri-kaynağı; sahipsiz `Instance`) · **`eventForm`** (akışsız/`Instance`'sız pop-up
  formu) → `models/service-settings/service.md`.
- **Organization (Organizasyon):** Kiracıyı temsil eder (→ `organization-settings/organization.md`).
- **Solution (Çözüm):** Bir veya birden çok servisi barındıran paket.
> Çok-kiracılık ve izolasyon → §9.

### 1.2 — Bileşenler (Building Blocks)
Bir servis **yedi yapı taşından** oluşur ve bunlar **iki katmana** ayrılır (krş. `service-settings/business-rule.md` §0):

| # | Bileşen | Katman | Ne işe yarar | Doküman |
|---|---|---|---|---|
| 1 | **Property'ler** (form alanları) | form | Formdaki giriş/görüntüleme elemanları | `service-settings/properties.md` |
| 2 | **Görüntüleme Profilleri** | form | Formun adım-bazlı görünümü (görünür/düzenlenebilir/zorunlu) | `service-settings/view-profile.md` |
| 3 | **İş Kuralları** | **form (frontend-realtime)** | Koşullu anlık form davranışı (göster/gizle, validasyon, değer, stil) | `service-settings/business-rule.md` |
| 4 | **Süreç Adımları** | **akış (motor)** | İş akışının rotası (adım tipleri) | `service-settings/process-step.md` |
| 5 | **Aksiyonlar** | **akış (motor)** | Adımlar arası **geçiş birimi** (kod + veri taşır); şablonu **ActionDto** | `service-settings/process-step-action.md` · `organization-settings/action.md` |
| 6 | **Durumlar** | akış | Kaydın mevcut aşaması (etiket) | `organization-settings/status.md` |
| 7 | **Stiller** | çapraz-kesen | Renk/görünüm varlığı (aksiyon, durum...) | `organization-settings/style.md` |

> **Katman ayrımı (kritik):** **form-mantığı** (property + profil + iş kuralı) **frontend'de, realtime** çalışır;
> **akış-mantığı** (adım + aksiyon + durum) **motorda** çalışır. İş kuralları motoru doğrudan etkilemez
> (→ `service-settings/business-rule.md` §0). **Style** çapraz-kesen bir bileşendir (→ `organization-settings/style.md`).

### 1.3 — Bileşenler Arası İlişkiler
| İlişki | Açıklama |
|---|---|
| Property → Görüntüleme Profili | Profil, hangi property'nin nasıl gösterileceğini belirler |
| Property → İş Kuralı | İş kuralları property değerlerine göre tetiklenir (frontend) |
| Görüntüleme Profili → İş Kuralı | Kurallar belirli profillerde çalışacak şekilde sınırlanabilir (`activeViewProfiles`) |
| Görüntüleme Profili → Süreç Adımı | Her adıma bir profil atanır (`processViewProfileId`) |
| Süreç Adımı → Aksiyon | Her adımın altında, ilerlemeyi taşıyan aksiyonlar bulunur |
| Aksiyon → Durum | Aksiyon tetiklendiğinde kaydın durumu değişebilir (`changeStatusId`) |
| Aksiyon → Süreç Adımı | Tetiklenen aksiyon, **`targetProcessStepId`** ile bir sonraki adıma yönlendirir (→ §4) |

> **Çalışma prensibi (iki katman):** Adım, işinin sonucunu bir **aksiyon koduna** eşler (`default`/`onFail`/`true`/
> `false`/switch/`response.action`) ve kendi adımındaki o kodlu **aksiyonu seçer**; seçilen aksiyonun
> **`targetProcessStepId`**'si **hangi adıma** ilerleneceğini belirler. **Kod = aksiyon seçimi · `targetProcessStepId`
> = adım yönlendirmesi** (`targetProcessStepId` **korunur** → §4).

### 1.4 — Tasarım Hedefleri
> Ürün hedefleri (bağlam). Bunlara bağlı **açık kararlar** merkezi `todo.md`'de izlenir.
- **Self-servis olgunluk** — süreçleri teknik-olmayan kullanıcı kursun (→ §2.1).
- **Hız/performans** — hızlı form/belge yükleme, hafif iş-kuralı değerlendirmesi.
- **Sade katman sınırı** — değer atama & karşılaştırma hem adım hem iş kuralı; sınır kararı → `todo.md` (Tier 0 "İki-katman sınırı") · `service-settings/business-rule.md` §6.

---

## 2. Motor Mimarisi (Orkestrasyon vs Yürütme)

### 2.1 — Tasarım Zamanı (Design-Time): bir süreç nasıl kurulur
> Bir süreç şu sırayla tasarlanır (hedef: **self-servis** — teknik-olmayan kullanıcı da kurabilsin):
1. **Property'ler** — alanları tanımla (kontrol tipi, etiket, veri kaynağı, kısıtlar).
2. **Görüntüleme Profilleri** — hangi alan nerede görünür/düzenlenir/zorunlu.
3. **İş Kuralları** — koşul → anlık form davranışı (frontend).
4. **Aksiyonlar** — şablon (**`ActionDto`**): kod, ikon, **actionType**, **styleId** (→ `organization-settings/action.md`).
5. **Durumlar** — `definition` + `styleId`.
6. **Süreç Adımları** — adım sırası/tipi, kullanıcı atama, **aksiyonları adımlara bağlama**.

> **[Hedef]** Bu sırayı **şablon + görsel akış editörü** ile **teknik-olmayan kullanıcıya** açmak; elle bağlama yükünü azaltmak (→ §1.4).

### 2.2 — Orkestrasyon vs Yürütme (çalışma zamanı mimarisi)
> _(Founder/teknik karar bekliyor. n8n dersi 1–2: orkestrasyonu yürütmeden ayır; durum DB'de, kuyruk yalnız iş
> ID'leri, worker'lar durumsuz.)_
- Süreçler/bileşenler: **(açık)**
- Tek-süreç mi, kuyruk-tabanlı dağıtık worker mı?: **teknoloji kararı verildi** (MVP Core BPM monolith → Hexagonal + **NATS kuyruk** + **durumsuz worker** → [`tech-stack/`](tech-stack/index.md)); **motor-içi orkestrasyon↔yürütme detayı açık → §12.**
- **Bulut + on-prem hibrit** dağıtım: **teknoloji kararı verildi** (on-prem + Private Cloud ready — K8s/Helm + Keycloak federasyon → [`tech-stack/`](tech-stack/index.md)); **operasyon detayı → §12.**

---

## 3. Veri Modeli ve Akışı
> **KARAR (v0.30) — koleksiyon-tabanlı.** Adımlar arası veri, **yapılandırılmış bir değer koleksiyonu** olarak **açıkça**
> (aksiyonla) akar; klasik BPMN'in token-tabanlı (kontrol token'ı + yan-kanal süreç değişkenleri) modeli **değildir**.

- **Veri birimi = `InstanceValue.data` ile aynı değer-modeli.** Akan koleksiyon, **`propertyValuesTemplates`** şekillerinden
  oluşur: skaler · `LabeledValue {value, display, translationCode}` · user-ref `{userId, nameSurname}` · phone
  `{countryCode, number}` · list-of-model (formList/file/groupByTaxReceipt) … Böylece **kullanıcı formu · aksiyon aktarımı
  (`changeList`/`parameters`) · Customer API** aynı **tek değer dilini** konuşur; bir değer adımdan adıma **veya** forma
  **kayıpsız** taşınır (ara dönüşüm/stringify yok). _(→ `models/processInstances/propertyValuesTemplates/index.md` · `instance-value.md`.)_
- **Adımlar arası aktarım = Aksiyon veri aktarım modeli** (→ `service-settings/process-step-action.md` §2):
  - **`changeList`** = **forma yazılan kalıcı** alan değerleri; **obje-map** `{ Property.code: value }`; §4.2'de forma
    **doğrudan JSONB merge** (`data = data || changeList`). Yalnız **yazılabilir** alanlara dokunur (`text` / `live` yansıma /
    `savePropertyToDb=false` istisnaları — bunlara değer yazılmaz).
  - **`parameters`** = adımlar arası **geçici** veri (**forma yazılmaz**); değer şekli aynı, ama **anahtar serbesttir**
    (bir form alanını besliyorsa konvansiyon olarak hedef `Property.code` kullanılır — zorunlu değil); `mergeParameter` ile
    zincir boyunca birikir (§2.1).
  - **`action`** = HTTP Request response'undan **zincirleme tetikleme** (kod eşleşmesi).
- **Bütünsel değer taşıma (KARAR):** Bir alanın değeri **model/dizi** ise (formList/groupByTaxReceipt/phone/mapViewer…),
  alt-alanlardan biri değişse bile o alanın **tüm değeri komple** taşınır — **kısmi patch yok** (merge o `code`'daki değeri
  bütünüyle değiştirir).
- **Kapsam sınırı:** Buradaki "koleksiyon-tabanlı" **temsil**i anlatır (payload = yapılandırılmış değer koleksiyonu).
  n8n'in **item-dizisi + otomatik per-item fan-out** (`runIndex`) semantiği **bu kararla gelmez**; çok-kayıt iterasyonu /
  loop / join hâlâ **ayrı açık başlıktır** (→ §4.5 · paralel dallanma, `todo.md`).
- **Soy ağacı (lineage):** parametre kaynağı, `mergeParameter` zinciri + `ProcessStepInstance` geçmişiyle izlenir
  (n8n `pairedItem` muadili ayrıntı sonra netleşecek).

---

## 4. Yürütme Algoritması

### 4.1 — Temel prensip: adımlar + aksiyonla ilerleme
Bir süreç, **süreç adımlarından** oluşan bir akıştır. Kontrol, adımdan adıma **aksiyon (action)** ile ilerler.
Her süreç adımı, **kontrol kendisine geldiğinde** kendi işini yapar (→ işlerin özeti `service-settings/process-step.md` §3);
işini tamamlayınca, **eğer bir parametre ürettiyse** bu parametreleri ilerleyeceği **aksiyon ile birlikte**
bir sonraki süreç adımına aktarır.

> Motorun ortak **"geçiş birimi" = action**'dır: hem akışı ilerletir, hem (varsa) veriyi (`parameters`) taşır,
> hem (varsa) form alanlarını (`changeList`) günceller. Bu, Flovo motorunu n8n'in örtük "konveyör" akışından
> ayıran temel tasarım kararıdır (n8n'de veri örtük akar; Flovo'da **niyetli/explicit** olarak action taşır).

### 4.2 — Her adımın giriş kuralı: önce `changeList` uygula
Aksiyonlar bir **`changeList`** taşır (→ `service-settings/process-step-action.md` §2): formdaki alanların **yeni değerleri**,
aksiyonla birlikte bir sonraki adıma iletilebilir. **Tüm süreç adımları, kendi işini yapmadan ÖNCE** şu
**evrensel kontrolü** uygular:

> **EĞER** gelen aksiyonun `changeList`'i **boş değilse** → `changeList`'teki form alanı değerlerini **güncelle**;
> **SONRA** adım kendi işine devam eder.

Bu, adım tipinden **bağımsız ortak bir ön-adımdır** (otomatik da olsa insan-tetiklemeli de olsa aynı). Yani
form state'i, her adım işini yapmadan önce **güncel hâle getirilir** — böylece karar veren adımlar (örn.
Karşılaştırma / Switch / Değer Atama) **en güncel form değerleriyle** çalışır.

### 4.3 — İki adım sınıfı: otomatik vs insan-tetiklemeli
Adımlar, **nasıl ilerledikleri** açısından ikiye ayrılır:

**A) Otomatik (sistem) adımları** — kontrol geldiğinde işini yapar ve **uygun aksiyonla otomatik** olarak bir
sonraki adıma ilerler; insan beklemez:

| Adım | İşini yapınca ilerlediği aksiyon |
|---|---|
| **Karşılaştırma** | koşul doğruysa `true`, değilse `false` aksiyonu |
| **Switch** | alandaki değere **eşleşen** aksiyon (yoksa **default**) |
| **HTTP Request** | response'taki `action` koduyla **aynı kodlu** aksiyon (boşsa/**async** ise **default** kodlu aksiyon) |
| **Flovo AI** | başarılıysa **`default`** (parametre taşır); hata olursa **`onFail`** |
| **Değer Atama** | işini yapar, ilerler |
| **Timer** | süre dolunca **default action** |
| **Bildirim** | bildirimi atar, ilerler |
| **Processing** | frontende form/response döner; **`default` kodlu `autoAction` varsa** onunla otomatik ilerler, **yoksa** bu adımda **bekler** (webhook/aksiyon gelene dek) |
| **Instance Creator · Süreç Adımı Tetikleme · Custom ID Creator · Timer Start/End** | işini yapıp ilerler |
| **Silme (Instance Deleter) · Yönlendirme (Form Yönlendirme)** | işini yapar; **giden aksiyonu varsa** ilerler, **yoksa kol burada sonlanır** (terminal olabilir → §4.4) |

**B) İnsan-tetiklemeli (human task) adımları** — süreç burada **durur ve bekler**; form **"aksiyon alınabilir"**
hâle gelir:
- **Kullanıcı / Kullanıcı Grubu** adımları. _(**Processing** frontende form/response döndürür; **`default` kodlu `autoAction` varsa**
  beklemeden ilerler (A grubu), **yoksa** burada **bekler** (B grubu — webhook/aksiyon gelene dek). Krş. §6.1.)_
- **Üst Form Kullanıcı** adımı (alt-servis) — Kullanıcı/Kullanıcı Grubu gibi bekler, **fakat** atananları ve görüntüleme
  profilini **kendi ayarında tutmaz**: bağlı olduğu **üst formun (parent instance)** güncel atananlarını (`InstanceAwaitingUser`)
  ve **`code`-eşleşen** görüntüleme profilini **anlık** devralır (→ `service-settings/process-step.md` §3.22).
- **`manual`, `eventForm`, `takePhoto`, `selectFile`, `scanBarcode`** aksiyonları **kullanıcı tarafından
  frontend'de** tetiklenir.
- Kullanıcılar, **kendilerinin (kullanıcı veya kullanıcı grubu üyesi olarak) yer aldığı** ve **o süreç adımında
  bekleyen** formları kendi listelerinde görür.
- Atanan kullanıcı, aksiyonlardan birini **manuel** seçerek tetikler → süreç ilerler (parametre/changeList taşınır).

> İnsan-tetiklemeli adımlar = motorun **bekle/devam-et** noktalarıdır (→ §6); süreç state'i kalıcılaştırılıp
> günlerce bekleyebilmelidir.

> **Adım atlama (skip):** Kullanıcı / Kullanıcı Grubu adımlarında **`skipIfPreApproved`** (önceden onaylanmışsa) veya
> **`skipIfUserProcessStarter`** (başlatan kullanıcıysa) aktifken, adımda **aksiyon alacak kişi = bu adımdan önce son onayı
> veren** (veya süreci **başlatan**) ise, form kullanıcıya **sunulmaz**; süreç **döngüye girmesin** diye
> **`skipWithThisProcessStepActionId`**'deki `ProcessStepAction` **otomatik tetiklenerek** ilerletilir — yani bu durumda adım
> bir **bekleme noktası olmaz** (→ `service-settings/process-step.md` §2).

### 4.4 — Yürütme döngüsü (pseudo)
```text
adım        = Başlangıç                               # ana süreç: Süreç Başlangıcı · alt süreç: Alt Süreç Başlangıcı
gelenAction = null                                   # kontrolü bu adıma getiren aksiyon

while adım bir BİTİŞ düğümü değilse:                   # Süreç Bitişi (ana) / Alt Süreç Bitişi (alt süreç) → aşağıdaki not
    # ── EVRENSEL GİRİŞ KURALI (her adımda, iş yapılmadan ÖNCE) ──
    if gelenAction?.changeList boş değilse:
        formAlanlarınıGüncelle(gelenAction.changeList)        # yeni değerleri forma yaz
    gelenParametreler = gelenAction?.parameters ?? {}         # bu adıma GELEN (in) parametreler

    # ── Adım kendi işini yapar ──
    if adım.tür == OTOMATİK:
        sonuç       = adım.işiniYap()
        gelenAction = adım.uygunAksiyonuSeç(sonuç)            # true/false · switch · response.action · default
        if gelenAction yoksa:                                 # terminal otomatik adım — giden aksiyon yok
            break                                             #   → kol burada sonlanır (ör. Instance Deleter / Form Yönlendirme)
        gelenAction.parameters = adım.ürettiğiParametreler()  # adımın ürettiği (out) — opsiyonel
    else:  # İNSAN-TETİKLEMELİ (Kullanıcı / Kullanıcı Grubu / Üst Form Kullanıcı)
        atanan = adım.atananıÇöz()                            # userType / userGroupType ile
        # Üst Form Kullanıcı (§3.22): atanan = üst formun güncel InstanceAwaitingUser'ı (anlık çözülür),
        #   görüntüleme profili = üst formun aktif adımının profil code'uyla eşleşen profil (yoksa isDefault)
        # ── ADIM ATLAMA (skip): önceki son onaylayan/başlatan aynı kişiyse döngüye girme (→ process-step §2) ──
        if (adım.skipIfPreApproved and atanan == öncekiSonOnaylayan) \
           or (adım.skipIfUserProcessStarter and atanan == süreçBaşlatan):
            gelenAction = adım.skipWithThisProcessStepActionId  # otomatik tetiklenir — BEKLENMEZ
        else:
            form.durum = "aksiyon alınabilir"
            göster(atanan, bekleyenFormListesi)               # atananlar formu listede görür
            gelenAction = bekle()                             # frontend: manuel / eventForm (changeList + out parameters taşır)

    # ── PARAMETRE BİRLEŞTİRME: mergeParameter ise gelen(in) korunur, üretilen(out) üstüne yazılır (→ process-actions §2.1)
    if gelenAction.mergeParameter:
        gelenAction.parameters = { ...gelenParametreler, ...(gelenAction.parameters ?? {}) }   # out ezer

    adım = gelenAction.targetProcessStepId                   # seçilen aksiyonun hedef adımı (binding → process-actions §1.2)
# BİTİŞ düğümü: kimseyi bekletmez; kol/süreç biter.
#   • Süreç Bitişi (§3.17)      — ana süreç; yetkililer sonradan erişebilir/geri taşıyabilir.
#   • Alt Süreç Bitişi (§3.21)  — bağımsız alt süreç; geri-taşıma yoktur.
# Ayrıca terminal bir otomatik adım (giden aksiyonu olmayan) yukarıdaki `break` ile de kolu sonlandırabilir.
```

### 4.5 — Henüz netleşmeyenler (→ §12)
- **Paralel dallanma / eşzamanlı kollar** var mı? (Şimdiye kadar anlatım **tek aktif adım / doğrusal-dallı**
  ilerleme; n8n'in çok-girdili "join/senkronizasyon"unun Flovo karşılığı tanımlı değil.)
- Bir adım **aynı anda birden çok sonraki adımı** tetikleyebilir mi, yoksa her zaman tek `action` → tek hedef mi?
- **Alt servisler (Form List)** ana süreçle eşzamanlı mı yürür? _(Kısmen netleşti: **ServiceTrigger** ilişki değişiminde
  alt-servisin alt sürecini tetikler — §5.3; **Üst Form Kullanıcı** ile alt-servis üst formun atananlarını devralır. Eşzamanlı
  **join/senkronizasyon** hâlâ açık.)_

---

## 5. Tetikleme ve Zamanlama

### 5.1 — Süreç başlatma
- Kullanıcı **yeni kayıt** oluşturduğunda süreç **Süreç Başlangıcı** adımından başlar (→ `service-settings/process-step.md` §3.1).
- **Süreç Başlangıcı**, altındaki **başlatma aksiyonlarının** frontend'de nasıl görüneceğini ayarlar (örn.
  `takePhoto` (Fotoğraf Çek) aksiyonunun **"aksiyon bekleyen formlar"** listesinde görünmesi) — yani sürecin **kullanıcı
  tarafından nasıl başlatılacağını** tanımlar.
- İlk **görüntüleme profili** yüklenir, form render edilir, **iş kuralları (frontend)** çalışır (→ §6.1, `service-settings/business-rule.md`).

### 5.2 — Zaman-tabanlı tetikleme
- **Timer** adımı (→ `service-settings/process-step.md` §3.7) süreçten bağımsız, **cron-benzeri** dinamik süre tanımlar; süre
  dolunca **default action** ile ilerler. **Timer Start / Timer End** ile yaşam döngüsü yönetilir.
> _(**ServiceTrigger** olay-tabanlı (ilişki değişimi) ve timer tetiklemeyi sağlar → §5.3. Açık kalan: **webhook/mesaj** olay
> tetikleme + çok-örneklilikte "en-fazla-bir-kez" / lider seçimi — n8n dersi 3 → §12.)_

### 5.3 — Olay/otomatik tetikleme (ServiceTrigger)
Bir servise bağlı **ServiceTrigger**'lar akıştan bağımsız **otomatik** çalışır (→ `models/service-settings/service-trigger.md`):
- **`whenAddedAssociate` / `whenRemoveAssociate`** — servisin **ilişki alanı** (Form List / `isAssociatedCombobox` Combobox)
  değişince (`AssociatedInstance` yazımı/silmesi; **DB-katmanı çekirdek** tespiti) **hedef instance'ın `subProcessStart`'ını**
  tetikler; parametre kaynağı ilişkiyi kuran üst form (`associatedInstanceId`), yürütme hedefi işaret edilen form (`instanceId`).
- **`timer`** — `cronExpression`'a göre hedef servisin **`processStart`**'ını çalıştırıp **yeni bağımsız bir ana süreç** başlatır.
- **`async`** ile tetikleyen işlem beklenir/beklenmez (bekleme **tetiklendiği yerde**).
> Böylece bir formdaki **ilişki değişikliği** veya bir **zamanlama**, süreci **akıştan bağımsız** tetikler. Alt-süreç mekaniği
> → `service-settings/process-step.md` §3.20.

---

## 6. Bekle / Devam Et ve Uzun-Soluklu Süreçler (İnsan-Döngüde)

### 6.1 — İnsan-tetiklemeli bekleme
**Kullanıcı / Kullanıcı Grubu** adımları motorun **bekle/devam-et** noktalarıdır (→ §4.3):
form **"aksiyon alınabilir"** hâle gelir, atanan kullanıcıların **bekleyen formlar** listesinde görünür ve
süreç, kullanıcı bir **manuel / eventForm aksiyonu** tetikleyene kadar **durur**. Süreç state'i **kalıcılaştırılıp
günlerce** bekleyebilmelidir (→ §8; n8n dersi 8: kalıcılaştır-ve-devam-et).
> **Processing** — otomatik ilerlemesi **opsiyoneldir:** adımda **`default` kodlu `autoAction`** aksiyonu **varsa** manuel
> aksiyon beklemeden onunla otomatik ilerler (bekleme noktası değildir); **yoksa** frontende form/response döndürüp bu adımda
> **bekler** — ilerleme dış **webhook**/başka aksiyonla olur (ör. `sampleProcess/integration`) (→ `service-settings/process-step.md` §3.18).

### 6.2 — Zaman Aşımı (Timeout)
Kullanıcı/grup adımlarında **timeout** tanımlanabilir; süre dolunca:
- **otomatik bildirim** gönderilebilir,
- belirlenen **aksiyonla otomatik ilerleme** yapılabilir.

Hesaplama tipleri: **çalışma takvimine göre** (iş günü/saat) · **normal takvime göre** (erteleme opsiyonlu) ·
**sabit zaman**.
> _(Açık: mesaj/olay bekleme (receive), uyuyan sürecin uyandırılması, retry/bekleme → §7 / §12.)_

### 6.3 — Aksiyon tetikleme isteğine response (form bilgileri)
Kullanıcı bir aksiyonu **manuel** tetiklediğinde frontend bir **HTTP request** gönderir. Süreç, bu aksiyonun ardından
**Kullanıcı · Kullanıcı Grubu · Üst Form Kullanıcı · Processing · Süreç Bitişi** adımlarından birine geldiğinde, **form bilgileri** bu
**tetikleme isteğinin response'unda** kullanıcıya geri döner.

> Yani bu **beş adım** = sürecin **kullanıcıya form döndürdüğü** duraklardır (formun gösterileceği adımlar). Processing'de
> **`showLoading`** ile form "yükleniyor" gösterilip giriş engellenebilir (→ `service-settings/process-step.md` §3.18). Frontende ek
> **veri itme**, **Bildirim**'in parametre seçeneğiyle de yapılabilir (→ `service-settings/process-step.md` §3.6).

---

## 7. Hata Yönetimi

### 7.1 — Adım-seviyesi hata yönlendirmesi: `onFail` aksiyonu
Bir adım işini yaparken **hata oluşursa**, adımın **`onFail` kodlu aksiyonu** tetiklenir (örn. Flovo AI hata
verirse → `onFail`; HTTP Request başarısız olursa → `onFail`). Yani hata, **`default` (başarı) akışından ayrı
bir koda** yönlendirilir. Bu, n8n'in "hata-çıkış dalı"nın (n8n dersi 9) Flovo karşılığıdır — ama burada **isimli
bir aksiyon kodu** olarak modellenir (`default` ↔ `onFail`).

> _(Doldurulacak / açık sorular: Her adımda `onFail` zorunlu/var mı, yoksa bazılarında mı? **Retry**
> (yeniden deneme + bekleme) olacak mı? **Süreç-seviye** hata akışı (global hata yakalayıcı) olacak mı?
> **Telafi/compensation** ve **denetim izi** nasıl ele alınacak?)_

---

## 8. Kalıcılık, Durum ve Denetim
- **Süreç geçmişi:** adımlar/aksiyonlar geçmişte tutulur — `showInHistory` (öğe **geçmişte görünür** mü); aksiyon tamamlanınca kullanıcıya tarihçeyi **otomatik gösterme** = `showHistory` (ayrı alan).
- **Çoklu dil:** metin alanları çeviri destekli; bildirimler TR/EN ayrı.
> _(Doldurulacak: ne saklanır — süreç tanımı · çalıştırma kaydı (instance/state) · veri · dosya/binary. Durum yaşam
> döngüsü (new / running / waiting / done). Saklama/pruning. **Denetim izi** (kurumsal/KVKK). **Dosya/binary depolama performansı**.)_

---

## 9. Ölçekleme ve Çok-Kiracılık (Multi-tenancy)
- İzolasyon **üç başlıkla**: `organizationId` (organizasyon/kiracı) · `solutionId` (çözüm) · `serviceId` (servis).
- **Platform:** mobil (iOS/Android) + Web tek kod tabanı.
> _(Doldurulacak: organizasyon-bazlı izolasyon, eşzamanlılık, yatay ölçekleme, kuyruk/worker (→ §2.2), on-prem ↔ bulut hibrit (→ §12).)_

---

## 10. Güvenlik
> _(Doldurulacak. n8n dersi 6: expression/kod değerlendirme = sert güvenlik sınırı (izolasyon baştan).
> Credential şifreleme, yetki/sandbox (Execute Command benzeri riskli adımlar), KVKK.)_

---

## 11. AI Entegrasyonu (Motor Seviyesinde)
> _(Doldurulacak. AI adımı motora nasıl gömülür — deterministik "AI adımı" vs otonom "ajan"? Takılabilir-strateji
> (model/memory/araç) deseni? "Herhangi bir adım = araç" + MCP? n8n cluster-node mimarisi referans.)_

---

## 12. Açık Kararlar / Çözülecek Sorular

> **Açık sorular tek yerde:** Bu dokümanın açık kararları/soruları, tutarsızlığı önlemek için **yalnız** merkezi
> [`todo.md`](todo.md) dosyasında toplanır (önceliklendirilmiş tüm-doküman listesi). İlgili maddeler orada `(flovo-bpm-engine §..)`
> atfıyla bulunur; verilen kararlar bu dokümanın **gövdesinde** anlatılır.

---

## 13. Notlar / Ham Düşünceler (toparlanmayı bekleyen)
> _(Buraya kurucunun ham düşünceleri yapıştırılır; sonra yukarıdaki bölümlere işlenir.)_

---

*Oluşturma: 2026-06-26 · Taslak iskelet; içerik kurucunun girdileriyle doldurulacaktır.*
