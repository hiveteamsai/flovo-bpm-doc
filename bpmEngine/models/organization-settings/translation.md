# Model — Translation

> **Durum:** 🟡 TASLAK (ilk çıkarım — gözden geçirilecek)
> **Amaç:** Bir **`code`**'a bağlı metnin dillere göre karşılıklarını tutar. Hem **ortak (Flovo)** hem
> **organizasyon** çevirileri tek modelde.
> **Davranış/kullanım (çözümleme motoru):** → `../../organization-settings/translation.md`

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Çeviri kaydı ID'si. |
| `code` | string | eşleştirme anahtarı | Çeviri **kodu** (serbest metin; istenirse `form.submit` gibi namespace). Metinler bu `code` ile çözülür. |
| `organizationId` | int? | FK → Organization.id | Sahibi organizasyon. **`null` = ortak (Flovo) çeviri** (herkes kullanır, salt-okunur). |
| `languageCode` | string | — | **Dil kodu** — sabit set (`tr`/`en`/`de`; krş. `organization.defaultLang`). |
| `definition` | string | — | Bu **dildeki metin** (`languageCode` dilinde). |

> **Kayıt-başına-dil:** Bir `code`'un her dili **ayrı satırdır**. Aktif dile (`languageCode = userLang`) uyan kaydın
> `definition`'ı döndürülür. Yeni dil = yeni **kayıt** (şema değişmez).

## Benzersizlik
- **`(organizationId, code, languageCode)` benzersiz** — bir organizasyonda bir `code`'un bir dili tek kayıt.
- `organizationId = null` + `code` + `languageCode` de benzersiz (ortak tarafta tek kayıt).

## İlişkiler
- **N – 1** → `Organization` (`organizationId`).
- **Kod eşleşmesi (FK değil):** `Property.code`/`definition`, `PropertyItem.code`, `Status.definition`, `Action.definition`
  gibi metinler `code` + `organizationId` ile buradan çözülür.

## Notlar / açık noktalar
- Ortak (`null`) kayıt güncellenince, onu **ezmiş** organizasyon kayıtları etkilenmemeli (teyit) → `../../todo.md`.

*Oluşturma: 2026-07-02.*
