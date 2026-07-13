# Enum — controlTypeId (Property / kontrol tipi)

> **Kullanan model:** [`property.md`](../service-settings/property.md) (`controlTypeId`)
> **Amaç:** Bir form alanının **hangi kontrol/görsel eleman** olarak render edileceğini ve hangi tipe-özel alanların geçerli olacağını belirler.
> **Tam tipe-özel alan kataloğu:** → [`../../service-settings/properties.md`](../../service-settings/properties.md) §3.

## Değerler
| Kod | Anlam (görünen ad) | Ne için |
|---|---|---|
| `textbox` | Textbox — metin girişi. | Serbest metin. |
| `numericTextbox` | Numeric Textbox — sayısal giriş. | Sayı/ondalık değerler. |
| `combobox` | Combobox — açılır seçim listesi. | Statik/dinamik seçenekten seçim. |
| `datepicker` | Datepicker — tarih seçici. | Tarih girişi. |
| `timePicker` | Time Picker — saat seçici. | Saat girişi. |
| `checkbox` | Checkbox — iki durumlu kutu. | Evet/hayır (bool). |
| `radiobuttonList` | Radiobutton List — tekli seçim listesi. | Seçeneklerden birini seçmek. |
| `file` | File — dosya yükleme. | Ek/dosya iliştirme. |
| `text` | Text (statik) — salt metin gösterimi. | Etiket/açıklama (giriş değil). |
| `barcode` | Barcode — barkod/QR giriş-tarama. | Tarayarak değer girmek. |
| `phone` | Phone — telefon girişi (maskeli). | Telefon numarası. |
| `mapViewer` | Map Viewer — harita/konum. | Konum seçimi/görüntüleme. |
| `formList` | Form List — alt servis kayıt listesi. | İç içe (child) kayıt yönetimi. |
| `flowInfo` | Flow Info — salt-okunur akış metadata. | Akış bilgisi göstermek. |
| `parentProperty` | Parent Property — üst/referans alan (salt-okunur). | Başka alandan türetilen gösterim. |
| `userInfo` | User Info — salt-okunur kullanıcı metadata. | Kullanıcı bilgisi göstermek. |
| `groupByTaxReceipt` | Group By Tax Receipt — vergi fişi gruplama. | Fiş bazlı gruplu giriş. |
| `keyValueList` | Key-Value List — anahtar-değer listesi. | Dinamik anahtar/değer çiftleri. |
| `imageAreaSelector` | Image Area Selector — görsel üzerinde alan/nokta seçimi. | Görsel üzerinde işaretleme. |

## Notlar
- Tam 19 kontrol tipinin tipe-özel alanları ve davranışları → [`../../service-settings/properties.md`](../../service-settings/properties.md) §3.
- `Property.propertyType` bu enum ile aynı kavramı ifade eder.
- Fiziksel depolama `controlTypeId` (int) üzerindendir; buradaki **kod** kanonik metin karşılığıdır (görünen ad "Anlam" sütununda).
- Kodlar **camelCase** olarak normalize edildi (v0.7).

*Oluşturma: 2026-07-10.*
