# Property Settings — Tipe-Özel Ayar Şemaları (İndeks)

> **Durum:** 🟢 DETAYLANIYOR (v0.37) — tip-başına `Property.settings` (JSONB) ayar şeması.
> **Amaç:** Her `propertyType` için o alanın **tipe-özel ayarlarını** tek tek tanımlar: hangi alanlar · tip · zorunluluk ·
> varsayılan · kısıt + **JSON Schema**. Backend `settings` **doğrulama kapısının** ve frontend **form-üreticisinin** doğrudan
> girdisidir. Bu klasör, `settings` JSONB'nin **tip-bazlı somut şema kataloğudur** (değer-şekli karşılığı →
> [`../../../processInstances/propertyValuesTemplates/index.md`](../../../processInstances/propertyValuesTemplates/index.md)).

## Bir alan nerede yaşar? (sınır kuralı — 3 katman)
Her tip dosyası, o tipin alanlarını **üç yere** ayırarak gösterir (→ [`../../property.md`](../../property.md) §2 karar notu):

| # | Katman | İçerik | Nerede |
|---|---|---|---|
| 1 | **`settings` (JSONB)** | Tipe-özel **render/istemci davranışı** ayarı — **bu şemaların konusu** | `Property.settings` (ayrımlayıcı `propertyType`) |
| 2 | **Çekirdek kolon** | Projektör/sorgu/motor katmanının **ilişkisel okuduğu** metadata + ilişki FK'leri | `Property` kolonları (→ [`../../property.md`](../../property.md) §1) |
| 3 | **Profil-bazlı** | **Görüntüleme profiline göre** değişen ayarlar | `ProcessViewProfilePropertySetting` (→ [`../../view-profile-property.md`](../../view-profile-property.md)) |

## Ortak kurallar (tüm tip şemaları)
- Her `settings` JSON Schema **`additionalProperties: false`** (kapalı-set; bilinmeyen anahtar **reddedilir**).
- `settings` içindeki **referans id'ler** (`dataSourceId`, `comboBoxItems` kaynağı…) DB FK'si değildir; **uygulama-katmanı**
  doğrulaması + silme koruması gerekir (→ [`../../../../todo.md`](../../../../todo.md) "Adım/alan `settings` referans bütünlüğü").
- Değer alanları (`defaultValue`, `value`) çoğu tipte **çekirdek kolonda**; şekli tipe göre değişir → değer şablonu dosyasına atıf.

## Tip dizini (18)
| propertyType | Ad | `settings` alanları (özet) | Dosya |
|---|---|---|---|
| `textbox` | Textbox | `minLine`·`maxLine`·`charMaxLength`·`showCharCount`·`keyboardType` | [`textbox.md`](./textbox.md) |
| `numericTextbox` | Numeric Textbox | `maxDecimalDigits`·`enableNegative`·`enableGroupSeperator`·`integerActive` | [`numeric-textbox.md`](./numeric-textbox.md) |
| `combobox` | Combobox | `isMultiSelect`·`manuelEntry`·`lazyLoading`·`headerText`·`isAssociatedCombobox` | [`combobox.md`](./combobox.md) |
| `datepicker` | Datepicker | `minimumDate`·`maximumDate`·`setAsToday`·`headerText` | [`datepicker.md`](./datepicker.md) |
| `timePicker` | Time Picker | `headerText` | [`time-picker.md`](./time-picker.md) |
| `checkbox` | Checkbox | (boş — `defaultValue` bool çekirdekte) | [`checkbox.md`](./checkbox.md) |
| `radiobuttonList` | Radiobutton List | `manuelEntry`·`lazyLoading` | [`radiobutton-list.md`](./radiobutton-list.md) |
| `file` | File | `allowMultiple`·`isCropActive`·`lazyLoading` | [`file.md`](./file.md) |
| `text` | Text (statik) | `fontSize`·`iconSize`·`isBold`·`textAlignment`·`stiky` | [`text.md`](./text.md) |
| `barcode` | Barcode | `barcodeFormat`·`scannerActive` | [`barcode.md`](./barcode.md) |
| `phone` | Phone | `keyboardType` (core `format`/değer objesi) | [`phone.md`](./phone.md) |
| `mapViewer` | Map Viewer | `mapPinIconUrl` (+ profil `editOnlyOwnPosition`) | [`map-viewer.md`](./map-viewer.md) |
| `formList` | Form List | `lazyLoading` (+ core FK'ler + profil-bazlı) | [`form-list.md`](./form-list.md) |
| `flowInfo` | Flow Info | `flowInfoValue` (core `reflectionMode`) | [`flow-info.md`](./flow-info.md) |
| `parentProperty` | Parent Property | (boş — hepsi çekirdek: FK'ler + `reflectionMode`/`reflectionPropagation`) | [`parent-property.md`](./parent-property.md) |
| `userInfo` | User Info | `userInfoValue` (core `reflectionMode`) | [`user-info.md`](./user-info.md) |
| `groupByTaxReceipt` | Group By Tax Receipt | `disableTaxAttachmentView`·`isActiveKkegAttachment` | [`group-by-tax-receipt.md`](./group-by-tax-receipt.md) |
| `keyValueList` | Key-Value List | `addNewEnabled`·`deleteEnabled`·`keyDescription`·`valueDescription`·`comboBoxItems`·`keyValueItems` | [`key-value-list.md`](./key-value-list.md) |

> _(Özet sütun kesin şema değildir; kesin alan/kısıt her tipin kendi dosyasındadır. Dosyalar oluşturuldukça link eklenir.)_

*Oluşturma: 2026-08-28.*
