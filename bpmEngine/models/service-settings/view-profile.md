# Model — ProcessViewProfile (görüntüleme profili)

> **Durum:** 🟡 TASLAK (ilk çıkarım — gözden geçirilecek)
> **Amaç:** Aynı formun **farklı süreç adımlarında/kullanıcılara** nasıl görüneceğini belirler (alan görünürlüğü/
> düzenlenebilirliği/zorunluluğu/sırası).
> **Davranış/kullanım:** → `../../service-settings/view-profile.md`

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Profil ID'si. |
| `serviceId` | int | FK → Service | Bağlı servis. |
| `code` | string | benzersiz | Profil kodu. |
| `definition` | string | — | Profil adı. |
| `translationCode` | string? | çeviri anahtarı | **Çeviri eşleşme anahtarı** (→ [`../organization-settings/translation.md`](../organization-settings/translation.md) `code`). `null` = çeviri **es geçilir**, doğrudan `definition` kullanılır. |
| `isDefault` | bool | — | Varsayılan profil mi (adımda belirtilmeyince kullanılır). |
| `processViewProfileProperty` | List\<ProcessViewProfileProperty\> | — | Profildeki alan yapılandırmaları (→ `view-profile-property.md`). |

## İlişkiler
- **N – 1** → `Service` (`serviceId`).
- **1 – N** ← `ProcessViewProfileProperty` (`viewProfileId`).
- **Referans:** `ProcessStep`'lerde `processViewProfileId` ile atanır; `BusinessRule.activeViewProfiles` ile kısıtlanır.

## Notlar / açık noktalar
- Form List alt-servis görüntüleme/seçim; profillerin servis-bazlı mı paylaşımlı mı olduğu → `../../todo.md`.

*Oluşturma: 2026-07-02.*
