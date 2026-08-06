# Model — InstanceAwaitingUser (formu bekleyen kullanıcı/grup)

> **Durum:** 🟢 TANIMLI
> **Yeni model.**
> **Amaç:** Bir form üzerinde **atanan / aksiyon alabilecek** kullanıcıları tutar (aksiyon bekleyenler). Form üzerinden
> aksiyon alabilecek kullanıcılar **doğrudan bu tablodan** tespit edilir — `ProcessStepInstance` tablosunu filtreleyerek
> kullanıcı/kullanıcı grubu/processing adımını bulmaya çalışmak **maliyeti artıracağı** için bu tablo tutulur.
> Bir form/adım için **birden çok** kayıt olabilir (n kullanıcı).
> _(**Not:** **Processing** adımında kullanıcı yine bu tabloya atanır ve formu "bekleyenler" listesinde görür, ancak
> form üzerinde **işlem alınamaz** → `../../service-settings/process-step.md` §3.18. Bu yüzden kapsam "atanan/bekleyen"dir,
> yalnızca "aksiyon alabilen" değil.)_

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Bekleme kaydı ID'si. |
| `instanceId` | int | FK → Instance.id | Beklenen form. |
| `organizationId` | int | (denormalize) | Kiracı — **RLS/tenant izolasyonu** (RLS Pattern B v2: her tenant-tabloda `organizationId`; DB-seviyesi izolasyon). |
| `processStepInstanceId` | int | FK → ProcessStepInstance.id | Bekleme hangi adım çalıştırmasında oluştu. |
| `userId` | int? | FK → User.id | Aksiyon alabilecek **kullanıcı**. _(`userId` **veya** `userGroupId`'den biri dolu olmak zorunda.)_ |
| `userGroupId` | int? | FK → UserGroup.id | Aksiyon alabilecek **kullanıcı grubu** (gruptaki üyeler aksiyon alabilir). |

## Kayıt oluşma senaryoları (kaç kayıt, hangi alan dolar)
Adımın atama tipine göre **bir veya birden çok** `InstanceAwaitingUser` kaydı oluşur:

| Senaryo | Kayıt sayısı | Dolan alan |
|---|---|---|
| **Kullanıcı** süreç adımı (tek kullanıcı) | **1** kayıt | `userId` |
| **Kullanıcı Grubu** adımı (bir `UserGroup`'tan beslenir) | **1** kayıt | `userGroupId` — o grubun üyeleri aksiyon alabilir |
| **Çoklu seçim** (multi-select combobox'tan **n kullanıcı** seçilmiş; bir gruba bağlı **değil**) | **n** kayıt | her biri için ayrı `userId` |

> Üçüncü senaryoda seçilen kullanıcılar bir `UserGroup` ile gruplanmadığından **grup id yoktur**; her kullanıcı için
> ayrı bir kayıt (`userId` dolu) oluşturulur.

## Senkronizasyon (önemli)
İş akışı ilerlerken bir **Kullanıcı / Kullanıcı Grubu / Processing** adımına gelindiğinde, o form üzerinde aksiyon
alabilecek kullanıcılar bu tabloda **güncellenir** (yeni aksiyon alabilecekler **eklenir**, artık alamayacaklar
**silinir**). Böylece tablo, formun **güncel** aksiyon alabilenler kümesiyle **sync** kalır.

## İlişkiler
- **N – 1** → `Instance` (`instanceId`), `ProcessStepInstance` (`processStepInstanceId`),
  `User` (`userId`), `UserGroup` (`userGroupId`).

## Notlar / açık noktalar
- **`userId` veya `userGroupId`'den biri dolu olmak zorunda** (ikisi birden değil).
- **Kullanıcı Grubu ataması:** `userGroupId` dolu olduğunda **gruptaki üyelerden herhangi biri** aksiyon alabilir; ilk aksiyon
  süreci ilerletir _(ilk fazda "hepsi onaylar" grup-onayı yoktur)_.

*Oluşturma: 2026-07-06.*
