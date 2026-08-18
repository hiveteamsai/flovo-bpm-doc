# Flovo — Style (Renk / Görünüm) Tasarımı

> **Durum:** 🟢 DETAYLANIYOR
> **Amaç:** Flovo'da **renk/görünüm (style)** varlığını tanımlamak. Style **çapraz-kesen** bir kavramdır: renk seçimi
> yapılan yerlerde (aksiyonlar, durumlar...) kullanılır.
>
> **İlişki:** `action.md` (aksiyonun `styleId`) · `status.md` (durum stili). _(Not: **form alanlarına bu Style
> varlığı uygulanmaz**; iş kuralındaki `setStyle` yalnız tekil görünüm niteliklerini —fontSize/titleColor gibi—
> değiştirir, Style varlığı seçmez → `../service-settings/business-rule.md`.)_

---

## 0. Style Nedir?
Bir **style**, bir öğenin **renk/görünümünü** tanımlayan yeniden-kullanılabilir bir varlıktır. En temel hâliyle bir
**arka plan rengi (bg color)** + **yazı rengi (font color)** çiftidir. Renk seçimi yapılan yerlerde (aksiyon butonu,
durum etiketi...) bir style **seçilerek** uygulanır. Genel kural: `bgColor` = arka plan; **`fontColor` = metin ve ikon
rengi** (örn. durum etiketinde `definition` + `icon`). _(Form alanları bu Style varlığını kullanmaz.)_

---

## 1. Dinamik Style Yönetimi
Renkler **dinamik** yönetilir; bunun için **ayrı bir Style yönetim sayfası** vardır.

### 1.1 — Sistem stilleri (`organizationId = null`)
- Hazır stiller sistemde tanımlı gelir (`organizationId = null`). **Tüm organizasyonlar görüntüleyip kullanabilir** ama
  **güncelleyemez** (read-only). Yalnız Flovo yönetir.

### 1.2 — Organizasyon stilleri (`organizationId = <org>`)
- Bir organizasyon, Style sayfasından **kendi stilini oluşturabilir**: bir **bg color** + bir **font color** seçer.
- Organizasyon **yalnız kendi** stillerini günceller; oluşturulan stiller sistem stilleriyle birlikte seçim listelerinde görünür.

> **Sahiplik & görünürlük:** Bir organizasyon **kendi stillerini** (`organizationId = <org>`) + **sistem stillerini**
> (`organizationId = null`) görür/kullanır. **Sistem stilleri (null) organizasyonlar tarafından güncellenemez.** Bir
> organizasyon başka organizasyonun stillerini göremez. _(Aynı model → `translation.md` §2 · `organization.md`.)_

### 1.3 — Kullanım
- Stiller, uygulamada **renk seçimi yapılan yerlerde** seçilebilir (aksiyon, durum...).
- Seçim, ilgili varlıkta **style referansı** (id/code) olarak tutulur.

---

## 2. Style Varlığı (veri modeli — taslak)
| Alan | Tip | Açıklama |
|---|---|---|
| `id` / `code` | int / string | Stil kimliği (referans için) |
| `name` | string | Stil adı (kullanıcıya görünen) |
| `bgColor` | string (hex/renk) | Arka plan rengi |
| `fontColor` | string (hex/renk) | Yazı rengi |
| `organizationId` | int / null | Sahibi organizasyon (FK → `organization.md` `id`). **`null` = sistem stili** (tüm organizasyonlarca kullanılır, salt-okunur). |

> **Kapsam (KARAR, v0.18):** yalnız **bg + font** yeterli; ek görünüm alanları (`fontSize`/`isBold`/`border`/`iconColor`) **eklenmez**.

---

## 3. Style Yönetim Sayfası (UI — taslak)
- **Liste:** sistem stilleri (kilit) + kullanıcı stilleri (düzenle/sil).
- **Oluştur/Düzenle:** ad + bg color seçici + font color seçici + **canlı önizleme** (örnek buton/etiket).
- **Seçici bileşen:** renk seçimi olan her ekranda kullanılan ortak "Style seç" dropdown'ı (önizlemeli).

---

## 4. Açık Kararlar / Sorular
> **Açık sorular tek yerde:** Bu dokümanın açık kararları/soruları, tutarsızlığı önlemek için **yalnız** merkezi
> [`todo.md`](../todo.md) dosyasında toplanır (önceliklendirilmiş tüm-doküman listesi). İlgili maddeler orada `(style §..)`
> atfıyla bulunur; verilen kararlar bu dokümanın **gövdesinde** anlatılır.

> **Çözülenler (yerel karar log'u):**
- [x] **Style tüketicisi = Action + Status**; form alanları Style **kullanmaz**, adımlar Style **tüketmez** (→ `../models/index.md` §5).
- [x] Style **kapsamı:** **organizasyon-bazlı** (`organizationId`) + **sistem** (`organizationId=null`, salt-okunur). Servis-bazlı ayrım yok.
- [x] **Alan kapsamı (v0.18):** yalnız **bg + font**; `fontSize`/`isBold`/`border`/`iconColor` gibi ek alanlar **eklenmez**.

---

## 5. Notlar / Ham Düşünceler
> _(Buraya ham düşünceler; sonra yukarı işlenir.)_

---

*Oluşturma: 2026-06-26.*
