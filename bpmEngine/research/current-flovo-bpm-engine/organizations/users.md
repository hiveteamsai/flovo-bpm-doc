# Kullanıcılar (Users)

## Genel Bakış

Kullanıcılar, organizasyondaki kişileri temsil eder. Her kullanıcı bir departmana, ünvana, yöneticiye, masraf yerine ve çalışma takvimine bağlanabilir. BPM süreçlerinde onay merci olarak kullanıcılar atanır. Kullanıcının yetki seviyesi (`authorizationLevel`) hangi aksiyonları görebileceğini ve ayarlara erişimini belirler.

---

## Veri Modeli (AccountUserDto)

### Temel Bilgiler

| Alan | Tip | Açıklama |
|------|-----|----------|
| `userId` | int | Kullanıcı ID'si |
| `userName` | String | Kullanıcı adı (giriş) |
| `accountId` | String | Hesap ID'si |
| `kod` | String | Kullanıcı kodu |
| `firstName` | String | Ad |
| `lastName` | String | Soyad |
| `fullName` | String (getter) | Ad + Soyad birleşimi |
| `profilePhoto` | String | Profil fotoğrafı URL'si |
| `status` | bool | Aktiflik durumu |
| `authorizationLevel` | int | Yetki seviyesi |
| `employmentStartDate` | DateTime | İşe başlama tarihi |

### Organizasyon Bağlantıları

| Alan | Tip | Açıklama |
|------|-----|----------|
| `departmantId` | String | Departman ID'si |
| `unvanId` | String | Ünvan ID'si |
| `yoneticiUserId` | String | Yönetici kullanıcı ID'si |
| `masrafYeriId` | String | Masraf merkezi ID'si |
| `accountWorkerLevelId` | int | Çalışan seviyesi ID'si |
| `selectedWorkingScheduleId` | int | Çalışma takvimi ID'si |
| `selectedCompanyIds` | List\<String\> | İlişkili şirket ID'leri |
| `selectedStaff` | AccountStaffDto | Seçili kadro |
| `selectedPosition` | AccountPositionDto | Seçili pozisyon |
| `syncronizationStatus` | bool | Senkronizasyon durumu |

### Sosyal Medya
`facebook`, `instagram`, `linkedin`, `twitter` — kullanıcı sosyal medya bağlantıları.

### İlişkili Koleksiyonlar

| Alan | Tip | Açıklama |
|------|-----|----------|
| `userExpenseLimits` | List\<UserExpenseLimit\> | Masraf tipi bazlı harcama limitleri |
| `userSolutions` | List\<UserSolutionDto\> | Kullanıcının erişebildiği çözümler |
| `userAccountAdditionalQualifications` | List\<UserAdditionalQualificationDto\> | Ek nitelik değerleri |
| `userAccountCreditCardDtos` | List\<AccountCreditCardDto\> | Kullanıcıya atanmış kredi kartları |

---

## Alt Modeller

### UserExpenseLimit (Harcama Limiti)
| Alan | Tip | Açıklama |
|------|-----|----------|
| `expenseType` | AccountExpenseTypeDto | Masraf tipi |
| `expenseCode` | String | Masraf kodu |
| `limit` | double | Limit tutarı |

### UserSolutionDto (Çözüm Erişimi)
| Alan | Tip | Açıklama |
|------|-----|----------|
| `userId` | int | Kullanıcı ID'si |
| `solutionId` | String | Çözüm ID'si |
| `name` | String | Çözüm adı |

---

## Çalışma Prensibi

1. **Kullanıcı Tanımlama:** Ad, soyad, kullanıcı adı, kod ve organizasyon bağlantıları ile oluşturulur.
2. **Hiyerarşi:** `yoneticiUserId` ile yönetici zinciri kurulur; BPM'de "Kullanıcının Yöneticisi" ve "Yönetici Zinciri" atamalarında kullanılır.
3. **Yetki Seviyesi:** `authorizationLevel`, aksiyon görünürlüğü ve ayar sayfalarına erişimi belirler (örn. çeviri ayarları 300+ seviye gerektirir).
4. **Harcama Limitleri:** Masraf tipi bazında kullanıcıya harcama limiti tanımlanabilir (`UserExpenseLimitDetailPage`).
5. **Çözüm Erişimi:** Kullanıcının hangi çözümlere erişebileceği `userSolutions` ile yönetilir.
6. **Aktivasyon:** Kullanıcı aktif/pasif duruma alınabilir.

---

## API Endpoint'leri

| Endpoint | HTTP | Açıklama |
|----------|------|----------|
| `GetAccountUsers` | POST | Kullanıcıları listele |
| `AddAccountUser` | POST | Kullanıcı ekle |
| `UpdateAccountUser` | POST | Kullanıcı güncelle |
| `ActivateAccountUser/{userId}` | POST | Kullanıcı aktive et/pasifleştir |

---

## Dosya Yapısı

```
lib/Models/Settings/OrganizationSettings/
├── AccountUserDto.dart
├── AccountUserInfoDto.dart
├── AccountExpenseLimitDto.dart
└── GetAccountUsersDto.dart

lib/Pages/Settings/OrganizationSettings/Users/
├── SettingsUsersPage.dart              # Liste sayfası
├── SettingsUserDetailPage.dart         # Detay/düzenleme sayfası
└── UserExpenseLimitDetailPage.dart     # Harcama limiti sayfası
```
