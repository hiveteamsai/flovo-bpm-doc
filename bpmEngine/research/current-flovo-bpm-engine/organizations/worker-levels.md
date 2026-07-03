# Çalışan Seviyeleri (Worker Levels)

## Genel Bakış

Çalışan seviyeleri, organizasyondaki personelin kademe/seviye tanımlarını temsil eder (örn. Uzman, Kıdemli Uzman, Yönetici). Kullanıcılara atanır ve onay hiyerarşisi, yetkilendirme veya raporlama senaryolarında kullanılabilir.

---

## Veri Modeli (AccountWorkerLevelDto)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Seviye ID'si |
| `accountId` | String | Hesap ID'si |
| `code` | String | Seviye kodu |
| `definition` | String | Seviye adı/tanımı |
| `status` | bool | Aktiflik durumu |
| `accountWorkerLevelAdditionalQualifications` | List | Ek nitelik değerleri |

`AccountWorkerLevelDto`, `IOrganizationParameter` arayüzünü uygular.

---

## Ek Nitelik İlişkisi (AccountWorkerLevelAdditionalQualificationDto)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Kayıt ID'si |
| `workerLevelId` | int | Çalışan seviyesi ID'si |
| `qualificationId` | int | Ek nitelik ID'si |
| `value` | String | Ek nitelik değeri |
| `qualification` | AccountAdditionalQualificationDto | Ek nitelik tanımı |

---

## Liste Yanıtı (GetListAccountWorkerLevelDto)

| Alan | Açıklama |
|------|----------|
| `accountWorkerLevelDtos` | Çalışan seviyeleri listesi |
| `accountWorkerLevelAdditionalQualificationDtos` | Ek nitelik değerleri |

---

## Çalışma Prensibi

1. **Tanımlama:** Kod ve tanım ile çalışan seviyesi oluşturulur.
2. **Kullanıcı Ataması:** Kullanıcılar `accountWorkerLevelId` ile bir seviyeye bağlanır.
3. **Ek Nitelikler:** Seviyeye özel dinamik alanlar tanımlanabilir (ek nitelik ilişki türü `WorkerLevels`).

---

## API Endpoint'leri

| Endpoint | HTTP | Açıklama |
|----------|------|----------|
| `GetAccountWorkerLevels` | POST | Seviyeleri listele |
| `AddOrUpdateAccountWorkerLevel` | POST | Seviye ekle/güncelle |
| `DeleteAccountWorkerLevel/{id}` | POST | Seviye sil |

---

## Dosya Yapısı

```
lib/Models/Settings/OrganizationSettings/
└── AccountWorkerLevelDto.dart   # GetListAccountWorkerLevelDto, AccountWorkerLevelDto

lib/Pages/Settings/OrganizationSettings/AccountWorkerLevel/
├── AccountWorkerLevelPage.dart          # Liste sayfası
└── AccountWorkerLevelDetailPage.dart    # Detay/düzenleme sayfası
```
