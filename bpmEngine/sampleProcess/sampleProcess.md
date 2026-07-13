# Örnek Süreçler — İndeks (sampleProcess)

> **Amaç:** Flovo BPM motoru üzerinde **self-servis** olarak nasıl süreç kurgulandığını **uçtan uca örneklerle**
> göstermek. Her örnek bir klasördedir: **`<ad>.jpg`** (görsel) + **`process.md`** (**detaylı spec:** amaç → diyagram →
> adım adım görev/ayar/aksiyon + **parametre akışı**). Bu örnekleri **bpm-engine'i iyileştirmek** için kullanırız.
>
> **Tasarım dokümanları:** adımlar → `../service-settings/process-step.md` · aksiyonlar → `../service-settings/process-step-action.md` / `../organization-settings/action.md` ·
> alanlar → `../service-settings/properties.md` · motor → `../flovo-bpm-engine.md`.

---

## Örnekler
| Örnek | Ne örnekliyor | Öne çıkan motor öğeleri |
|---|---|---|
| [**expense**](./expense/process.md) — Masraf oluşturma | 3 başlatma yöntemi · AI tarama · loading kart · hata telafisi | Instance Creator · **Processing(showLoading)** · **Flovo AI(Masraf)** · **default/onFail** · Bildirim · **Instance Deleter** |
| [**createPdf**](./createPdf/process.md) — PDF (senkron) | Dış sunucuda PDF üretip **bekleyerek** dönme | **HTTP Request (`async=false`)** · `parameters` · Bildirim |
| [**createPdfAsync**](./createPdfAsync/process.md) — PDF (async) | Beklemeden ilerleme + dış sistemden **geri dönüş** | **HTTP Request (`async=true`)** · **Webhook** |
| [**integration**](./integration/process.md) — Asenkron entegrasyon | Uzun aktarımı **durum güncelleyerek** bekleme | HTTP Request async · **Processing(showLoading=false)** · **Webhook** · Süreç Bitişi |
| [**scanBarcode**](./scanBarcode/process.md) — Barkod ile var olanı aç | Yanıta göre **koşullu dallanma** | **`response.action` zinciri** (`createForm`/`yonlendir`) · **Form Yönlendirme** · Instance Creator |

---

## Özetler

### 1. expense — Masraf Oluşturma
Süreç Başlangıcı altında **3 aksiyon** (`takePhoto` / `selectFile` / `manual`). Fotoğraf/Dosya → Instance Creator (thumbnail'dan
form üretir) → **Processing** (loading kart) → **Flovo AI (Masraf)** → **Bildirim** (parametre-modu) → Kullanıcı. AI
**hata** verirse `onFail` → Bildirim (toast) → **Instance Deleter** (telafi). "Belgesiz" kolu AI'sız, doğrudan form üretip kullanıcıya.

### 2. createPdf — PDF (Senkron)
**HTTP Request** adımı form id ile müşteri sunucusuna istek atar, **`async=false`** → **bekler**; başarıda `default` →
**Bildirim** (mesajlı) → Kullanıcı. (Önünde başka bir süreç vardır; görsel yalnız PDF bölümüdür.)

### 3. createPdfAsync — PDF (Asenkron)
Aynı iş **`async=true`**: istek atılır, **beklenmez** → `default` → Kullanıcı. Müşteri sunucusu PDF'i bitirince
**Webhook** aksiyonunu `parameters` ile tetikler → **Bildirim**.

### 4. integration — Asenkron Entegrasyon
**HTTP Request (async)** ile entegrasyon başlatılır → **Processing "Aktarım Bekleniyor"** (`showLoading=false`,
**durum güncellenir**, forma güncel bilgi). Müşteri sunucusu bitince **Webhook** → **Süreç Bitişi**.

### 5. scanBarcode — Barkod ile Var Olanı Aç
**2 başlatma aksiyonu** (`scanBarcode` / eventForm-barkod gir). Barkod **HTTP Request (Function)** ile sunucuya gider;
yanıt **`action=yonlendir`** ise **Form Yönlendirme** (var olan form açılır), **`action=createForm`** ise **Instance Creator**
(barkod init değerli yeni form) → Kullanıcı.

---

## Motor için Çıkarımlar (bpm-engine'i iyileştirmek)
Örneklerden çıkan, tasarım dokümanlarında **netleştirilmesi/eklenmesi** gereken davranışlar:

1. ✅ **Processing `showLoading`** — `../service-settings/process-step.md` §3.18'e **işlendi:** bu adımda formun **detayı/değerleri**
   görünmesin isteniyorsa **aktif** edilir (frontend "yükleniyor" gösterir, girişi engeller). `false` = normal görünüm
   (+ genelde durum güncelleme). _(→ açık soru merkezi listede: Processing durum değişimi, ../todo.md)_
2. ✅ **Aksiyonu tetikleyen HTTP isteğine response** — `../flovo-bpm-engine.md` **§6.3**'e işlendi: süreç **Kullanıcı /
   Kullanıcı Grubu / Processing / Süreç Bitişi** adımlarına geldiğinde **form bilgileri** tetikleme isteğinin response'unda döner.
3. ✅ **Bildirim kanalları + parametre** — `../service-settings/process-step.md` **§3.6**'ya işlendi: **3 kanal** (Mail / Bildirim-Push / Toast);
   **parametre yalnız Push ve Toast**'ta (UI'da görünmez, runtime veri güncelleme). Mail'de parametre yok.
4. ✅ **Webhook** — `../service-settings/process-step-action.md` **§3.6**'ya işlendi: **uygulama dışından HTTP request ile** (müşteri sunucusu →
   Flovo Customer API) tetiklenen aksiyon; async geri-dönüş kolu.
5. ✅ **Instance Creator init değerleri** — `../service-settings/process-step.md` **§3.12**'ye işlendi: alana karşılık değer veya thumbnail url;
   aksiyon `parameters`'ı ile eşleşip alanlara initial değer atanır.
6. **`response.action` zinciri** (scanBarcode): custom kodlar (`createForm`/`yonlendir`) → aynı kodlu aksiyon → her
   aksiyonun **`targetProcessStepId`**'si hedef adıma götürür. §1.2 modelini doğrular. _(zaten modelde — onay.)_
7. ✅ **Flovo Customer API** — **`../flovo-customer-api.md`** oluşturuldu (endpoint listesi + teorik iş özeti; müşteri
   sunucusundaki custom code'un Flovo formlarını okuyup/yazıp **Webhook** tetiklemesi için).

## Açık Noktalar

> **Açık sorular tek yerde:** Bu dokümanın açık kararları/soruları, tutarsızlığı önlemek için **yalnız** merkezi
> [`todo.md`](../todo.md) dosyasında toplanır (önceliklendirilmiş tüm-doküman listesi). İlgili maddeler orada `(sampleProcess §..)`
> atfıyla bulunur; verilen kararlar bu dokümanın **gövdesinde** anlatılır.

> **Çözülenler (yerel karar log'u):**
- ✅ **integration** ikinci webhook'u **modellendi:** `transferFail` (`webhook`) → başlatıcıya (`integrationStart`) geri dönüş;
  `transferOk` → `processEnd`. Aynı bekleme noktasında **webhook koduna göre dallanma** (→ `integration/process.md`).

---

*Oluşturma: 2026-06-30 · Klasörlerdeki `process.md` notları + görseller temel alınarak derlendi.*
