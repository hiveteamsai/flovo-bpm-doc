# Flovo — Süreç Adımı Aksiyonları (Process Actions) Tasarımı

> **Durum:** 🟢 DETAYLANIYOR
> **Amaç:** Bir süreç adımında **tetiklenebilen** aksiyonları, taşıdıkları veriyi ve görünümlerini tanımlamak.
> (Adım **tipleri** → `process-step.md`; motorun bunları **nasıl çalıştırdığı** → `../flovo-bpm-engine.md`;
> aksiyon **şablonu** → `../organization-settings/action.md`.)
>
> **Terim:** Bir **aksiyon (action)** = bir süreç adımında **tetiklenebilen** işlem. Tetiklendiğinde süreci ilerletir
> ve (gerekirse) veri taşır / form alanlarını günceller. Bir adım birden çok aksiyon barındırabilir.

---

## 0. Aksiyon Nedir?
- **Adım ↔ Aksiyon ilişkisi:** Bir adımda birden çok aksiyon olabilir; her aksiyonun bir **türü (`actionType`, §3)**,
  bir **görünümü (`styleId`, §4)** ve bir **veri aktarım modeli (§2)** vardır. Tanımı bir **şablondan** (`../organization-settings/action.md`) gelir.
- **Aksiyon kodu (action code):** Her aksiyonun bir **kod**u vardır; bir adım, ilerleyeceği aksiyonu bu **koda göre**
  seçer (örn. HTTP Request response'undaki `action` koduyla aynı kodlu aksiyon; Switch'te alandaki değere eşleşen kod;
  Karşılaştırma'da `true`/`false`). **Ayrılmış kodlar:** **`default`** = eşleşme yoksa / async / başarılı varsayılan
  ilerleme; **`onFail`** = adımda **hata** oluşunca → adım-seviyesi hata yönlendirmesi (`../flovo-bpm-engine.md` §7).

---

## 1. Aksiyon Veri Modeli

### 1.1 — Aksiyon Şablonu (`ActionDto`) → `../organization-settings/action.md`
Aksiyon **tanımı**, yeniden kullanılabilir bir **şablondur (`ActionDto`)**: `code` · `definition` · **`translationCode`** ·
`icon` · `styleId` · `actionType` · `validation` · `stayOnPage` · `showInHistory` · `showHistory` · `actionDisplayType`.
Bir süreç adımına aksiyon eklenirken, tanımlı ActionDto'lar arasından seçilir ve bu alanlar **kopyalanır**.
**Detay → `../organization-settings/action.md`.**

### 1.2 — Adım-Aksiyon Binding (`ProcessStepActionDto`)
Bir aksiyon **bir adıma bağlandığında** ek alanlar tanımlanır. Şablon alanları (`code`/`definition`/`translationCode`/`icon`/
`styleId`/`actionType`) ActionDto'dan **bir kez kopyalanır** (snapshot); aşağıda yalnız **adım-özel** alanlar tutulur.
_(`translationCode` `null` ise doğrudan `definition` kullanılır → çeviri es geçilir.)_

> **Not:** Kopyalama **oluşturma anında bir kereliktir**; sonrasında ActionDto ile bu binding **bağımsızdır** (biri
> değişince diğeri etkilenmez). Bu yüzden binding'de **`actionId` / canlı bağ tutulmaz.**

| Alan | Açıklama |
|---|---|
| `id` | Binding kaydı ID'si (primary key) |
| `processStepId` | Bağlı süreç adımı (FK → `process-step.md`) |
| `targetProcessStepId` | Aksiyon çalışınca **ilerlenecek hedef süreç adımı** |
| `changeStatusId` | Aksiyon sonrası atanacak **durum** (→ `../organization-settings/status.md`) |
| `mergeParameter` | **Parametre birleştirme** (bool) — hedefe taşınan `parameters`, adıma **gelen** parametrelerle birleştirilsin mi (§2.1). |
| `authorizationLevel` | **Yetki seviyesi** (aksiyonu kim yürütebilir) |
| `actionDisplayAuthorizedUserGroupId` | Aksiyonu **görebilecek** kullanıcı grubu |
| `showInHistory` | Geçmiş görüntülemede bu aksiyon görünür mü |
| `showHistory` | Aksiyon tamamlanınca kullanıcıya akış tarihçesini **otomatik göster** |
| `environmentRestriction` | Ortam kısıtı |

> **[İki ayrı katman]** **Aksiyon kodu** ile **`targetProcessStepId`** farklı işler yapar:
> - **Aksiyon kodu** = adımın **hangi aksiyonu tetikleyeceğini** seçer (`default` / `onFail` / `true` / `false` / switch / HTTP `response.action`).
> - **`targetProcessStepId`** = tetiklenen aksiyonun **hangi süreç adımına ilerleyeceğini** belirler.
>
> **Akış:** adım sonucu → **kod** → o kodlu aksiyon → aksiyonun **`targetProcessStepId`**'si → **sonraki adım**.

---

## 2. Aksiyon Veri Aktarım Modeli (`parameters` · `changeList` · `action`)
Bir aksiyon tetiklendiğinde taşıdığı veri modeli **3 alandan** oluşur. **Üçü de opsiyoneldir ve boş olabilir.**

| Alan | Ne için | Ne zaman dolar |
|---|---|---|
| **`parameters`** | Bir süreç adımından **diğer süreç adımına aktarılacak (geçici) veriyi** taşır (forma yazılmaz). Değer şekli `InstanceValue` ile **ortak**; **anahtar serbest**. | Adımlar arası veri geçişi gerekiyorsa. |
| **`changeList`** | **Formdaki alan değişikliklerini** taşır — **obje-map** `{ Property.code: value }`; aksiyon tetiklendiğinde bu alanların **yeni değerleri forma yazılır (kalıcı).** | Form alanlarında değişiklik olduğunda. |
| **`action`** | **HTTP Request** adımının **response**'undan gelebilen alan. Response'ta bir `action` (kod) varsa, adımdaki **aynı kodlu aksiyon** tetiklenir. | HTTP Request adımı çalışıp response döndüğünde. |

```jsonc
{
  "parameters": { /* adımdan adıma taşınacak GEÇİCİ veri — obje-map, serbest anahtar        — opsiyonel */ },
  "changeList": { /* forma yazılacak KALICI değerler   — obje-map { "Property.code": value } — opsiyonel */ },
  "action":     { /* HTTP response'undan gelen, tetiklenecek aksiyon                          — opsiyonel */ }
}
```

> **`changeList`**, her adım **iş yapmadan ÖNCE** forma uygulanır (evrensel giriş kuralı → `../flovo-bpm-engine.md` §4.2):
> `InstanceValue.data = data || changeList` (**doğrudan JSONB merge**).

### 2.1 — Parametre birleştirme (`mergeParameter`)
Varsayılan davranışta bir aksiyon, hedefe **yalnız kendi ürettiği** `parameters`'ı taşır; adıma **gelen** (`in`)
parametreler bir sonraki adıma **otomatik geçmez**. Bir aksiyonun binding'inde **`mergeParameter = true`** ise, aksiyon
hedefe taşıdığı `parameters`'a **bu adıma gelen parametreleri de ekler**:

> **Sıra:** önce **gelen (`in`)** parametreler `parameters`'a konur; **sonra** aksiyonun **ürettiği (`out`)** parametreler
> eklenir. **Anahtar çakışırsa `out` ezer** (aksiyonun ürettiği değer, gelen değeri geçersiz kılar).
>
> `parameters(out+in) = { ...gelenParametreler, ...aksiyonunÜrettiği }`   *(sağdaki — `out` — kazanır)*

- **`mergeParameter = false` (vars.):** hedefe yalnız `out` gider; `in` **düşer**.
- **`mergeParameter = true`:** `in` **korunur**, `out` üstüne yazılır → parametreler zincir boyunca **birikerek** akar.

**Ne zaman gerekir:** Bir değer birden çok adım **ötede** kullanılacaksa (özellikle **döngü/yönlendirme** kollarında),
ara adımların onu her seferinde yeniden üretmesi gerekmez — `mergeParameter = true` ile taşınır. Örnek: yönlendirme
zincirinde başlatıcı/atanan/aktarım-hedefi bilgisinin hop'tan hop'a taşınması → `../sampleProcess/referred`.

> **`changeList` ile farkı:** `changeList` **forma** yazılan **kalıcı** alan değerleridir; `parameters` ise adımlar arası
> taşınan **geçici** veridir (forma yazılmaz). `mergeParameter` yalnız **`parameters`**'ı ilgilendirir.

### 2.2 — Değer modeli (ortak değer dili)
Motor **koleksiyon-tabanlıdır** (→ `../flovo-bpm-engine.md` §3): hem `changeList` hem `parameters` içindeki değerler,
**`InstanceValue.data` ile aynı değer-modelini** kullanır — yani **`propertyValuesTemplates`** şekilleri (skaler ·
`LabeledValue {value, display, translationCode}` · user-ref `{userId, nameSurname}` · phone `{countryCode, number}` ·
list-of-model …). Böylece bir değer **kayıpsız** akar: forma yazmak = düz JSONB merge, adıma taşımak = aynı objeyi geçirmek.

| Boyut | `changeList` | `parameters` |
|---|---|---|
| **Yapı** | **obje-map** `{ code: value }` | **obje-map** `{ key: value }` |
| **Anahtar** | **zorunlu `Property.code`** (yazılan servisin **yazılabilir** alanı) | **serbest** — bir form alanını besliyorsa konvansiyon olarak hedef `Property.code` |
| **Değer şekli** | `propertyValuesTemplates` (InstanceValue ile ortak) | `propertyValuesTemplates` (aynı) |
| **Hedef / ömür** | **forma yazılır** (`InstanceValue.data`, kalıcı, Attr'a projeksiyon, Change'e log) | **forma yazılmaz** (geçici; `mergeParameter` ile birikir) |

- **Yazılamaz alanlar `changeList`'e konmaz:** `text` (statik label) · **`live`** yansımalar (`flowInfo`/`userInfo`/`parentProperty`) ·
  `savePropertyToDb=false` — bunlar `InstanceValue.data`'ya da yazılmaz (→ `../models/processInstances/instance-value.md` anahtar konvansiyonu).
- **Bütünsel değer taşıma:** Bir alanın değeri **model/dizi** ise (formList/groupByTaxReceipt/phone/mapViewer…), alt-alanlardan
  biri değişse bile o alanın **tüm değeri komple** taşınır — **kısmi patch yok** (merge o `code`'daki değeri bütünüyle değiştirir).
- **Doğrulama:** `changeList` değerleri de tip-başına **JSON Schema kapısıyla** doğrulanır (kullanıcı girişi / API ile **aynı** kapı).

---

## 3. `actionType` — Aksiyon Türleri (kataloğu)
`actionType` = aksiyonun **türü / tetiklenme-davranış biçimi**.

> **Aksiyon tipi seti = sabit / kapalı (KARAR).** `actionType` değerleri **önceden tanımlı, kapalı bir settir**; plugin/SDK
> ile yeni bir aksiyon tipi **eklenemez**. Her tipin davranışı **Flovo tarafından** geliştirilir/bakılır (→ `process-step.md`
> §1 karar notu).

### 3.1 — `manual` (Manuel)
Kullanıcı frontend'de **elle** tetikler (ek form/pop-up yok). İnsan-tetiklemeli adımlarda kullanılır.

### 3.2 — `eventForm`
Aksiyon alınırken bir **pop-up form** gösterir; kullanıcı doldurarak aksiyonu tamamlar (neden/ek bilgi girişi).
- Aksiyon tanımlanırken **`formType = eventForm`** olan servislerin **görüntüleme profilleri** listelenir; seçili profildeki
  **alanlar (property) pop-up** olarak çıkar, **iş kuralları (`BusinessRule`)** ile alanlara özellik kazandırılabilir.
- Pop-up'ta girilen değerler **aksiyon parametresi (`parameters`)** ile taşınır; bu yüzden eventForm için **`Instance`
  oluşturulmaz / akış gerekmez** (→ `../models/service-settings/service.md` `formType = eventForm`).

### 3.3 — `takePhoto` (Fotoğraf Çek)
**Kamerayı açar**; çekilen fotoğrafı bir **file property**'sine yazar/forma ekler (insan-tetiklemeli). İlgili alan → `properties.md` §3.8.
> _(Detaylandırılacak: hedef file property, kırpma.)_

### 3.4 — `selectFile` (Dosya Seç)
**Dosya seçiciyi açar**; seçilen dosyayı bir **file property**'sine ekler. İlgili alan → `properties.md` §3.8.
> _(Detaylandırılacak: çoklu dosya, hedef property.)_

### 3.5 — `scanBarcode` (Barcode Tara)
**Barkod okuyucuyu açar**; okunan değeri bir **property**'ye yazar (manuel giriş opsiyonludur). İlgili alan → `properties.md` §3.10.
> _(Detaylandırılacak: hedef property, barkod formatı.)_

### 3.6 — `webhook` (Webhook)
**Uygulama dışından bir HTTP request ile tetiklenebilen** aksiyon türü. Frontend'de elle tetiklenmez; örn. **müşteri
sunucusundaki custom code**, **Flovo Customer API** ile bu Webhook aksiyonunu (**`parameters`** ile) tetikler ve süreci
ilerletir — async HTTP Request'in (→ `process-step.md` §3.2) **geri-dönüş kolu** olarak yaygın kullanılır.

> **Webhook aksiyonu nereye bağlanır (anlam karmaşasını önle):**
> - **Ana süreci başlatmak (dışarıdan):** Webhook aksiyonu **Süreç Başlangıcı**'na (`process-step.md` §3.1) eklenir → dış
>   çağrı **yeni bir ana süreç çalıştırması** başlatır.
> - **Ana süreç içinde bir adımı ilerletmek:** Webhook aksiyonu ilgili **var olan adıma** eklenir → o adımı ilerletir.
> - **Bağımsız bir alt süreci tetiklemek:** Aksiyon değil, **Alt Süreç Başlangıcı** adımı (`process-step.md` §3.20) hedeflenir;
>   oradaki webhook o adıma bağlı **`default`** aksiyonuna dönüşür (aksiyonun bağlanacağı bir adım olmama sorunu böyle çözülür).
>
> Üç durumda da webhook **bir süreç adımına** bağlıdır → `ProcessStepInstance.processStepId` sorunsuz atılır. Örn.
> `../sampleProcess/createPdfAsync` (bağımsız alt süreç), `../sampleProcess/integration`. İlgili: **`../flovo-customer-api.md`**.
> _(Detaylandırılacak: webhook URL/secret, payload → `parameters`/`changeList` eşlemesi, güvenlik, idempotency.)_

### 3.7 — `autoAction` (Autoaction)
**Kullanıcı eylemi olmadan otomatik** tetiklenen aksiyon (örn. adıma gelince / koşul sağlanınca). Otomatik adımların
"kendiliğinden ilerleme"sini aksiyon düzeyinde ifade eder.
> **`default` ile ilişkisi (Processing):** **Processing** adımının otomatik ilerlemesi **opsiyoneldir** — adımda **`default` kodlu
> bir `autoAction`** varsa manuel aksiyon beklenmeden onunla ilerler; **yoksa** adım **bekler** (webhook/başka aksiyon gelene dek
> → `process-step.md` §3.18). _(Diğer otomatik adımlar — Flovo AI, HTTP Request vb. — zaten `default`/`onFail` ile ilerler.)_
> _(Detaylandırılacak: genel tetikleme koşulu ifadesi.)_

---

## 4. `styleId` — Renk / Görünüm
Aksiyonun `styleId` alanı, bir **Style** varlığına **referanstır** (renk/görünüm: bg + font). Style **çapraz-kesen** bir
varlıktır (aksiyon, durum) ve **ayrı dokümanda** tanımlanır → **`../organization-settings/style.md`**.

---

## 5. Adım-Ortak Aksiyon Ayarları (her adımda bulunabilecek özellikler)
> _(Doldurulacak — "yazım ve güvenilirlik deneyimini" tanımlar.)_ Bu başlıkların **açık kararları** merkezi `todo.md`'de
> izlenir (retry/onFail → "Hata yönetimi" · expression/veri eşleme/koşullu → "Aksiyon parametrelerinde ifade/kod desteği" ·
> credential → "Güvenlik" · yetki/rol → "Yetkilendirme").
- **İfade (expression) motoru** — alanları dinamik doldurma, önceki adıma erişim
- **Veri eşleme (sürükle-bırak)**
- **Yeniden deneme (retry on fail)** — max deneme + bekleme
- **Hata davranışı** — `onFail` aksiyonu (§0)
- **Koşullu çalışma** — adım yalnız X koşulunda çalışsın
- **Yetki/rol kısıtı** — aksiyonu kim yürütebilir (`authorizationLevel`, `actionDisplayAuthorizedUserGroupId`)
- **Credential / kimlik yönetimi** (ayrı, şifreli, paylaşılabilir)

---

## 6. Katalog Dokümantasyon Şablonu (§3 `actionType` girişlerini yazarken)
> Aksiyonun **alan tanımları** (şablon) → `../organization-settings/action.md`. Aşağıdaki iskelet, §3'teki **tür (actionType) katalog
> girişlerini** anlatmak için kullanılır.

```
### <actionType Adı>
- **actionType:** (`manual` / `eventForm` / `takePhoto` / ...)
- **Tetiklenme:** (manuel / otomatik / dış çağrı)
- **Hangi adımlarda kullanılır:**
- **Veri aktarımı:** (parameters / changeList / action — hangileri dolar)
- **Hedef property / ayar:** (varsa)
```

---

## 7. Açık Kararlar / Sorular
> **Açık sorular tek yerde:** Bu dokümanın açık kararları/soruları, tutarsızlığı önlemek için **yalnız** merkezi
> [`todo.md`](../todo.md) dosyasında toplanır (önceliklendirilmiş tüm-doküman listesi). İlgili maddeler orada `(process-step-action §..)`
> atfıyla bulunur; verilen kararlar bu dokümanın **gövdesinde** anlatılır.

> **Çözülenler (yerel karar log'u):**
- [x] **Genişletilebilirlik (aksiyon seti) — ÇÖZÜLDÜ (v0.30):** `actionType` **sabit / kapalı settir**; plugin/SDK ile yeni
  aksiyon tipi **eklenemez**; davranışları **Flovo** geliştirir/bakar (→ §3 karar notu · `process-step.md` §1).

---

## 8. Notlar / Ham Düşünceler
> _(Buraya ham düşünceler; sonra yukarı işlenir.)_

---

*Oluşturma: 2026-06-26.*
