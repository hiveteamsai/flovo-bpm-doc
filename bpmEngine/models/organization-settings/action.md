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
| `code` | string | benzersiz | Aksiyon kodu **ve yönlendirme tanımlayıcısı** (`default`, `onFail`, `true`/`false`, switch değeri...). Adım bu koda göre aksiyon seçer. **Çeviri için kullanılmaz** → `translationCode`. |
| `definition` | string | — | Aksiyon adı/etiketi — **varsayılan dildeki** metin (çeviri: `translationCode` → Translation). |
| `translationCode` | string? | çeviri anahtarı | **Çeviri eşleşme anahtarı** (→ [`translation.md`](./translation.md) `code`). `null` = çeviri **es geçilir**, doğrudan `definition` kullanılır. |
| `icon` | string | — | İkon. |
| `styleId` | int | FK → Style.id | Renk/görünüm (bg + font). |
| `actionType` | ActionType | — | Aksiyonun **türü** (aşağıda) — [`../enums/action-type.md`](../enums/action-type.md). |
| `defaultAction` | bool | — | Varsayılan aksiyon mu (↔ `default` kodu; birleşim açık → `../../todo.md`). |
| `validation` | bool | — | Form validasyonu gerekli mi. |
| `stayOnPage` | bool | — | Aksiyon sonrası sayfada kal. |
| `showHistory` | bool | — | Süreç geçmişini göster. |
| `actionDisplayType` | ActionDisplayType | — | Görünürlük — [`../enums/action-display-type.md`](../enums/action-display-type.md): `invisible` / `everywhere` / `onlyFormDetail` / `onlyFastApprove`. |

### `actionType` değerleri (bu modeldeki rol)
Enum tanımı → [`../enums/action-type.md`](../enums/action-type.md). Bu modelde aksiyonun tetiklenme davranışını belirler:
- `manual` (Manuel) — kullanıcının elle bastığı standart aksiyon.
- `eventForm` — aksiyon anında `formType=eventForm` servisin profili pop-up açılır; sonuç `parameters` ile döner.
- `takePhoto` (Fotoğraf Çek) / `selectFile` (Dosya Seç) / `scanBarcode` (Barcode Tara) — aksiyon cihaz eylemini (kamera/dosya/tarayıcı) tetikler.
- `webhook` (Webhook) — aksiyon dış uç noktaya HTTP çağrısı yapar.
- `autoAction` (Autoaction) — koşul sağlanınca kullanıcı etkileşimi olmadan otomatik çalışır.

_(davranış kataloğu → `../../service-settings/process-step-action.md` §3.)_

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
