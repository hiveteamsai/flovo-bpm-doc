# Model — CreditCard (Kredi Kartı — organizasyon ayarı)

> **Durum:** 🟡 TASLAK — eski uygulama DTO'sundan türetildi.
> **Kaynak DTO:** `../../research/current-flovo-bpm-engine/organizations/credit-cards.md` (`AccountCreditCardDto`).
> **Dönüşüm:** `account*`→`organization*`; `accountId` (string) → **`organizationId` (int)**; `kod`/`tanim`→`code`/`definition`;
> `accountCompanyId`→`companyId`.
> **Amaç:** Harcama/masraf süreçlerinde kullanılan **kurumsal kartlar**. Şirkete ve isteğe bağlı kullanıcıya bağlanır.

## Alanlar
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Kart ID'si. |
| `organizationId` | int | FK → `organization.md` | Sahibi organizasyon. |
| `companyId` | int | FK → `company.md` | Bağlı şirket. |
| `code` | string | — | Kart kodu. |
| `definition` | string | — | Kart adı/tanımı. |
| `cardNumber` | string | — | Kart numarası. |
| `userId` | int? | FK → `user.md` | Bağlı kullanıcı (opsiyonel). |
| `isCommonCard` | bool | — | Ortak kart mı (herkes kullanabilir). |
| `active` | bool | — | Aktif/pasif — **null olamaz**, varsayılan `true`. `false` = frontend'de **görünür/düzenlenebilir** ama BPM işlemede kullanılmaz. |
| `deleted` | bool | — | Soft-delete — **null olamaz**, varsayılan `false`. `true` = frontend'de **gizli/aktarılmaz/salt** + BPM işlemede kullanılmaz. |
| `synchronizationStatus` | bool | — | Senkron durumu. |

## Benzersizlik
> `(organizationId, code)` **benzersiz** — aynı organizasyonda aynı `code`'lu iki kayıt olamaz. **`deleted=true` kayıtlar kontrole dahil değildir** (soft-delete edilenler bu kontrolde sayılmaz).

## İlişkiler
- **N – 1** → `Organization`, `Company` (`companyId`), `User` (`userId`).
- **Kullanım:** Masraf/harcama formlarında ödeme aracı; kullanıcıya **`CreditCard.userId`** (tek yönlü FK) ile atanır — `User` tarafında liste alanı yoktur.

*Oluşturma: 2026-07-03.*
