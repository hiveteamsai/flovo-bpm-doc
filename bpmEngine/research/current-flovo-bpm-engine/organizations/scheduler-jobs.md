# Zamanlanmış Görevler (Scheduler Jobs)

## Genel Bakış

Zamanlanmış görevler, arka planda periyodik olarak çalışan otomatik işleri temsil eder. Cron ifadesi ile zamanlaması yapılır; aktif/pasif duruma alınabilir, çalışma geçmişi (log) izlenebilir ve destekliyorsa manuel olarak tetiklenebilir. BPM motorunun zaman tabanlı otomasyonlarını (örn. hatırlatma, zaman aşımı işleme, toplu işlemler) besler.

---

## Veri Modeli (SchedulerJobDto)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Görev ID'si |
| `functionName` | String | Çalıştırılan fonksiyon adı |
| `cronExpression` | String | Zamanlama (cron ifadesi) |
| `description` | String | Görev açıklaması |
| `accountCode` | String | Hesap kodu |
| `category` | String | Görev kategorisi |
| `isEnabled` | bool | Aktif/pasif durumu |
| `lastRunAt` | DateTime | Son çalışma zamanı |
| `lastRunStatus` | String | Son çalışma durumu |
| `createdAt` | DateTime | Oluşturulma zamanı |
| `updatedAt` | DateTime | Güncellenme zamanı |
| `supportsManualInvoke` | bool | Manuel tetiklemeyi destekliyor mu |

> `copyWith({isEnabled})` metodu ile durum değişikliği için kopya üretilir (immutable güncelleme).

---

## Çalışma Geçmişi (SchedulerJobLogDto)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Log ID'si |
| `functionName` | String | Fonksiyon adı |
| `accountCode` | String | Hesap kodu |
| `startTime` | DateTime | Başlangıç zamanı |
| `endTime` | DateTime | Bitiş zamanı |
| `status` | String | Çalışma durumu |
| `errorMessage` | String | Hata mesajı (başarısızsa) |
| `triggeredBy` | String | Tetikleyen (zamanlayıcı / manuel) |
| `triggeredByUserId` | String | Manuel tetikleyen kullanıcı ID'si |
| `durationSeconds` | double | Çalışma süresi (saniye) |

---

## Çalışma Prensibi

1. **Listeleme:** `scheduler-jobs` ile tanımlı görevler listelenir; her görevin cron ifadesi, son çalışma durumu ve kategorisi gösterilir.
2. **Aktif/Pasif:** `scheduler-jobs/{id}/toggle-status` ile görev etkinleştirilir veya devre dışı bırakılır.
3. **Log İzleme:** `scheduler-jobs/{id}/logs` ile görevin çalışma geçmişi (başlangıç/bitiş, durum, süre, hata) görüntülenir.
4. **Manuel Tetikleme:** `supportsManualInvoke: true` olan görevler `scheduler-jobs/{id}/invoke` ile elle çalıştırılabilir.

---

## API Endpoint'leri

| Endpoint | HTTP | Açıklama |
|----------|------|----------|
| `scheduler-jobs` | POST | Görevleri listele |
| `scheduler-jobs/{id}/toggle-status` | POST | Görevi aktif/pasif yap |
| `scheduler-jobs/{id}/logs` | POST | Görev çalışma geçmişini getir |
| `scheduler-jobs/{id}/invoke` | POST | Görevi manuel tetikle |

---

## Dosya Yapısı

```
lib/Models/Settings/OrganizationSettings/
├── SchedulerJobDto.dart
└── SchedulerJobLogDto.dart

lib/Pages/Settings/OrganizationSettings/SchedulerJobs/
├── SchedulerJobsPage.dart        # Liste sayfası
└── SchedulerJobDetailPage.dart   # Detay + log + manuel tetikleme
```
