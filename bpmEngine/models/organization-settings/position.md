# Model — Position (Pozisyon — organizasyon ayarı)

> **Durum:** 🟡 TASLAK — eski uygulama DTO'sundan türetildi.
> **Kaynak DTO:** `../../research/current-flovo-bpm-engine/organizations/positions.md` (`AccountPositionDto` · `AccountStaffDto`).
> **Adlandırma:** Eski "Pozisyon/Position" → **`Position`**; eski "Kadro/Staff" (`AccountStaffDto`) → **`Staff`** (alt model).
> **Dönüşüm:** `account*`→`organization*`; `accountId` (string) → **`organizationId` (int)**; `kod`/`tanim`→`code`/`definition`;
> `selectedCompanyId`→`companyId`; `status` (bool)→`active`; `sycnronizationStatus`→`synchronizationStatus`; `accountStaffs`→`staff` (alt model).
> **Amaç:** Organizasyon şemasındaki **fiili görev yeri** tanımı (örn. "Satış Müdürlüğü"). Bir **şirkete** bağlıdır ve altında
> somut personel slotları (**Staff / kadro**) tutar.

## Alanlar — Position
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Pozisyon ID'si. |
| `organizationId` | int | FK → `organization.md` | Sahibi organizasyon. |
| `code` | string | — | Kod. |
| `definition` | string | — | Ad/tanım. |
| `companyId` | int | FK → `company.md` | Bağlı şirket (tekil, N–1). **Oluşturmada zorunlu** (0 olamaz); boş bırakılırsa varsayılan şirket (`isDefaultCompany`) kullanılır. |
| `active` | bool | — | Aktif/pasif — **null olamaz**, varsayılan `true`. `false` = frontend'de **görünür/düzenlenebilir** ama BPM işlemede kullanılmaz. |
| `deleted` | bool | — | Soft-delete — **null olamaz**, varsayılan `false`. `true` = frontend'de **gizli/aktarılmaz/salt** + BPM işlemede kullanılmaz. |
| `synchronizationStatus` | bool | — | Harici sistemle senkron durumu. |

## Alt model — Staff (Kadro)
Bir pozisyonun altındaki **somut personel slotu**. **1 kadro ↔ 1 kullanıcı**. Kadroların ayrı yönetim yüzeyi/endpoint'i
yoktur; **pozisyon kaydıyla birlikte** oluşturulur/güncellenir/silinir (pozisyon silinince altındaki kadrolar da silinir).

| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Kadro ID'si. |
| `positionId` | int | FK → Position | Bağlı pozisyon. |
| `code` | string | — | Kod. |
| `definition` | string | — | Ad/tanım. |
| `userId` | int? | FK → `user.md` | Atanan kullanıcı (**1 kadro 1 kullanıcı**). Oluşturmada zorunlu; **tekil atama kuralı** gereği geçici boşalabilir (aşağıda). |
| `active` | bool | — | Aktif/pasif — Position ile aynı kural (**null olamaz**, varsayılan `true`). |
| `synchronizationStatus` | bool | — | Senkron durumu. |

> **Tekil atama kuralı:** Bir kullanıcı **aynı anda yalnız bir kadroya** bağlı olabilir. Kullanıcı yeni bir kadroya atanırsa,
> **önceki kadronun `userId`'si otomatik temizlenir** (null olur). Kadro kullanıcı seçiminde, o pozisyondaki başka kadrolara
> **zaten atanmış** kullanıcılar listeden çıkarılır.

## Benzersizlik
> **Position:** `(organizationId, code)` **benzersiz** — aynı organizasyonda aynı `code`'lu iki pozisyon olamaz.
> **Staff:** `(positionId, code)` **benzersiz**; ayrıca **`userId` organizasyon genelinde benzersiz** (bir kullanıcı tek kadro).
> **`deleted=true` Position kayıtları** benzersizlik kontrolüne dahil değildir (soft-delete edilenler sayılmaz).

## İlişkiler
- **Position** — **N – 1** → `Organization` (`organizationId`), `Company` (`companyId`). **1 – N** ← `Staff` (`positionId`).
- **Staff** — **N – 1** → `Position` (`positionId`). **1 – 1** → `User` (`userId`, atanan kullanıcı).
- **Kullanıcı yansıması:** Bir kullanıcının pozisyon/kadro bilgisi **`Staff.userId` üzerinden** türetilir; `User` modelinde
  ayrıca **depolanmaz**, kullanıcı detayında **salt-okunur** gösterilir (→ `user.md`).

## Notlar
- **Position ≠ Profession ≠ Staff:** **`Profession`** (`profession.md`) = meslek/görev tanımı (örn. Müdür, Uzman);
  **`Position`** = organizasyonel görev yeri (örn. Satış Müdürlüğü); **`Staff`** = pozisyondaki somut personel slotu.
- **`IOrganizationParameter`:** `Position`, iş kurallarının veri kaynaklarında (fillDataSource) **organizasyon parametresi**
  olarak kullanılabilir.

*Oluşturma: 2026-07-13.*
