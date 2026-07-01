# Görüntüleme Profilleri (View Profiles)

## Genel Bakış

Görüntüleme profilleri, bir formun farklı süreç adımlarında nasıl görüntüleneceğini kontrol eden yapıdır. Her profil, hangi alanların gösterileceğini, hangilerinin düzenlenebilir olacağını ve hangilerinin zorunlu olacağını belirler. Böylece aynı form farklı kullanıcılara farklı şekillerde sunulabilir.

---

## Veri Modeli (ProcessViewProfileDto)

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `id` | int | Otomatik | Profil ID'si |
| `accountId` | String | Evet | Hesap ID'si |
| `serviceId` | int | Evet | Bağlı servis ID'si |
| `code` | String | Evet | Profil kodu |
| `definition` | String | Evet | Profil tanımı |
| `isDefault` | bool | Hayır | Varsayılan profil mi |
| `showOnDataGrid` | bool | Hayır | Rapor olarak yayınla |
| `processViewProfileFields` | List | Hayır | Profildeki alan tanımları |
| `processViewProfileProperty` | Object | Hayır | Rapor özellikleri |

---

## Profil Alan Yapısı (ProcessViewProfileFieldDto)

Her profil, formun alanlarını ayrı ayrı yapılandırır:

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Alan kaydı ID'si |
| `viewProfileId` | int | Bağlı profil ID'si |
| `fieldId` | int | Form alanı (property) ID'si |
| `visible` | bool | Alan görünür mü |
| `enabled` | bool | Alan düzenlenebilir mi |
| `required` | bool | Alan zorunlu mu |
| `order` | int | Sıralama (sürükle-bırak ile değiştirilebilir) |
| `showOnListingPage` | bool | Liste sayfasında gösterilsin mi |
| `subFieldsViewProfiles` | String | Alt alanlar görüntüleme profili |
| `deletableStatuses` | String | Silinebilir durumlar |
| `cardViewProfile` | String | Kart görünümü profili |
| `childFieldsProcessViewProfileFieldDtos` | List | Alt alan profilleri |

---

## Rapor Özellikleri (ProcessViewProfileProperty)

Profil rapor olarak yayınlandığında ek özellikler:

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Kayıt ID'si |
| `viewProfileId` | int | Profil ID'si |
| `isUserReport` | bool | Kullanıcı raporu mu |
| `userGroupId` | int | Erişim yetkisi olan kullanıcı grubu |
| `showAsManager` | bool | Yönetici olarak göster |
| `showToEveryone` | bool | Herkese göster |

---

## Çalışma Prensibi

1. **Tanımlama:** Her servis için bir veya birden fazla görüntüleme profili tanımlanır.
2. **Varsayılan Profil:** `isDefault: true` olan profil, süreç adımında profil belirtilmediğinde kullanılır. `code` değeri "default" olan profil özel anlam taşır (liste sayfasında göster seçeneği aktif olur).
3. **Adıma Atama:** Süreç adımlarında `processViewProfileId` alanı ile kullanıcının göreceği profil belirlenir.
4. **Çalışma Zamanı:** Form açıldığında:
   - Aktif süreç adımının profili yüklenir
   - `visible: false` olan alanlar gizlenir
   - `enabled: false` olan alanlar salt okunur olur
   - `required: true` olan alanlar zorunlu hale gelir
   - Alanlar `order` değerine göre sıralanır
5. **Alan Kopyalama:** Mevcut bir profilden alan yapılandırması kopyalanabilir.
6. **Rapor Yayınlama:** `showOnDataGrid: true` ayarı ile profil bir rapor haline gelir ve belirli kullanıcı gruplarına gösterilebilir.

---

## WorkRule Entegrasyonu

İş kuralları (WorkRule) ile birlikte çalışır:
- `ActionType.ChangeViewProfile` ile çalışma zamanında profil değiştirilebilir
- WorkRule koşullarında `WorkRuleConditionCompareType.ViewProfile` ile aktif profil kontrol edilebilir
- WorkRule'lar `activeViewProfiles` listesi ile sadece belirli profillerde çalışacak şekilde kısıtlanabilir

---

## API Endpoint'leri

| Endpoint | HTTP | Açıklama |
|----------|------|----------|
| `GetProcessViewProfiles` | POST | Profilleri listele |
| `AddOrUpdateProcessViewProfile` | POST | Profil ekle/güncelle |
| `DeleteProcessViewProfile/{id}` | POST | Profil sil |

### İstek Header'ları

```
accountId: string
solutionid: string
ServiceId: string
```

---

## Dosya Yapısı

```
lib/Models/Settings/FlvSettings/ViewProfile/
└── ProcessViewProfileDto.dart  # Tüm modeller (GetProcessViewProfileDto, ProcessViewProfileDto, ProcessViewProfileFieldDto, ProcessViewProfileProperty)

lib/Pages/Settings/FlvSettings/ViewProfile/
├── ViewProfileSettingsPage.dart              # Liste sayfası
├── ViewProfileSettingsDetailPage.dart        # Detay sayfası (mobil)
├── ViewProfileSettingsDetailWebPage.dart     # Detay sayfası (web/geniş ekran)
├── ViewProfileFieldSettingsDetailPage.dart   # Alan detay ayarları
└── ViewProfileRaporSettings.dart             # Rapor özellikleri ayarları
```
