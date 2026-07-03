# Ek Nitelikler (Additional Qualifications)

## Genel Bakış

Ek nitelikler, standart organizasyon alanlarının dışında, organizasyon varlıklarına (kullanıcı, departman, ünvan, masraf merkezi, çalışan seviyesi) eklenebilen özel/dinamik alanlardır. Böylece her organizasyon kendi ihtiyacına göre ek veri alanları tanımlayabilir (örn. "SGK No", "Personel Sicil No", "Bölge").

---

## Veri Modeli (AccountAdditionalQualificationDto)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Ek nitelik ID'si |
| `accountId` | String | Hesap ID'si |
| `code` | String | Nitelik kodu |
| `definition` | String | Nitelik tanımı |
| `status` | bool | Aktiflik durumu |
| `accountCompanyIds` | List\<String\> | İlişkili şirket ID'leri |
| `accountAdditionalQualificationRelations` | List | İlişkilendirildiği varlık türleri |

---

## İlişki Ayarı (AccountAdditionalQualificationRelationDto)

Bir ek niteliğin hangi organizasyon varlıklarına uygulanacağını belirler.

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Kayıt ID'si |
| `accountAdditionalQualificationId` | int | Ek nitelik ID'si |
| `relationalSetting` | RelationalSetting | İlişkilendirilen varlık türü |
| `required` | bool | Bu varlık için zorunlu mu |

### İlişki Türleri (RelationalSetting)

| Index | Enum | Açıklama |
|-------|------|----------|
| 0 | `Users` | Kullanıcılar |
| 1 | `Departments` | Departmanlar |
| 2 | `Professions` | Ünvanlar |
| 3 | `CostCenters` | Masraf merkezleri |
| 4 | `WorkerLevels` | Çalışan seviyeleri |

---

## Varlık Değer Modeli (UserAdditionalQualificationDto)

Bir organizasyon varlığına atanmış ek nitelik değerini tutar. Her varlık türünün kendi değer DTO'su vardır (departman: `AccountDepartmentAdditionalQualificationDto`, ünvan: `AccountProfessionAdditionalQualificationDto`, masraf merkezi: `AccountCostCenterQualificationDto`, çalışan seviyesi: `AccountWorkerLevelAdditionalQualificationDto`).

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Kayıt ID'si |
| `userId` | int | Varlık ID'si |
| `accountUserAdditionalQualificationId` | int | Ek nitelik tanım ID'si |
| `value` | String | Atanan değer |

---

## Çalışma Prensibi

1. **Tanımlama:** Ek nitelik kod, tanım ve durum ile oluşturulur.
2. **İlişkilendirme:** `relationalSetting` ile niteliğin hangi varlık türlerine (kullanıcı/departman/ünvan/masraf merkezi/çalışan seviyesi) uygulanacağı seçilir. Her ilişki için `required` (zorunluluk) ayarlanabilir (`RelationalSettingDetailPage`).
3. **Değer Atama:** İlgili varlık düzenlenirken (örn. bir kullanıcı), tanımlı ek nitelikler için değer girilir.
4. **Şirket Kapsamı:** `accountCompanyIds` ile nitelik belirli şirketlerle sınırlandırılabilir.

---

## API Endpoint'leri

| Endpoint | HTTP | Açıklama |
|----------|------|----------|
| `GetAccountAdditionalQualifications` | POST | Ek nitelikleri listele |
| `AddOrUpdateAccountAdditionalQualification` | POST | Ek nitelik ekle/güncelle |
| `DeleteAccountAdditionalQualification/{id}` | POST | Ek nitelik sil |

---

## Dosya Yapısı

```
lib/Models/Settings/OrganizationSettings/
└── AccountUserAdditionalQualificationDto.dart  # Tüm ek nitelik modelleri + RelationalSetting enum

lib/Pages/Settings/OrganizationSettings/AdditionalQualification/
├── AdditionalQualificationPage.dart          # Liste sayfası
├── AdditionalQualificationDetailPage.dart    # Detay sayfası
└── RelationalSettingDetailPage.dart          # İlişki ayarı sayfası
```
