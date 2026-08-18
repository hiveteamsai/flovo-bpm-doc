# Flovo — Form Alanları / Bileşenleri (Properties) Tasarımı

> **Durum:** 🟢 DETAYLANIYOR
> **Amaç:** Bir Flovo **formunda yer alabilecek alan (property) tiplerini** ve her birinin **detay ayarlarını** tanımlamak.
>
> **İlişki:** Bu alanlar `process-step-action.md` §2'deki **`changeList`** ile güncellenir; **zorunluluk / görünürlük /
> düzenlenebilirlik** alanın kendisinde değil, **görüntüleme profilinde** tutulur (→ `view-profile.md`); alanlar
> `process-step.md`'deki **Instance Creator / Instance Deleter / Değer Atama** adımlarıyla yönetilir. **Form List** (§3.13) bir
> alt-servis alanıdır.

---

## 0. Form Alanı (Property) Nedir?
Bir **property**, metadata-driven (server-tanımlı) formdaki tek bir **giriş veya görüntüleme** elemanıdır (metin
kutusu, tarih seçici, dosya, harita...). Her property bir **kontrol tipi** (`propertyType`) ile render edilir, bir
**veriye bağlanır** (binding: `code`) ve değeri aksiyonların **`changeList`**'i ile güncellenebilir. Bir servis
(form) birden çok property içerir.

> **Tasarım ilkesi:** **ince ortak çekirdek (§2)** + **tipe-özel ayarlar (§3)** ayrımı (performans + self-servis).

---

## 1. Alan Taksonomisi (mantıksal gruplar)
- **Girdi:** Textbox · Numeric Textbox · Phone
- **Seçim:** Combobox · Radiobutton List · Checkbox
- **Tarih/Saat:** Datepicker · Time Picker
- **Medya & Dosya:** File · Barcode
- **Statik / Bilgi:** Text · Flow Info · User Info
- **Konum:** Map Viewer
- **İlişkisel:** Form List · Parent Property
- **Özel:** Group By Tax Receipt · Key-Value List

---

## 2. Ortak Property Çekirdeği (her alanda bulunan temel alanlar)
Tipe-özel ayarlar → §3.

### 2.1 — Kimlik & bağlama
| Alan | Tip | Açıklama |
|---|---|---|
| `id` | int | Alan ID'si (primary key) |
| `serviceId` | int | Bağlı servis ID'si (FK) |
| `code` | string | Alan kodu (benzersiz — binding key; **çeviri için kullanılmaz** → `translationCode`) |
| `definition` | string | Alan tanımı / kullanıcıya görünen etiket — **varsayılan dildeki** metin |
| `translationCode` | string? | **Çeviri eşleşme anahtarı** (→ `../organization-settings/translation.md` `code`). `null` = çeviri **es geçilir**, doğrudan `definition` kullanılır. |
| `propertyType` | int | Kontrol tipi (→ `../models/enums/property-type.md`) |

### 2.2 — Görünüm & yardım
| Alan | Açıklama |
|---|---|
| `hint` | Placeholder metni |
| `helperText` | Yardımcı (alt) metin |
| `leadingView` / `trailingView` (+pozisyon) | Sol/sağ ikon |

> **Alana-özel görünüm alanları (çekirdekte değil):**
> - `headerText` — **her alanda yoktur**; yalnız **pop-up açan alanlarda** (Combobox, Datepicker, Time Picker vb.)
>   açılan pop-up'ın **başlığında** görünen metindir (→ §3.3 / §3.4 / §3.5).
> - `fontSize` · `iconSize` · `isBold` · `textAlignment` · `stiky` — **Text** (statik başlık) alanına özeldir (→ §3.9).

### 2.3 — Davranış & kalıcılık
| Alan | Açıklama |
|---|---|
| `defaultValue` | Varsayılan değer |
| `format` | Format (tarih/sayı/maske) |
| `saveAndRefreshOnAfterChange` | Alanın değeri değişince **kaydet isteği atıp formu yeniler** (refresh) |
| `backingField` | Gizli/arka-plan alan |
| `savePropertyToDb` | Değeri kaynak JSONB'ye (`InstanceValue.data`) kaydet |
| `saveChangeLog` | Değişiklik geçmişi tut (→ `InstanceValueChange`) |
| `projectToAttr` | **Fihriste (projeksiyona) yansı** — `true` = değer `InstanceAttr`/`InstanceListItem`'a yazılır (rapor/filtre/sıra/aralık/isim-arama); `false` = yalnız JSONB (eşittir için GIN yeter). Tipik %10–20 `true`. |
| `state` · `environmentRestriction` · `organizationRestriction` | Durum / kapsam kısıtı |

> **Değer saklama:** `savePropertyToDb` (kaynağa yaz) · `projectToAttr` (fihriste yansı) · `saveChangeLog` (geçmiş) alanları,
> değerlerin **JSONB kaynak-hakikat + türetilebilir fihrist** (CQRS + Outbox) mimarisini besler. Model + mimari →
> [`../models/processInstances/instance-value.md`](../models/processInstances/instance-value.md) · `instance-attr.md` · `../research/property-value-storage/form-deger-saklama-v2.html`.

> **Görünürlük/zorunluluk ayrımı:** **Zorunluluk (`required`) / görünürlük (`visible`) / düzenlenebilirlik (`enabled`)**
> property'de **değil**, **görüntüleme profilinde** tutulur (→ `view-profile.md` §2): *alan = ne olduğu*, *profil = nerede nasıl göründüğü*.

### 2.4 — Veri kaynağı alanları (seçim alanları için)
`dataSource` · `dataSourceId` · `dataSourceValue` (dinamik) · `propertyItems` (statik liste — öğe modeli → §2.6) ·
`propertyTransferParameters` · `lazyLoading` · `manuelEntry` · `isMultiSelect` · `hasTranslation`. _(Kullanımı → §3.3 / §3.7)_

> **`hasTranslation` + etiketli değer (`LabeledValue`):** Kodu ile görünen adı farklı olan seçim değerleri (combobox/radio/
> key-value…) depoya `{value, display, translationCode}` şekliyle yazılır (rapor isim-araması `InstanceAttr.display`). Statik
> liste display'i `propertyItems`'ten, dinamik/iş-kuralı listede istekle gelir. → [`../models/processInstances/propertyValuesTemplates/labeled-value.md`](../models/processInstances/propertyValuesTemplates/labeled-value.md).

> **Seçenek kaynağı iki yolla dolar (Combobox / Radiobutton):**
> 1. **Statik** — ayarlardan eklenen **`propertyItems`** ile (yönetici öğeleri elle tanımlar; öğe modeli → §2.6).
> 2. **Dinamik** — **iş kuralı `fillDataSource`** ile çalışma-zamanında (frontend) doldurulur. Ayarlanan iş kuralına göre
>    kaynak **farklı tiplerden** beslenebilir: **organizasyon verileri** · **kullanıcı bilgileri** · **başka bir servisin
>    instance'ları** · dış/API kaynağı vb. (→ `business-rule.md` §3 `fillDataSource`).
> _(Ayrıca combobox'ın seçilen değeri bir **ilişki kaydı** da üretebilir → §3.3 `isAssociatedCombobox`.)_

> **`dataSource` tek anlamlı (KARAR):** `dataSource*` artık **yalnız** seçim alanlarının (Combobox / Radiobutton) **dinamik
> seçenek kaynağıdır**; eskiden aynı adı statik nokta listesi için kullanan **Image Area Selector alan tipi kaldırıldı**, çift
> anlam ortadan kalktı. Seçenek verisi için **ayrı tablo açılmaz** — **statik = `propertyItems`** (`PropertyItem` modeli, §2.6),
> **dinamik = iş kuralı `fillDataSource`**; mevcut `PropertyItem` yapısı **aynen kullanılmaya devam eder**.

### 2.5 — İlişki alanları (ilişkisel alanlar için)
`childServiceId` · `serviceItemControlId` · `refPropertyId` · `parentPropertyId` · `relatedPropertyIds` · `reflectionMode` · `reflectionPropagation`.
_(Kullanımı → §3.13 Form List, §3.15 Parent Property; `reflectionMode` ayrıca **§3.14 Flow Info / §3.16 User Info**'da da geçerli — `reflectionPropagation` yalnız `parentProperty`+`materialized`)_

### 2.6 — PropertyItem (seçim öğesi — statik liste elemanı)
`propertyItems`, seçim alanlarının (Combobox §3.3 · Radiobutton List §3.7) **statik seçeneklerini** tutan listedir.
Listedeki her eleman bir **PropertyItem**'dir:

| Alan | Tip | Açıklama |
|---|---|---|
| `id` | int | Öğe ID'si |
| `propertyId` | int | Bağlı olduğu alan (property) |
| `value` | string | **Seçilen değer** (alanın value'suna yazılır) — `propertyId` içinde **benzersiz** |
| `translationCode` | string? | **Çeviri eşleşme anahtarı** — `../organization-settings/translation.md` `code`'u ile eşleşir; öğe metni buradan çözülür. **`null` = çeviri es geçilir**, doğrudan `definition` kullanılır |
| `definition` | string | Öğe tanımı — **varsayılan dildeki** metin (yönetim ekranında görünen ad) |

> **Neden `translationCode` ≠ `value`?** Farklı comboboxlar aynı `value` kümesini (örn. `0`·`1`·`2`·`3`) kullanabilir.
> Çeviriler birbirine karışmasın diye **çeviri eşleşmesi `translationCode` üzerinden** yapılır; `value` yalnız
> **seçilen değeri** taşır. Böylece iki farklı alanda aynı `value` olsa bile **farklı `translationCode` → farklı çeviri** olur.
> _(Bu, tüm çevrilebilir modellerde geçerli olan **iş kodu ≠ çeviri anahtarı** standardının bir örneğidir →
> `../organization-settings/translation.md` §3.1.)_
> - **Benzersizlik:** `(propertyId, value)` benzersiz — bir alanda aynı `value`'lu iki öğe olamaz.
> - **Görünen metin:** `translationCode` → `../organization-settings/translation.md` §3 çözümlemesiyle **aktif dile** göre
>   gösterilir; anahtar `null` ise doğrudan `definition`.

---

## 3. Alan Kataloğu (form alan tipleri)

### 3.1 — `textbox` (Textbox)
Yazı yazılabilen alan. `minLine`/`maxLine` ile **tek satır** ya da **çok satırlı** metin girişi yapılır (ayrı bir
çok-satır alanı yoktur).
**Ayarlar:** `minLine` / `maxLine` (satır sayısı — 1 = tek satır, >1 = çok satır) · `charMaxLength` (maks. karakter) ·
`showCharCount` (sayaç) · `keyboardType` (klavye) · **maske** · `hint` · `defaultValue`.

### 3.2 — `numericTextbox` (Numeric Textbox)
Sadece sayı girilen alan.
**Ayarlar:** `maxDecimalDigits` (ondalık basamak sayısı — maks.) · `enableNegative` (negatif) ·
`enableGroupSeperator` (binlik ayraç) · `integerActive` (tam sayı) · `defaultValue`.

### 3.3 — `combobox` (Combobox)
Listeden seçim yapmak için olan alan.
**Ayarlar (veri kaynağı → §2.4):** `propertyItems` (statik öğeler) · `dataSource`/`dataSourceId`/`dataSourceValue`
(dinamik) · `isMultiSelect` (çoklu) · `manuelEntry` (serbest giriş) · `lazyLoading` · `headerText` (seçim pop-up'ının başlığı).
> Combobox yalnız **liste seçimi** yapar; alt-servis bağlamaz (alt-servis için → §3.13 Form List).

**İlişkili combobox (başka bir servisin instance'ıyla ilişki kuran seçim):**
- `isAssociatedCombobox` (bool) — `true` ise bu combobox, düz liste yerine **başka bir servisin instance'larından** seçim
  yaptırır; seçim, o instance ile bir **ilişki** kurar. `false` (vars.) = ilişki kurmayan düz liste seçimi.
- `associatedServiceId` (int) — `isAssociatedCombobox=true` iken **zorunludur**; comboboxun **seçenek kaynağı** olan servis.
  Seçilen instance'ın **id'si** alanın **`value`'suna** (propertyValue) yazılır.

> **Çalışma (ilişki kaydı):** `isAssociatedCombobox=true` iken, alanın instance'taki **`propertyValue`'su her
> değiştiğinde**, seçilen instance için **`AssociatedInstance`** tablosuna bir **ilişki kaydı** yazılır:
> `associatedPropertyId` = bu combobox · `associatedInstanceId` = comboboxu **içeren** instance · `instanceId` = combobox'ta
> **seçilen** instance (→ `../models/processInstances/associated-instance.md`). `false` iken hiçbir ilişki kaydı düşmez.

### 3.4 — `datepicker` (Datepicker)
Tarih seçim alanı (tarih+saat opsiyonu).
**Ayarlar:** `minimumDate` · `maximumDate` · `setAsToday` (bugünü varsayılan yap) · `format` · `headerText` (takvim pop-up'ının başlığı).

### 3.5 — `timePicker` (Time Picker)
Saat seçim alanı.
**Ayarlar:** `format` (saat formatı) · `defaultValue` · `headerText` (saat seçim pop-up'ının başlığı).

### 3.6 — `checkbox` (Checkbox)
Tikleme alanı.
**Ayarlar:** `defaultValue` (bool — başlangıçta işaretli mi).

### 3.7 — `radiobuttonList` (Radiobutton List)
Birden fazla seçimden birini seçmek için olan alan.
**Ayarlar (veri kaynağı → §2.4):** `propertyItems` (statik) veya `dataSource*` (dinamik) · varsayılan seçim.

### 3.8 — `file` (File)
Dosya seçimi yapılan alan.
**Ayarlar:** `allowMultiple` (çoklu dosya) · `isCropActive` (fotoğraf kırpma) · `savePropertyToDb` · `lazyLoading`.
> Flovo AI (`process-step.md` §3.3) dosyayı bu alandan veya form thumbnail'inden alır.

### 3.9 — `text` (Text statik)
Başlık, açıklama vb. gibi **statik label** alanı (girdi değildir).
**Ayarlar (bu alana özel tipografi/yerleşim):** `defaultValue` (gösterilecek statik metin) · `fontSize` (yazı boyutu) ·
`iconSize` (ikon boyutu) · `isBold` (kalın) · `textAlignment` (hizalama) · `stiky` (yapışkan/sabit başlık).

### 3.10 — `barcode` (Barcode)
Barcode görseli yer alan alan. **`value`** olarak bir **string** değer tutar ve `barcodeFormat`'a göre bu değeri form
üzerinde **barkod görseline render eder**.
**Yerleşim:** Barkod görselinin **altında bir text alanı**, text alanının **sağında kamerayı açan bir ikon** bulunur.
**Düzenleme (alan editlenebilirse):**
- **Textbox üzerinden** değer elle güncellenebilir, **veya**
- **kamera ile barkod tarayarak** `value` güncellenir (ikon kamerayı açar).
- `value` her değiştiğinde barkod görseli **yeniden render edilir**.
**Ayarlar:** `barcodeFormat` (hem render hem okuma) · `scannerActive` (kamera/tarayıcı ile okuma aktif).
> İlgili: Custom ID Creator `createWithBarcode` (→ `process-step.md` §3.11); `scanBarcode` (Barcode Tara) aksiyonu (`process-step-action.md` §3.5).

### 3.11 — `phone` (Phone)
Telefon numarası girilen alan.
**Ayarlar:** `format`/maske (ülke/numara) · `keyboardType` (telefon klavyesi).

### 3.12 — `mapViewer` (Map Viewer)
Harita üzerinde **seçim ve görüntüleme** alanı.
**Ayarlar:** konum **seçimi** + **görüntüleme**; koordinat/adres değeri.

### 3.13 — `formList` (Form List)
Farklı bir **servis (süreç)** formlarının bu alan altında forma **eklenerek veya yenisi oluşturularak**
ilişkilendirilip görüntülendiği **alt-servis** alanı.
**Ayarlar (alan-düzeyi, `Property`'de — ilişki → §2.5):** `childServiceId` (alt servis) · `serviceItemControlId` ·
`reOrder` (sıralama) · `parameterTransfer`/`propertyTransferParameters` (ana↔alt parametre aktarımı) ·
`editOnlyOwnPosition` · `lazyLoading`.

**Profil bazında (görüntüleme profiline göre) ayarlar** → `../models/service-settings/view-profile-property.md` (key kataloğu) / `view-profile.md`
(override; `ProcessViewProfilePropertySetting`):
- `activeStartActions` (list\<ProcessStepAction id\>) — yeni kayıt oluştururken sunulacak **başlangıç aksiyonları**
  (`childService` Süreç Başlangıcı'na bağlı aksiyonlardan seçilir; **boş = yeni oluşturma yok**). **`addNewEnabled`'in yerini alır.**
- `addFromExistingStatusIds` (list\<Status id\>) — **var olandan ekle**'de hangi durumdaki formlar eklenebilir
  (**boş = pasif**). **`addFromExistingRecordsIsActive`'in yerini alır.**
- `selectableVisible` (bool) — satır **seçim/tik kutusu** bu profilde **görünür** mü (seçim modu profil bazında açılır/kapanır;
  **boş/false = kapalı**). **Eski alan-düzeyi `selectableModeActive`'in yerini alır.**
- _(öneri)_ `selectedEditable` (bool) — `selectableVisible` açıksa, **tikler bu profilde düzenlenebilir** mi (örn. yönetici ✓ / başlatan ✗).
> Form List, **liste seçimi** yapan Combobox'tan farklıdır; **alt-servis kayıtları** bağlar/görüntüler.
> Alt-servisin **görüntülenecek alanları / seçilebilirliği** view-profile ile ayarlanır
> (→ `../models/service-settings/view-profile-property.md`). Süreç Adımı Tetikleme / Değer Atama bu alt-servisle çalışır.
> **Kalan açık ayarlar** (`reOrder`/`editOnlyOwnPosition` profil-bazlılığı) → [`../todo.md`](../todo.md).

### 3.14 — `flowInfo` (Flow Info)
**Akış (süreç) ile ilgili bilgileri** forma getirmek için kullanılır — oluşturulma tarihi (createdDate), oluşturan
kullanıcı (creator user), durum (status) vb. **Salt-okunur** akış metadata'sı.
**Ayarlar:** `flowInfoValue` (hangi akış bilgisi getirilecek) · **`reflectionMode`** — değerin **oluşturma-anı mı (snapshot) güncel mi (live)** gösterileceği: `live` (canlı, **vars.**) · `snapshot` (dondurulmuş). `materialized` **yok** (yalnız parentProperty). → [`../models/enums/reflection-mode.md`](../models/enums/reflection-mode.md). Girdi değildir. _(Kullanıcı bilgisi → §3.16 User Info.)_

### 3.15 — `parentProperty` (Parent Property)
**Düzenlenebilir bir alan değildir.** Bağlı olduğu **parent**'taki (üst süreç/form) hangi alanın forma getirilmesi
isteniyorsa seçim yapılır; parent'ın seçilmiş alanını **`reflectionMode`'a göre** getirir (salt-okunur yansıma):
`snapshot` (kopyala+dondur, **vars.**) · `live` (kopyalamaz, okurken join/referans) · `materialized` (kopya + **`AssociatedInstance`
üzerinden yayılımla tazelenir**). → [`../models/enums/reflection-mode.md`](../models/enums/reflection-mode.md).
`materialized` iken tazelemenin **ne zaman** yapılacağı **`reflectionPropagation`** ile ayarlanır: `async` (arka planda, **vars.**) ·
`sync` (yazma anında, guardrail'li) → [`../models/enums/reflection-propagation.md`](../models/enums/reflection-propagation.md). Yayılım
mekanizması (ayrı bir "link" tablosu **yok**; `AssociatedInstance` + `Property` metadata ile çözülür) →
[`../models/processInstances/reflection-propagation.md`](../models/processInstances/reflection-propagation.md).
**Modelleme (ilişki → §2.5):** `parentPropertyId` (üst alan) · `refPropertyId` (referans alınan alan) · `relatedPropertyIds` · `reflectionMode` · `reflectionPropagation` (yalnız `materialized`).

### 3.16 — `userInfo` (User Info)
**Kullanıcı bilgilerini** forma getirmek için kullanılır — örn. **giriş yapan kullanıcının** adı, e-postası, departmanı,
ünvanı, yöneticisi vb. **Salt-okunur** kullanıcı metadata'sı (Flow Info'nun **kullanıcı karşılığı**).
**Ayarlar:** `userInfoValue` (hangi kullanıcı bilgisi getirilecek) · **`reflectionMode`** — `snapshot` (oluşturma-anı dondurulmuş, **vars.**) · `live` (User'dan güncel). `materialized` **yok** (yalnız parentProperty). → [`../models/enums/reflection-mode.md`](../models/enums/reflection-mode.md). Girdi değildir.

### 3.17 — `groupByTaxReceipt` (Group By Tax Receipt)
Masraf/fiş kalemlerini **vergiye göre gruplandıran** özel alan (masraf süreçleri). Kullanıcı **satır satır** kalem ekler;
her satırda **gider türü** (ExpenseType), **vergi oranı** (Tax) ve **tutar** seçilir/girilir; kalem ve vergi toplamları
otomatik hesaplanır.
**Ayarlar:** `disableTaxAttachmentView` (vergi eki görünümünü gizle) · `isActiveKkegAttachment` (KKEG — kanunen kabul
edilmeyen gider eki aktif).
**Çalışma:** Değer, kalemlerin listesi (gider türü + vergi + tutar) olarak saklanır. Required ise **en az bir** dolu
satır ve **her satırın tamamlanmış** olması zorunludur.

### 3.18 — `keyValueList` (Key-Value List)
**Anahtar-değer** çiftleri listesini gösteren/giren alan. İki sütun (**Key** / **Value**) halinde, kullanıcı **artı**
butonuyla satır ekler; **Value** bir **combobox** ile seçilir.
**Ayarlar:** `addNewEnabled` (yeni satır ekleme) · `deleteEnabled` (satır silme) · `keyDescription` / `valueDescription`
(sütun başlıkları) · `comboBoxItems` (Value seçenek kaynağı) · `keyValueItems` (başlangıç çiftleri).
**Çalışma:** Her satır `key` (metin) + `value` (combobox seçimi) taşır. Required ise en az bir satır ve **tüm satırların
dolu** (key boş değil, value seçili) olması zorunludur.

---

## 4. Açık Kararlar / Sorular
> **Açık sorular tek yerde:** Bu dokümanın açık kararları/soruları, tutarsızlığı önlemek için **yalnız** merkezi
> [`todo.md`](../todo.md) dosyasında toplanır (önceliklendirilmiş tüm-doküman listesi). İlgili maddeler orada `(properties §..)`
> atfıyla bulunur; verilen kararlar bu dokümanın **gövdesinde** anlatılır.

> **Çözülenler (yerel karar log'u):**
- [x] **Form List ayarlarının profil bazında değişmesi** — **KARAR (B2):** profil-bazlı override `ProcessViewProfilePropertySetting {key,value}`
  (→ `../models/service-settings/view-profile-property.md`). Form List: `addNewEnabled`→**`activeStartActions`**, `addFromExistingRecordsIsActive`→**`addFromExistingStatusIds`** (profil); `selectedEnable`→**`selectableVisible`** (profil-bazlı; eski alan-düzeyi `selectableModeActive` **kaldırıldı**).

---

## 5. Notlar / Ham Düşünceler
> _(Buraya ham düşünceler; sonra yukarı işlenir.)_

---

*Oluşturma: 2026-06-26.*
