# Model — ProcessTransfer (Süreç Transferi — organizasyon ayarı)

> **Durum:** 🟡 TASLAK — eski uygulama DTO'sundan türetildi.
> **Kaynak DTO:** `../../research/current-flovo-bpm-engine/organizations/process-transfer.md` (`ProcessTransferDto`).
> **Dönüşüm:** id'ler int; sahiplik → **`organizationId` (int)**.
> **Amaç:** Bir kullanıcının **bekleyen süreç görevlerini** başka kullanıcıya **servis bazında** devretme işlemi
> (örn. izne çıkan/ayrılan personel).

## Alanlar (işlem/komut)
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Transfer kaydı ID'si (kayıt tutulursa). |
| `organizationId` | int | FK → `organization.md` | Kiracı. |
| `fromUserId` | int | FK → `user.md` | Görevleri **devreden** kullanıcı. |
| `toUserId` | int | FK → `user.md` | Görevleri **devralan** kullanıcı. |
| `serviceId` | int | FK → `../service-settings/service.md` | Transfer edilecek servis. |

## İlişkiler
- **N – 1** → `Organization`, `User` (`fromUserId`, `toUserId`), `Service` (`serviceId`).

## Notlar
- Bu bir **operasyon/komut**tur (kalıcı yapılandırma varlığı değil): `fromUser`'ın seçili servisteki bekleyen görevleri `toUser`'a aktarılır.
  Denetim için **kayıt** tutulacaksa `id` + zaman damgası eklenir (→ `../../todo.md`).

*Oluşturma: 2026-07-03.*
