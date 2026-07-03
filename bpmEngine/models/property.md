# Model — Property (form alanı)

> **Durum:** 🟡 TASLAK (ilk çıkarım — gözden geçirilecek)
> **Amaç:** Metadata-driven formdaki tek bir **giriş/görüntüleme elemanı**. Bir **kontrol tipi** (`controlTypeId`) ile
> render edilir, `code` ile veriye bağlanır.
> **Davranış/kullanım + tam alan kataloğu:** → `../servis-ayarlari/properties.md`
>
> **Tasarım ilkesi:** ince **ortak çekirdek** + **tipe-özel alanlar** (`controlTypeId`'ye göre).

## 1. Çekirdek alanlar (her alanda)

### 1.1 Kimlik & bağlama
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Alan ID'si. |
| `serviceId` | int | FK → Service | Bağlı servis. |
| `code` | string | benzersiz (binding key) | Alanın veriye bağlandığı anahtar; çeviri eşleşmesi için de kullanılır. |
| `definition` | string | — | Alan tanımı / kullanıcıya görünen etiket (çeviri: `code` → Translation). |
| `controlTypeId` | int | — | Kontrol tipi (§3 tipe-özel alanları belirler). |

### 1.2 Görünüm & yardım
| Alan | Tip | Açıklama / amaç |
|---|---|---|
| `hint` | string | Placeholder metni. |
| `helperText` | string | Yardımcı (alt) metin. |
| `leadingView` / `trailingView` (+pozisyon) | string | Sol/sağ ikon. |

### 1.3 Davranış & kalıcılık
| Alan | Tip | Açıklama / amaç |
|---|---|---|
| `defaultValue` | (tipe göre) | Varsayılan değer. |
| `format` | string | Format (tarih/sayı/maske). |
| `saveAndRefreshOnAfterChange` | bool | Değer değişince **kaydet isteği atıp formu yeniler** (refresh). |
| `backingField` | — | Gizli/arka-plan alan. |
| `savePropertyToDb` | bool | Veritabanına kaydet. |
| `saveChangeLog` | bool | Değişiklik geçmişi tut. |
| `state` | — | Alan durumu. |
| `environmentRestriction` | string | Ortam kısıtı. |
| `organizationRestriction` | string | Organizasyon kapsam kısıtı. |

> **Not:** `visible` / `enabled` / `required` bu modelde **değil**, `ProcessViewProfileProperty`'de tutulur.

### 1.4 Veri kaynağı alanları (seçim alanları için)
| Alan | Tip | Açıklama / amaç |
|---|---|---|
| `dataSource` / `dataSourceId` / `dataSourceValue` | — | **Dinamik** veri kaynağı. |
| `propertyItems` | List\<PropertyItem\> | **Statik** seçenekler (→ `property-item.md`). |
| `propertyTransferParameters` | — | Kaynağa aktarılan parametreler. |
| `lazyLoading` | bool | Tembel yükleme. |
| `manuelEntry` | bool | Serbest giriş. |
| `isMultiSelect` | bool | Çoklu seçim. |

### 1.5 İlişki alanları (ilişkisel alanlar için)
| Alan | Tip | Açıklama / amaç |
|---|---|---|
| `childServiceId` | int | Alt servis (Form List). |
| `serviceItemControlId` | int | Alt-servis öğe kontrolü. |
| `refPropertyId` | int | Referans alınan alan (Parent Property). |
| `parentPropertyId` | int | Üst alan. |
| `relatedPropertyIds` | List\<int\> | İlişkili alanlar. |

## 2. Tipe-özel alanlar (`controlTypeId`'ye göre — özet)
> Tam açıklama → `../servis-ayarlari/properties.md` §3.

| Kontrol tipi | Alanlar |
|---|---|
| Textbox | `minLine` · `maxLine` · `charMaxLength` · `showCharCount` · `keyboardType` · maske |
| Numeric Textbox | `maxDecimalDigits` · `enableNegative` · `enableGroupSeperator` · `integerActive` |
| Combobox | `propertyItems`/`dataSource*` · `isMultiSelect` · `manuelEntry` · `lazyLoading` · `headerText` |
| Datepicker | `minimumDate` · `maximumDate` · `setAsToday` · `format` · `headerText` |
| Time Picker | `format` · `defaultValue` · `headerText` |
| Checkbox | `defaultValue` (bool) |
| Radiobutton List | `propertyItems`/`dataSource*` · varsayılan seçim |
| File | `allowMultiple` · `isCropActive` · `savePropertyToDb` · `lazyLoading` |
| Text (statik) | `defaultValue` · `fontSize` · `iconSize` · `isBold` · `textAlignment` · `stiky` |
| Barcode | `barcodeFormat` · `scannerActive` (`value` = string) |
| Phone | `format`/maske · `keyboardType` |
| Map Viewer | konum seçimi/görüntüleme; koordinat/adres |
| Form List | `childServiceId` · `serviceItemControlId` · `selectableModeActive` · `reOrder` · `parameterTransfer`/`propertyTransferParameters` · `editOnlyOwnPosition` · `lazyLoading` · **profil-bazlı ayarlar → `view-profile-property.md`:** `activeStartActions`, `addFromExistingStatusIds` |
| Flow Info | `flowInfoValue` (salt-okunur akış metadata) |
| Parent Property | `parentPropertyId` · `refPropertyId` · `relatedPropertyIds` (salt-okunur) |
| User Info | `userInfoValue` (salt-okunur kullanıcı metadata) |
| Group By Tax Receipt | `disableTaxAttachmentView` · `isActiveKkegAttachment` |
| Key-Value List | `addNewEnabled` · `deleteEnabled` · `keyDescription` · `valueDescription` · `comboBoxItems` · `keyValueItems` |
| Image Area Selector | `imageUrl` · `aspectRatio` · `dataSource` (nokta: `code`·`x`·`y`·`isSelected`) |

## İlişkiler
- **N – 1** → `Service` (`serviceId`).
- **1 – N** ← `PropertyItem` (`propertyId`), `ProcessViewProfileProperty` (`propertyId`).

## Notlar / açık noktalar
- Çekirdek ↔ tipe-özel ayrımının nihai listesi; Form List ayarları; `dataSource` çift anlamı → `../todo.md`.

*Oluşturma: 2026-07-02.*
