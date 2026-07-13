# Yeni Flovo BPM vs n8n — Karşılaştırma

> **Amaç:** Yeni Flovo BPM motoru tasarımını, olgun ve iyi belgelenmiş bir referans motor olan **n8n** ile
> kıyaslamak; **nerede örtüşüyor, nerede ayrışıyor, n8n neyi kanıtlamış ve bizde hangi konu başarılı/eksik.**
>
> **Kaynak:** Tasarım dokümanları → `../../flovo-bpm-engine.md`, `../../service-settings/*`, `../../organization-settings/*` ·
> n8n analizleri → `../n8n/n8n-motor-nasil-calisir.md`, `../n8n/n8n-surec-adimlari-analizi.md`.
>
> **Uyarı — kategori farkı:** n8n **genel amaçlı entegrasyon/otomasyon** aracıdır (400+ konektör, item-dizi veri akışı);
> Flovo **kurumsal, form-merkezli BPM** platformudur (kayıt/form + adım-aksiyon + insan görevleri). Bu yüzden kıyas
> "hangisi iyi" değil, **"n8n'in kanıtlanmış motor çözümlerinden Flovo tasarımı ne öğrenmeli/farklılaşmalı"** eksenindedir.

---

## 0. Konumlandırma — Temel Felsefe Farkı
| Boyut | n8n | Yeni Flovo BPM |
|---|---|---|
| **Birincil amaç** | Sistemler arası **otomasyon/entegrasyon** | **Kurumsal iş süreçleri** (masraf, İK, envanter, denetim) |
| **Merkezî varlık** | **Workflow** (node graf'ı) + akan **item dizisi** | **Servis/Form** (kayıt) + **süreç adımı/aksiyon** |
| **Kullanıcı** | Otomasyon kuran teknik/yarı-teknik kişi | **Self-servis** süreç kuran kurumsal kullanıcı + son kullanıcı (form dolduran) |
| **İnsan görevi** | Wait (form/onay) ikincil | **Birinci sınıf** (Kullanıcı / Kullanıcı Grubu adımları, yetki, durum) |
| **Veri akışı** | Öğe (item) **dizisi** node'dan node'a | **Form kaydı** + adımlar arası `parameters`/`changeList`/`action` |
| **UI** | Serbest canvas (soldan sağa graf) | Form + süreç adımı + görüntüleme profili (adım-bazlı görünüm) |

> **Sonuç:** n8n **veri-akışı** motorudur; Flovo **kayıt/süreç** motorudur. Ortak çekirdek: adım grafiği, koşullu
> dallanma, bekleme/geri-dönüş, dış çağrı. Ayrışma: Flovo'da **form/kayıt + insan görevi + yetki + i18n** birinci sınıf.

---

## 1. Motor / Yürütme Mimarisi
| Konu | n8n (kanıtlanmış) | Yeni Flovo (tasarım durumu) |
|---|---|---|
| **Orkestrasyon ↔ yürütme ayrımı** | main (oluştur+kuyrukla) vs worker (çalıştır) | ❔ Tanımlı değil (`flovo-bpm-engine.md` motor iç mekaniği placeholder) |
| **Durum kalıcılığı** | State Postgres'te; Redis yalnız iş ID'si; worker'lar durumsuz | ❔ Tasarlanmadı |
| **Adım yürütme çekirdeği** | `nodeExecutionStack` + `waitingExecution` (ready-stack + join tablosu) | ❔ Yürütme algoritması detayı yok (adım→kod→aksiyon→hedef adım seviyesinde tanımlı) |
| **Bekle/devam et** | **Wait node**: <65 sn bellek, ≥65 sn DB'ye serileştir; webhook/form/zaman ile uyanır | ✅ Kavramsal karşılık var: **Processing/Kullanıcı bekleme + Webhook** (async geri dönüş, Customer API) — ama **kalıcılaştır-ve-devam-et** iç mekaniği yazılmadı |
| **Tetikleyiciler** | Webhook/Cron/Poll/Form/Chat/Email; "en-fazla-bir-kez", lider seçimi | ⚠️ **Webhook** var (Customer API); Süreç Başlangıcı manuel; **zamanlanmış/cron/poll tetikleyici tanımlı değil** |
| **Ölçekleme** | queue mode (BullMQ), multi-main HA, worker eşzamanlılığı | ❔ Tasarlanmadı |

**Örtüşme:** Flovo'nun **aksiyon-kodu → aksiyon → `targetProcessStepId`** modeli, n8n'in "çıkış→bağlantı→sonraki node"
gezinmesinin **BPM/form diline** uyarlanmış hâlidir. Flovo'da **Webhook + HTTP Request `async`** ikilisi, n8n'in **Wait +
resume URL** ilkelinin karşılığıdır.

---

## 2. Süreç Adımları / Node Envanteri
| n8n kategorisi | n8n örnekleri | Yeni Flovo karşılığı |
|---|---|---|
| **Trigger** | Webhook, Schedule, Form, Chat, Email, Error, Sub-workflow | **Süreç Başlangıcı** + **Webhook** (aksiyon); ⚠️ Schedule/Chat/Email/Error-trigger **yok** |
| **Akış kontrol** | IF, **Switch**, Filter, Merge, **Loop**, **Wait**, Stop&Error, Sub-workflow | **Switch** ✅ · **Processing/Kullanıcı** (bekleme) ✅ · **Süreç Adımı Tetikleme** (≈Sub-workflow) ✅ · ⚠️ **Merge/join, Loop (multi-instance), Filter** açık değil |
| **Veri işleme** | Set/Edit Fields, Aggregate, Sort, Split Out, Code, AI Transform | **Değer Atama** (≈Set) ✅ · ⚠️ toplama/sıralama/split, **Code adımı yok** (kasıtlı: no-code odak) |
| **Entegrasyon** | **HTTP Request** + 400+ konektör | **HTTP Request** ✅ (+ **Flovo Customer API** ile çift yön) · ⚠️ hazır konektör kataloğu yok (kasıtlı) |
| **AI** | Agent, Chain, Extractor, Classifier + cluster alt-node'ları | **Flovo AI** + **Flovo AI (Masraf)** ✅ (domain-özel) · ⚠️ takılabilir model/memory/tool mimarisi yok |
| **Form/insan** | Form Trigger, Wait(form), Send&Wait | **Kullanıcı / Kullanıcı Grubu**, **eventForm** aksiyon, **Instance Creator/Yönlendirme/Silme** ✅ (Flovo burada **daha zengin**) |

> **Flovo'nun güçlü tarafı:** form/kayıt yaşam döngüsü adımları (**Instance Creator/Silme/Yönlendirme**, eventForm, barkod init).
> n8n'de bunlar yok; n8n form'u yalnız tetikleyici/onay olarak görür. **Flovo'nun zayıf tarafı:** genel akış-kontrol
> ilkelleri (join, loop, filter) ve veri-şekillendirme node'ları henüz yok.

---

## 3. Veri Modeli & Değişkenler
| Konu | n8n | Yeni Flovo |
|---|---|---|
| **Taşınan veri** | `INodeExecutionData[]` — **item dizisi** (`json`+`binary`+`pairedItem`) | **Form kaydı** + adımlar arası `parameters`/`changeList`/`action` |
| **Soy ağacı (lineage)** | `pairedItem` (çıktı↔girdi eşlemesi) — güçlü ama kırılgan | ❔ Yok (form-merkezli olduğu için doğrudan gerekmeyebilir) |
| **Dinamik ifade** | `{{ }}` expression motoru (Tournament + sandbox), `$json/$node/$now...` | ⚠️ Tanımlı değil — `changeList`/`parameters` eşlemesi statik; ifade dili kararı açık |
| **Çoklu çalıştırma** | `runIndex` (döngü/çatal aynı node'u çok kez) | ❔ Modellenmedi |

> **Ayrışma:** n8n **koleksiyon (dizi)** üzerinde çalışır; Flovo **tek kayıt/form** üzerinde. Kurumsal onay/denetim için
> Flovo'nun **tek-kayıt + durum + geçmiş** modeli daha tanıdık ve denetlenebilirdir; ama **toplu işleme** (bir adımda N kayıt)
> senaryosunda n8n'in item-dizi modeli avantajlıdır — Flovo'da bu **Form List / Süreç Adımı Tetikleme** ile mi çözülecek, açık.

---

## 4. Akış Kontrol Derinliği
| İlkel | n8n | Yeni Flovo |
|---|---|---|
| **Exclusive gateway** | IF (true/false) | ✅ Aksiyon-kodu (`true`/`false`) + **Switch** |
| **Çok-yollu** | Switch (kural/ifade, fallback) | ✅ **Switch** adımı |
| **Join / senkron** | Merge (append/combine/SQL), waitingExecution | ⚠️ **Yok** — paralel dalların birleşimi tanımlı değil |
| **Döngü** | Loop Over Items (batch, `done`/`loop`) | ⚠️ **Yok** — multi-instance/iterasyon adımı tanımlı değil |
| **Bekleme** | Wait (süre/zaman/webhook/form) | ✅ **Processing/Kullanıcı + Webhook** (async) |
| **Hata durdurma** | Stop&Error → Error Trigger | ⚠️ Kısmi: aksiyon **`onFail`** kolu var; workflow-seviye hata akışı yok |
| **Alt-süreç** | Execute Sub-workflow (senkron/async, veri geri dönüşü) | ✅ **Süreç Adımı Tetikleme** — ama senkron/async + veri-dönüş semantiği tam yazılmadı |

---

## 5. Yapay Zeka
| Konu | n8n | Yeni Flovo |
|---|---|---|
| **Model** | Cluster: sabit kök + **takılabilir** Chat Model/Memory/Tool/Parser portları; sağlayıcı değiştirilebilir | **Flovo AI** + **Flovo AI (Masraf)** — **domain-özel, hazır** adımlar |
| **Yapısal çıktı** | Information Extractor / Output Parser (JSON şema) | ✅ AI adımı formu doldurur (`changeList` ile alanlara yazar) — masraf senaryosu net |
| **Ajan/otonomi** | AI Agent (araç çağıran, döngülü) | ⚠️ Otonom ajan/araç mimarisi yok (kurumsal determinizm açısından makul) |

> **Değerlendirme:** Flovo'nun AI'ı **kullanıma-hazır ve süreç-entegre** (fiş→form). n8n'in AI'ı **jenerik ve
> genişletilebilir**. Kurumsal determinizm için Flovo'nun **deterministik AI adımı** tercihi doğru; ama ileride
> "**takılabilir model/sağlayıcı**" fikri (OpenAI↔Claude değişimi tel çekmeden) örnek alınabilir.

---

## 6. Çapraz-Kesen Yetenekler (n8n'in "güvenilirlik" katmanı)
| Yetenek | n8n | Yeni Flovo |
|---|---|---|
| **Expression / sandbox** | `{{ }}` + izole V8; **RCE CVE'leri** yaşandı → sert güvenlik sınırı | ❔ İfade dili yok; eklenirse **baştan sandbox** olarak tasarlanmalı |
| **Retry (node-seviye)** | Retry On Fail + max tries + bekleme | ⚠️ Tanımlı değil (HTTP Request'te implicit olabilir) |
| **Hata modeli (3 katman)** | node-retry + node-davranış (stop/continue/hata-çıkışı) + workflow hata-akışı | ⚠️ Yalnız aksiyon `onFail`; çok katmanlı model yok |
| **Credentials** | Ayrı, **at-rest şifreli**, paylaşılabilir katman | ❔ Tasarlanmadı (HTTP Request kimlikleri nerede tutulacak?) |
| **Pin Data (mock)** | Node çıktısını dondurup test | ❔ Yok |
| **i18n** | Yerleşik form/kayıt çevirisi **yok** | ✅ **`code`-bazlı çeviri motoru** (ortak+organizasyon, `definition`=varsayılan dil) — **Flovo burada n8n'den ileride** |
| **Çok-kiracılık** | Proje/rol paylaşımı; org-seviye i18n yok | ✅ **Organization** varlığı (defaultLang, idle timeout, logo) |

---

## 7. Genişleme, Entegrasyon & Ölçekleme
- **Entegrasyon:** n8n = 400+ hazır konektör + HTTP Request kaçış kapısı. Flovo = **HTTP Request + Flovo Customer API**
  (müşteri custom code'u formları okur/yazar, Webhook tetikler). **Kasıtlı sadelik** — ama hazır konektör iştahı oluşursa
  Flovo'nun bir "konektör kataloğu" stratejisi gerekebilir.
- **Ölçekleme:** n8n'in queue/worker/multi-main modeli olgun. Flovo'da **motor dağıtım mimarisi henüz yok**; bulut-tabanlı
  hedef için (main/worker ayrımı, durumsuz worker, DB-merkezli state) **n8n'in 1–3. dersleri** doğrudan uygulanabilir.
- **Uzun-soluklu süreç:** n8n'in **kalıcılaştır-ve-devam-et** (Wait→DB serileştirme) ilkeli, Flovo'nun **Webhook ile
  günlerce bekleyen** süreçleri için birebir örnek — Flovo'da bu davranış **kavramsal** var, **iç mekaniği** yazılmalı.

---

## 8. Başarılı / Başarısız Değerlendirme (n8n'e göre)

### ✅ Başarılı / n8n'e göre güçlü olduğumuz alanlar
- **Form/kayıt yaşam döngüsü birinci sınıf:** Instance Creator/Silme/Yönlendirme, eventForm, barkod init — n8n'de karşılığı yok.
- **İnsan görevi + yetki + durum** modeli olgun (Kullanıcı/Kullanıcı Grubu, authorizationLevel, changeStatusId) — kurumsal onay/denetim için n8n'den daha uygun.
- **Yerleşik i18n:** organizasyon-seviye çeviri motoru (`code`/`definition`/override) — n8n'de form/kayıt çevirisi yok. **Net üstünlük.**
- **Çok-kiracılık:** `Organization` + ortak/organizasyon çevirisi ayrımı; n8n org-seviye i18n sunmaz.
- **Domain-özel AI:** Flovo AI (Masraf) süreç-entegre, kullanıma hazır; n8n jenerik AI'ı kurmayı gerektirir.
- **Determinizm/denetlenebilirlik:** tek-kayıt + durum + geçmiş modeli, n8n'in item-dizi + otonom ajan modeline göre kurumsal denetim için daha öngörülebilir.

### ⚠️ Başarısız / eksik / n8n'in kanıtlayıp bizde olmayanlar
- **Motor iç mekaniği yok:** yürütme durumu/kalıcılık, **bekleme-noktası serileştirme**, `runData` eşdeğeri, ölçekleme (queue/worker) `flovo-bpm-engine.md`'de **placeholder**. n8n'in en olgun kısmı tam da bu.
- **Akış-kontrol ilkeleri eksik:** **join/merge (paralel senkron)** ve **loop (multi-instance)** tanımlı değil; Filter/veri-şekillendirme yok.
- **Hata modeli sığ:** yalnız aksiyon `onFail`; n8n'in **3 katmanlı** (retry + node-davranış + hata-akışı) modeli yok.
- **Expression/ifade katmanı yok:** dinamik veri eşlemesi (`{{ }}` benzeri) ve — eklenirse — **sandbox güvenliği** kararı açık. n8n'in RCE CVE'leri bunun ne kadar kritik olduğunu gösteriyor.
- **Credentials katmanı yok:** HTTP Request/Customer API kimlikleri için ayrı, şifreli, paylaşılabilir kimlik yönetimi tasarlanmadı.
- **Tetikleyici çeşitliliği dar:** Schedule/cron, poll, e-posta, chat tetikleyicileri yok (yalnız manuel başlangıç + Webhook).
- **Alt-süreç semantiği yarım:** Süreç Adımı Tetikleme'nin senkron/async + veri-geri-dönüş + lineage davranışı yazılmadı.
- **Toplu/koleksiyon işleme belirsiz:** bir adımda N kayıt işleme (n8n item-dizi) senaryosu Flovo'da nasıl karşılanacak açık.

---

## 9. n8n'den Alınacak Somut Dersler (öneri)
1. **Orkestrasyonu yürütmeden ayır** (main/worker); **durum DB'de, worker durumsuz** — bulut hedefi için 1. günden.
2. **Kalıcılaştır-ve-devam-et** ilkelini `flovo-bpm-engine.md`'ye yaz: bekleme noktasında (Processing/Webhook) yürütme durumunu serileştir; Customer API tetiği ile devam et.
3. **Stack + bekleme-tablosu** çekirdeği: hazır-adım kuyruğu + çok-girdili adım için join tablosu; gezinme sırası **deterministik**.
4. **3 katmanlı hata modeli**: aksiyon-retry + adım-davranış (durdur/devam/`onFail` dalı) + **süreç-seviye hata akışı**.
5. **Döngü için sert koruma** (max iterasyon) — n8n'in `done→self` OOM vakası uyarıcı.
6. **İfade eklenirse sandbox baştan**: expression'ı kolaylık değil **güvenlik sınırı** olarak tasarla.
7. **Credentials'ı ayrı, şifreli, paylaşılabilir** katman yap (HTTP Request/Customer API için).
8. **Alt-süreç (Süreç Adımı Tetikleme)** için senkron/async + veri-dönüş semantiğini netleştir (n8n Execute Sub-workflow modeli).

---

## Kaynaklar
- n8n motor iç yapısı → `../n8n/n8n-motor-nasil-calisir.md`
- n8n adım/node envanteri → `../n8n/n8n-surec-adimlari-analizi.md`
- Flovo motor → `../../flovo-bpm-engine.md` · adımlar → `../../service-settings/process-step.md` · aksiyon → `../../service-settings/process-step-action.md`
- Flovo Customer API → `../../flovo-customer-api.md` · çeviri → `../../organization-settings/translation.md` · organizasyon → `../../organization-settings/organization.md`

---

*Oluşturma: 2026-07-01 · Tasarım dokümanları ile `../n8n/` analizleri karşılaştırılarak derlendi. n8n tarafı 2025/2026 sürümüne dayanır.*
