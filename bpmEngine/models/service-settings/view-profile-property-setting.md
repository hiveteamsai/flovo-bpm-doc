# Model — ProcessViewProfilePropertySetting (profil-bazlı alan override'ı)

> **Durum:** 🟡 TASLAK (ilk çıkarım — gözden geçirilecek)
> **Amaç:** Bir alanın **tipe-özel** görünüm/davranış ayarını **görüntüleme profili bazında** tutar. `Property`'deki
> varsayılanı **profil düzeyinde ezer** (override). `viewProfilePropertyId` altındaki `key`/`value` kayıtları bir
> **dictionary** oluşturur; `Property`'nin **`propertyType`**'sine göre geçerli key'ler yorumlanır.
> **Key kataloğu:** → `view-profile-property.md` (propertyType'a göre key'ler).

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Kayıt ID'si. |
| `viewProfilePropertyId` | int | FK → ProcessViewProfileProperty.id | Hangi profil-alan yapılandırmasına ait. |
| `key` | string | — | Ayar anahtarı (propertyType'a göre; → `view-profile-property.md` kataloğu). |
| `value` | string | — | Ayar değeri. **Liste tipi** key'lerde bir **id listesi** tutar (JSON dizi ya da CSV). |

## Benzersizlik
- **`(viewProfilePropertyId, key)` benzersiz** — bir profil-alan için bir key tek kez.

## İlişkiler
- **N – 1** → `ProcessViewProfileProperty` (`viewProfilePropertyId`).
- **Soft referans (value içindeki id'ler, FK değil):**
  - `activeStartActions` → `ProcessStepAction` id'leri (childService Süreç Başlangıcı aksiyonları).
  - `addFromExistingStatusIds` → `Status` id'leri.

## Çalışma (runtime)
Bir `viewProfileProperty` için tüm setting kayıtları yüklenir → **dictionary (`key` → `value`)**; `Property`'nin
`propertyType`'ına göre yorumlanır. Belirtilmeyen key → `Property` varsayılanı (merge).

*Oluşturma: 2026-07-02.*
