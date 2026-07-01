# Aksiyonlar (Actions)

## Genel Bakış

Aksiyonlar, BPM sürecinde kullanıcının bir adımda gerçekleştirebileceği eylemleri tanımlayan yapıdır. Her aksiyon bir olay tetikler ve sürecin bir sonraki adıma geçmesini sağlar. Aksiyonlar servis bazlı tanımlanır ve birden fazla süreç adımında tekrar kullanılabilir.

---

## Veri Modeli (ProcessActionDto)

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `id` | int | Otomatik | Benzersiz aksiyon ID'si |
| `accountId` | String | Evet | Hesap ID'si |
| `serviceId` | int | Evet | Bağlı olduğu servis ID'si |
| `code` | String | Evet | Aksiyon kodu (benzersiz tanımlayıcı) |
| `definition` | String | Evet | Aksiyon tanımı/adı |
| `icon` | String | Evet | FontAwesome ikon kodu |
| `actionType` | String | Evet | Aksiyon tipi (backend'den gelen listeden seçilir) |
| `defaultAction` | bool | Hayır | Varsayılan aksiyon mu |
| `validation` | bool | Hayır | Form validasyonu gerekli mi |
| `reasonRequired` | bool | Hayır | Sebep girişi zorunlu mu |
| `stayOnPage` | bool | Hayır | Aksiyon sonrası sayfada kal |
| `showHistory` | bool | Hayır | Süreç geçmişini göster |
| `actionDisplayType` | ActionDisplayType | Hayır | Görüntüleme tipi |

---

## Aksiyon Görüntüleme Tipleri (ActionDisplayType)

Aksiyonun nerede ve nasıl görüntüleneceğini belirler:

| Index | Enum | Açıklama |
|-------|------|----------|
| 0 | `invisible` | Görünmez (gizli aksiyon) |
| 1 | `everywhere` | Her yerde görünsün |
| 2 | `onlyFormDetail` | Sadece form detayında |
| 3 | `onlyFastApprove` | Sadece hızlı onay ekranında |

---

## Aksiyon Tipi (actionType)

Aksiyonun stilini belirleyen renk/görünüm sınıfıdır. Backend'den gelen `processActionTypes` listesinden seçilir. Tipik değerler:

- `success` - Başarılı/Onay (yeşil)
- `danger` - Tehlikeli/Red (kırmızı)
- `warning` - Uyarı (sarı)
- `info` - Bilgi (mavi)
- `primary` - Birincil (mor/mavi)

---

## Süreç Adımında Aksiyon Kullanımı

Aksiyonlar `ProcessStepActionDto` aracılığıyla süreç adımlarına bağlanır. Bu bağlama sırasında ek özellikler tanımlanır:

| Alan | Tip | Açıklama |
|------|-----|----------|
| `targetProcessStepId` | int | Aksiyon sonrası gidilecek adım |
| `changeStatusId` | int | Aksiyon sonrası atanacak durum |
| `action` | String | Aksiyon davranışı (fire-event, new-instance vb.) |
| `authorizationLevel` | int | Yetki seviyesi |
| `environmentRestriction` | String | Ortam kısıtlaması |
| `showInHistory` | bool | Süreç geçmişinde gösterilsin mi |
| `actionDisplayAuthorizedUserGroupId` | int | Aksiyonu görebilecek kullanıcı grubu |

### Aksiyon Davranışları (action field)

| Değer | Açıklama |
|-------|----------|
| `fire-event` | Standart olay tetikleme (varsayılan) |
| `new-instance` | Aynı serviste yeni kayıt oluştur |
| `new-instance-referenced` | Referanslı yeni kayıt oluştur |
| `new-instance-other` | Başka serviste yeni kayıt oluştur |
| `take-photo` | Kamera ile fotoğraf çek |
| `select-file` | Dosya seçici aç |
| `take-barcode` | Barkod okuyucu aç |
| `manuel-barcode-input` | Manuel barkod girişi |
| `excel-export` | Excel'e aktar |
| `expform-new-instance-other` | Masraf formu - başka serviste kayıt |
| `expform-take-photo` | Masraf formu - fotoğraf çek |
| `expform-select-file` | Masraf formu - dosya seç |
| `expform-add-exist-expense` | Masraf formu - mevcut masraf ekle |
| `add-test-receipt` | Test fişi ekle |

---

## Çalışma Prensibi

1. **Tanımlama:** Aksiyonlar servis ayarlarından bağımsız olarak tanımlanır (kod, tanım, ikon, tip).
2. **Bağlama:** Tanımlanan aksiyonlar süreç adımlarına eklenir ve hedef adım/durum bilgisi atanır.
3. **Çalışma Zamanı:** Kullanıcı form üzerinde aksiyona tıkladığında:
   - `validation: true` ise form validasyonu yapılır
   - `reasonRequired: true` ise sebep giriş ekranı açılır
   - `showHistory: true` ise süreç geçmişi gösterilir
   - Aksiyon tetiklenir ve kayıt `targetProcessStepId` ile belirtilen adıma ilerler
   - `changeStatusId` varsa kaydın durumu güncellenir
4. **Sayfada Kalma:** `stayOnPage: true` ise aksiyon sonrası kullanıcı aynı sayfada kalır.

---

## API Endpoint'leri

| Endpoint | HTTP | Açıklama |
|----------|------|----------|
| `GetProcessActions` | POST | Aksiyonları listele |
| `AddOrUpdateProcessAction` | POST | Aksiyon ekle/güncelle |
| `DeleteProcessAction/{id}` | POST | Aksiyon sil |

### İstek Header'ları

```
accountId: string
solutionid: string
ServiceId: string
```

---

## Dosya Yapısı

```
lib/Models/Settings/FlvSettings/Action/
├── ActionDto.dart           # ProcessActionDto modeli
├── ActionDisplayType.dart   # Görüntüleme tipi enum'u
└── GetListActionDto.dart    # Liste yanıt modeli

lib/Pages/Settings/FlvSettings/Actions/
├── FlvActionsSettingsPage.dart       # Liste sayfası
└── FlvActionSettingDetailPage.dart   # Detay/düzenleme sayfası
```
