# Departmanlar (Departments)

## Genel Bakış

Departmanlar, organizasyonun hiyerarşik birim yapısını tanımlar. Her departmanın bir yöneticisi, üst departmanı ve masraf merkezi bağlantısı olabilir. BPM süreçlerinde "departman yöneticisi" tipi kullanıcı atamalarında bu yapı kullanılır.

---

## Veri Modeli (AccountDepartmentDto)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Departman ID'si |
| `accountId` | String | Hesap ID'si |
| `departmanAdi` | String | Departman adı |
| `departmanKodu` | String | Departman kodu |
| `departmanYoneticiUserId` | int | Departman yöneticisi kullanıcı ID'si |
| `ustDepartmentId` | int | Üst departman ID'si (hiyerarşi) |
| `costCenterId` | int | Bağlı masraf merkezi ID'si |
| `status` | bool | Aktiflik durumu |
| `syncronizationStatus` | bool | Senkronizasyon durumu |
| `selectedCompanyIds` | List\<String\> | İlişkili şirket ID'leri |
| `accountDepartmentAdditionalQualifications` | List | Departmana özel ek nitelik değerleri |

### Yardımcı Veriler (initializeFromGetDto ile doldurulur)
- `accountCompanyDtos` — Seçilebilir şirketler
- `accountUserInfoDtos` — Yönetici seçimi için kullanıcılar
- `accountDepartmentDtos` — Üst departman seçimi için departmanlar
- `accountCostCenterDtos` — Masraf merkezi seçimi

---

## Ek Nitelik İlişkisi (AccountDepartmentAdditionalQualificationDto)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Kayıt ID'si |
| `departmentId` | int | Departman ID'si |
| `qualificationId` | int | Ek nitelik ID'si |
| `value` | String | Ek nitelik değeri |
| `qualification` | AccountAdditionalQualificationDto | Ek nitelik tanımı |

---

## Çalışma Prensibi

1. **Hiyerarşi:** `ustDepartmentId` ile departmanlar ağaç yapısında düzenlenir.
2. **Yönetici Ataması:** `departmanYoneticiUserId`, BPM süreç adımlarındaki "Departman Yöneticisi" kullanıcı tipinde onay merci olarak kullanılır.
3. **Masraf Merkezi Bağlantısı:** `costCenterId` ile departman bir masraf merkezine bağlanır.
4. **Çok Şirketlilik:** `selectedCompanyIds` ile departman birden fazla şirkete atanabilir.
5. **Ek Nitelikler:** Departmana özel dinamik alanlar (ek nitelikler) tanımlanabilir.

---

## API Endpoint'leri

| Endpoint | HTTP | Açıklama |
|----------|------|----------|
| `GetAccountDepartments` | POST | Departmanları listele |
| `AddAccountDepartment` | POST | Departman ekle |
| `UpdateAccountDepartment` | POST | Departman güncelle |
| `DeleteAccountDepartment/{id}` | POST | Departman sil |

---

## Dosya Yapısı

```
lib/Models/Settings/OrganizationSettings/
├── AccountDepartmentDto.dart
└── GetAccountDepartmentsDto.dart

lib/Pages/Settings/OrganizationSettings/Departments/
├── DepartmenstPage.dart         # Liste sayfası
└── DepartmentDetailPage.dart    # Detay/düzenleme sayfası
```
