# Model — Property (form alanı)

> **Durum:** 🟡 TASLAK (ilk çıkarım — gözden geçirilecek)
> **Amaç:** Metadata-driven formdaki tek bir **giriş/görüntüleme elemanı**. Bir **kontrol tipi** (`propertyType`) ile
> render edilir, `code` ile veriye bağlanır.
> **Davranış/kullanım + tam alan kataloğu:** → `../../service-settings/properties.md`
>
> **Tasarım ilkesi:** ince **ortak çekirdek** + **tipe-özel alanlar** (`propertyType`'a göre).

## 1. Çekirdek alanlar (her alanda)

### 1.1 Kimlik & bağlama
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Alan ID'si. |
| `serviceId` | int | FK → Service | Bağlı servis. |
| `code` | string | benzersiz (binding key) | Alanın veriye bağlandığı anahtar — yalnız **bağlama**; çeviri için kullanılmaz → `translationCode`. **Immutable:** `InstanceValue.data` JSONB anahtarı + `InstanceAttr.propertyCode` + API/iş kuralı kimliği olduğundan **dondurulur** (yalnız **draft penceresi** — ilk `Instance` yokken — değişebilir; sonrası kilit). Değiştirmek = eski JSONB anahtarı öksüz kalır, sorgu/API/iş kuralı kırılır. |
| `definition` | string | — | Alan tanımı / kullanıcıya görünen etiket — **varsayılan dildeki** metin (çeviri: `translationCode` → Translation). |
| `translationCode` | string? | çeviri anahtarı | **Çeviri eşleşme anahtarı** (→ [`../organization-settings/translation.md`](../organization-settings/translation.md) `code`). `null` = çeviri **es geçilir**, doğrudan `definition` kullanılır. |
| `propertyType` | PropertyType | — | Kontrol tipi (§2 tipe-özel alanları belirler) — [`../enums/property-type.md`](../enums/property-type.md). |

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
| `savePropertyToDb` | bool | Değerin `InstanceValue.data`'ya (kaynak JSONB'ye) yazılıp yazılmayacağı. |
| `saveChangeLog` | bool | Değişiklik geçmişi tut → değer değişince `InstanceValue.data` update TX'inde [`../processInstances/instance-value-change.md`](../processInstances/instance-value-change.md) satırı düşer. |
| `projectToAttr` | bool | **Fihriste (projeksiyona) yazılsın mı?** `true` = değer `InstanceValue.data`'dan [`../processInstances/instance-attr.md`](../processInstances/instance-attr.md) / [`../processInstances/instance-list-item.md`](../processInstances/instance-list-item.md)'a yansıtılır (rapor/filtre/sıra/aralık/isim-arama). `false` = yalnız JSONB'de kalır (**eşittir** sorgusu için GIN yeter). Tipik alanların **%10–20'si** `true`. `savePropertyToDb`'den **farklı**: o kaynağa yazımı, bu fihriste yansımayı belirler. |
| `isReflectionSource` | bool | **Türetilmiş (servis yayınında hesaplanır):** bu alan, başka bir servisin `parentProperty` (`materialized`) alanı tarafından **yansıtılan kaynak** mı? `true` ise değeri değişince yansıma yayılımı tetiklenir; `false` (çoğu alan) → yayılım consumer'ı **hızlı çıkış** yapar (ek maliyet yok). Mekanizma → [`../processInstances/reflection-propagation.md`](../processInstances/reflection-propagation.md). |
| `state` | — | Alan durumu. |
| `environmentRestriction` | string | Ortam kısıtı. |
| `organizationRestriction` | string | Organizasyon kapsam kısıtı. |
| `settings` | JSONB | **Tipe-özel ayarlar** (`propertyType`'a göre — §2). Ayrı alt-tablo/kolon **açılmaz** → gömülü JSONB; ayrımlayıcı `propertyType`; tip-başına **JSON Schema** ile doğrulanır. `ProcessStep.settings` deseniyle **birebir aynı** (v0.31 kararı). Yalnız **projektör/sorgu katmanının ilişkisel okuduğu metadata** çekirdek kolonda kalır (§2 karar notu). |

> **Not:** `visible` / `enabled` / `required` bu modelde **değil**, `ProcessViewProfileProperty`'de tutulur.

### 1.4 Veri kaynağı alanları (seçim alanları için)
| Alan | Tip | Açıklama / amaç |
|---|---|---|
| `dataSource` / `dataSourceId` / `dataSourceValue` | — | **Dinamik** veri kaynağı. |
| `propertyItems` | List\<PropertyItem\> | **Statik** seçenekler (→ `property-item.md`). |
| `lazyLoading` | bool | Tembel yükleme. |
| `manuelEntry` | bool | Serbest giriş. |
| `isMultiSelect` | bool | Çoklu seçim. |
| `hasTranslation` | bool | Alanın **değer seçenekleri çeviri kullanıyor mu** (yardımcı bayrak). Etiketli seçimler `LabeledValue` şekliyle (`{value, display, translationCode}`) yazılır → [`../processInstances/propertyValuesTemplates/labeled-value.md`](../processInstances/propertyValuesTemplates/labeled-value.md). Liste her zaman `PropertyItem` olmak zorunda değildir (dinamik/iş-kuralı listede display istekle gelir). |

### 1.5 İlişki alanları (ilişkisel alanlar için)
| Alan | Tip | Açıklama / amaç |
|---|---|---|
| `childServiceId` | int | Alt servis (Form List). |
| `serviceItemControlId` | int | Alt-servis öğe kontrolü. |
| `refPropertyId` | int | Referans alınan alan (Parent Property). |
| `parentPropertyId` | int | Üst alan. |
| `relatedPropertyIds` | List\<int\> | İlişkili alanlar. |
| `reflectionMode` | ReflectionMode | **Salt-okunur/türetilen alanlarda** (`parentProperty` · `userInfo` · `flowInfo`) — değerin **oluşturma-anı mı (dondurulmuş)** yoksa **güncel mi** gösterileceği: `snapshot` (kopyala+dondur) · `live` (canlı okuma) · `materialized` (kopya + **`AssociatedInstance` üzerinden yayılımla** tazelenir — **yalnız `parentProperty`**). **Tipe-göre varsayılan:** `parentProperty`/`userInfo` → `snapshot` · `flowInfo` → `live`. → [`../enums/reflection-mode.md`](../enums/reflection-mode.md). |
| `reflectionPropagation` | ReflectionPropagation | **Yalnız `parentProperty` + `reflectionMode=materialized`** — kopyanın üst değişince **ne zaman** tazeleneceği: `async` (arka planda, **vars.**) · `sync` (yazma anında, guardrail'li). → [`../enums/reflection-propagation.md`](../enums/reflection-propagation.md) · mekanizma [`../processInstances/reflection-propagation.md`](../processInstances/reflection-propagation.md). |

## 2. Tipe-özel alanlar (`propertyType`'a göre — özet)
> Tam açıklama → `../../service-settings/properties.md` §3.
>
> **Depolama — KARAR (v0.31): tipe-özel alanlar JSONB `settings`'te gömülü.** Aşağıdaki tablodaki tipe-özel ayarlar
> `Property`'de **ayrı kolon açılmadan** `settings` (JSONB) içinde tutulur; ayrımlayıcı `propertyType`; her tip için ayrı
> **JSON Schema** ile doğrulanır (referans bütünlüğü uygulama katmanında). Bu, `ProcessStep.settings` (v0.12) deseninin
> **aynısıdır** ve "şişman model" (her tip için çoğu-boş kolon) sorununu kaldırır; yeni alan tipi = **yeni JSON Schema**
> (kolon değişikliği yok, kapalı-set genişletmesi çekirdek geliştirmesiyle).
>
> **Çekirdekte kalan (kolon) ↔ `settings`'e giden ayrım (sınır kuralı):** Bir tipe-özel alan **yalnız render/istemci
> davranışı** için tüketiliyorsa → `settings`. Buna karşılık **projektör/sorgu/motor katmanının ilişkisel okuduğu
> metadata gerçek kolonda kalır** (çoğu tipte boş olsa bile): kimlik/bağlama (`code`, `propertyType`), değer-saklama/
> projeksiyon (`savePropertyToDb`, `projectToAttr`, `saveChangeLog`, `hasTranslation`), yansıma metadata'sı
> (`reflectionMode`, `reflectionPropagation`, `isReflectionSource`, `refPropertyId`, `parentPropertyId`, `relatedPropertyIds`),
> ve ilişki FK'leri (`childServiceId`, `associatedServiceId`, `serviceItemControlId`). Aşağıdaki §2 tablosundaki **saf
> render/davranış** ayarları (ör. `minLine`/`maxLine`, `barcodeFormat`, `headerText`, `isCropActive`, `setAsToday`,
> `enableGroupSeperator`, `keyDescription`…) `settings`'e girer. _(Statik seçenek listesi `propertyItems` bir alt-koleksiyon
> olarak `PropertyItem` tablosunda kalır; `settings`'e gömülmez.)_
> **Enum'lar:** kontrol tipi → [`../enums/property-type.md`](../enums/property-type.md) · `keyboardType` (Textbox/Phone) → [`../enums/keyboard-type.md`](../enums/keyboard-type.md) · `barcodeFormat` (Barcode) → [`../enums/barcode-format.md`](../enums/barcode-format.md) · `reflectionMode` (parentProperty/userInfo/flowInfo) → [`../enums/reflection-mode.md`](../enums/reflection-mode.md) · `reflectionPropagation` (parentProperty A′) → [`../enums/reflection-propagation.md`](../enums/reflection-propagation.md).

| Kontrol tipi | Alanlar |
|---|---|
| `textbox` | `minLine` · `maxLine` · `charMaxLength` · `showCharCount` · `keyboardType` · maske |
| `numericTextbox` | `maxDecimalDigits` · `enableNegative` · `enableGroupSeperator` · `integerActive` |
| `combobox` | `propertyItems`/`dataSource*` · `isMultiSelect` · `manuelEntry` · `lazyLoading` · `headerText` · `isAssociatedCombobox` · `associatedServiceId` |
| `datepicker` | `minimumDate` · `maximumDate` · `setAsToday` · `format` · `headerText` |
| `timePicker` | `format` · `defaultValue` · `headerText` |
| `checkbox` | `defaultValue` (bool) |
| `radiobuttonList` | `propertyItems`/`dataSource*` · varsayılan seçim |
| `file` | `allowMultiple` · `isCropActive` · `savePropertyToDb` · `lazyLoading` |
| `text` (statik) | `defaultValue` · `fontSize` · `iconSize` · `isBold` · `textAlignment` · `stiky` |
| `barcode` | `barcodeFormat` · `scannerActive` (`value` = string) |
| `phone` | `format`/maske · `keyboardType` |
| `mapViewer` | konum seçimi/görüntüleme; koordinat/adres · **profil-bazlı → `view-profile-property.md`:** `editOnlyOwnPosition` |
| `formList` | `childServiceId` · `serviceItemControlId` · `lazyLoading` · **profil-bazlı ayarlar → `view-profile-property.md`:** `reOrder`, `activeStartActions`, `addFromExistingStatusIds`, `selectableVisible`, `selectedEditable` |
| `flowInfo` | `flowInfoValue` · `reflectionMode` (`snapshot`/`live` — vars. `live`; salt-okunur akış metadata) |
| `parentProperty` | `parentPropertyId` · `refPropertyId` · `relatedPropertyIds` · `reflectionMode` (`snapshot`/`live`/`materialized`) · `reflectionPropagation` (`async`/`sync` — yalnız `materialized`) (salt-okunur) |
| `userInfo` | `userInfoValue` · `reflectionMode` (`snapshot`/`live` — vars. `snapshot`; salt-okunur kullanıcı metadata) |
| `groupByTaxReceipt` | `disableTaxAttachmentView` · `isActiveKkegAttachment` |
| `keyValueList` | `addNewEnabled` · `deleteEnabled` · `keyDescription` · `valueDescription` · `comboBoxItems` · `keyValueItems` |

> **İlişkili combobox (`isAssociatedCombobox` · `associatedServiceId`):** `combobox` alanında `isAssociatedCombobox=true`
> iken **`associatedServiceId` zorunludur**; combobox o servisin **instance'larından** seçim yaptırır ve seçilen
> **instance id'si** alanın **`value`'suna** yazılır. Alanın instance'taki **`propertyValue`'su her değiştiğinde**, seçilen
> **her** instance için **`AssociatedInstance`** tablosuna bir **ilişki kaydı** düşer (→ [`../processInstances/associated-instance.md`](../processInstances/associated-instance.md)).
> **`isMultiSelect` ile birleşebilir:** çoklu ilişkili combobox tek alanla **birden çok instance'ı** ilişkilendirir (her seçim ayrı `AssociatedInstance` kaydı — Form List benzeri).
> `false` (vars.) = düz liste seçimi, ilişki kaydı **düşmez**. Davranış → `../../service-settings/properties.md` §3.3.

## İlişkiler
- **N – 1** → `Service` (`serviceId`).
- **1 – N** ← `PropertyItem` (`propertyId`), `ProcessViewProfileProperty` (`propertyId`).
- **Mantıksal (`code` üzerinden, id-FK değil):** `InstanceAttr.propertyCode` · `InstanceListItem.listCode`/`attrCode` ·
  `InstanceValueChange.propertyCode` — değer katmanı **code-keyed**dir. Yansıma yayılımı da (`materialized`) üst↔child alan eşlemesini **`code`** ile yapar (→ [`../processInstances/reflection-propagation.md`](../processInstances/reflection-propagation.md)).

## Notlar / açık noktalar
- **Değer saklama bağı (metadata-driven projeksiyon):** `Property`, değerlerin **nasıl saklanıp fihristleneceğini**
  belirleyen metadata'yı taşır — `code` (JSONB anahtarı, immutable) · `projectToAttr` (fihriste yansı) · `savePropertyToDb`
  (kaynağa yaz) · `saveChangeLog` (geçmiş) · `hasTranslation`/`reflectionMode`. Generic projektör bu metadata'ya bakarak
  `InstanceValue.data`'dan `InstanceAttr`/`InstanceListItem` üretir (alan adı koda gömülü değildir). Değer modelleri →
  [`../processInstances/instance-value.md`](../processInstances/instance-value.md) · [`instance-attr.md`](../processInstances/instance-attr.md) · [`instance-list-item.md`](../processInstances/instance-list-item.md) · [`labeled-value.md`](../processInstances/propertyValuesTemplates/labeled-value.md).
- **Çekirdek ↔ tipe-özel ayrım — ÇÖZÜLDÜ (v0.31):** tipe-özel ayarlar JSONB `settings`'te (tip-başına JSON Schema);
  projektör/sorgu/motor katmanının okuduğu metadata çekirdek kolonda kalır (→ §2 karar notu). Alanların hangi tarafa
  düştüğü **sınır kuralıyla** belirlenir (render/davranış → `settings`; ilişkisel-okunan metadata → kolon). _(Form List `reOrder`
  (profil-bazlı) + mapViewer `editOnlyOwnPosition` (profil-bazlı) → **ÇÖZÜLDÜ v0.33**; `parameterTransfer`/`propertyTransferParameters`
  **kaldırıldı** — ana↔alt akış `parentProperty` ile.)_
- **İndeks stratejisi — KARAR (v0.31):** `InstanceValue.data` (JSONB) üzerinde **GIN** (eşittir / `@>` / anahtar-var — `projectToAttr=false`
  alanlar) · `projectToAttr=true` alanlar için **`InstanceAttr` tipli değer kolonuna B-tree** (aralık / sıra / isim-arama / filtre);
  gerekirse kısmi/ifade indeksi. Böylece alanların çoğu yalnız JSONB'de (ucuz), yalnız rapor-kritik ~%10–20 fihristte indekslenir.
- **`dataSource` çift anlamı — ÇÖZÜLDÜ:** `Image Area Selector` (`imageAreaSelector`) alan tipi **kaldırıldı**; `dataSource*`
  artık yalnız Combobox/Radiobutton **dinamik seçenek kaynağı**. Seçenek verisi için ayrı tablo yok — statik `propertyItems`
  (`PropertyItem`) **devam** (davranış → `../../service-settings/properties.md` §2.4).

*Oluşturma: 2026-07-02.*
