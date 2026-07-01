# n8n Motoru Nasıl Çalışır? — Yürütme Motoru İçyapısı (Detaylı)

> **Amaç:** Yeni Flovo'nun **BPM motorunu** tasarlamadan önce, n8n'in **yürütme motorunun içyapısını**
> derinlemesine anlamak. Bu doküman "n8n'de hangi adımlar var" değil (onun için → `n8n-surec-adimlari-analizi.md`),
> **"motor bir iş akışını nasıl çalıştırır"** sorusunu cevaplar: süreçler, tetikleyici kaydı, node-node
> yürütme algoritması, veri modeli, expression değerlendirme, kalıcılık, bekle/devam et, hata yönetimi, döngü, ölçekleme.
>
> **Kaynak:** n8n resmî dokümanları (`docs.n8n.io`) + GitHub kaynak kodu
> (`packages/cli`, `packages/core/src/execution-engine/workflow-execute.ts`, `n8n-workflow`), 2025/2026 sürümü.
> Bazı düşük-seviye detaylar (alan adları, 65 sn eşiği vb.) kaynak-kodu okumalarından türetilmiştir; uygulamadan
> önce güncel sürüme karşı doğrulanmalı.
>
> **İlgili:** Adım envanteri → `n8n-surec-adimlari-analizi.md` · Pazar perspektifi → `../../../archive/marketResearch/n8n.md`

---

## 0. Büyük Resim — Bir İş Akışının Hayatı (30 saniyede)

```
   [Tetikleyici]          [Orkestrasyon]            [Yürütme]              [Kalıcılık]
   webhook/cron/poll  →   execution kaydı oluştur → node-node çalıştır  →  sonuç + durum DB'ye
        |                  (gerekirse kuyruğa it)    (stack + run data)      (success/error/waiting)
        |                        main süreç              worker süreç            PostgreSQL
        └─ aktif workflow'ların tetikleyicileri "Active Workflow Manager" ile kayıtlı tutulur
```

n8n özünde bir **Node.js/TypeScript monoliti**dir (mono-repo; çekirdek paket `packages/cli`, motor
`packages/core`). Tek süreç olarak da çalışır, üretimde **paylaşılan bir PostgreSQL + Redis** etrafında
uzmanlaşmış süreçlere de bölünebilir. İki temel çalışma modu vardır (`EXECUTIONS_MODE`):

- **`regular` (varsayılan):** Tek süreç her şeyi yapar — UI/API sunar, webhook dinler, cron/poll çalıştırır
  **ve iş akışlarını aynı süreçte yürütür.** Basit; ama UI ile yürütme aynı event-loop için yarışır, ağır bir
  iş akışı editörü kilitleyebilir. Dev/düşük hacim için uygun.
- **`queue` (üretim):** Yürütme, main süreçten ayrı **worker** süreçlerine Redis üzerinden devredilir. Ölçeklenebilir mimari.

> **BPM motoru için 1. ders (en önemli):** **Orkestrasyonu (execution oluştur + kuyruğa it) yürütmeden
> (çalıştır) ayır.** main-vs-worker ayrımı tüm ölçeklenebilirliğin temel kaldıracıdır.

---

## 1. Deployment Mimarisi — Süreçler ve Rolleri

| Süreç | Komut | Ne yapar? |
|---|---|---|
| **Main** | `n8n start` | UI + REST API sunar. **Active Workflow Manager**'ı barındırır (tetikleyici/webhook/cron/poll kaydı). Tetikleyici olayı gelince **execution kaydı oluşturur**; queue modunda **işi Redis kuyruğuna iter, kendisi üretim iş akışını çalıştırmaz.** Multi-main'de sadece **lider** main "en-fazla-bir-kez" görevleri (cron/poll) çalıştırır. |
| **Worker** | `n8n worker` | UI/API'siz başsız (headless) örnek. Kuyruktan iş çeker, workflow + credentials'ı DB'den yükler, **iş akışını yürütür**, sonucu/durumu DB'ye yazar, Redis ile tamamlandı sinyali verir. **Yatayda ölçeklenen birim budur.** |
| **Webhook** | `n8n webhook` | (Opsiyonel) Yalnızca gelen webhook HTTP isteklerini kabul eder, execution oluşturur, kuyruğa iter. Webhook girişini editörden bağımsız ölçeklemek için. `N8N_DISABLE_PRODUCTION_MAIN_PROCESS=true` ile main'i webhook havuzundan çıkar. |
| **Database** | PostgreSQL (üretim) / SQLite (varsayılan) | **Tek doğruluk kaynağı:** workflow'lar, credentials, executions + execution data, webhook kayıtları, ayarlar, kullanıcılar. Tüm süreçler okur/yazar. |
| **Redis** | — | **Mesaj kuyruğu / job broker (BullMQ).** Workflow *verisini saklamaz* — yalnız bekleyen execution işlerini (≈ execution ID + metadata) ve HA'da main'ler arası **pub/sub koordinasyonunu** taşır. |

> **BPM motoru için 2. ders:** **Durum (state) Postgres'te, kuyruk (Redis) yalnız iş ID'leri taşır.**
> Worker'lar **durumsuz**dur; her işte DB'den yeniden yükler. Bu, temiz yatay ölçekleme ve takılan-iş kurtarmayı sağlar.

---

## 2. Tetikleyiciler ve Zamanlayıcı — Runtime'da Nasıl Kayıtlı Kalır?

### "Active Workflow" kavramı
Bir workflow "aktif"tir = yayınlanmış/aktif **ve** bir başlangıç node'u (tetikleyici/webhook/poller) içerir.
Yaşam döngüsünü **Active Workflow Manager** (`packages/cli/src/active-workflow-manager.ts`) yönetir.

### Açılışta / aktifleştirmede kayıt
- Sunucu açılınca `ActiveWorkflowManager.init()` çalışır ve DB'de aktif işaretli **tüm workflow'ları toplu aktive eder.**
- Her birinin geçerli bir başlangıç node'u olduğunu doğrular, sonra **tetikleyiciyi tipine göre kaydeder:**
  - **Webhook node'ları →** `webhook_entity` satırı (**metot + yol → workflow/node** eşlemesi) + bellekte rota kaydı; gelen istekler doğru workflow'a çözülür.
  - **Schedule/cron →** süreç-içi zamanlayıcıya node'un cron ifadesi + zaman dilimiyle kaydedilir.
  - **Polling →** bir zamanlayıcıya kaydedilir; n8n periyodik olarak node'un poll fonksiyonunu çağırıp dış serviste yeni veri arar.
  - **Trigger/event node'ları →** uzun-ömürlü bağlantılarını/dinleyicilerini açar.
- Editörde aktifleştirme aynı kayıt yolunu **canlı** çağırır (yeniden başlatma gerekmez); deaktive etme tetikleyiciyi söker. Multi-main'de aktif/pasif değişimi Redis pub/sub ile tüm main'lere yayılır.

### Nasıl ateşlenir?
- **Cron/Schedule:** Süreç-içi zamanlayıcı cron ifadesini zaman dilimine göre değerlendirir; eşleşince execution oluşturur. *Tuzak: zamanlama yalnız workflow **aktif/yayında** iken ateşlenir; manuel çalıştırma her durumda çalışır.*
- **Webhook:** Gelen HTTP isteği → kayıtlı yol→workflow eşlemesinde aranır → execution oluşur. **Production webhook** (aktif workflow, kalıcı yol) ile **test webhook** (geçici; yalnız editör "Listen" açıkken) ayrıdır.
- **Polling:** Sabit aralıklı zamanlayıcı poll fonksiyonunu çağırır; son sorgudan beri yeni öğeler execution başlatır. **Minimum aralık 1 dakika.**

### Queue modunda tetikleyiciler (kritik tasarım noktası)
**Tetikleyiciler, zamanlayıcılar ve poller'lar MAIN süreçte çalışır, worker'da değil.** Bunlar
"en-fazla-bir-kez" görevlerdir ve (lider) main'e aittir: main execution oluşturup kuyruğa iter; **worker'lar
yalnız yürütür.** Multi-main'in **lider seçimi** (Redis TTL anahtarı + pub/sub) gerektirmesinin sebebi tam
budur — yoksa bir cron N kez ateşlenir.

> **BPM motoru için 3. ders:** **Tetikleyiciler "en-fazla-bir-kez" ve tek sahipli olmalı.** Çok-örnekliye
> geçtiğiniz an lider seçimi/koordinasyon gerekir; bunu sonradan değil **1. günden** tasarla.

---

## 3. Çekirdek Yürütme Algoritması (En Önemli Bölüm)

Orkestratör: `packages/core/src/execution-engine/workflow-execute.ts` içindeki **`WorkflowExecute`** sınıfı.
Giriş noktaları: `run()` (başlangıç durumunu kurar) ve `processRunExecutionData()` (ana işleme döngüsü; `IRun` döndürür).

### 3.1 — Üç çekirdek veri yapısı
Tüm durum `IRunExecutionData` içinde taşınır; canlı çalışma seti `executionData` alt nesnesinde:

| Yapı | Ne tutar? |
|---|---|
| **`nodeExecutionStack`** | **Şimdi çalışmaya hazır** node'ların yapılacaklar listesi. Her eleman `IExecuteData = { node, data (girdi öğeleri), source }`. |
| **`waitingExecution`** | **Birden fazla girdisi olan** ve hâlâ bazı dallarını bekleyen node'ların **kısmi girdisi**. Anahtar: `waitingExecution[nodeAdı][runIndex].main[girdiIndeksi]`. |
| **`waitingExecutionSource`** | Bekleyen her girdinin kaynağını izleyen paralel yapı. |
| **`runData`** (sonuç biriktirici) | `runData[nodeAdı][runIndex] = ITaskData`. **Her node'un ürettiği her çıktının kalıcı kaydı.** `ITaskData = { startTime, executionTime, source, data: { main: [...] }, error?, executionStatus, ... }`. |

### 3.2 — Ana döngü (adım adım)
`processRunExecutionData()` kabaca şöyle döner:

1. **`nodeExecutionStack` boş değilken** (ve iptal/hedef'e ulaşılmadıkça) döngüye gir.
2. **Sıradaki node'u al.** Motor en son ittiğini alır (`pop` mantığı) → özünde **LIFO / derinlik-öncelikli (DFS)**. Ama sıra **`executionOrder` ayarına** bağlıdır:
   - **`v1`** (yeni workflow'larda varsayılan): adaylar **canvas konumuna göre sıralanır** ("en sol-üstteki önce") → **kararlı, soldan-sağa** sıra.
   - **`v0`** (eski): saf DFS (`unshift`).
   - *Dürüst cevap:* özünde **stack-tabanlı (DFS-eğilimli)**, ama v1 adayları konuma göre yeniden sıralayıp deterministik yapar.
3. **`runIndex` belirle:** `runIndex = runData[node].length ?? 0`. Node her çalıştığında sonuç bir sonraki indekse eklenir → **döngü/çatallanmaların aynı node'u birden çok kez çalıştırmasının** mekanizması budur.
4. **Node'u çalıştır** (`runNode()`). Çıktı: çıkış-konektörü başına bir dizi → `outputs[çıkışIndeksi] = [öğe, öğe, ...]`.
5. **Sonucu kaydet:** `ITaskData` üret, `runData[node]`'a ekle.
6. **Bağlantıları takip et:** `connectionsBySourceNode[node].main`'e bak; her çıkış indeksi ve bağlantı için, o çıkışta öğe varsa **`addNodeToBeExecuted(...)`** çağır.
7. Stack boşalınca **`waitingExecution`'ı kontrol et;** girdileri artık tamamlanan node'ları terfi ettir, sonra sonlandır.
8. **Sonlandır:** durumu ayarla (`success`/`error`/`waiting`/`canceled`), `workflowExecuteAfter` kancalarını çalıştır, tetikleyici fonksiyonlarını kapat.

### 3.3 — Çatallanma (çoklu çıkış)
**IF / Switch** gibi node'lar yalnızca **birden çok çıkış dizisi** döndürür: `[ trueÖğeler, falseÖğeler ]`.
Döngü her çıkış indeksini bağımsız gezip her birinin bağlantılarını takip eder. **Dal özel bir şey değildir** —
yalnızca dolu birden çok çıkış konektörü; her biri aşağı akışta stack girdisi doğurur.

### 3.4 — Birleştirme / tüm girdileri bekleme (kilit mekanizma)
Bu tamamen **`addNodeToBeExecuted()`** içinde `waitingExecution` ile yönetilir:

1. Aşağı akıştaki bir node'a ulaşılınca motor hedefin kaç **gelen `main` bağlantısı** olduğunu sayar.
2. **Tek girdi varsa** → doğrudan `nodeExecutionStack`'e itilir (çalışmaya hazır).
3. **Birden fazla girdi varsa** (örn. Merge) → **henüz çalıştırılmaz:**
   - Her girdi `i` için `waitingExecution[hedef][runIndex].main[i] = null` başlatılır.
   - Gelen dalın verisi kendi girdi indeksine yazılır.
   - **"Tüm veri geldi mi?"** kontrol edilir; herhangi bir indeks `null` ise node beklemede kalır.
   - **Ancak her girdi indeksi dolunca** birleşmiş çok-girdili `IExecuteData` stack'e taşınır, bekleme kaydı silinir.

Yani çok-girdili node **kendisini besleyen her üst dal veri teslim edene kadar bloke olur.** Bu, motorun
**join/senkronizasyon ilkeli**dir. (Hiç gelmeyen bir dal merge'i kalıcı bloke edebilir.)

> **BPM motoru için 4. ders:** **Stack + bekleme-tablosu** temiz, kanıtlanmış bir çekirdektir: çalışmaya hazır
> node'lar için ready-stack + join senkronizasyonu için node-başına kısmi-girdi tablosu. **Gezinme sırasını
> açık ve deterministik yap** (n8n'in v0→v1 göçü, sırayı örtük bırakmanın maliyetini gösterir).

---

## 4. Item Veri Modeli ve Node İçi Yürütme

### 4.1 — Öğe (item) şekli
Bir bağlantı üzerinde akan veri `INodeExecutionData[]` — bir **öğe dizisi**. Her öğe:

```json
{
  "json":   { /* asıl yük — $json bunu açar */ },
  "binary": { "<anahtar>": { "data": "<base64>", "mimeType": "...", "fileName": "...", "fileExtension": "..." } },
  "pairedItem": { "item": 0, "input": 0 }
}
```
Node çıktısı `INodeExecutionData[][]` — **çıkış konektörleri dizisi** (`output[0]` = 1. çıkıştaki öğeler, `output[1]` = 2. çıkış...).

### 4.2 — Node-içi yürütme modları
- **Run Once for All Items (varsayılan):** Node'un `execute()`'i **bir kez** çağrılır, **tüm girdi dizisini** alır; döngüyü kendi yönetir, tüm çıktı dizisini döndürür. Verimli; toplama/dönüştürme node'ları böyle çalışır.
- **Run Once for Each Item:** Motor node mantığını **öğe başına bir kez** çağırır; her çağrı tek öğe görür (`$json` o tek öğe). Çıktılar dizide toplanır. **Öğe bağlama (lineage) otomatik**tir.
- **`executeOnce` ayarı:** açıksa girdiyi `[0]`'a kırpar → node yalnız ilk öğeyle çalışır.

### 4.3 — `pairedItem` (soy ağacı / lineage)
Sorusu: "bu çıktı öğesini hangi girdi öğesi üretti?" — böylece `$('Önceki Node').item` gibi ifadeler **doğru
karşılık gelen satıra** çözülür (her zaman `[0]`'a değil). Yapı: `{ item: <girdiÖğeİndeksi>, input?: <girdiKonektörİndeksi> }`
(bir çıktı birden çok girdiden türerse **dizi** de olabilir).

**Otomatik bağlama kuralları:** 1 girdi→1 çıktı = indeksle 1:1; 1 girdi→çok çıktı = hepsi o tek girdiye; çok girdi/çok çıktı = **konuma göre**.
**Bağlama kopar:** bir node öğeleri *karşılığı korumadan* yeniden oluşturursa (örn. `pairedItem` set etmeyen Code node) veya bazı sınırlarda (tarihsel olarak alt-iş-akışı sınırı). Kopunca `$('Node').item` → "Paired item data unavailable" hatası.

> **BPM motoru için 5. ders:** **Öğe-olarak-dizi + açık lineage güçlü ama kırılgan** — n8n'in en yaygın
> runtime hataları lineage kopmalarıdır. Lineage'ı **motorun koruduğu birinci-sınıf bir özellik** yap; Code
> node ve alt-iş-akışı sınırlarında bile otomatik hayatta kalsın.

### 4.4 — Çoklu çalıştırma / `runIndex`
Aynı node **birden çok kez** çalışabilir (döngü içi, veya farklı dalların ayrı ayrı ulaşması). Her çalıştırma
yeni kayıt: `runData[node][0]`, `runData[node][1]`... `runIndex` ile indekslenir. Döngü yardımcıları geçerli
indeksi açar (`$('Loop Over Items').context['currentRunIndex']`).

---

## 5. Expression (İfade) Motoru

### 5.1 — Sözdizimi ve zamanlama
İfadeler node parametreleri içinde **`{{ ... }}`**. **Tembel (lazy)** değerlendirilir: **node çalışmadan hemen
önce, öğe başına** her parametrenin ifadesi o anki veri bağlamına çözülür. Kullanılmayan referanslar çözülmez
(veri proxy'si JS Proxy üzerine kurulu, erişimde çözer).

### 5.2 — Motor: Tournament + sandbox
n8n kendi şablon kütüphanesini, **Tournament**'ı (`riot-tmpl` uyumlu yeniden yazım) kullanır: ifadeyi **AST**'ye
ayrıştırır, tehlikeli AST düğümlerini **etkisizleştirir** (AST-tabanlı sandbox), sonra `Function` ile derler/çalıştırır.
Sertleştirilmiş sürümlerde değerlendirme **izole V8 bağlamına** taşınır (bellek/zaman limitli isolate, "Safe Globals").
Enjekte edilen kütüphaneler: **Luxon** (tarih: `$now`, `$today`), **JMESPath** (JSON sorgu).

> ⚠️ **Güvenlik notu (önemli):** n8n bu alanda gerçek **sandbox-escape RCE CVE'leri** yaşadı (CVE-2026-1470 / 2026-0863).
> **BPM motoru için 6. ders: Expression değerlendirmesini bir kolaylık değil, sert bir GÜVENLİK SINIRI olarak ele al** —
> izolasyonu (ayrı V8 isolate/süreç) baştan tasarla, sonradan yamamaya çalışma.

### 5.3 — Veri proxy'si ve değişkenler
Değişkenleri **`WorkflowDataProxy`** sunar: `$json`, `$binary`, `$input` (`.item/.all()/.first()/.last()`),
`$('Node')` / `$node["Name"]` (`.item` lineage ile çözülür), `$items('Node', çıkış, run)`, `$workflow`,
`$execution` (id, mode, **`resumeUrl`**), `$now`, `$today`, `$env`, `$parameter`, `$vars`, `$prevNode`, `$runIndex`, `$itemIndex`.
`$('Önceki').item` çözümü: proxy geçerli öğenin `pairedItem`'ını okur, geri yürüyüp hangi girdiden geldiğini bulur,
`runData` ve her node'un pairedItem'ı üzerinden **çok-sıçramalı** olarak referans node'daki eşleşen öğeye haritalar.

---

## 6. Kalıcılık ve Veritabanı

### 6.1 — Ne saklanır?
| Veri | Tablo(lar) |
|---|---|
| Workflow'lar | `workflow_entity` (+ `workflow_history`, `workflow_statistics`, tag tabloları) |
| Credentials | `credentials_entity` — **at-rest şifreli** (`N8N_ENCRYPTION_KEY`) |
| Executions | `execution_entity` (metadata + durum), `execution_data` (node girdi/çıktı verisi), `execution_metadata` |
| Webhook kayıtları | `webhook_entity` (metot + yol → workflow/node) |
| Ayar/kullanıcı/değişken | `settings`, `user`, `variables`, community node tabloları |
| İkili veri | DB **referans/metadata** tutar; gerçek baytlar moda göre ayrı (bkz. 6.4) |

### 6.2 — Desteklenen veritabanları
- **SQLite** — varsayılan (`~/.n8n/database.sqlite`). `DB_SQLITE_VACUUM_ON_STARTUP=true` ile pruning sonrası yer geri alınır.
- **PostgreSQL** — üretim için önerilen; queue & multi-main için **gerekli.**
- **MySQL/MariaDB — v1.0'da deprecated, v2.0'da kaldırıldı.** 2025/2026 tasarımı için yok say.

### 6.3 — Execution durum yaşam döngüsü
`new` (oluştu, başlamadı) → `running` → `success` / `error` / `crashed` (beklenmedik sistem hatası, örn. worker öldü);
`waiting` (Wait/onay/zamanlayıcıda duraklı); `canceled` (manuel durdurma); `unknown`.

### 6.4 — Hangi execution verisi saklanır + pruning
- `EXECUTIONS_DATA_SAVE_ON_SUCCESS` (varsayılan `all`), `..._ON_ERROR` (`all`), `..._SAVE_MANUAL_EXECUTIONS` (`true`), `..._ON_PROGRESS` (varsayılan `false`; node-node ara sonuçları → çökme kurtarma için ama I/O maliyetli).
- **Pruning** (`EXECUTIONS_DATA_PRUNE`, varsayılan **açık**): yaş **veya** sayıyla siler — `MAX_AGE` varsayılan **336 sa (14 gün)**, `PRUNE_MAX_COUNT` varsayılan **10.000** (`0`=sınırsız). **İki aşamalı silme:** önce soft-delete, sonra hard-delete (`HARD_DELETE_BUFFER` varsayılan 1 sa güvenlik penceresi). **Asla budanmaz:** `new`/`running`/`waiting` durumları ve etiketli/derecelendirilmiş execution'lar.

### 6.5 — İkili veri saklama modları (`N8N_DEFAULT_BINARY_DATA_MODE`)
`default` (bellekte; büyük dosyada ağır) · `filesystem` (diskte) · `s3` (ölçek için önerilen) · `database`.
**Queue-modu tuzağı (tasarım-kritik):** `filesystem` **queue ile uyumsuz** — dosya tek worker'a yereldir ama
herhangi bir worker herhangi bir işi alabilir → **paylaşımlı depo** şart: **S3** (önerilen) veya `database`.

> **BPM motoru için 7. ders:** Dağıttığın an **büyük yükler paylaşımlı dış depo (S3)** ister. Ayrıca
> **pruning + iki-aşamalı silme + duruma-göre saklama kurallarını erken kur** — execution verisi patlayarak
> büyür ve DB boyutuna hâkim olur.

---

## 7. Bekle / Devam Et ve Uzun-Soluklu Yürütmeler

### Wait node mekaniği — eşik
- **Kısa bekleme (< ~65 sn):** Süreç **bellekte kalır;** DB'ye offload **etmez**; süreç-içi zamanlayıcıyla devam eder.
- **Uzun bekleme (≥ 65 sn) veya dış-resume:** Motor **tüm yürütme durumunu DB'ye serileştirir** (`IRunExecutionData` + o ana kadarki `runData` + workflow'daki konum), süreç durabilir; resume koşulu ateşlenince motor **durumu yeniden yükleyip Wait node'dan devam eder.** Bu süre boyunca execution **`waiting`** durumundadır.

### Resume modları
1. Süre kadar bekle · 2. Belirli zamanda (sunucu saati) · 3. **Webhook çağrısıyla** — `$execution.resumeUrl` ile execution'a özel URL · 4. **Form gönderiminde.**
*Tuzak:* resume URL belirli execution'a bağlı → URL'i *gönderen* node, Wait ile **aynı execution**'da çalışmalı.

> **BPM motoru için 8. ders:** **Kalıcılaştır-ve-devam-et** (bekleme noktalarında `runExecutionData`'yı DB'ye
> serileştir) uzun-soluklu / insan-döngüde akışların temelidir — **BPM'in kalbi.** 65 sn bellek-içi vs DB-offload
> ayrımı kopyalanmaya değer makul bir optimizasyondur.

---

## 8. Alt İş Akışları (Execute Sub-workflow)

- **Veri girişi:** Ebeveynin girdi öğeleri çocuğun **Execute Sub-workflow Trigger** node'una akar. İki mod: **tüm öğelerle bir kez** veya **her öğe için bir kez** (öğe başına ayrı çocuk execution).
- **Veri çıkışı:** Çocuğun **son node'u** çıktısını ebeveyndeki Execute Sub-workflow node'una döndürür.
- **Senkron vs asenkron:** **"Wait for Sub-Workflow Completion"** — AÇIK = ebeveyn çocuk bitene kadar bloke (senkron, varsayılan); KAPALI = ateşle-unut.
- **Kayıtlar:** Her çağrı **ayrı execution kaydı** oluşturur (çapraz-bağlı). Tarihsel olarak bu sınır **`pairedItem` lineage'ını düşürür** — yeni motorda lineage'ı iş-akışı sınırından geçirmeyi planla.

→ BPM'de **Call Activity** karşılığı; modülerlik/yeniden-kullanımın temeli.

---

## 9. Hata Yönetimi (Runtime)

### Bir node hata fırlatınca
`runNode()` fırlatmayı yakalar. Davranış node'un **`onError`** ayarına bağlı (eski: `continueOnFail` boolean):
- **`stopWorkflow` (varsayılan):** node verisi kayda geri itilir, döngü kırılır, execution **`error`** işaretlenir, sonlanır.
- **`continueRegularOutput`:** hata öğesi (`.error` alanlı öğe) **normal çıkıştan** geçirilir, akış devam eder.
- **`continueErrorOutput`:** `handleNodeErrorOutput()` hatalı öğeleri **ayrı bir hata çıkışına** (son main çıkışı) yönlendirir; başarılar/başarısızlıklar iki dala ayrılır; hata öğeleri pairedItem ile kaynağa bağlı kalır. → editördeki görünür **hata-çıkış dalı.** (AI tool node'ları varsayılan olarak continue-on-fail.)

### Node-seviyesi retry
`for (tryIndex = 0; tryIndex < maxTries; tryIndex++)` ile sarılı. `retryOnFail=true` iken etkin.
`maxTries` = `min(5, max(2, maxTries||3))` → varsayılan 3, sert üst sınır 5. `waitBetweenTries` varsayılan 1000 ms, üst sınır 5000 ms.

### Hata iş akışları / Error Trigger
İlk node'u **Error Trigger** olan ayrı bir workflow, hedef workflow'un **Settings → Error workflow**'una atanır.
Ana workflow başarısız olunca n8n bu hata-akışını **çağırır** ve JSON yük geçirir (execution id/url, error mesaj/stack,
`lastNodeExecuted`, mode; workflow id/name). *Not: `execution.id/url` DB-kayıtlı execution gerektirir; trigger node hatalarında yoktur.*

### Bütün-execution retry & çökme kurtarma
Başarısız bir **execution bütün olarak yeniden denenebilir** (`retryOf` ile bağlı yeni execution). Ayrı bir
**Execution Recovery Service** çökme sonrası durumu olay-günlüğünden yeniden kurar; ardışık `crashed` execution'lar
workflow'u **otomatik deaktive** edebilir.

> **BPM motoru için 9. ders:** Üç katmanlı hata modeli sun — (a) node-seviye retry, (b) node-seviye davranış
> (durdur / devam / **hata-çıkış dalı**), (c) workflow-seviye **hata iş akışı** (telafi/bildirim). Bu, BPM'in
> error end event + boundary error + compensation üçlüsünün pragmatik karşılığıdır.

---

## 10. Döngüler

### Loop Over Items (Split In Batches)
**Kendini besleyen durumlu bir node**tur:
- İki çıkış: **`loop`** (geçerli batch) ve **`done`** (bitince tüm sonuç).
- Her çağrıda saklı girdiden sıradaki **batch**'i (boyut = Batch Size) dilimler, `loop`'tan yayar. Gövde node'ları batch'i işler ve **loop node'unun girdisine geri bağlanır** → sonraki çalıştırmayı tetikler.
- **Durum** node'un `context`'inde: `noItemsLeft`, `currentRunIndex` + kalan öğeler. Her yineleme yeni `runIndex`.
- **Sonlanma:** öğe kalmayınca `loop`'tan yaymayı bırakır, biriken sonucu `done`'dan yayar, motor `done` dalını izler.

### Motorun döngüyü ele alışı
Motor bir node'un üst node'una geri beslenmesine izin verir; özel "döngü opcode"u yoktur — graf'taki çevrim + node'un
iç sayacı sürer. **Tehlike:** `done` çıkışını tekrar loop'a bağlamak gerçek sonsuz çevrim → sınırsız `runData` →
**heap OOM / çökme** (belgelenmiş arıza modu).

> **BPM motoru için 10. ders:** Döngü/çevrim için **sert koruma ekle** (max yineleme, run-data sınırlama).
> n8n'in `done→self` OOM çökmesi uyarıcı bir vakadır; node-içi sayaca tek başına güvenme.

---

## 11. Kısmi Yürütme (Partial Execution v2) — Geliştirici Hızının Sırrı

"Buradan çalıştır" yalnız bir **alt-graf** çalıştırır: seçili node + girdisini doldurmak için gereken minimum
üst node kümesi — değişmeyen her şey için **önceki `runData` ve pin'lenmiş veri yeniden kullanılır.**

**v2 algoritması (`runPartialWorkflow2`):**
1. Workflow'dan **`DirectedGraph`** kur.
2. **Alt-graf çıkar:** devre dışı node'ları ele; tetikleyici(ler) ile **hedef node** arası ilgili kısmı bul.
3. **Kirli (dirty) node'ları hesapla** ve run-data'larını sil (yeniden çalışmaya zorla); değişmeyenler `runData`'sını korur.
4. **`findStartNodes`:** hedeften tetikleyiciye **geriye** yürüyüp her yoldaki **en erken kirli node'u** başlangıç yap.
5. **`recreateNodeExecutionStack`:** stack'i yeniden kur; her başlangıç node'unun girdisini **pin verisinden** (varsa) veya üst node'ların **önceki `runData`'sından** çekerek doldur.
6. Yeniden kurulan stack'i normal `processRunExecutionData()` döngüsüne ver.

**Kirli node** = parametresi, bağlantıları **veya** pin verisi son çalıştırmadan beri değişen node (ve aşağı bağımlıları).
**Pin'lenmiş veri:** manuel/kısmi çalıştırmada node'un çıktısını **dondurur** (node çalışmaz, pin öğeleri ikame edilir). Yalnız **tek main çıkışlı** node'lar pin'lenebilir; **production execution pin'i yok sayar.**

> **BPM motoru için 11. ders:** Kısmi yürütme (alt-graf + kirli-node + önbellekli run/pin'den stack yeniden kurma)
> **builder'ı hızlı yapan** özelliktir. `runData` önbelleği ve dirty-tracking modelini **1. günden** tasarla.

---

## 12. Ölçekleme (Queue Mode Detayı)

**Akış:** Tetikleyici main'de (veya webhook sürecinde) ateşlenir → main `execution_entity` (durum `new`) oluşturur
ve **BullMQ ile Redis kuyruğuna iş iter** (yük küçük: execution ID + bağlam). → Redis bekleyen işleri tutar; **sıradaki
boş worker** işi alır. → Worker workflow + credentials'ı DB'den yükler, çalıştırır (`running`), sonucu + nihai durumu
DB'ye yazar. → Tamamlanma Redis ile main'e sinyallenir (UI güncellenir). n8n'in kendi kıyaslaması: ~23 → ~162 req/s.

**Eşzamanlılık & worker sayısı:** Yatay = daha çok `n8n worker`. Worker-başına eşzamanlılık = `--concurrency=<N>`
(varsayılan 10). `N8N_CONCURRENCY_PRODUCTION_LIMIT` üretim eşzamanlılığını sınırlar. Toplam ≈ worker × eş-zamanlılık.

**Sağlık & zarif kapanış:** `QUEUE_HEALTH_CHECK_ACTIVE`/`_PORT`; `N8N_GRACEFUL_SHUTDOWN_TIMEOUT` (SIGTERM'de yeni iş
almayı kes, devam edenleri bitir). BullMQ stalled-job ayarları (`QUEUE_WORKER_LOCK_DURATION`, `..._STALLED_INTERVAL`,
`..._MAX_STALLED_COUNT`) ölen worker'ın işini yeniden kuyruğa alır → **iş kaybolmaz.**

**Multi-main (HA):** Birden çok main, hepsi queue modda, **aynı PostgreSQL + Redis**, **aynı n8n sürümü**,
sticky-session'lı load balancer arkası. `N8N_MULTI_MAIN_SETUP_ENABLED=true`. **Redis pub/sub neden şart:**
tetikleyiciler "en-fazla-bir-kez" → yalnız **lider** main sahiplenir (TTL anahtarıyla lider seçimi); aktif/pasif
ve ayar değişiklikleri pub/sub ile yayılır; lider çökerse takipçi devralır.

**Önemli env değişkenleri (motoru yöneten):** `EXECUTIONS_MODE`, `EXECUTIONS_TIMEOUT` (varsayılan `-1`/kapalı),
`N8N_CONCURRENCY_PRODUCTION_LIMIT`, `N8N_ENCRYPTION_KEY` (**tüm örneklerde aynı olmalı** yoksa paylaşılan
credential'lar çözülemez), `QUEUE_BULL_REDIS_*`, `N8N_MULTI_MAIN_SETUP_*`, `WEBHOOK_URL`, `N8N_DEFAULT_BINARY_DATA_MODE`, `DB_*`.

---

## 13. Özet: BPM Motoru Tasarımı İçin 11 Ders

| # | Ders | n8n'deki kanıt |
|---|---|---|
| 1 | **Orkestrasyonu yürütmeden ayır** (oluştur+kuyrukla vs çalıştır) | main vs worker |
| 2 | **Durum DB'de, kuyruk yalnız iş ID'leri; worker'lar durumsuz** | Postgres + Redis + worker reload |
| 3 | **Tetikleyiciler "en-fazla-bir-kez", tek sahipli → lider seçimi 1. günden** | multi-main + Redis pub/sub |
| 4 | **Stack + bekleme-tablosu çekirdeği; gezinme sırası açık/deterministik** | nodeExecutionStack + waitingExecution; v0→v1 |
| 5 | **Lineage'ı motor-korumalı birinci-sınıf yap** (Code/sub-workflow'da hayatta kalsın) | pairedItem kırılganlığı |
| 6 | **Expression = sert güvenlik sınırı; izolasyonu baştan kur** | Tournament sandbox + RCE CVE'leri |
| 7 | **Dağıtınca paylaşımlı dış depo (S3); pruning + iki-aşamalı silme erken** | binary mode + EXECUTIONS_DATA_PRUNE |
| 8 | **Kalıcılaştır-ve-devam-et = uzun-soluklu/insan-döngüde akışların kalbi** | Wait node DB serileştirme |
| 9 | **Üç katmanlı hata: node-retry + node-davranış + workflow hata-akışı** | onError + Error Trigger |
| 10 | **Döngü/çevrim için sert koruma (max yineleme, run-data sınırı)** | done→self OOM vakası |
| 11 | **Kısmi yürütme (dirty-node + önbellekli stack) builder'ı hızlandırır** | partial execution v2 |

---

## Kaynaklar
- n8n motor kaynağı: https://github.com/n8n-io/n8n/blob/master/packages/core/src/execution-engine/workflow-execute.ts
- Yürütme motoru (DeepWiki): https://deepwiki.com/n8n-io/n8n/2-workflow-execution-engine
- Veri erişimi & expression sistemi: https://deepwiki.com/n8n-io/n8n/2.3-workflow-data-access-and-expression-system
- Kısmi yürütme & hata: https://deepwiki.com/n8n-io/n8n/2.4-partial-execution-and-error-handling
- Queue mode: https://docs.n8n.io/hosting/scaling/queue-mode/
- Queue mode env değişkenleri: https://docs.n8n.io/hosting/configuration/environment-variables/queue-mode/
- Execution data (kaydetme & pruning): https://docs.n8n.io/hosting/scaling/execution-data/
- Binary data ölçekleme & dış depo (S3): https://docs.n8n.io/hosting/scaling/binary-data/ , https://docs.n8n.io/hosting/scaling/external-storage/
- Manuel/kısmi/production execution: https://docs.n8n.io/workflows/executions/manual-partial-and-production-executions/
- Data pinning: https://docs.n8n.io/data/data-pinning/
- Wait node: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.wait
- Execute Sub-workflow: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executeworkflow/
- Error Trigger: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.errortrigger/
- Loop Over Items (Split in Batches): https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.splitinbatches
- Tournament (expression kütüphanesi): https://github.com/n8n-io/tournament
- Expression sandbox RCE (CVE-2026-1470 & 2026-0863, JFrog): https://research.jfrog.com/post/achieving-remote-code-execution-on-n8n-via-sandbox-escape/
- Split in Batches sonsuz döngü OOM (issue): https://github.com/n8n-io/n8n/issues/21817

---

*Hazırlık tarihi: 2026-06-25 · 2 paralel araştırma ajanının n8n resmî doküman + kaynak kod taramasından sentezlenmiştir.
Düşük-seviye mekanizma detayları (alan adları, eşikler) hedef sürüme karşı doğrulanmalıdır.*
