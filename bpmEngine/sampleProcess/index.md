# Örnek Süreçler (sampleProcess) — İndeks

> **Amaç:** Flovo BPM motoru üzerinde **self-servis** olarak nasıl süreç kurgulandığını **uçtan uca örneklerle**
> göstermek. Her örnek kendi alt klasöründedir: **`<ad>.jpg`** (görsel) + **`process.md`** (**detaylı spec:** amaç →
> diyagram → adım adım görev/ayar/aksiyon + **parametre akışı**) + **`index.md`**. Bu örnekleri **bpm-engine'i
> iyileştirmek** için kullanırız.
>
> **Tasarım dokümanları:** adımlar → `../service-settings/process-step.md` · aksiyonlar → `../service-settings/process-step-action.md` / `../organization-settings/action.md` ·
> alanlar → `../service-settings/properties.md` · motor → `../flovo-bpm-engine.md`.

---

## Alt klasörler (örnek süreçler)
| Klasör | İçerik (özet) | İndeks |
|---|---|---|
| **expense/** | **Masraf oluşturma** — 3 başlatma yöntemi (fotoğraf/dosya/belgesiz) · **Flovo AI (Masraf)** tarama · Processing loading kartı · hata telafisi (Instance Deleter). | [`expense/index.md`](./expense/index.md) |
| **createPdf/** | **PDF (senkron)** — dış sunucuda PDF üretip **HTTP Request `async=false`** ile bekleyerek dönme; sonuç bildirimi. | [`createPdf/index.md`](./createPdf/index.md) |
| **createPdfAsync/** | **PDF (asenkron)** — **HTTP Request `async=true`** ile beklemeden ilerleme; PDF hazır olunca **Webhook** ile bağımsız alt süreçten bildirim. | [`createPdfAsync/index.md`](./createPdfAsync/index.md) |
| **integration/** | **Asenkron entegrasyon** — uzun aktarımı **Processing (`showLoading=false`)** ile durum güncelleyerek bekleme; **Webhook** sonucuna göre bitiş/başa dönüş. | [`integration/index.md`](./integration/index.md) |
| **scanBarcode/** | **Barkod ile var olanı aç** — yanıttaki **`response.action`** koduna göre **koşullu dallanma**; Form Yönlendirme veya Instance Creator. | [`scanBarcode/index.md`](./scanBarcode/index.md) |
| **referred/** | **Yönlendirmeli onay** — kontrol grubu → yönlendirilen kullanıcı + yönetici zinciri → TransferUser Kontrol (Karşılaştırma) döngüsü → muhasebe. **Odak:** **`mergeParameter`** ile parametrelerin zincir boyunca **birikerek** taşınması. | [`referred/index.md`](./referred/index.md) |
| **expenseAndCreditCard/** 🟡 | **Masraf & Kredi Kartı Ekstresi** — **4 bağlantılı servis** (Masraf Formu · Masraf · Ekstre · Ekstre Satırı). **Odak:** **ServiceTrigger** (servis-seviyesi otomatik tetikleyici) + **triggerProcessStep** + **Üst Form Kullanıcı (ParentUser)** birlikte. **Her servis ayrı `.md`** (tek `process.md` değil). **TASLAK.** | [`expenseAndCreditCard/index.md`](./expenseAndCreditCard/index.md) |

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
8. ✅ **`mergeParameter` (parametre birikimi)** (referred) — `../service-settings/process-step-action.md` **§2.1**'e +
   model alanına işlendi: `mergeParameter = true` olan aksiyon, hedefe **gelen (`in`) + ürettiği (`out`)** parametreleri
   birlikte taşır (**`out` çakışmada ezer**); yönlendirme/döngü kollarında bağlamı korur. Motor döngüsü `../flovo-bpm-engine.md` §4.4.

## Açık Noktalar

> **Açık sorular tek yerde:** Bu dokümanın açık kararları/soruları, tutarsızlığı önlemek için **yalnız** merkezi
> [`todo.md`](../todo.md) dosyasında toplanır (önceliklendirilmiş tüm-doküman listesi). İlgili maddeler orada `(sampleProcess §..)`
> atfıyla bulunur; verilen kararlar ilgili örneğin **`process.md`** gövdesinde anlatılır.

> **Çözülenler (yerel karar log'u):**
- ✅ **integration** ikinci webhook'u **modellendi:** `transferFail` (`webhook`) → başlatıcıya (`integrationStart`) geri dönüş;
  `transferOk` → `processEnd`. Aynı bekleme noktasında **webhook koduna göre dallanma** (→ `integration/index.md`).

---

*Oluşturma: 2026-06-30 · Güncelleme: alt klasör bazlı hiyerarşik indeks (her örnek kendi `index.md`'sine).*
