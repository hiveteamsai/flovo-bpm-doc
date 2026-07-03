# Model — Action (ActionDto — şablon)

> **Durum:** 🟡 TASLAK (ilk çıkarım — gözden geçirilecek)
> **Amaç:** Yeniden kullanılabilir **aksiyon şablonu**. Bir süreç adımına aksiyon eklenirken bu şablondan seçilir ve
> alanları binding'e (`ProcessStepAction`) **kopyalanır**.
> **Davranış/kullanım:** → `../../organization-settings/action.md` · binding → `../../service-settings/process-step-action.md`

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Şablon ID'si. |
| `organizationId` | int | FK → Organization.id | Sahibi organizasyon. **Organizasyon havuzu**: o organizasyonun **tüm servislerinde** kullanılabilir. |
| `code` | string | benzersiz | Aksiyon kodu **ve yönlendirme tanımlayıcısı** (`default`, `onFail`, `true`/`false`, switch değeri...). Adım bu koda göre aksiyon seçer. |
| `definition` | string | — | Aksiyon adı/etiketi (çeviri: `code` → Translation). |
| `icon` | string | — | İkon. |
| `styleId` | int | FK → Style.id | Renk/görünüm (bg + font). |
| `actionType` | enum | — | Aksiyonun **türü** (aşağıda). |
| `defaultAction` | bool | — | Varsayılan aksiyon mu (↔ `default` kodu; birleşim açık → `../../todo.md`). |
| `validation` | bool | — | Form validasyonu gerekli mi. |
| `stayOnPage` | bool | — | Aksiyon sonrası sayfada kal. |
| `showHistory` | bool | — | Süreç geçmişini göster. |
| `actionDisplayType` | enum | — | Görünürlük: `invisible` / `everywhere` / `onlyFormDetail` / `onlyFastApprove`. |

### `actionType` değerleri
`Manuel` · `withForm` · `Fotoğraf Çek` · `Dosya Seç` · `Barcode Tara` · `Webhook` · `Autoaction`
_(katalog → `../../service-settings/process-step-action.md` §3.)_

## Benzersizlik
> `(organizationId, code)` **benzersiz** — aynı organizasyonda aynı `code`'lu iki aksiyon şablonu olamaz.

## İlişkiler
- **N – 1** → `Organization` (`organizationId`), `Style` (`styleId`).
- **Kopya kaynağı (FK değil):** Adıma aksiyon eklenirken Action alanları `ProcessStepAction`'a **bir kez kopyalanır**;
  **canlı bağ/FK tutulmaz** — Action sonradan değişince mevcut adım-aksiyonları **etkilenmez** (iki taraf bağımsız).

## Notlar / açık noktalar
- **Karar:** Action → ProcessStepAction **bağımsız kopyadır** (snapshot); canlı referans yok.
- `defaultAction` (bool) ↔ `default` (kod) birleşimi → `../../todo.md`.

*Oluşturma: 2026-07-02.*
