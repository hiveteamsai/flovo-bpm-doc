# Flovo — Süreç Adımı Aksiyonları (Process Actions) Tasarımı

> **Durum:** 🟢 DETAYLANIYOR
> **Amaç:** Bir süreç adımında **tetiklenebilen** aksiyonları, taşıdıkları veriyi ve görünümlerini tanımlamak.
> (Adım **tipleri** → `process-step.md`; motorun bunları **nasıl çalıştırdığı** → `../flovo-bpm-engine.md`;
> aksiyon **şablonu** → `../genel-ayarlar/action.md`.)
>
> **Terim:** Bir **aksiyon (action)** = bir süreç adımında **tetiklenebilen** işlem. Tetiklendiğinde süreci ilerletir
> ve (gerekirse) veri taşır / form alanlarını günceller. Bir adım birden çok aksiyon barındırabilir.

---

## 0. Aksiyon Nedir?
- **Adım ↔ Aksiyon ilişkisi:** Bir adımda birden çok aksiyon olabilir; her aksiyonun bir **türü (`actionType`, §3)**,
  bir **görünümü (`style`, §4)** ve bir **veri aktarım modeli (§2)** vardır. Tanımı bir **şablondan** (`../genel-ayarlar/action.md`) gelir.
- **Aksiyon kodu (action code):** Her aksiyonun bir **kod**u vardır; bir adım, ilerleyeceği aksiyonu bu **koda göre**
  seçer (örn. HTTP Request response'undaki `action` koduyla aynı kodlu aksiyon; Switch'te alandaki değere eşleşen kod;
  Karşılaştırma'da `true`/`false`). **Ayrılmış kodlar:** **`default`** = eşleşme yoksa / async / başarılı varsayılan
  ilerleme; **`onFail`** = adımda **hata** oluşunca → adım-seviyesi hata yönlendirmesi (`../flovo-bpm-engine.md` §7).

---

## 1. Aksiyon Veri Modeli

### 1.1 — Aksiyon Şablonu (`ActionDto`) → `../genel-ayarlar/action.md`
Aksiyon **tanımı**, yeniden kullanılabilir bir **şablondur (`ActionDto`)**: `code` · `definition` · `icon` ·
`style` · `actionType` · `defaultAction` · `validation` · `stayOnPage` · `showHistory` · `actionDisplayType`.
Bir süreç adımına aksiyon eklenirken, tanımlı ActionDto'lar arasından seçilir ve bu alanlar **kopyalanır**.
**Detay → `../genel-ayarlar/action.md`.**

### 1.2 — Adım-Aksiyon Binding (`ProcessStepActionDto`)
Bir aksiyon **bir adıma bağlandığında** ek alanlar tanımlanır. Şablon alanları (`code`/`definition`/`icon`/`style`/
`actionType`) ActionDto'dan **kopyalanır**; aşağıda yalnız **adım-özel** alanlar tutulur.

| Alan | Açıklama |
|---|---|
| `targetProcessStepId` | Aksiyon çalışınca **ilerlenecek hedef süreç adımı** |
| `changeStatusId` | Aksiyon sonrası atanacak **durum** (→ `../genel-ayarlar/status.md`) |
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

### 3.1 — Manuel
Kullanıcı frontend'de **elle** tetikler (ek form/pop-up yok). İnsan-tetiklemeli adımlarda kullanılır.

### 3.2 — withForm
Aksiyon alınırken bir **form / pop-up** gösterir; kullanıcı bunu doldurarak aksiyonu tamamlar (neden/ek bilgi girişi).
> _(Açık: gösterilen form serbest pop-up mı, formun bir görüntüleme profili mi? → §7)_

### 3.3 — Fotoğraf Çek
**Kamerayı açar**; çekilen fotoğrafı bir **file property**'sine yazar/forma ekler (insan-tetiklemeli). İlgili alan → `properties.md` §3.8.
> _(Detaylandırılacak: hedef file property, kırpma.)_

### 3.4 — Dosya Seç
**Dosya seçiciyi açar**; seçilen dosyayı bir **file property**'sine ekler. İlgili alan → `properties.md` §3.8.
> _(Detaylandırılacak: çoklu dosya, hedef property.)_

### 3.5 — Barcode Tara
**Barkod okuyucuyu açar**; okunan değeri bir **property**'ye yazar (manuel giriş opsiyonludur). İlgili alan → `properties.md` §3.10.
> _(Detaylandırılacak: hedef property, barkod formatı.)_

### 3.6 — Webhook
**Uygulama dışından bir HTTP request ile tetiklenebilen** aksiyon türü. Frontend'de elle tetiklenmez; örn. **müşteri
sunucusundaki custom code**, **Flovo Customer API** ile bu Webhook aksiyonunu (**`parameters`** ile) tetikler ve süreci
ilerletir — async HTTP Request'in (→ `process-step.md` §3.2) **geri-dönüş kolu** olarak yaygın kullanılır.
> Örn. `../sampleProcess/createPdfAsync`, `../sampleProcess/integration`. İlgili: **`../flovo-customer-api.md`**.
> _(Detaylandırılacak: webhook URL/secret, payload → `parameters`/`changeList` eşlemesi, güvenlik, idempotency.)_

### 3.7 — Autoaction
**Kullanıcı eylemi olmadan otomatik** tetiklenen aksiyon (örn. adıma gelince / koşul sağlanınca). Otomatik adımların
"kendiliğinden ilerleme"sini aksiyon düzeyinde ifade eder.
> _(Detaylandırılacak: tetikleme koşulu, `default` ile ilişkisi.)_

---

## 4. `style` — Renk / Görünüm
Aksiyonun `style` alanı, bir **Style** varlığına **referanstır** (renk/görünüm: bg + font). Style **çapraz-kesen** bir
varlıktır (aksiyon, durum, alan...) ve **ayrı dokümanda** tanımlanır → **`../genel-ayarlar/style.md`**.

---

## 5. Adım-Ortak Aksiyon Ayarları (her adımda bulunabilecek özellikler)
> _(Doldurulacak — "yazım ve güvenilirlik deneyimini" tanımlar.)_
- [ ] **İfade (expression) motoru** — alanları dinamik doldurma, önceki adıma erişim
- [ ] **Veri eşleme (sürükle-bırak)**
- [ ] **Yeniden deneme (retry on fail)** — max deneme + bekleme
- [ ] **Hata davranışı** — `onFail` aksiyonu (§0)
- [ ] **Koşullu çalışma** — adım yalnız X koşulunda çalışsın
- [ ] **Yetki/rol kısıtı** — aksiyonu kim yürütebilir (`authorizationLevel`, `actionDisplayAuthorizedUserGroupId`)
- [ ] **Credential / kimlik yönetimi** (ayrı, şifreli, paylaşılabilir)

---

## 6. Katalog Dokümantasyon Şablonu (§3 `actionType` girişlerini yazarken)
> Aksiyonun **alan tanımları** (şablon) → `../genel-ayarlar/action.md`. Aşağıdaki iskelet, §3'teki **tür (actionType) katalog
> girişlerini** anlatmak için kullanılır.

```
### <actionType Adı>
- **actionType:** (Manuel / withForm / Fotoğraf Çek / ...)
- **Tetiklenme:** (manuel / otomatik / dış çağrı)
- **Hangi adımlarda kullanılır:**
- **Veri aktarımı:** (parameters / changeList / action — hangileri dolar)
- **Hedef property / ayar:** (varsa)
```

---

## 7. Açık Kararlar / Sorular
- [ ] **`defaultAction` bool ↔ `default` kodu** — ikisi de "varsayılan"ı işaret ediyor; nasıl birleşsin? (→ `../genel-ayarlar/action.md`)
- [ ] **`withForm` formu** — serbest bir pop-up form mu, yoksa formun bir **görüntüleme profili** mi? (→ `view-profile.md`)
- [ ] **`changeList` öğesinin yapısı** (form alanı id + yeni değer + tip?)
- [ ] **`action` nesnesinin şekli** (tetiklenecek sonraki aksiyon kodu mu?)
- [ ] `action` zinciri (HTTP Request → action → ...) **sonsuz döngüye** karşı nasıl korunur?
- [ ] Aksiyonlar sabit set mi, iş ortağı/müşteri tarafından eklenebilir mi?
- [ ] Aksiyon parametreleri ne kadar "ifade" (kod) destekler (no-code ↔ pro-code dengesi)?

---

## 8. Notlar / Ham Düşünceler
> _(Buraya ham düşünceler; sonra yukarı işlenir.)_

---

*Oluşturma: 2026-06-26.*
