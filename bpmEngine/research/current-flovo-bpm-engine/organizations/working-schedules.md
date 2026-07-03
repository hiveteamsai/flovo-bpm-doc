# Çalışma Takvimleri (Working Schedules)

## Genel Bakış

Çalışma takvimleri, organizasyonun haftalık çalışma saatlerini tanımlar. Haftanın 7 günü için ayrı ayrı aktiflik ve iki adede kadar çalışma periyodu (örn. öğle arası ile bölünmüş mesai) belirlenir. BPM süreçlerindeki **Timer / zaman aşımı** hesaplamalarında ("çalışma takvimine göre") ve izin/gün hesaplamalarında kullanılır.

---

## Veri Modeli (WorkingScheduleDto)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Takvim ID'si |
| `code` | String | Takvim kodu |
| `definition` | String | Takvim adı/tanımı |
| `explanation` | String | Açıklama |
| `isDefaultSchedule` | bool | Varsayılan takvim mi |
| `dayOfTheWeeks` | List\<WorkingScheduleDayOfTheWeek\> | Haftanın günleri (7 eleman) |

`WorkingScheduleDto`, `IOrganizationParameter` arayüzünü uygular.

---

## Gün Modeli (WorkingScheduleDayOfTheWeek)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Kayıt ID'si |
| `active` | bool | O gün çalışılıyor mu |
| `day` | int | Gün numarası (1=Pazartesi ... 7=Pazar) |
| `period1Start` | DateTime | 1. periyot başlangıç saati |
| `period1End` | DateTime | 1. periyot bitiş saati |
| `period2Start` | DateTime | 2. periyot başlangıç saati (opsiyonel) |
| `period2End` | DateTime | 2. periyot bitiş saati (opsiyonel) |

---

## Hesaplama Mantığı (Model İçi Metodlar)

Model, çalışma saatlerine dayalı zaman hesaplamaları için zengin yardımcı metodlar içerir:

| Metod | Açıklama |
|-------|----------|
| `isInDay(date)` | Verilen tarihin çalışma günü olup olmadığı |
| `getDayOfTheWeekWithDate(date)` | Tarihe karşılık gelen gün tanımı |
| `getWorkDayHour(date, isStart)` | O günün mesai başlangıç/bitiş saati |
| `addDay(day, date)` | Belirtilen sayıda çalışma günü ekler (tatilleri atlar) |
| `findNextWorkDay(dateTime)` | Bir sonraki çalışma zamanını bulur |
| `differenceinDay(...)` | Gün içindeki çalışılan saat farkı |
| `difference(start, end, vacationDays)` | İki tarih arası toplam çalışma günü (tatiller düşülür) |
| `checkHoliday(date, vacationDays)` | Tatil kontrolü (0=değil, 1=tam, 2=yarım gün) |

Bu metodlar, BPM Timer adımlarının "çalışma takvimine göre" (`WorkStyle.calismaTakvimineGore`) zaman aşımı hesaplamalarında kullanılır.

---

## Çalışma Prensibi

1. **Tanımlama:** Takvim kod, tanım ve açıklama ile oluşturulur.
2. **Gün Ayarları:** Haftanın 7 günü için aktiflik ve 1-2 çalışma periyodu tanımlanır.
3. **Varsayılan Takvim:** `isDefaultSchedule: true` olan takvim, kullanıcıya özel takvim atanmadığında kullanılır.
4. **Kullanıcı Ataması:** Kullanıcılar `selectedWorkingScheduleId` ile bir takvime bağlanır. `getWorkingScheduleWithUserId` endpoint'i ile kullanıcının takvimi çekilebilir.
5. **BPM Entegrasyonu:** Timer adımlarında ve tatil günleriyle birlikte iş günü/saat hesaplamalarında kullanılır.

---

## API Endpoint'leri

| Endpoint | HTTP | Açıklama |
|----------|------|----------|
| `GetWorkingSchedule` | POST | Takvimleri listele |
| `AddOrUpdateWorkingSchedule` | POST | Takvim ekle/güncelle |
| `DeleteWorkingSchedule/{id}` | POST | Takvim sil |
| `getWorkingScheduleWithUserID/{userId}` | POST | Kullanıcının takvimini getir |

---

## Dosya Yapısı

```
lib/Models/Settings/OrganizationSettings/
└── WorkingScheduleDto.dart   # GetWorkingScheduleDto, WorkingScheduleDto, WorkingScheduleDayOfTheWeek

lib/Pages/Settings/OrganizationSettings/WorkingSchedule/
├── SettingsWorkingSchedulePage.dart          # Liste sayfası
└── SettingsWorkingScheduleDetailPage.dart    # Detay/düzenleme sayfası
```
