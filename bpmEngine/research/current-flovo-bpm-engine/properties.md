# Form Alanları (Properties)

## Genel Bakış

Form alanları (Property), BPM sürecinde kullanıcının veri girişi yaptığı ve bilgi görüntülediği temel yapı taşlarıdır. Her servis (form) birden fazla alan içerir ve her alan farklı bir kontrol tipiyle (metin kutusu, tarih seçici, combobox vb.) render edilir.

---

## Veri Modeli (PropertyDto)

### Temel Alanlar

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `propertyId` | int | Otomatik | Alan ID'si |
| `accountId` | String | Evet | Hesap ID'si |
| `serviceId` | int | Evet | Servis ID'si |
| `solutionId` | String | Hayır | Çözüm ID'si |
| `code` | String | Evet | Alan kodu |
| `definition` | String | Evet | Alan tanımı |
| `propertyName` | String | Evet | Alan adı (teknik isim) |
| `label` | String | Evet | Kullanıcıya gösterilen etiket |
| `controlTypeId` | int | Evet | Kontrol tipi |
| `keyboardType` | int | Hayır | Klavye tipi |

### Görünüm Alanları

| Alan | Tip | Açıklama |
|------|-----|----------|
| `hint` | String | Placeholder metin |
| `helperText` | String | Yardımcı metin |
| `headerText` | String | Başlık metni |
| `leadingView` | String | Sol ikon |
| `trealingView` | String | Sağ ikon |
| `leadingViewPosition` | bool | Sol ikon pozisyonu |
| `trealingViewPosition` | bool | Sağ ikon pozisyonu |
| `fontSize` | double | Yazı boyutu |
| `iconSize` | double | İkon boyutu |
| `isBold` | bool | Kalın yazı |
| `colorType` | String | Renk tipi |
| `textAlignment` | TextAlignment | Metin hizalaması |
| `stiky` | bool | Yapışkan alan |

### Davranış Alanları

| Alan | Tip | Açıklama |
|------|-----|----------|
| `defaultValue` | String | Varsayılan değer |
| `format` | String | Format (tarih, sayı) |
| `minimumDate` | DateTime | Minimum tarih |
| `maximumDate` | DateTime | Maksimum tarih |
| `setAsToday` | bool | Bugünü varsayılan yap |
| `showCharCount` | int | Karakter sayısını göster |
| `charMaxLength` | int | Maksimum karakter uzunluğu |
| `maximumNumberDecimalDigits` | int | Ondalık basamak sayısı |
| `enableNegative` | bool | Negatif değere izin ver |
| `enableGroupSeperator` | bool | Grup ayracı (binlik) aktif |
| `precition` | String | Hassasiyet |
| `integerActive` | bool | Tam sayı modu |
| `manuelEntry` | bool | Manuel giriş |
| `isMultiSelect` | bool | Çoklu seçim |
| `onAfterChange` | bool | Değişiklik sonrası tetikleme |
| `backingField` | bool | Arka plan alanı (gizli) |

### Veri Kaynağı Alanları

| Alan | Tip | Açıklama |
|------|-----|----------|
| `dataSource` | String | Veri kaynağı URL/tanımı |
| `dataSourceId` | int | Veri kaynağı ID'si |
| `dataSourceValue` | String | Veri kaynağı değeri |
| `propertyItems` | List | Statik seçenek listesi |
| `propertyTransferParameters` | List | Transfer parametreleri |

### İlişki Alanları

| Alan | Tip | Açıklama |
|------|-----|----------|
| `refPropertyId` | int | Referans alan ID'si (kopyalanan alandan) |
| `parentPropertyId` | int | Üst alan ID'si |
| `relatedPropertyIds` | String | İlişkili alan ID'leri |
| `childServiceId` | int | Alt servis ID'si |
| `serviceItemControlId` | int | Servis öğe kontrol ID'si |

### Kısıtlama Alanları

| Alan | Tip | Açıklama |
|------|-----|----------|
| `accountRestriction` | String | Hesap kısıtlaması |
| `environmentRestriction` | String | Ortam kısıtlaması |
| `state` | int | Alan durumu |

### Özel Özellikler

| Alan | Tip | Açıklama |
|------|-----|----------|
| `flowInfoValue` | int | Süreç bilgisi değeri |
| `userInfoValue` | int | Kullanıcı bilgisi değeri |
| `integratedArea` | Object | Entegre alan ayarları |
| `additionalQualificationId` | int | Ek nitelik ID'si |
| `scannerActive` | bool | Barkod tarayıcı aktif |
| `barcodeFormat` | BarcodeFormat | Barkod formatı |
| `savePropertyToDb` | bool | Veritabanına kaydet |
| `isCropActive` | bool | Kırpma aktif (fotoğraf) |
| `lazyLoading` | bool | Tembel yükleme |
| `addNewEnabled` | bool | Yeni ekleme aktif |
| `addFromExistingRecordsIsActive` | bool | Mevcut kayıtlardan ekleme |
| `selectedEnable` | bool | Seçim aktif |
| `reOrder` | bool | Yeniden sıralama |
| `parameterTransfer` | bool | Parametre transferi |
| `saveChangeLog` | bool | Değişiklik kaydını tut |
| `allowMultiple` | bool | Çoklu değere izin ver |
| `editOnlyOwnPosition` | bool | Sadece kendi kaydını düzenle |

---

## Kontrol Tipleri (ControlType)

Her alan bir kontrol tipi ile render edilir:

| Index | Enum | Açıklama |
|-------|------|----------|
| 0 | `Entry` | Metin girişi |
| 1 | `MaskedEntry` | Maskeli metin girişi |
| 2 | `NumericTextbox` | Sayısal giriş |
| 3 | `Editor` | Çok satırlı metin |
| 4 | `ComboBox` | Açılır liste |
| 5 | `NumericUpDown` | Sayısal artırma/azaltma |
| 6 | `DatePicker` | Tarih seçici |
| 7 | `TimePicker` | Saat seçici |
| 8 | `DateTimePicker` | Tarih-saat seçici |
| 9 | `Photo` | Fotoğraf |
| 10 | `CheckBox` | Onay kutusu |
| 11 | `DataGrid` | Veri tablosu (alt form) |
| 12 | `MultiSelect` | Çoklu seçim |
| 13 | `ModalList` | Modal liste (aranabilir) |
| 14 | `ImageList` | Resim listesi |
| 15 | `ObjectAccessController` | Nesne erişim kontrolü |
| 16 | `TableFieldDisplayController` | Tablo alan görüntüleyici |
| 17 | `GroupByTaxReceiptController` | Vergi fişi gruplandırıcı |
| 18 | `MapViewerControl` | Harita görüntüleyici |
| 19 | `Barcode` | Barkod |
| 20 | `FileController` | Dosya yükleyici |
| 21 | `RadioButtonListController` | Radyo buton listesi |
| 22 | `KeyValueListControl` | Anahtar-değer listesi |
| 23 | `TextControl` | Salt okunur metin |
| 24 | `DataGridControl` | Veri grid kontrolü |
| 25 | `FlowInfo` | Süreç bilgisi |
| 26 | `UserInfo` | Kullanıcı bilgisi |
| 27 | `ServiceItemControl` | Servis öğe kontrolü |
| 28 | `ImageAreaSelector` | Resim alan seçici |
| 29 | `PhoneNumber` | Telefon numarası |

---

## Kontrol Tipine Özel Ayar Sayfaları

Her kontrol tipi için özelleştirilmiş ayar sayfaları mevcuttur:

| Kontrol Tipi | Ayar Sayfası |
|-------------|-------------|
| Entry | `EntryPropertySettings.dart` |
| NumericTextbox | `NumericTextboxSettings.dart` |
| ComboBox | `ComboboxPropertySettings.dart` |
| DatePicker/TimePicker | `DatePropertySettings.dart` / `TimePropertySettings.dart` |
| ModalList | `ModalListSettings.dart` |
| DataGrid | `DataGridPropertySettings.dart` |
| File | `FilePropertySettings.dart` |
| Barcode | `BarcodeSettings.dart` |
| MapViewer | `MapViewSettings.dart` |
| FlowInfo | `FlowInfoSettings.dart` |
| UserInfo | `UserInfoSettings.dart` |
| TextControl | `TextPropertySettings.dart` |
| GroupByTax | `GroupByTaxSettings.dart` |

---

## Çalışma Prensibi

1. **Tanımlama:** Her servis için alanlar tanımlanır. Alan kodu, tipi, etiketi ve davranış özellikleri belirlenir.
2. **Kopyalama:** Mevcut çözüm alanlarından kopyalanarak yeni alan oluşturulabilir (`refPropertyId`).
3. **Görüntüleme Profili:** Alanlar, görüntüleme profilleri aracılığıyla hangi adımda gösterileceği/düzenleneceği kontrol edilir.
4. **İş Kuralları:** WorkRule'lar aracılığıyla alanların değerleri, görünürlükleri ve veri kaynakları dinamik olarak yönetilir.
5. **Veri Kaynağı:** ModalList ve ComboBox gibi alanlar harici veri kaynaklarından veya statik öğelerden (`propertyItems`) beslenir.

---

## API Endpoint'leri

| Endpoint | HTTP | Açıklama |
|----------|------|----------|
| `GetProperties` | POST | Alanları listele |
| `AddOrUpdateProperty` | POST | Alan ekle/güncelle |
| `DeleteProperty/{id}` | POST | Alan sil |

### İstek Header'ları

```
accountId: string
solutionid: string
ServiceId: string
```

---

## Dosya Yapısı

```
lib/Models/Settings/FlvSettings/Property/
└── PropertyDto.dart  # Tüm modeller (GetListPropertyDto, PropertyDto, PropertyItemsDto, vb.)

lib/Models/Enums/
└── ControlType.dart  # Kontrol tipi enum

lib/Pages/Settings/FlvSettings/Property/
├── PropertiesSettingsPage.dart          # Alan listesi sayfası
├── PropertyDetailSettingsPage.dart      # Alan detay sayfası
├── IntegratedAreaDetailPage.dart        # Entegre alan detay
├── IntegratedAreaParameterDetailPage.dart # Entegre alan parametre
└── Properties/
    ├── EntryPropertySettings.dart       # Metin girişi ayarları
    ├── NumericTextboxSettings.dart      # Sayısal giriş ayarları
    ├── TextPropertySettings.dart        # Salt metin ayarları
    ├── DatePropertySettings.dart        # Tarih ayarları
    ├── TimePropertySettings.dart        # Saat ayarları
    ├── FilePropertySettings.dart        # Dosya ayarları
    ├── BarcodeSettings.dart             # Barkod ayarları
    ├── MapViewSettings.dart             # Harita ayarları
    ├── FlowInfoSettings.dart            # Süreç bilgisi ayarları
    ├── UserInfoSettings.dart            # Kullanıcı bilgisi ayarları
    ├── DataGridPropertySettings.dart    # DataGrid ayarları
    ├── GroupByTaxSettings.dart          # Vergi gruplandırma ayarları
    ├── Combobox/
    │   ├── ComboboxPropertySettings.dart       # ComboBox ayarları
    │   └── ComboboxElementDetailSettings.dart  # ComboBox öğe detay
    └── ModalList/
        ├── ModalListSettings.dart              # Modal liste ayarları
        ├── ModalListParameterPage.dart         # Parametre sayfası
        └── FillServiceItemParameterPage.dart   # Servis öğe parametre
```
