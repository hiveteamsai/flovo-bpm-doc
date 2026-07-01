# n8n Süreç Adımları (Node) Analizi — Yeni Flovo BPM Motoru İçin Referans

> **Amaç:** Yeni yapılacak Flovo'nun **BPM motorunu** tasarlamadan önce, pazarın en hızlı büyüyen
> node-tabanlı iş akışı motoru olan **n8n**'in **her bir süreç adımını** (node tipini) ve o adımlarda
> **yapılabilecek özellikleri** çıkartmak. Bu doküman bir "ne yapmalıyız" kararı değil, bir
> **yetenek envanteri / yapı taşı haritasıdır**. Tasarım kararları ayrı dokümanlarda alınacaktır.
>
> **Kaynak:** n8n resmi dokümanları (`docs.n8n.io`) + n8n GitHub kaynak kodu (`@n8n/nodes-langchain`),
> 2025/2026 güncel sürümü. n8n hızlı geliştiği için sağlayıcı (model/embedding) listeleri zamanla değişir.
>
> **İlgili dosya:** Pazar/rakip perspektifi için → `../../../archive/marketResearch/n8n.md`

---

## 0. n8n'in Temel Modeli — Adımları Anlamak İçin Önce Bu

BPM motorumuzu tasarlamadan önce n8n'in çalışma modelini anlamak şart; çünkü "adımda ne yapılabilir"
sorusunun cevabı bu modele bağlı.

### 0.1 — Her şey bir "node" (adım)
Bir n8n iş akışı (workflow), birbirine bağlanan **node'lardan** (süreç adımları) oluşur. Akış soldan
sağa ilerler: **tetikleyici → işlem → koşul → işlem → ...** Her adım veriyi alır, dönüştürür, bir
sonraki adıma verir.

### 0.2 — Veri yapısı: "item" dizisi (en kritik kavram)
Adımlar arasında veri **item (öğe) dizisi** olarak akar. Her item iki anahtar taşır:
- **`json`** — normal yapısal veri (alanlar/değerler)
- **`binary`** (opsiyonel) — dosya/medya içeriği (base64 + mimeType + fileName)
- **`pairedItem`** — bu çıktı öğesinin hangi girdi öğesinden türediğini izleyen "soy ağacı" bilgisi

```json
[
  {
    "json": { "tutar": 1500, "kategori": { "ad": "Yemek" } },
    "binary": { "fis": { "data": "<base64>", "mimeType": "image/png", "fileName": "fis.png" } },
    "pairedItem": 0
  }
]
```

> **BPM motoru için ders:** Her adım **aynı veri şeklini** (item dizisi) alır ve üretir; bu tek-tip
> sözleşme, adımların gelişigüzel zincirlenebilmesinin temelidir. n8n token-tabanlı klasik BPMN'den
> farklı olarak **koleksiyon (dizi) üzerinde** çalışır — her "gateway" tek bir token değil, bir öğe
> kümesi yönetir. Bu bilinçli bir tasarım kararıdır; bizim motorumuzda da net karar verilmeli.

### 0.3 — Adım = Kaynak (Resource) + İşlem (Operation)
Uygulama entegrasyon node'ları tutarlı bir desen izler: önce **Kaynak** (entity türü: Mesaj, Kanal,
Satır...), sonra o kaynağa uygulanacak **İşlem** (Gönder, Güncelle, Sil...), sonra işleme göre değişen
**alanlar**. Bu desen 400+ node'u "bir kez öğren, her yerde kullan" yapar.

---

## 1. SÜREÇ BAŞLATMA ADIMLARI (Trigger / Tetikleyici Node'lar)

Her iş akışı bir tetikleyici ile başlar. n8n'de iki yapısal sınıf vardır:
- **Olay-itme (event-push / webhook tarzı):** n8n bir HTTP dinleyici açar; dış olay **anında** tetikler.
- **Zamanlı-çekme (polling/scheduled):** n8n bir servisi **periyodik** sorgular; yeni veri varsa tetikler.

| # | Adım (Node) | Süreci ne başlatır? | Yapılabilecek başlıca özellikler / ayarlar |
|---|---|---|---|
| 1 | **Manual Trigger** | İnsan editörde "Execute workflow"e basar | Test/geliştirme için; parametre yok; workflow başına tek tane. |
| 2 | **Schedule Trigger (Cron)** | Saat/zaman | Saniye/Dakika/Saat/Gün/Hafta/Ay aralıkları **veya** tam **Cron** ifadesi (6 alanlı, saniye dahil). Birden çok kural eklenebilir. Zaman dilimi workflow ayarına bağlı. |
| 3 | **Webhook** | Gelen HTTP isteği | **Metot:** GET/POST/PUT/PATCH/DELETE/HEAD. **Kimlik doğrulama:** Yok/Basic/Header/JWT. **Yol (path):** rastgele veya özel (`/:id` rota parametreleri). **Yanıt modu:** Anında / Son node bitince / "Respond to Webhook" ile / **Streaming**. **Test URL** (editörde) vs **Production URL** (yayında). Seçenekler: ikili/dosya yükleme, ham gövde (raw), IP beyaz listesi, bot yoksay, CORS, özel başlık/yanıt kodu. 16 MB varsayılan limit. |
| 4 | **n8n Form Trigger** | Kullanıcı n8n-barındırmalı formu gönderir | Çok sayfalı form. **Alan tipleri:** Metin, Textarea, E-posta, Sayı, Şifre, Tarih, Açılır liste, Onay kutusu, Radyo, **Dosya yükleme**, Gizli alan, Özel HTML. Her alan: etiket/isim/placeholder/varsayılan/zorunlu. Kimlik: Yok/Basic. Yanıt: gönderince / iş akışı bitince. Özel CSS, buton etiketi, bot yoksay. |
| 5 | **Chat Trigger** | Kullanıcı sohbet arayüzünde mesaj yazar | AI chatbot için (Agent/Chain'e bağlanmalı). **Mod:** Barındırılan sohbet / Gömülü (kendi arayüzün). Kimlik: Yok/Basic/n8n kullanıcı. Yanıt: son node / yanıt node'u / **streaming**. Önceki oturumu yükle (Memory ile), dosya yükleme, başlangıç mesajları, özel CSS. Her mesaj = 1 execution. |
| 6 | **Email Trigger (IMAP)** | İzlenen posta kutusuna yeni e-posta gelir | IMAP kimlik bilgisi; posta kutusu seçimi; **eylem:** okundu işaretle/bırak; **ekleri indir**; **format:** RAW/Resolved/Simple; özel arama kuralları; periyodik yeniden bağlanma. |
| 7 | **Error Trigger** | Başka bir iş akışının **hata** ile bitmesi | Bir "hata iş akışının" ilk adımı. Ana workflow ayarında "Error workflow" olarak atanır. Aldığı veri: execution ID/URL, hata mesajı, stack trace, hatalı node, retry durumu. Sadece **otomatik** hatalarda tetiklenir. |
| 8 | **Execute Sub-workflow Trigger** | Başka bir iş akışı bu alt-akışı çağırır | Alt iş akışının ilk adımı. **Girdi tanımı:** alanlarla tanımla / JSON örneğiyle / "tüm veriyi kabul et". Çağıran iş akışına veri geri döner ("View sub-execution" ile izlenir). → BPM'de **"Call Activity"** karşılığı. |
| 9 | **Local File Trigger** | Dosya sisteminde değişiklik | Dosya/klasör ekleme-değişme-silme olayları izlenir. Sembolik link dahil, ignore deseni, max derinlik. **n8n Cloud'da yok**; v2'de varsayılan kapalı (güvenlik). |
| 10 | **SSE Trigger** | Sunucu-gönderimli olay (Server-Sent Events) | Bir SSE uç noktasına bağlanır, her itilen olayda tetikler. Tek parametre: URL. |
| 11 | **MCP Server Trigger** | Bir MCP istemcisi bağlanır/araç çağırır | n8n'i **MCP sunucusu** yapar; n8n iş akışlarını dış AI ajanlarına **araç** olarak sunar. Çıktısını aşağı akıtmaz; sadece tool node'larına bağlanır. Bearer/Header auth. SSE + streamable HTTP. |
| 12 | **n8n Trigger** | Örnek/iş akışı yaşam-döngüsü olayları | "Aktif workflow güncellendi" / "Örnek (instance) başladı" / "Workflow yayınlandı". Eski Activation/Workflow Trigger'ın yerine. |
| 13 | **RSS Feed Read Trigger** | RSS beslemesine yeni içerik düşer (polling) | Besleme URL'i + Poll zamanları (Saatlik/Günlük/Haftalık/Aylık/Her X/Cron). |
| 14 | **Evaluation Trigger** | n8n "Evaluations" özelliğinde veri kümesi satırı | AI iş akışlarını test/puanlama için bir veri kümesini (örn. Google Sheets) satır satır çalıştırır. (Niş.) |
| — | **Activation / Workflow Trigger** | (DEPRECATED) | Yerini `n8n Trigger` aldı. |

### Polling (zamanlı-çekme) tetikleyiciler nasıl çalışır?
Native webhook'u olmayan uygulama tetikleyicileri (Gmail Trigger, Airtable Trigger, Google Sheets
Trigger...) **periyodik sorgu** yapar. Ortak **Poll Times** parametresi: Her Dakika / Saat / Gün /
Hafta / Ay / Her X / Cron. **Minimum aralık 1 dakika.** Yeni veri bulan her sorgu tetikler; boş sorgu
execution sayılmaz. Native webhook'u olan uygulamalar (Stripe, Notion, Typeform...) anında tetiklenir.

---

## 2. AKIŞ KONTROL ADIMLARI (Flow Control / Yönlendirme)

n8n çekirdek mantığı dört işe ayırır: **Bölme** (IF/Switch/Filter), **Birleştirme** (Merge/Compare),
**Döngü** (Loop Over Items), **Bekletme** (Wait). Artı yardımcı kontrol node'ları.

| # | Adım (Node) | Ne yapar? | Yapılabilecek başlıca özellikler / ayarlar |
|---|---|---|---|
| 1 | **IF** | Öğeyi **2 çıkışa** (true/false) ayırır | Koşul birleştirici: **AND/OR**. Tip-bazlı operatörler — String (eşit/içerir/başlar/regex...), Sayı (>, <, ≥, ≤...), Tarih (önce/sonra...), Boolean, Array (uzunluk, içerir...), Object (var/boş). Seçenekler: büyük-küçük harf yoksay, gevşek tip doğrulama. → BPM **exclusive gateway**. |
| 2 | **Switch** | **Çok dallı** yönlendirme | **Mod:** Kurallar (çıkış başına bir kural) veya İfade (çıkış indeksini döndüren ifade + çıkış sayısı). Çıkış yeniden adlandırma. **Fallback:** yok / ekstra çıkış / çıkış 0. "Eşleşen tüm çıkışlara gönder" seçeneği. → BPM çok-yollu gateway. |
| 3 | **Filter** | Koşulu sağlamayan öğeleri **eler** (tek çıkış) | IF ile aynı operatörler; AND/OR. IF'ten farkı: "false" dalı yok, eşleşmeyen öğe tamamen düşer. |
| 4 | **Merge** | Birden fazla akışı birleştirir | **Mod:** Append (arka arkaya), Combine (eşleşen alana göre — inner/outer/left/right join; pozisyona göre; tüm kombinasyonlar/kartezyen), **SQL Query** (AlaSQL ile join), Choose Branch. Çakışma yönetimi (derin/sığ), bulanık karşılaştırma, çoklu eşleşme. → BPM **join / parallel gateway senkronu**. |
| 5 | **Loop Over Items (Split In Batches)** | Yinelemeli işleme | **İki çıkış:** `loop` (her turda bir batch) ve `done` (tüm batch'ler bitince). Batch boyutu. Reset seçeneği (sayfalama için). Bağlam ifadeleri: `noItemsLeft`, `currentRunIndex`. Sonsuz döngüye karşı sonlandırma şartı şart. → BPM **multi-instance loop**. |
| 6 | **Wait** | Yürütmeyi duraklatır, veriyi DB'ye yazar, koşulda devam eder | **Devam modları:** (a) Süre kadar bekle, (b) Belirli zamanda, (c) **Webhook çağrısıyla** (execution'a özel resume URL; metot/auth/yanıt + max bekleme), (d) **Form gönderiminde** (onay formu). → BPM'de **user task + timer event + message event** üçlüsünün karşılığı; süreç günlerce uyuyabilir. (En kritik insan-döngüde adımı.) |
| 7 | **Stop And Error** | Yürütmeyi bilerek başarısızlıkla durdurur | Hata tipi: özel mesaj veya yapısal hata nesnesi (JSON). Error Trigger'a/hata iş akışına yönlenir. → BPM **error end event / boundary error**. |
| 8 | **No Operation (NoOp)** | Hiçbir şey yapmaz, veriyi aynen geçirir | Sadece okunabilirlik/dokümantasyon (bir dalın bittiğini işaretlemek). |
| 9 | **Execute Sub-workflow** | Aynı n8n üzerinde başka iş akışını çağırır | Kaynak: DB/Dosya/Parametre/URL. **Mod:** tüm öğelerle bir kez / her öğe için bir kez. **"Alt-akış bitene kadar bekle"** (senkron) veya ateşle-devam et (asenkron). Girdi şeması eşleme. → BPM **Call Activity** (yeniden kullanım/modülerlik). |
| 10 | **Execute Command** | Host makinede kabuk komutu çalıştırır | Tek/çok komut; bir kez veya öğe başına. Çıktı: stdout/stderr/exit code. **Cloud'da yok**; v2'de varsayılan kapalı (güvenlik). |
| 11 | **Compare Datasets** | İki akışı karşılaştırır, **4 çıkışa** ayırır | Çıkışlar: Sadece A'da / Sadece B'de / Aynı / Farklı. Eşleştirme anahtarı; fark çözümü (A kullan/B kullan/karışık/her iki versiyon); atlanacak alanlar; bulanık karşılaştırma. |
| 12 | **Limit** | Aşağı geçen öğe sayısını sınırlar | Max öğe; ilk/son öğeleri tut. |
| 13 | **Sort** | Öğe listesini sıralar | Simple (alan(lar)a göre artan/azalan), Random (karıştır), Code (özel JS karşılaştırıcı). |
| 14 | **Remove Duplicates** | Yinelenen öğeleri kaldırır | Mevcut girdi içinde / **önceki yürütmelerde görülenleri** (kalıcı dedup DB'si: yeni/daha büyük/daha geç değer) / geçmişi temizle. Karşılaştırılacak alan seçimi; geçmiş boyutu. |

---

## 3. VERİ İŞLEME ADIMLARI (Data Transformation)

Dış servise gitmeden veriyi yeniden şekillendiren "core" node'lar. Bunların ~%80'i kod yazmadan
dönüşümü çözer; geri kalanı için **Code** kaçış kapısı vardır.

### 3.1 — Saf veri şekillendirme
| Adım | Ne yapar? | Başlıca işlemler/seçenekler |
|---|---|---|
| **Edit Fields (Set)** | Alan değeri ekler/değiştirir (en çok kullanılan) | Manuel eşleme veya ham JSON çıktı; sadece set edilen alanları tut / girdiyi koru; nokta notasyonu; tip zorlama. |
| **Filter** | Koşulu sağlamayan öğeleri eler | Tip-bazlı operatörler; AND/OR. |
| **Aggregate** | Çok öğeyi tek öğeye toplar | Bireysel alanlar (her alanı listeye) veya tüm öğe verisi (tek listeye). |
| **Summarize** | Pivot-tablo: gruplama + istatistik | Append/Average/Concatenate/Count/Count Unique/Max/Min/Sum + "böl-ölçütü" (pivot boyutu). |
| **Sort** | Sıralar | Simple / Random / Code. |
| **Limit** | Öğe sayısını sınırlar | İlk/son N öğe. |
| **Split Out** | Dizi içeren tek öğeyi çok öğeye açar (Aggregate'in tersi) | Açılacak alan; diğer alanları dahil et/etme/seç. |
| **Remove Duplicates** | Yinelenenleri kaldırır | Bkz. §2.14 (akış kontrol olarak da listelendi). |
| **Rename Keys** | Alan adlarını değiştirir | Çoklu eski→yeni eşleme; Regex modu (desen, derinlik). |

### 3.2 — Kod & AI dönüşümü
| Adım | Ne yapar? | Başlıca işlemler/seçenekler |
|---|---|---|
| **Code** | Özel **JavaScript / Python** çalıştırır | **Mod:** Tüm öğelerle bir kez (diziyi görür, dizi döndürür) / **Her öğe için bir kez**. JS erişimi: `$input.all()/.first()/.last()`, `$json`, `items`, `$('Node')`. Python: `_input/_json/_items/_item`. Çıktı: `[{json:{...}}]`. Kısıt: içeriden dosya/HTTP yok (ilgili node'ları kullan). Python v1.111+ native runner. |
| **AI Transform** | Dönüşüm kodunu **doğal dilden** üretir | Düz dille tarif et → n8n Code mantığını yazıp çalıştırır. |

### 3.3 — Tarih, kripto, ikili/dosya yardımcıları
| Adım | Ne yapar? | Başlıca işlemler |
|---|---|---|
| **Date & Time** | Tarih işle/formatla | Ekle/Çıkar/Şimdi al/Formatla/Parça çıkar/Yuvarla/İki tarih arası süre. |
| **Crypto** | Kriptografik işlemler | Generate (random/UUID), Hash (MD5/SHA256/SHA512), HMAC, Sign, Encrypt/Decrypt. |
| **Edit Image** | Görüntü işleme | Blur/Border/Composite/Create/Crop/Draw/Resize/Rotate/Text/Transparent + Multi Step. |
| **Compression** | Sıkıştır/aç | ZIP/GZIP compress, decompress. |
| **HTML** | HTML ayrıştır/üret | Extract (CSS seçici → Attribute/HTML/Text/Value) ve Generate (şablondan, `{{ }}` ile). |
| **Markdown** | Markdown↔HTML | Markdown→HTML, HTML→Markdown. |
| **XML** | XML↔JSON | XML→JSON, JSON→XML (attribute/character key, CDATA). |
| **Extract from File** | İkili dosyayı JSON'a çevirir | **CSV/HTML/JSON/ICS/ODS/PDF/RTF/Text/XLS/XLSX** + Base64'e taşı. |
| **Convert to File** | JSON'u ikili dosyaya çevirir | **CSV/HTML/ICS/JSON/ODS/RTF/XLS/XLSX/Text** + Base64'ten dosyaya. |
| **Read/Write Files from Disk** | Host dosya sistemi | Oku (glob desenleri) / Yaz (ekleme dahil). |

> Not: Eski **Move Binary Data** node'u artık Extract/Convert işlemlerine ve Edit Fields'e gömüldü
> (json ↔ binary taşıma).

---

## 4. ENTEGRASYON / PROTOKOL ADIMLARI

### 4.1 — HTTP Request (evrensel konektör — en güçlü jenerik node)
Herhangi bir REST/HTTP API'ye bağlanır. Bir entegrasyon yoksa "kendin yaz"ın yoludur.
- **Metotlar:** GET/POST/PUT/PATCH/DELETE/HEAD/OPTIONS.
- **Kimlik doğrulama:** Önceden tanımlı kimlikler **veya** jenerik (Basic/Custom/Digest/Header/OAuth1/OAuth2/Query Auth).
- **Sorgu/başlık/gövde:** isim-değer çiftleri veya ham JSON. Gövde tipleri: form-urlencoded, form-data (ikili dosya ekle), JSON, n8n ikili dosya, Raw (özel MIME).
- **Sayfalama (pagination):** "her istekte parametre güncelle" veya "yanıt sonraki URL'i içerir". Değişkenler: `$pageCount`, `$request`, `$response`.
- **Batch'leme:** batch boyutu + batch'ler arası gecikme (ms) → hız sınırlama.
- **Retry / Timeout:** başarısızlıkta yeniden dene, yanıt timeout'u, yönlendirme takibi, SSL yoksay, proxy.
- **İkili/dosya:** gövdede/form-data ile gönder; yanıtı JSON/metin/dosya olarak al.
- **cURL içe aktar:** bir `curl` komutunu yapıştır → node otomatik ayarlanır.
- **AI araç modu:** Agent kullanınca yanıt optimizasyonu (alan seç, HTML CSS-seç, kısalt → token tasarrufu).

### 4.2 — Diğer protokol/jenerik node'lar
| Adım | Ne yapar? | İşlemler |
|---|---|---|
| **Respond to Webhook** | Webhook çağıranına özel yanıt | Text/JSON/Binary/JWT/Redirect/No Data; yanıt kodu/başlık; streaming. |
| **GraphQL** | GraphQL uç noktası sorgular | GET/POST; raw GraphQL veya JSON. |
| **FTP / SFTP** | Dosya transferi | List/Download/Upload/Delete/Rename. |
| **SSH** | Uzak sunucuya SSH | Komut çalıştır + dosya indir/yükle. |
| **RSS Read** | RSS/Atom besleme okur | Besleme URL'i. |
| **Send Email (SMTP)** | SMTP ile e-posta gönder | Send / **Send and Wait for Response** (insan-döngüde); Text/HTML/Both; ek/CC/BCC. |

### 4.3 — Kaynak + İşlem deseni (400+ uygulama node'u)
Tüm uygulama konektörleri (Slack, Google Sheets, Postgres, Salesforce, Notion...) aynı 3 adımlı kalıbı izler:
**Kaynak (Resource)** → **İşlem (Operation)** → işleme göre değişen **alanlar** (her alan statik veya ifade).

**Somut örnekler:**
- **Postgres / MySQL:** Execute Query/SQL, Insert, Insert or Update (upsert), Select, Update, Delete.
- **Google Sheets:** *Document* (Create/Delete); *Sheet* (Append Row, Append or Update Row, Clear, Create, Delete, Get Row(s), Update Row...).
- **Slack:** *Message* (Send, Send and Wait for Response, Update, Delete); Channel/File/User/Reaction/Star/User Group.

**Entegrasyon sayısı:** Resmî olarak **400+** yerleşik node; topluluk node'larıyla **500–1000+** olarak da anılır. Resmî rakam: **400+**.

---

## 5. YAPAY ZEKA ADIMLARI (Advanced AI / LangChain — Cluster Nodes)

n8n'in AI tasarımı **"cluster node"** kavramına dayanır ve bir BPM motoru için en öğretici kısımdır.

### 5.1 — Kavramsal model: Kök (Root) node + Alt (Sub) node (önce bunu oku)
- Bir **cluster** = **tek bir kök node** + **bir/çok alt node**.
- **Kök node:** ana işlevi tanımlar, soldan-sağa ana veri akışında çalışır (örn. AI Agent, LLM Chain, Vector Store).
- **Alt node:** köke **alttan özel bir port** ile takılır, ana akışta yer almaz; kökü yapılandırır/genişletir (örn. Chat Model, Memory, Tool, Output Parser, Embeddings).
- **Özel bağlantı portları** (her port yalnız belirli alt node tipini kabul eder):

| Port | Ne takılır | Tüketen kök node |
|---|---|---|
| `ai_languageModel` | Chat Model / LLM | Agent, tüm Chain'ler |
| `ai_memory` | Memory | Agent (Chain'ler **memory kullanamaz**) |
| `ai_tool` | Tool (araç) | Agent (+ Vector Store "araç olarak") |
| `ai_outputParser` | Output Parser | Agent, Chain |
| `ai_embedding` | Embeddings | Vector Store, bazı retriever |
| `ai_document` | Document Loader | Vector Store (insert) |
| `ai_textSplitter` | Text Splitter | Document Loader |
| `ai_vectorStore` | Vector Store | Retriever, Vector Store Tool |
| `ai_retriever` | Retriever | Retrieval QA Chain, Reranker |
| `ai_reranker` | Reranker (Cohere) | Vector Store / Retriever hattı |

> **BPM motoru için en önemli ders:** Bu **takılabilir-strateji (pluggable strategy)** desenidir. "AI adımı"
> sabit bir kök; model/memory/araç/parser ise stabil portların arkasında değiştirilebilir parçalar. GPT-4'ten
> Claude'a geçmek = OpenAI alt node'unu çıkar, Anthropic'i tak; gerisi değişmez. No-code bir motorda
> kullanıcının sağlayıcıyı yeniden tel çekmeden değiştirmesini sağlar.

### 5.2 — Ajanlar & Zincirler (kök node'lar)
| Adım | Ne yapar? | Notlar |
|---|---|---|
| **AI Agent** (Tools Agent) | **Otonom orkestratör** | Hedefi alır, takılı **araçları** görür, hangisini hangi argümanla çağıracağına karar verir, sonucu kendine besler, döngüyle nihai cevabı üretir. Portlar: Chat Model (zorunlu, tool-calling destekli), Memory (ops.), Tools (ops.), Output Parser (ops.). Ayarlar: prompt kaynağı, **System Message**, **Max Iterations** (varsayılan 10), ara adımları döndür, streaming, ikili görüntü geçişi, insan-onay kapısı. |
| **Basic LLM Chain** | Tek, durumsuz LLM çağrısı | Memory **yok**. Üret/dönüştür. Chat Model (zorunlu) + Output Parser (ops.). |
| **Question & Answer / Retrieval QA Chain** | RAG: soru → retriever'dan belge → LLM cevaplar | Chat Model + Retriever. Memory yok. |
| **Summarization Chain** | Uzun belgeyi özetler | Map-Reduce / Refine / Stuff stratejileri (context window'u aşan girdiler için chunk'lama). |
| **Information Extractor** | Serbest metinden yapısal alan çeker | Şema tanımla → JSON döner (örn. fatura → tutar/tarih/satıcı). |
| **Text Classifier** | Metni tanımlı kategorilere sınıflar | Fallback / "hiçbiri" yönetimi. |
| **Sentiment Analysis** | Duygu analizi | Kategoriler + skor. |
| **OpenAI Assistant** | OpenAI Assistants API sarmalayıcı | Tools Agent'tan ayrı kök node. |

> Tasarım notu: **Chain = deterministik tek-amaçlı** (tek çağrı, otonomi yok); **Agent = otonom orkestratör**
> (çok adım, araç kullanır, durumlu). BPM motorumuz iki ayrı "adım tipi" sunabilir: tahmin edilebilir
> **"AI adımı" (chain)** vs açık-uçlu **"AI ajan adımı" (agent)**.

### 5.3 — Chat Model'ler / LLM'ler (alt node, `ai_languageModel`)
Köke takılan, birbirinin yerine geçebilen model sağlayıcıları:
OpenAI, Anthropic, Azure OpenAI, AWS Bedrock, Google Gemini, Google Vertex, Groq, Mistral Cloud, Cohere,
DeepSeek, **Ollama (yerel/self-host)**, OpenRouter, xAI Grok, NVIDIA, Alibaba, MiniMax, Moonshot, Vercel AI
Gateway, Lemonade. (Ayrıca completion-tipi: OpenAI/Cohere/Ollama/HuggingFace.)
**Ortak ayarlar:** model, temperature, max tokens, top-p, ceza katsayıları, timeout, retry, JSON yanıt, base
URL override. **Model Selector** alt node'u: tek port arkasında **çoklu model** + yönlendirme/fallback.

### 5.4 — Memory (alt node, `ai_memory`)
Ajana **konuşma durumu** (sohbet geçmişi) verir; "session key" ile çoklu konuşma izlenir.
- **Simple / Window Buffer** (bellekte, kalıcı değil — varsayılan), **Redis**, **Postgres**, **MongoDB**, **Motorhead**, **Xata**, **Zep** (uzun vadeli/özetleyen).
- **Chat Memory Manager:** bir memory deposunu programatik oku/yaz/temizle.

### 5.5 — Tools / Araçlar (alt node, `ai_tool`)
Ajanın çağırabildiği yetenekler. Ajan her aracın **isim + açıklama + girdi şemasını** görür; LLM ne zaman
çağıracağına karar verir (açıklama = "LLM için API dokümanı").
- **Calculator, Code Tool, HTTP Request Tool, Vector Store Tool, Wikipedia, SerpAPI, SearXNG, Wolfram|Alpha, Think Tool.**
- **Call n8n Workflow Tool:** bir alt-iş-akışını **araç** olarak çağırır → **bir BPM süreci, çağrılabilir araç olur**. (Açıklama alanı LLM'e "ne zaman kullan"ı söyler; girdiler `$fromAI()` ile model tarafından doldurulabilir.)
- **MCP Client Tool:** ajanı dış **MCP sunucularına** bağlar, onların araçlarını ajana açar.
- **"Herhangi bir uygulama node'u araç olarak":** 1000+ entegrasyon node'u (Slack, Gmail, Sheets, DB...) ajana araç olarak takılabilir; alanları çalışma anında **`$fromAI()`** ile LLM doldurur. Ajana ~100+ gerçek-dünya eylemi kazandıran şey budur.
- **AI Agent Tool:** bir ajan başka bir ajana araç olur (çok-ajanlı desen).

### 5.6 — Vector Store'lar (kök node; araç/retriever olarak da)
Gömülü (embedded) veriyi tutar, benzerlik (vektör) araması yapar. **4 mod:** Get Many (sorgula), Insert
Documents (göm+yaz — Embeddings + Document Loader gerekir), Retrieve as Vector Store (Chain/Tool için),
Retrieve as Tool (Agent'a doğrudan araç). **insert = yazma, retrieve = okuma.**
Desteklenen: In-Memory/Simple, Pinecone, Qdrant, Supabase, **PGVector**, Milvus, Weaviate, MongoDB Atlas,
Azure AI Search, ChromaDB, Redis, Oracle DB, Zep.

### 5.7 — Embeddings (alt node, `ai_embedding`)
Metni vektöre çevirir: OpenAI, Azure OpenAI, AWS Bedrock, Cohere, Google Gemini/Vertex, HuggingFace,
Mistral, **Ollama (yerel)**, NVIDIA, Oracle DB, Lemonade. **Önemli:** insert ve query'de **aynı** embedding modeli kullanılmalı.

### 5.8 — Document Loader & Text Splitter
- **Document Loader** (`ai_document`): Default Data Loader, GitHub Loader, Binary/JSON Input Loader.
- **Text Splitter** (`ai_textSplitter`): Character, **Recursive Character** (önerilen varsayılan), Token. Ayarlar: chunk boyutu, overlap, ayraç.

### 5.9 — Output Parser'lar (alt node, `ai_outputParser`)
"Belirli çıktı formatı" açıkken yapısal çıktıyı zorlar/doğrular:
- **Structured Output Parser** (JSON şema/örnek), **Auto-fixing** (hata olursa LLM'e düzelttirir — kendi Chat Model'i gerekir), **Item List**.

### 5.10 — Retriever & Reranker
- **Retriever** (`ai_retriever`): Vector Store Retriever (standart RAG), Contextual Compression (sıkıştır/filtrele), MultiQuery (LLM soruyu çeşitlendirir → recall artar), Workflow Retriever (alt-akışla özel getirme).
- **Reranker** (`ai_reranker`): Reranker Cohere (getirilen belgeleri alaka sırasına göre yeniden sıralar; tek yerleşik).

### 5.11 — Yeni kategoriler (BPM açısından önemli)
- **Guardrails:** AI adımları etrafında içerik/PII/güvenlik filtreleri (girdi/çıktı koruması).
- **MCP:** hem MCP Client Tool hem MCP Server Trigger (n8n iş akışlarını dış ajanlara araç olarak açma).
- **Vendors:** tek-sağlayıcı tam-özellikli uygulama node'ları (OpenAI/Anthropic/Gemini/Microsoft/Ollama...) — chat/görüntü/ses/dosya işlemlerini normal app node'u olarak paketler (alt node değil).

---

## 6. HER ADIMDA YAPILABİLECEK ORTAK ÖZELLİKLER

Bunlar **neredeyse her node'da** bulunan çapraz-kesen yeteneklerdir — tasarımda tek tek node'lardan
**daha kritik**, çünkü "yazım ve güvenilirlik deneyimini" bunlar tanımlar.

### 6.1 — Expression'lar (`{{ }}` — dinamik veri)
Her alan sabit değerden **ifadeye** geçebilir; `{{ ... }}` içinde JS-benzeri kod dinamik veri çeker.
`$` yazınca otomatik tamamlama. Başlıca değişkenler:
- **Mevcut öğe/girdi:** `$json` (mevcut öğe JSON'u), `$binary`, `$input` (`.item/.all()/.first()/.last()`).
- **Diğer node verisi:** `$('Node Adı').item.json / .all() / .first() / .last()`, `$prevNode`.
- **Workflow/execution metası:** `$workflow`, `$execution`, `$runIndex`, `$itemIndex`, `$parameter`.
- **Tarih:** `$now`, `$today` (Luxon).
- **Yardımcı:** `$if()`, `$ifEmpty()`, `$max()`, `$min()`, `$jmespath()`.
- **Ortam/gizli/AI:** `$vars` (workflow değişkenleri), `$secrets` (harici kasa), `$fromAI()` (alanı LLM doldursun); HTTP için `$request/$response/$pageCount`.

### 6.2 — Veri eşleme (sürükle-bırak)
INPUT panelinden bir alanı parametreye sürükle → otomatik ifade üretir (`{{ $json.fruit }}`). Adımlar
arası veriyi kodsuz tel çekmenin yolu.

### 6.3 — Node "Settings" sekmesi (her adımda)
- **Notes:** node üzerinde serbest dokümantasyon; canvas'ta gösterilebilir.
- **Always Output Data:** node hiçbir şey üretmese bile boş öğe çıkar (alt akış çalışsın diye).
- **Execute Once:** node'u sadece **ilk** öğeyle bir kez çalıştır (kalanı yoksay).
- **Retry On Fail:** başarısızlıkta yeniden dene → **Max Tries** + **denemeler arası bekleme (ms)**.
- **On Error (hata davranışı):**
  - **Stop Workflow** — tüm yürütmeyi durdur.
  - **Continue (regular output)** — son geçerli veriyle devam.
  - **Continue (using error output)** — node'da beliren **ayrı hata-çıkış dalına** yönlendir (hatayı açıkça yönet). → BPM **boundary error event** karşılığı.

### 6.4 — Pin Data (geliştirme/mock)
Bir node'un çıktısını **dondurur**; sonraki yürütmelerde kaynaktan çekmek yerine bu sabit veriyi kullanır
(canlı API'yi yormadan alt akışı test). Kısıt: tek çıkışlı node'lar; ikili veri pinlenemez.

### 6.5 — Credentials (kimlik bilgisi) yönetimi
- **Node'dan ayrı katman:** kimlikler ayrı tutulur; node'lar yalnız *talep eder*; sadece yetkili node tipi okuyabilir.
- **Yeniden kullanılabilir/paylaşılabilir:** bir kimlik çok node/workflow'da; kişi veya **proje** ile paylaşım (paylaşılan kullanıcı *kullanır* ama gizli değeri *göremez*).
- **Tipler:** OAuth2, OAuth1, API key/token, Basic Auth + HTTP'nin jenerik auth tipleri.
- **Şifreleme:** DB'de **at-rest şifreli** (`N8N_ENCRYPTION_KEY`); self-host'ta anahtar rotasyonu.

---

## 7. BPM MOTORU TASARIMI İÇİN ÇIKARIMLAR (n8n → Flovo)

n8n'in adım envanterini klasik **BPMN** kavramlarına ve bizim motorumuzun ihtiyaçlarına bağlayalım:

### 7.1 — n8n adımları ↔ BPMN karşılıkları
| n8n yapısı | BPMN/BPM karşılığı |
|---|---|
| Webhook / Form / Chat / Schedule / Email triggers | **Start events** (message/timer/conditional) |
| IF / Switch | **Exclusive / Inclusive gateway** |
| Merge / Compare Datasets | **Parallel join / senkronizasyon** |
| Loop Over Items | **Multi-instance loop** |
| **Wait** (süre/zaman/webhook/form) | **User task + Timer event + Message event** (en kritik) |
| Execute Sub-workflow | **Call Activity** (yeniden kullanım) |
| Stop And Error + Error Trigger | **Error end event / boundary error / telafi (compensation)** |
| HTTP/uygulama node'ları | **Service task** |
| AI Agent / Chain | **AI-destekli iş adımı (yeni nesil)** |

### 7.2 — Mutlaka örnek alınması gereken 5 mimari fikir
1. **Tek-tip veri sözleşmesi (item dizisi: json + binary + pairedItem).** Her adımın aynı şekli alıp
   üretmesi, gelişigüzel zincirlemenin ve no-code deneyimin temelidir.
2. **Üç yeniden-kullanılabilir ilkel:** (a) az sayıda jenerik **veri-şekillendirme** node'u (Set, Filter,
   Aggregate/Summarize, Sort/Limit, Split Out, Remove Duplicates) → dönüşümlerin %80'i; (b) iki **kaçış
   kapısı** — **HTTP Request** (her API) ve **Code** (her mantık); (c) tek-tip **Kaynak+İşlem** deseni.
3. **Çapraz-kesen güvenilirlik özellikleri** (tek tek node'lardan önemli): expression motoru, sürükle-eşle,
   Settings sekmesi (**retry + hata-çıkış dalı**), Pin Data (mock), ayrı/şifreli/paylaşılabilir credentials.
4. **Wait node = uzun-soluklu süreç + insan-döngüde** ilkel. Veriyi DB'ye yazıp günlerce uyuyabilen,
   webhook/form/zaman ile uyanan adım. Masraf onayı / İK süreçleri için **olmazsa olmaz**.
5. **AI cluster mimarisi (takılabilir-strateji):** sabit "AI adımı" kökü + değiştirilebilir
   model/memory/araç/parser portları. "Herhangi bir adım = araç" (`$fromAI()` + Workflow Tool) ve **MCP**
   ile süreç hem AI'ı *çağırır* hem AI tarafından *çağrılır*.

### 7.3 — Bilinçli karar verilmesi gereken noktalar (n8n'in sınırları/tercihleri)
- **Koleksiyon vs token:** n8n öğe-dizisi üzerinde çalışır (klasik token-tabanlı BPMN değil). Bizim
  motorumuz hangisini benimseyecek? Kurumsal onay/denetim için token+vaka modeli daha tanıdık olabilir.
- **AI iki katman:** Kurumsal süreçler **varsayılan olarak deterministik chain** kullanmalı (tahmin
  edilebilirlik/denetlenebilirlik); otonom **agent** sadece gerçekten açık-uçlu adımlara saklanmalı.
- **Memory yalnız agent'ta ve session-key'li:** Konuşma durumu yeniden başlatmada hayatta kalacaksa
  kalıcı depo (Postgres/Redis) bilinçli planlanmalı.
- **Güvenlik:** Execute Command / Local File gibi güçlü ama riskli adımlar n8n'de Cloud'da kapalı /
  varsayılan devre dışı. Bizde de **yetki/sandbox** modeli baştan tasarlanmalı.
- **RAG hattı yeniden-kullanılabilir blok:** Embeddings → Loader/Splitter → Vector Store (insert) →
  Retriever (+Reranker) → QA Chain/Agent → "şirket belgeleri üzerinde cevap" gibi Flovo özelliklerinin temeli.

---

## Kaynaklar
- n8n Core nodes: https://docs.n8n.io/integrations/builtin/core-nodes/
- n8n Trigger nodes: https://docs.n8n.io/integrations/builtin/trigger-nodes/
- Flow logic (looping/merging/splitting): https://docs.n8n.io/flow-logic/
- Veri yapısı: https://docs.n8n.io/data/data-structure/
- Expression'lar / yerleşik değişkenler: https://docs.n8n.io/code/builtin/overview/ , https://docs.n8n.io/data/expressions/
- Code node: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.code/
- HTTP Request: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/
- Advanced AI / LangChain: https://docs.n8n.io/advanced-ai/langchain/overview/
- Cluster nodes (root/sub): https://docs.n8n.io/integrations/builtin/cluster-nodes/ , .../root-nodes/ , .../sub-nodes/
- AI Agent / Tools Agent: https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/
- Call n8n Workflow Tool: https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolworkflow/
- Kaynak kod (otoriter node envanteri): https://github.com/n8n-io/n8n → `packages/@n8n/nodes-langchain/nodes/`
- Entegrasyon sayısı (resmî): https://n8n.io/integrations/

---

*Hazırlık tarihi: 2026-06-25 · 3 paralel araştırma ajanının n8n resmî doküman + kaynak kod taramasından sentezlenmiştir. n8n hızlı geliştiği için sağlayıcı/node listeleri hedef sürüme karşı doğrulanmalıdır.*
