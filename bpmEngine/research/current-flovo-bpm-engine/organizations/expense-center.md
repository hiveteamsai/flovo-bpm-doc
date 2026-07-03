# Masraf Merkezi (Expense Center / Cost Center)

## Genel Bakış

Masraf merkezleri (Cost Center), organizasyonun maliyet takibi yaptığı muhasebesel birimleri temsil eder. Departmanlar ve kullanıcılar masraf merkezlerine bağlanabilir; masraf/harcama süreçlerinde maliyetlerin doğru birime yansıtılmasını sağlar.

---

## Veri Modeli (AccountCostCenterDto)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Masraf merkezi ID'si |
| `accountId` | String | Hesap ID'si |
| `accountCompanyId` | int | Bağlı şirket ID'si |
| `kod` | String | Masraf merkezi kodu |
| `tanim` | String | Masraf merkezi adı/tanımı |
| `status` | bool | Aktiflik durumu |
| `syncronizationStatus` | bool | Senkronizasyon durumu |
| `accountCompanyDtos` | List\<AccountCompanyDto\> | İlişkili şirketler |
| `accountCostCenterQualifications` | List | Ek nitelik değerleri |

`AccountCostCenterDto`, `IOrganizationParameter` arayüzünü uygular; `companyCode` getter'ı ilişkili şirket kodlarını birleştirir.

---

## Ek Nitelik İlişkisi (AccountCostCenterQualificationDto)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Kayıt ID'si |
| `costCenterId` | int | Masraf merkezi ID'si |
| `qualificationId` | int | Ek nitelik ID'si |
| `value` | String | Ek nitelik değeri |
| `qualification` | AccountAdditionalQualificationDto | Ek nitelik tanımı |

---

## Çalışma Prensibi

1. **Tanımlama:** Kod, tanım ve şirket ile masraf merkezi oluşturulur.
2. **Departman/Kullanıcı Bağlantısı:** Departmanlar (`costCenterId`) ve kullanıcılar (`masrafYeriId`) masraf merkezine bağlanır.
3. **Masraf Süreçleri:** Harcama/masraf formlarında maliyetin hangi merkeze yansıtılacağı belirlenir.
4. **Ek Nitelikler:** Masraf merkezine özel dinamik alanlar tanımlanabilir.

---

## API Endpoint'leri

| Endpoint | HTTP | Açıklama |
|----------|------|----------|
| `GetAccountCostCenters` | POST | Masraf merkezlerini listele |
| `AddAccountCostCenter` | POST | Masraf merkezi ekle |
| `UpdateAccountCostCenter` | POST | Masraf merkezi güncelle |
| `DeleteAccountCostCenter/{id}` | POST | Masraf merkezi sil |

---

## Dosya Yapısı

```
lib/Models/Settings/OrganizationSettings/
├── AccountCostCenterDto.dart
└── GetAccountCostCentersDto.dart

lib/Pages/Settings/OrganizationSettings/ExpenseCenter/
├── ExpenseCenterPage.dart          # Liste sayfası
└── ExpenseCenterDetailPage.dart    # Detay/düzenleme sayfası
```
