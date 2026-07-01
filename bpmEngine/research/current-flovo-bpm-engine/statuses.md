# Durumlar (Statuses)

## Genel Bakış

Durumlar, BPM sürecindeki bir kaydın mevcut aşamasını temsil eden etiketlerdir. Her aksiyon tetiklendiğinde kaydın durumu değiştirilebilir. Durumlar görsel gösterim, filtreleme ve raporlama amacıyla kullanılır.

---

## Veri Modeli (ProcessStatusDto)

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `id` | int | Otomatik | Benzersiz durum ID'si |
| `accountId` | String | Evet | Hesap ID'si |
| `serviceId` | int | Evet | Bağlı olduğu servis ID'si |
| `code` | String | Evet | Durum kodu (benzersiz tanımlayıcı) |
| `definition` | String | Evet | Durum tanımı/adı |
| `icon` | String | Evet | FontAwesome ikon kodu |
| `statusType` | String | Evet | Durum tipi (backend'den gelen listeden) |

---

## Durum Tipi (statusType)

Backend'den gelen `statusTypes` listesinden seçilir. Durum tipleri kaydın genel durumunu kategorize eder (örn: beklemede, onaylandı, reddedildi vb.).

---

## Çalışma Prensibi

1. **Tanımlama:** Durumlar servis ayarlarında tanımlanır (kod, tanım, ikon, tip).
2. **Atama:** Süreç adımlarındaki aksiyonlara `changeStatusId` atanarak, aksiyonun tetiklenmesi durumunda kaydın durumu otomatik güncellenir.
3. **Görüntüleme:** Kayıtlar listelenirken durum bilgisi ikon ve renk ile gösterilir.
4. **Filtreleme:** Kullanıcılar kayıtları durumlarına göre filtreleyebilir.

### Durum Akışı Örneği

```
[Taslak] → Onay Aksiyonu → [Onay Bekliyor] → Onayla → [Onaylandı]
                                             → Reddet → [Reddedildi]
```

---

## API Endpoint'leri

| Endpoint | HTTP | Açıklama |
|----------|------|----------|
| `GetProcessStatuses` | POST | Durumları listele |
| `AddOrUpdateProcessStatus` | POST | Durum ekle/güncelle |
| `DeleteProcessStatus/{id}` | POST | Durum sil |

### İstek Header'ları

```
accountId: string
solutionid: string
ServiceId: string
```

---

## Dosya Yapısı

```
lib/Models/Settings/FlvSettings/Status/
├── StatusDto.dart         # ProcessStatusDto modeli
└── GetListStatusDto.dart  # Liste yanıt modeli

lib/Pages/Settings/FlvSettings/Statuses/
├── FlvStatusesSettingsPage.dart      # Liste sayfası
└── FlvStatusSettingsDetailPage.dart  # Detay/düzenleme sayfası
```
