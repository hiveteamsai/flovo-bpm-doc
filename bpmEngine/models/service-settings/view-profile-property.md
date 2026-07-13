# Model — ProcessViewProfileProperty (profil alan yapılandırması)

> **Durum:** 🟡 TASLAK (ilk çıkarım — gözden geçirilecek)
> **Amaç:** Bir görüntüleme profilinde **tek bir alanın** nasıl görüneceği: görünür/düzenlenebilir/zorunlu + sıra.
> **Davranış/kullanım:** → `../../service-settings/view-profile.md` §2

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Kayıt ID'si. |
| `viewProfileId` | int | FK → ProcessViewProfile.id | Bağlı profil. |
| `propertyId` | int | FK → Property.id | Yapılandırılan form alanı. |
| `visible` | bool | — | Alan görünür mü. |
| `enabled` | bool | — | Alan düzenlenebilir mi (salt-okunur değil). |
| `required` | bool | — | Alan zorunlu mu. |
| `order` | int | — | Sıralama (sürükle-bırak). |

> **Neden burada?** `visible`/`enabled`/`required` alanın kendisinde (`Property`) değil, **profilde** tutulur:
> *alan = ne olduğu*, *profil = nerede nasıl göründüğü*.

## İlişkiler
- **N – 1** → `ProcessViewProfile` (`viewProfileId`), `Property` (`propertyId`).
- **1 – N** ← `ProcessViewProfilePropertySetting` (`viewProfilePropertyId`) — **profil-bazlı tipe-özel override** (→ `view-profile-property-setting.md`).

## Tipe-özel override key'leri (`propertyType`'a göre)
Bir alanın **tipe-özel** görünüm/davranış ayarları **profil bazında** `ProcessViewProfilePropertySetting` (key-value)
ile tutulur. `viewProfilePropertyId` altındaki kayıtlar bir **dictionary** oluşturur; ilgili `Property`'nin
**`propertyType` (`controlTypeId`)**'sine göre hangi key'lerin geçerli olduğu belirlenir. Belirtilmeyen key →
`Property` varsayılanı. _(Eski uygulamada bu ayarlar **Property**'de —profil-bağımsız— yönetiliyordu; **görüntüleme
bazında** olması gerektiği için buraya taşındı.)_

### `formList` (Form List)
| key | value tipi | Ne yapar |
|---|---|---|
| `activeStartActions` | list\<int\> (ProcessStepAction id) | Yeni kayıt oluştururken **hangi başlangıç aksiyonlarının** sunulacağı. `childService`'in **Süreç Başlangıcı** adımına bağlı `ProcessStepAction`'lardan seçilenler aktif olur. **Boş liste = yeni oluşturma yok.** _(`addNewEnabled` bool'unun yerini alır.)_ |
| `addFromExistingStatusIds` | list\<int\> (Status id) | **Var olandan ekle**: hangi **durumdaki** formlar bu listeye eklenebilir. **Boş liste = "var olandan ekle" pasif.** _(`addFromExistingRecordsIsActive` bool'unun yerini alır.)_ |
| `selectableVisible` | bool | Satır **seçim/tik kutusunun** bu profilde **görünür** olup olmadığı. **Boş/false = seçim modu kapalı.** _(Eski **alan-düzeyi** `Property.selectableModeActive`'in yerini alır — artık **profil bazında**.)_ |
| `selectedEditable` _(öneri)_ | bool | `selectableVisible` açıksa, tikler bu profilde **değiştirilebilir** mi (örn. yönetici ✓, süreç başlatan ✗). |

> **Not:** Satır **seçim/tik** görünürlüğü (`selectableVisible`) ve **düzenlenebilirliği** (`selectedEditable`) artık
> **profil bazında** (görüntüleme profili) yönetilir; eski **alan-düzeyi** `selectableModeActive` **kaldırıldı**.

> Diğer Form List ayarları (`reOrder`, `editOnlyOwnPosition`) da profil-bazlı yönetilecekse aynı katalogla eklenir
> (şimdilik `Property`'de → `../../todo.md`). Diğer alan tipleri (`combobox`, `file`, `keyValueList`…) için override key'leri
> **ihtiyaç doğdukça** buraya eklenir.

## Notlar / açık noktalar
- **Karar (B2):** tipe-özel, profil-bazlı ayarlar `ProcessViewProfilePropertySetting {key, value}` ile **override**
  edilir; `visible/enabled/required/order` genel kolonları birinci sınıf kalır. Runtime'da etkin ayar =
  *override varsa o, yoksa `Property` varsayılanı*.

*Oluşturma: 2026-07-02.*
