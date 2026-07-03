# Süreç Transferi (Process Transfer)

## Genel Bakış

Süreç transferi, bir kullanıcının üzerindeki bekleyen süreç görevlerini başka bir kullanıcıya devretmek için kullanılır. Tipik senaryo: İzne çıkan veya işten ayrılan bir personelin açık işlerinin bir başkasına aktarılması. Servis bazında transfer yapılabilir.

---

## Veri Modeli (ProcessTransferDto)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `fromUserId` | int | Kaynak kullanıcı ID'si (görevleri devreden) |
| `toUserId` | int | Hedef kullanıcı ID'si (görevleri devralan) |
| `serviceId` | int | Transfer edilecek servis ID'si |

---

## Yardımcı Veriler (GetProcessTransferDataDto)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `services` | List\<ServiceSummary\> | Transfer yapılabilecek servisler |
| `users` | List\<ProcessTransferUserDto\> | Kaynak/hedef seçilebilecek kullanıcılar |

### Kullanıcı Modeli (ProcessTransferUserDto)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Kullanıcı ID'si |
| `fullName` | String | Ad-soyad |
| `userName` | String | Kullanıcı adı |
| `status` | bool | Aktiflik durumu |

---

## Çalışma Prensibi

1. **Veri Yükleme:** `GetProcessTransferData` ile transfer yapılabilecek servisler ve kullanıcılar çekilir.
2. **Seçim:** Kaynak kullanıcı (`fromUserId`), hedef kullanıcı (`toUserId`) ve servis (`serviceId`) seçilir.
3. **Transfer:** `ProcessTransfer` endpoint'i çağrılarak kaynak kullanıcının seçili servisteki bekleyen görevleri hedef kullanıcıya aktarılır.

---

## API Endpoint'leri

| Endpoint | HTTP | Açıklama |
|----------|------|----------|
| `GetProcessTransferData` | POST | Transfer için servis ve kullanıcı verilerini getir |
| `ProcessTransfer` | POST | Süreç görevlerini transfer et |

---

## Dosya Yapısı

```
lib/Models/Settings/OrganizationSettings/
└── ProcessTransferDto.dart   # ProcessTransferDto, GetProcessTransferDataDto, ProcessTransferUserDto

lib/Pages/Settings/OrganizationSettings/ProcessTransfer/
└── ProcessTrasferPage.dart   # Transfer sayfası
```
