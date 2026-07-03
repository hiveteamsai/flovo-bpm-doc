# Model — WorkRule (iş kuralı)

> **Durum:** 🟡 TASLAK — iş kuralları **frontend'de realtime** çalışır ve BPM motorundan bağımsızdır; bu model
> **en son** kesinleşecek (→ `../todo.md`).
> **Amaç:** Form üzerinde **koşul → aksiyon** tabanlı dinamik davranış (göster/gizle, validasyon, değer, veri kaynağı, stil).
> **Davranış/kullanım:** → `../servis-ayarlari/work-rule.md`

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Kural ID'si. |
| `organizationId` | int | FK → Organization.id | Kiracı. |
| `serviceId` | int | FK → Service | Bağlı servis. |
| `code` | string | — | Kural kodu. |
| `definition` | string | — | Kural adı/tanımı. |
| `icon` | string | — | İkon. |
| `environmentRestriction` | string | — | Ortam kısıtı. |
| `actionType` | enum | — | Kural aksiyonu (aşağıda). |
| `workRuleRuntimeType` | enum | — | Çalışma zamanı: `always` / `firstOpening` / `whenChanging`. |
| `workRuleConditionType` | enum | — | Koşul birleştirme: VE / VEYA. |
| `workRuleConditions` | List\<WorkRuleCondition\> | — | Koşul listesi (recursive → `work-rule-condition.md`). |
| `activeViewProfiles` | List\<int\> | FK → ProcessViewProfile.id | Yalnız bu görüntüleme profillerinde çalış. |
| `shouldNotWorkInReadonlyMode` | bool | — | Salt-okunur modda çalışmasın. |

### `actionType` değerleri (frontend)
`SetViewForProperties` (visible/enabled/required) · `ChangeViewProfile` · `ApplyValidation` · `ShowMessage` ·
`AssignValueToProperty` · `FillDataSource` · `AssignValueToPropertyAttribute` _(isim teyit)_ ·
`SetStyle` _(tekil görünüm niteliği — fontSize/titleColor; `style.md` Style varlığını **seçmez**)_.

> `AssignValueToProperty` değer kaynakları (`ValueAssignType`): `FixedValue` · `PropertyValue` · `FromCalculation` ·
> `FromDataSet` · `Search` · `HttpRequest`.

## İlişkiler
- **N – 1** → `Organization` (`organizationId`), `Service` (`serviceId`).
- **N – N** → `ProcessViewProfile` (`activeViewProfiles`).
- **1 – N** ← `WorkRuleCondition` (`workRuleId`).

## Notlar / açık noktalar
- İki-katman sınırı (adım ↔ iş kuralı), `FillDataSource` kaynak tipleri, performans (alan-bağımlı tetikleme) → `../todo.md`.

*Oluşturma: 2026-07-02.*
