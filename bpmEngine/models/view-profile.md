# Model — ProcessViewProfile (görüntüleme profili)

> **Durum:** 🟡 TASLAK (ilk çıkarım — gözden geçirilecek)
> **Amaç:** Aynı formun **farklı süreç adımlarında/kullanıcılara** nasıl görüneceğini belirler (alan görünürlüğü/
> düzenlenebilirliği/zorunluluğu/sırası).
> **Davranış/kullanım:** → `../servis-ayarlari/view-profile.md`

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Profil ID'si. |
| `serviceId` | int | FK → Service | Bağlı servis. |
| `code` | string | benzersiz | Profil kodu. |
| `definition` | string | — | Profil adı. |
| `isDefault` | bool | — | Varsayılan profil mi (adımda belirtilmeyince kullanılır). |
| `processViewProfileProperty` | List\<ProcessViewProfileProperty\> | — | Profildeki alan yapılandırmaları (→ `view-profile-property.md`). |

## İlişkiler
- **N – 1** → `Service` (`serviceId`).
- **1 – N** ← `ProcessViewProfileProperty` (`viewProfileId`).
- **Referans:** `ProcessStep`'lerde `processViewProfileId` ile atanır; `WorkRule.activeViewProfiles` ile kısıtlanır;
  iş kuralı `ChangeViewProfile` ile çalışma-zamanı değiştirilebilir.

## Notlar / açık noktalar
- Form List alt-servis görüntüleme/seçim; profillerin servis-bazlı mı paylaşımlı mı olduğu → `../todo.md`.

*Oluşturma: 2026-07-02.*
