# Model — ProcessTransfer (Süreç Transferi — organizasyon ayarı)

> **Durum:** 🟢 Gözden geçirildi (v0.36)
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
- **Uzlaştırma (kapsam ayrımı):** Bu model, **yöneticinin bekleyen görevleri toplu yeniden-atamasını** (görev toplu devri) tarifler.
  Kalıcı **vekalet (proxy)** sisteminden — bir kullanıcının başkası **adına** işlem yapması — **AYRIDIR** → `../../todo.md` (Vekalet).
- **Denetim kaydı:** Kayıt tutulacaksa `id` + zaman damgası eklenir; genel denetim izi/loglama yaklaşımına atıf → `../../todo.md` (loglama modeli).

*Oluşturma: 2026-07-03.*
