# Tatil Günleri (Vacation Days)

## Genel Bakış

Tatil günleri, organizasyonun resmi tatil ve çalışılmayan günlerini tanımlar. Çalışma takvimi ile birlikte iş günü/süre hesaplamalarında dikkate alınır; tam gün veya yarım gün tatil olarak işaretlenebilir. BPM Timer/zaman aşımı hesaplamaları bu günleri atlar.

---

## Veri Modeli (AccountVacationDay)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Tatil ID'si |
| `accountId` | String | Hesap ID'si |
| `startingDate` | DateTime | Başlangıç tarihi |
| `endingDate` | DateTime | Bitiş tarihi |
| `halfDay` | bool | Yarım gün tatil mi |
| `definition` | String | Tatil tanımı/adı |

`AccountVacationDay`, `IOrganizationParameter` arayüzünü uygular.

---

## Çalışma Prensibi

1. **Tanımlama:** Başlangıç ve bitiş tarihi ile tatil aralığı oluşturulur.
2. **Yarım Gün:** `halfDay: true` ise gün hesaplamalarında 0.5 gün olarak sayılır.
3. **Çalışma Takvimi Entegrasyonu:** `WorkingScheduleDto.checkHoliday()` metodu, bir tarihin tatil olup olmadığını kontrol eder:
   - `0` — tatil değil
   - `1` — tam gün tatil
   - `2` — yarım gün tatil
4. **Süre Hesaplama:** İzin/süre hesaplamalarında (`difference` metodu) tatil günleri toplam iş gününden düşülür.

---

## API Endpoint'leri

| Endpoint | HTTP | Açıklama |
|----------|------|----------|
| `accountvacationdaysget` | POST | Tatil günlerini listele |
| `accountvacationdaysadd` | POST | Tatil günü ekle |
| `accountvacationdaysupdate` | POST | Tatil günü güncelle |
| `accountvacationdaysdelete` | POST | Tatil günü sil |

---

## Dosya Yapısı

```
lib/Models/Settings/OrganizationSettings/
└── AccountVacationDay.dart

lib/Pages/Settings/OrganizationSettings/VacationDay/
├── SettingsVacationDayPage.dart          # Liste sayfası
└── SettingsVacationDayDetailPage.dart    # Detay/düzenleme sayfası
```
