# Model — Translation

> **Durum:** 🟡 TASLAK (ilk çıkarım — gözden geçirilecek)
> **Amaç:** Bir **`code`**'a bağlı metnin dillere göre karşılıklarını tutar. Hem **ortak (Flovo)** hem
> **organizasyon** çevirileri tek modelde.
> **Davranış/kullanım (çözümleme motoru):** → `../../organization-settings/translation.md`

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Çeviri kaydı ID'si. |
| `code` | string | eşleştirme anahtarı | Çeviri **kodu** (serbest metin; istenirse `form.submit` / `department.01` gibi namespace). Kaynak modellerin **`translationCode`**'u buraya eşleşir. |
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
- **Kod eşleşmesi (FK değil):** Çevrilebilir modeller buraya **kendi `code`'larıyla değil**, ayrı **`translationCode`**
  alanıyla bağlanır: **`Model.translationCode` → `Translation.code`** (+ `organizationId` + `languageCode`).
  `translationCode` **`null`** ise çeviri **es geçilir**, kaynağın `definition`'ı doğrudan kullanılır.
  Alanı taşıyan modellerin **tam listesi** ve gerekçe → `../../organization-settings/translation.md` **§3.1**.

## Neden ayrı `translationCode`?
Bu tablonun ad-uzayı **organizasyon geneli**dir (`(organizationId, code, languageCode)`) ve **varlık ayrımı içermez**;
modellerin `code`'u ise yalnız **model-içi** benzersizdir. İş kodu doğrudan anahtar yapılsaydı Departman `"01"` ile
Şirket `"01"` **aynı** çeviri satırına düşerdi. Ayrı alan bu çakışmayı keser; ayrıca iki kayıt **aynı** `translationCode`
vererek çeviriyi **bilinçli paylaşabilir**.

## Notlar / açık noktalar
- Ortak (`null`) kayıt güncellenince, onu **ezmiş** organizasyon kayıtları etkilenmemeli (teyit) → `../../todo.md`.
- **`translationCode` ad-uzayı kuralı (KARAR, v0.18):** anahtar **otomatik üretilmez** (`<varlık>.<code>` gibi bir şema yok);
  alan **opsiyoneldir**. Girilmezse çeviri Translation tablosundan **çekilmez**, doğrudan `definition` kullanılır. Serbest
  metin; namespace kullanımı kullanıcının tercihidir (zorunlu değil).

*Oluşturma: 2026-07-02.*
