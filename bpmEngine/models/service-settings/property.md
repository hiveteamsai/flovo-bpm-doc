# Model — Property (form alanı)

> **Durum:** 🟡 TASLAK (ilk çıkarım — gözden geçirilecek)
> **Amaç:** Metadata-driven formdaki tek bir **giriş/görüntüleme elemanı**. Bir **kontrol tipi** (`controlTypeId`) ile
> render edilir, `code` ile veriye bağlanır.
> **Davranış/kullanım + tam alan kataloğu:** → `../../service-settings/properties.md`
>
> **Tasarım ilkesi:** ince **ortak çekirdek** + **tipe-özel alanlar** (`controlTypeId`'ye göre).

## 1. Çekirdek alanlar (her alanda)

### 1.1 Kimlik & bağlama
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Alan ID'si. |
| `serviceId` | int | FK → Service | Bağlı servis. |
| `code` | string | benzersiz (binding key) | Alanın veriye bağlandığı anahtar — yalnız **bağlama**; çeviri için kullanılmaz → `translationCode`. |
| `definition` | string | — | Alan tanımı / kullanıcıya görünen etiket — **varsayılan dildeki** metin (çeviri: `translationCode` → Translation). |
| `translationCode` | string? | çeviri anahtarı | **Çeviri eşleşme anahtarı** (→ [`../organization-settings/translation.md`](../organization-settings/translation.md) `code`). `null` = çeviri **es geçilir**, doğrudan `definition` kullanılır. |
| `controlTypeId` | ControlType | — | Kontrol tipi (§2 tipe-özel alanları belirler) — [`../enums/control-type.md`](../enums/control-type.md). |

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
> Tam açıklama → `../../service-settings/properties.md` §3.
> **Enum'lar:** kontrol tipi → [`../enums/control-type.md`](../enums/control-type.md) · `keyboardType` (Textbox/Phone) → [`../enums/keyboard-type.md`](../enums/keyboard-type.md) · `barcodeFormat` (Barcode) → [`../enums/barcode-format.md`](../enums/barcode-format.md).

| Kontrol tipi | Alanlar |
|---|---|
| `textbox` | `minLine` · `maxLine` · `charMaxLength` · `showCharCount` · `keyboardType` · maske |
| `numericTextbox` | `maxDecimalDigits` · `enableNegative` · `enableGroupSeperator` · `integerActive` |
| `combobox` | `propertyItems`/`dataSource*` · `isMultiSelect` · `manuelEntry` · `lazyLoading` · `headerText` |
| `datepicker` | `minimumDate` · `maximumDate` · `setAsToday` · `format` · `headerText` |
| `timePicker` | `format` · `defaultValue` · `headerText` |
| `checkbox` | `defaultValue` (bool) |
| `radiobuttonList` | `propertyItems`/`dataSource*` · varsayılan seçim |
| `file` | `allowMultiple` · `isCropActive` · `savePropertyToDb` · `lazyLoading` |
| `text` (statik) | `defaultValue` · `fontSize` · `iconSize` · `isBold` · `textAlignment` · `stiky` |
| `barcode` | `barcodeFormat` · `scannerActive` (`value` = string) |
| `phone` | `format`/maske · `keyboardType` |
| `mapViewer` | konum seçimi/görüntüleme; koordinat/adres |
| `formList` | `childServiceId` · `serviceItemControlId` · `reOrder` · `parameterTransfer`/`propertyTransferParameters` · `editOnlyOwnPosition` · `lazyLoading` · **profil-bazlı ayarlar → `view-profile-property.md`:** `activeStartActions`, `addFromExistingStatusIds`, `selectableVisible`, `selectedEditable` |
| `flowInfo` | `flowInfoValue` (salt-okunur akış metadata) |
| `parentProperty` | `parentPropertyId` · `refPropertyId` · `relatedPropertyIds` (salt-okunur) |
| `userInfo` | `userInfoValue` (salt-okunur kullanıcı metadata) |
| `groupByTaxReceipt` | `disableTaxAttachmentView` · `isActiveKkegAttachment` |
| `keyValueList` | `addNewEnabled` · `deleteEnabled` · `keyDescription` · `valueDescription` · `comboBoxItems` · `keyValueItems` |
| `imageAreaSelector` | `imageUrl` · `aspectRatio` · `dataSource` (nokta: `code`·`x`·`y`·`isSelected`) |

## İlişkiler
- **N – 1** → `Service` (`serviceId`).
- **1 – N** ← `PropertyItem` (`propertyId`), `ProcessViewProfileProperty` (`propertyId`).

## Notlar / açık noktalar
- Çekirdek ↔ tipe-özel ayrımının nihai listesi; Form List ayarları; `dataSource` çift anlamı → `../../todo.md`.

*Oluşturma: 2026-07-02.*
