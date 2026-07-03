# Ünvanlar (Titles / Professions)

## Genel Bakış

Ünvanlar (kod içinde `Profession` olarak geçer), organizasyondaki çalışan görev/meslek tanımlarını temsil eder. Kullanıcılara atanabilir ve BPM süreçlerinde "ünvana göre yönetici" atamalarında kullanılır.

---

## Veri Modeli (AccountProfessionDto)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Ünvan ID'si |
| `accountId` | String | Hesap ID'si |
| `kod` | String | Ünvan kodu |
| `tanim` | String | Ünvan adı/tanımı |
| `status` | bool | Aktiflik durumu |
| `sycnronizationStatus` | bool | Senkronizasyon durumu |
| `selectedCompanyIds` | List\<String\> | İlişkili şirket ID'leri |
| `accountCompanyDtos` | List\<AccountCompanyDto\> | İlişkili şirketler |
| `accountProfessionAdditionalQualifications` | List | Ünvana özel ek nitelik değerleri |

`AccountProfessionDto`, `IOrganizationParameter` arayüzünü uygular. `companyCode` getter'ı ilişkili şirket kodlarını virgülle birleştirir.

---

## Ek Nitelik İlişkisi (AccountProfessionAdditionalQualificationDto)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Kayıt ID'si |
| `professionId` | int | Ünvan ID'si |
| `qualificationId` | int | Ek nitelik ID'si |
| `value` | String | Ek nitelik değeri |
| `qualification` | AccountAdditionalQualificationDto | Ek nitelik tanımı |

---

## Çalışma Prensibi

1. **Tanımlama:** Ünvanlar kod ve tanım ile oluşturulur.
2. **Şirket İlişkisi:** `selectedCompanyIds` ile bir veya birden fazla şirkete atanır.
3. **Yönetici Ataması:** BPM süreç adımlarındaki "Ünvana Göre Yönetici" (`unvanaGoreYonetici`) kullanıcı tipinde ünvan ID'leri (degree) kullanılarak onay merci belirlenir.
4. **Ek Nitelikler:** Ünvana özel dinamik alanlar tanımlanabilir.

---

## API Endpoint'leri

| Endpoint | HTTP | Açıklama |
|----------|------|----------|
| `GetAccountProfessions` | POST | Ünvanları listele |
| `AddAccountProfession` | POST | Ünvan ekle |
| `UpdateAccountProfession` | POST | Ünvan güncelle |
| `DeleteAccountProfession/{id}` | POST | Ünvan sil |

---

## Dosya Yapısı

```
lib/Models/Settings/OrganizationSettings/
├── AccountProfessionDto.dart
└── GetAccountProfessionsDto.dart

lib/Pages/Settings/OrganizationSettings/Titles/
├── TitlesPage.dart         # Liste sayfası
└── TitleDetailPage.dart    # Detay/düzenleme sayfası
```
