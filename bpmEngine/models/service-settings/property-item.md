# Model — PropertyItem (seçim öğesi)

> **Durum:** 🟡 TASLAK (ilk çıkarım — gözden geçirilecek)
> **Amaç:** Seçim alanlarının (Combobox, Radiobutton List) **statik seçeneği**. Bir `Property`'nin `propertyItems`
> listesindeki tek eleman.
> **Davranış/kullanım:** → `../../service-settings/properties.md` §2.6

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Öğe ID'si. |
| `propertyId` | int | FK → Property.id | Bağlı olduğu alan. |
| `value` | string | — | **Seçilen değer** (alanın value'suna yazılır). `(propertyId, value)` **benzersiz**. |
| `code` | string | — | **Çeviri eşleşme kodu** (→ Translation `code`); öğe metni buradan çözülür. |
| `definition` | string | — | Öğe tanımı (yönetim ekranında görünen ad). |

## Benzersizlik
- **`(propertyId, value)` benzersiz** — bir alanda aynı `value`'lu iki öğe olamaz.

## Neden `code` ≠ `value`?
Farklı comboboxlar aynı `value` kümesini (`0`·`1`·`2`·`3`) kullanabilir. Çeviriler karışmasın diye **çeviri eşleşmesi
`code` üzerinden** yapılır; `value` yalnız seçilen değeri taşır.

## İlişkiler
- **N – 1** → `Property` (`propertyId`).
- **Kod eşleşmesi (FK değil):** `code` → `Translation` (aktif dile göre metin).

*Oluşturma: 2026-07-02.*
