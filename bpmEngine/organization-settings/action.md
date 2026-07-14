# Flovo — Aksiyon Şablonu (ActionDto) Tasarımı

> **Durum:** 🟢 DETAYLANIYOR
> **Amaç:** Yeniden kullanılabilir **aksiyon şablonunu (`ActionDto`)** tanımlamak. ActionDto, bir aksiyonun **tanım
> bilgisini** (kod, etiket, ikon, stil, tür...) tutar; bir süreç adımına aksiyon eklenirken bu şablondan **kopyalanır**.
>
> **İlişki:** Adıma bağlanması · veri aktarımı · `actionType` kataloğu → `../service-settings/process-step-action.md` · Renk/görünüm →
> `style.md` · Durum değişimi (binding) → `status.md` · Adım tipleri → `../service-settings/process-step.md`.

---

## 0. ActionDto Nedir? (şablon mantığı)
**ActionDto**, **organizasyon-bazlı** (havuz) tanımlanan **yeniden kullanılabilir bir aksiyon şablonudur** — o organizasyonun tüm servislerinde kullanılabilir. Bir süreç adımına yeni
aksiyon eklenirken, tanımlı **ActionDto'lar arasından seçim** yapılır ve şablonun bilgileri (`code`, `definition`,
`icon`, `styleId`, `actionType`...) **adımın aksiyonuna kopyalanır.** Adıma-özel bağlama bilgileri (hedef adım, durum,
yetki...) ise **binding**'de tutulur → `../service-settings/process-step-action.md` §1.2.

> **İki katman:** **(a) ActionDto = şablon (bu doküman)** · **(b) ProcessStepAction = adıma bağlı kopya + adım-özel
> alanlar** (`../service-settings/process-step-action.md` §1.2). Aynı ActionDto **birden çok adımda** tekrar kullanılabilir.

---

## 1. ActionDto Veri Modeli (alanlar)
| Alan | Tip | Açıklama |
|---|---|---|
| `id` | int | Şablon ID'si (primary key) |
| `organizationId` | int | Sahibi organizasyon (FK → `organization.md` `id`); **organizasyon havuzu** — tüm servislerde kullanılır |
| `code` | string | Aksiyon kodu — benzersiz **ve yönlendirme tanımlayıcısı** (`default`, `onFail`, `true`/`false`, switch değeri...) |
| `definition` | string | Aksiyon adı/etiketi |
| `icon` | string | İkon |
| `styleId` | int | Renk/görünüm (bg + font) — **Style** varlığına FK referans (→ `style.md`) |
| `actionType` | ActionType | Aksiyonun **türü** (`manual` / `eventForm` / `takePhoto` / `selectFile` / `scanBarcode` / `webhook` / `autoAction`); tür kataloğu → `../service-settings/process-step-action.md` §3 |
| `defaultAction` | bool | Varsayılan aksiyon mu _(↔ `default` kodu — `../service-settings/process-step-action.md` §7)_ |
| `validation` | bool | Form validasyonu gerekli mi |
| `stayOnPage` | bool | Aksiyon sonrası sayfada kal |
| `showHistory` | bool | Süreç geçmişini göster |
| `actionDisplayType` | ActionDisplayType | Görünürlük: `invisible` / `everywhere` / `onlyFormDetail` / `onlyFastApprove` |

> **[Karar]** `actionType` ve `styleId` **ActionDto şablonunda** yaşar; adıma eklenince **kopyalanır**. Adım-binding
> bunları **tekrar tutmaz** (→ `../service-settings/process-step-action.md` §1.2).

---

## 2. Adıma Ekleme: kopyalama mantığı
1. Süreç adımında **"aksiyon ekle"** denir.
2. Tanımlı **ActionDto'lar listelenir**; biri **seçilir**.
3. Seçilen ActionDto'nun **`code` / `definition` / `icon` / `styleId` / `actionType` ...** alanları adımın aksiyonuna
   **kopyalanır**.
4. Adıma-özel **binding** alanları girilir: **hedef adım (`targetProcessStepId`)**, durum (`changeStatusId`),
   yetki (`authorizationLevel`)... → `../service-settings/process-step-action.md` §1.2.
   _(`targetProcessStepId` = aksiyon çalışınca **hangi süreç adımına** ilerleyeceği.)_

```
ActionDto (şablon)            Süreç Adımı'na ekleme
┌───────────────────┐         ┌──────────────────────────────────┐
│ code, definition, │  seç →  │ (kopya) code/definition/icon/     │
│ icon, styleId,    │ ──────▶ │ styleId/actionType                │
│ actionType, ...   │         │ + binding: targetProcessStepId,   │
└───────────────────┘         │            changeStatusId,        │
                              │            authorizationLevel      │
                              └──────────────────────────────────┘
```

---

## 3. Açık Kararlar / Sorular
> **Açık sorular tek yerde:** Bu dokümanın açık kararları/soruları, tutarsızlığı önlemek için **yalnız** merkezi
> [`todo.md`](../todo.md) dosyasında toplanır (önceliklendirilmiş tüm-doküman listesi). İlgili maddeler orada `(action §..)`
> atfıyla bulunur; verilen kararlar bu dokümanın **gövdesinde** anlatılır.

> **Çözülenler (yerel karar log'u):**
- [x] **Kopya ↔ canlı referans:** **Karar** — ActionDto adıma eklenince alanları **bir kez kopyalanır**; kopya
      **bağımsızdır** — ActionDto sonradan değişince mevcut adım-aksiyonları **güncellenmez** (canlı referans/FK yok).
- [x] ActionDto'lar **organizasyon-bazlı** (havuz) tanımlanır; organizasyonun tüm servislerinde kullanılır.

---

## 4. Notlar / Ham Düşünceler
> _(Buraya ham düşünceler; sonra yukarı işlenir.)_

---

*Oluşturma: 2026-06-30.*
