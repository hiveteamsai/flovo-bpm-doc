# Şirketler (Companies)

## Genel Bakış

Şirketler, organizasyonun hukuki/mali tüzel kişiliklerini temsil eder. Organizasyon ayarlarındaki birçok bileşen (departman, ünvan, masraf merkezi, kullanıcı, kredi kartı, ek nitelik) belirli şirketlerle ilişkilendirilir. Bu yapı çok şirketli (multi-company) organizasyonların tek hesap altında yönetilmesini sağlar.

---

## Veri Modeli (AccountCompanyDto)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Şirket ID'si |
| `accountId` | String | Hesap ID'si |
| `kod` | String | Şirket kodu |
| `tanim` | String | Şirket adı/tanımı |
| `isDefaultCompany` | bool | Varsayılan şirket mi |
| `syncronizationStatus` | bool | Harici sistemle senkronizasyon durumu |

`AccountCompanyDto`, `IOrganizationParameter` arayüzünü uygular; böylece iş kurallarındaki veri kaynaklarında (FillDataSource) organizasyon parametresi olarak kullanılabilir.

---

## Çalışma Prensibi

1. **Tanımlama:** Şirketler kod ve tanım ile oluşturulur.
2. **Varsayılan Şirket:** `isDefaultCompany: true` olan şirket, şirket seçimi yapılmadığında varsayılan olarak kullanılır.
3. **İlişkilendirme:** Diğer organizasyon bileşenleri `selectedCompanyIds` / `accountCompanyDtos` alanları ile bir veya birden fazla şirkete bağlanır.
4. **Senkronizasyon:** `syncronizationStatus` harici ERP/muhasebe sistemleriyle senkronize edilen kayıtları işaretler.

---

## API Endpoint'leri

| Endpoint | HTTP | Açıklama |
|----------|------|----------|
| `GetAccountCompanies` | POST | Şirketleri listele |
| `AddAccountCompany` | POST | Şirket ekle |
| `UpdateAccountCompany` | POST | Şirket güncelle |
| `DeleteAccountCompany/{id}` | POST | Şirket sil |

---

## Dosya Yapısı

```
lib/Models/Settings/OrganizationSettings/
└── AccountCompanyDto.dart

lib/Pages/Settings/OrganizationSettings/Companies/
├── CompaniesPage.dart          # Liste sayfası
└── CompaniesDetailPage.dart    # Detay/düzenleme sayfası
```
