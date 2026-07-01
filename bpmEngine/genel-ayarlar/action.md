# Flovo — Aksiyon Şablonu (ActionDto) Tasarımı

> **Durum:** 🟢 DETAYLANIYOR
> **Amaç:** Yeniden kullanılabilir **aksiyon şablonunu (`ActionDto`)** tanımlamak. ActionDto, bir aksiyonun **tanım
> bilgisini** (kod, etiket, ikon, stil, tür...) tutar; bir süreç adımına aksiyon eklenirken bu şablondan **kopyalanır**.
>
> **İlişki:** Adıma bağlanması · veri aktarımı · `actionType` kataloğu → `../servis-ayarlari/process-step-action.md` · Renk/görünüm →
> `style.md` · Durum değişimi (binding) → `status.md` · Adım tipleri → `../servis-ayarlari/process-step.md`.

---

## 0. ActionDto Nedir? (şablon mantığı)
**ActionDto**, servis-bazlı tanımlanan **yeniden kullanılabilir bir aksiyon şablonudur.** Bir süreç adımına yeni
aksiyon eklenirken, tanımlı **ActionDto'lar arasından seçim** yapılır ve şablonun bilgileri (`code`, `definition`,
`icon`, `style`, `actionType`...) **adımın aksiyonuna kopyalanır.** Adıma-özel bağlama bilgileri (hedef adım, durum,
yetki...) ise **binding**'de tutulur → `../servis-ayarlari/process-step-action.md` §1.2.

> **İki katman:** **(a) ActionDto = şablon (bu doküman)** · **(b) ProcessStepAction = adıma bağlı kopya + adım-özel
> alanlar** (`../servis-ayarlari/process-step-action.md` §1.2). Aynı ActionDto **birden çok adımda** tekrar kullanılabilir.

---

## 1. ActionDto Veri Modeli (alanlar)
| Alan | Tip | Açıklama |
|---|---|---|
| `code` | string | Aksiyon kodu — benzersiz **ve yönlendirme tanımlayıcısı** (`default`, `onFail`, `true`/`false`, switch değeri...) |
| `definition` | string | Aksiyon adı/etiketi |
| `icon` | string | İkon |
| `style` | ref → Style | Renk/görünüm (bg + font) — **Style** varlığına referans (→ `style.md`) |
| `actionType` | enum | Aksiyonun **türü** (Manuel / withForm / Fotoğraf Çek / Dosya Seç / Barcode Tara / Webhook / Autoaction); tür kataloğu → `../servis-ayarlari/process-step-action.md` §3 |
| `defaultAction` | bool | Varsayılan aksiyon mu _(↔ `default` kodu — `../servis-ayarlari/process-step-action.md` §7)_ |
| `validation` | bool | Form validasyonu gerekli mi |
| `stayOnPage` | bool | Aksiyon sonrası sayfada kal |
| `showHistory` | bool | Süreç geçmişini göster |
| `actionDisplayType` | enum | Görünürlük: `invisible` / `everywhere` / `onlyFormDetail` / `onlyFastApprove` |

> **[Karar]** `actionType` ve `style` **ActionDto şablonunda** yaşar; adıma eklenince **kopyalanır**. Adım-binding
> bunları **tekrar tutmaz** (→ `../servis-ayarlari/process-step-action.md` §1.2).

---

## 2. Adıma Ekleme: kopyalama mantığı
1. Süreç adımında **"aksiyon ekle"** denir.
2. Tanımlı **ActionDto'lar listelenir**; biri **seçilir**.
3. Seçilen ActionDto'nun **`code` / `definition` / `icon` / `style` / `actionType` ...** alanları adımın aksiyonuna
   **kopyalanır**.
4. Adıma-özel **binding** alanları girilir: **hedef adım (`targetProcessStepId`)**, durum (`changeStatusId`),
   yetki (`authorizationLevel`)... → `../servis-ayarlari/process-step-action.md` §1.2.
   _(`targetProcessStepId` = aksiyon çalışınca **hangi süreç adımına** ilerleyeceği.)_

```
ActionDto (şablon)            Süreç Adımı'na ekleme
┌───────────────────┐         ┌──────────────────────────────────┐
│ code, definition, │  seç →  │ (kopya) code/definition/icon/     │
│ icon, style,      │ ──────▶ │ style/actionType                  │
│ actionType, ...   │         │ + binding: targetProcessStepId,   │
└───────────────────┘         │            changeStatusId,        │
                              │            authorizationLevel      │
                              └──────────────────────────────────┘
```

---

## 3. Açık Kararlar / Sorular
- [ ] **Kopya ↔ canlı referans:** ActionDto sonradan değişince adımlardaki kopyalar güncellensin mi (canlı referans),
      yoksa kopya **bağımsız** mı kalsın?
- [ ] **`defaultAction` bool ↔ `default` kodu** — ikisi de "varsayılan"ı işaret ediyor; nasıl birleşir? (→ `../servis-ayarlari/process-step-action.md` §7)
- [ ] **`actionDisplayType`** gözden geçirilecek (`invisible`/`everywhere`/`onlyFormDetail`/`onlyFastApprove`).
- [ ] ActionDto'lar servis-bazlı mı, çözüm/hesap-bazlı **paylaşımlı** mı tanımlanır?

---

## 4. Notlar / Ham Düşünceler
> _(Buraya ham düşünceler; sonra yukarı işlenir.)_

---

*Oluşturma: 2026-06-30.*
