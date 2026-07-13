# Pozisyonlar ve Kadrolar (Positions & Staff)

## Genel Bakış

Pozisyonlar ve kadrolar, organizasyonun **organizasyonel yapı taşlarını** tanımlar. Bir **pozisyon**, belirli bir şirkete bağlı organizasyonel bir görev/yer tanımıdır; **kadro** ise o pozisyon altındaki somut bir personel slotudur ve isteğe bağlı olarak bir kullanıcıya atanabilir.

Ünvanlardan (`Profession`) farklı olarak pozisyon/kadro yapısı, organizasyon şemasındaki **fiili görev yerlerini** ve bu yerlere atanan personeli yönetmek için kullanılır. Kullanıcı kaydında pozisyon ve kadro bilgisi, kadro ataması üzerinden otomatik olarak yansır.

---

## Veri Modeli

### Pozisyon (AccountPositionDto)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Pozisyon ID'si |
| `accountId` | String | Hesap ID'si |
| `kod` | String | Pozisyon kodu |
| `tanim` | String | Pozisyon adı/tanımı |
| `selectedCompanyId` | int | Bağlı şirket ID'si |
| `status` | bool | Aktiflik durumu |
| `sycnronizationStatus` | bool | Harici sistemle senkronizasyon durumu |
| `accountStaffs` | List\<AccountStaffDto\> | Pozisyona bağlı kadrolar |

`AccountPositionDto`, `IOrganizationParameter` arayüzünü uygular; iş kurallarındaki veri kaynaklarında (FillDataSource) organizasyon parametresi olarak kullanılabilir.

### Kadro (AccountStaffDto)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Kadro ID'si |
| `accountPositionId` | int | Bağlı pozisyon ID'si |
| `kod` | String | Kadro kodu |
| `tanim` | String | Kadro adı/tanımı |
| `userId` | int | Atanan kullanıcı ID'si |
| `status` | bool | Aktiflik durumu |
| `sycnronizationStatus` | bool | Senkronizasyon durumu |

---

## Liste Yanıtı (GetAccountPositionsDto)

| Alan | Açıklama |
|------|----------|
| `accountPositionDtos` | Pozisyon listesi (kadrolar dahil) |
| `accountCompanyDtos` | Şirket seçimi için şirketler |

---

## Kullanıcı İlişkisi

Kullanıcı modelinde (`AccountUserDto`) pozisyon ve kadro alanları bulunur:

| Alan | Tip | Açıklama |
|------|-----|----------|
| `selectedPosition` | AccountPositionDto | Kullanıcının bağlı olduğu pozisyon |
| `selectedStaff` | AccountStaffDto | Kullanıcının atandığı kadro |

Bu alanlar kullanıcı detay sayfasında **salt okunur** gösterilir; doğrudan düzenlenemez. Kullanıcının pozisyon/kadro bilgisi, kadro tanımında `userId` atanmasıyla belirlenir.

---

## Çalışma Prensibi

### Pozisyon Yönetimi

1. **Oluşturma:** Kod, tanım ve şirket zorunludur. Yeni pozisyon oluşturulurken kullanıcının varsayılan şirketi (`defaultCompanyId`) otomatik seçilir.
2. **Şirket Bağlantısı:** Her pozisyon tek bir şirkete (`selectedCompanyId`) bağlanır.
3. **Durum ve Senkronizasyon:** Pozisyon aktif/pasif yapılabilir; `sycnronizationStatus` harici sistem entegrasyonunu işaretler.
4. **Kayıt:** Pozisyon ve altındaki kadrolar birlikte `AddOrUpdateAccountPosition` ile kaydedilir.

### Kadro Yönetimi

1. **Tanımlama:** Kadro, bir pozisyonun detay sayfasından eklenir. Kod, tanım ve kullanıcı ataması zorunludur.
2. **Kullanıcı Ataması:** Kadroya bir kullanıcı (`userId`) atanır. Kullanıcı seçiminde aynı pozisyondaki diğer kadrolara zaten atanmış kullanıcılar listeden çıkarılır.
3. **Tekil Atama Kuralı:** Aynı kullanıcı aynı pozisyondaki başka bir kadroya atandığında, önceki kadrodaki `userId` otomatik olarak temizlenir.
4. **Görüntüleme:** Kadro listesinde kadro tanımı ve atanan kullanıcının adı-soyadı gösterilir.
5. **Silme:** Kadro, pozisyon detayından silinebilir; pozisyon silindiğinde tüm kadrolar da silinir.

### Pozisyon vs Ünvan

| Kavram | Model | Amaç |
|--------|-------|------|
| **Ünvan** | `AccountProfessionDto` | Meslek/görev tanımı (örn. Müdür, Uzman) |
| **Pozisyon** | `AccountPositionDto` | Organizasyonel görev yeri (örn. Satış Müdürlüğü) |
| **Kadro** | `AccountStaffDto` | Pozisyondaki somut personel slotu |

---

## Validasyon Kuralları

### Pozisyon
- `kod` — zorunlu
- `tanim` — zorunlu
- `selectedCompanyId` — zorunlu (0 olamaz)

### Kadro
- `kod` — zorunlu
- `tanim` — zorunlu
- `userId` — zorunlu (0 olamaz)

---

## API Endpoint'leri

| Endpoint | HTTP | Açıklama |
|----------|------|----------|
| `GetAccountPositions` | GET | Pozisyonları ve kadroları listele |
| `AddOrUpdateAccountPosition` | POST | Pozisyon ekle/güncelle (kadrolar dahil) |
| `DeleteAccountPosition/{id}` | DELETE | Pozisyon sil (kadrolar dahil) |

> Kadrolar için ayrı bir API endpoint'i yoktur; tüm kadro işlemleri pozisyon kaydı üzerinden yürütülür.

---

## Dosya Yapısı

```
lib/Models/Settings/OrganizationSettings/
├── AccountPositionDto.dart      # AccountPositionDto, AccountStaffDto
└── GetAccountPositionsDto.dart

lib/Pages/Settings/OrganizationSettings/Positions/
├── PositionPage.dart            # Pozisyon liste sayfası
├── PositionDetailPage.dart      # Pozisyon detay + kadro yönetimi
└── StaffDetailPage.dart         # Kadro ekleme/düzenleme
```

---

## İlgili Dokümanlar

- [Kullanıcılar](./users.md) — `selectedPosition` ve `selectedStaff` alanları
- [Şirketler](./companies.md) — Pozisyonların şirket bağlantısı
- [Ünvanlar](./titles.md) — Ünvan ile pozisyon farkı
