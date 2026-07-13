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
Aksiyon **tanımı**, yeniden kullanılabilir bir **şablondur (`ActionDto`)**: `code` · `definition` · `icon` ·
`styleId` · `actionType` · `defaultAction` · `validation` · `stayOnPage` · `showHistory` · `actionDisplayType`.
Bir süreç adımına aksiyon eklenirken, tanımlı ActionDto'lar arasından seçilir ve bu alanlar **kopyalanır**.
**Detay → `../organization-settings/action.md`.**

### 1.2 — Adım-Aksiyon Binding (`ProcessStepActionDto`)
Bir aksiyon **bir adıma bağlandığında** ek alanlar tanımlanır. Şablon alanları (`code`/`definition`/`icon`/`styleId`/
`actionType`) ActionDto'dan **bir kez kopyalanır** (snapshot); aşağıda yalnız **adım-özel** alanlar tutulur.

> **Not:** Kopyalama **oluşturma anında bir kereliktir**; sonrasında ActionDto ile bu binding **bağımsızdır** (biri
> değişince diğeri etkilenmez). Bu yüzden binding'de **`actionId` / canlı bağ tutulmaz.**

| Alan | Açıklama |
|---|---|
| `id` | Binding kaydı ID'si (primary key) |
| `processStepId` | Bağlı süreç adımı (FK → `process-step.md`) |
| `targetProcessStepId` | Aksiyon çalışınca **ilerlenecek hedef süreç adımı** |
| `changeStatusId` | Aksiyon sonrası atanacak **durum** (→ `../organization-settings/status.md`) |
| `authorizationLevel` | **Yetki seviyesi** (aksiyonu kim yürütebilir) |
| `actionDisplayAuthorizedUserGroupId` | Aksiyonu **görebilecek** kullanıcı grubu |
| `showInHistory` | Süreç geçmişinde göster |
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
| **`parameters`** | Bir süreç adımından **diğer süreç adımına aktarılacak veriyi** taşır. | Adımlar arası veri geçişi gerekiyorsa. |
| **`changeList`** | **Formdaki alan değişikliklerini** taşır; aksiyon tetiklendiğinde listedeki form alanlarının **yeni değerleri güncellenir.** | Form alanlarında değişiklik olduğunda. |
| **`action`** | **HTTP Request** adımının **response**'undan gelebilen alan. Response'ta bir `action` (kod) varsa, adımdaki **aynı kodlu aksiyon** tetiklenir. | HTTP Request adımı çalışıp response döndüğünde. |

```jsonc
{
  "parameters": { /* adımdan adıma taşınacak veri                  — opsiyonel */ },
  "changeList": [ /* güncellenecek form alanları + yeni değerleri    — opsiyonel */ ],
  "action":     { /* HTTP response'undan gelen, tetiklenecek aksiyon — opsiyonel */ }
}
```

> **`changeList`**, her adım **iş yapmadan ÖNCE** forma uygulanır (evrensel giriş kuralı → `../flovo-bpm-engine.md` §4.2).

---

## 3. `actionType` — Aksiyon Türleri (kataloğu)
`actionType` = aksiyonun **türü / tetiklenme-davranış biçimi**.

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
> _(Detaylandırılacak: tetikleme koşulu, `default` ile ilişkisi.)_

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

---

## 8. Notlar / Ham Düşünceler
> _(Buraya ham düşünceler; sonra yukarı işlenir.)_

---

*Oluşturma: 2026-06-26.*
