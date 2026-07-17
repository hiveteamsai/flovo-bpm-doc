# Model — PropertyItem (seçim öğesi)

> **Durum:** 🟡 TASLAK (ilk çıkarım — gözden geçirilecek)
> **Amaç:** Seçim alanlarının (`combobox`, `radiobuttonList`) **statik seçeneği**. Bir `Property`'nin `propertyItems`
> listesindeki tek eleman.
> **Davranış/kullanım:** → `../../service-settings/properties.md` §2.6

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Öğe ID'si. |
| `propertyId` | int | FK → Property.id | Bağlı olduğu alan. |
| `value` | string | — | **Seçilen değer** (alanın value'suna yazılır). `(propertyId, value)` **benzersiz**. |
| `translationCode` | string? | çeviri anahtarı | **Çeviri eşleşme anahtarı** (→ [`../organization-settings/translation.md`](../organization-settings/translation.md) `code`); öğe metni buradan çözülür. `null` = çeviri **es geçilir**, doğrudan `definition` kullanılır. |
| `definition` | string | — | Öğe tanımı — **varsayılan dildeki** metin (yönetim ekranında görünen ad). |

## Benzersizlik
- **`(propertyId, value)` benzersiz** — bir alanda aynı `value`'lu iki öğe olamaz.

## Neden `translationCode` ≠ `value`?
Farklı comboboxlar aynı `value` kümesini (`0`·`1`·`2`·`3`) kullanabilir. Çeviriler karışmasın diye **çeviri eşleşmesi
`translationCode` üzerinden** yapılır; `value` yalnız seçilen değeri taşır. _(Aynı ilke tüm modellerde standarttır —
iş kodu ile çeviri anahtarı ayrıdır; → [`../organization-settings/translation.md`](../organization-settings/translation.md).)_

## İlişkiler
- **N – 1** → `Property` (`propertyId`).
- **Kod eşleşmesi (FK değil):** `translationCode` → `Translation.code` (aktif dile göre metin).

*Oluşturma: 2026-07-02.*
