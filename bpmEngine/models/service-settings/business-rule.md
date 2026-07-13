# Model — BusinessRule (iş kuralı)

> **Durum:** 🟡 TASLAK — iş kuralları **frontend'de realtime** çalışır ve BPM motorundan bağımsızdır; bu model
> **en son** kesinleşecek (→ `../../todo.md`).
> **Amaç:** Form üzerinde **koşul → aksiyon** tabanlı dinamik davranış (göster/gizle, validasyon, değer, veri kaynağı, stil).
> **Davranış/kullanım:** → `../../service-settings/business-rule.md`

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
| `businessRuleActionType` | enum | — | Kural aksiyonu (aşağıda) — [`../enums/business-rule-action-type.md`](../enums/business-rule-action-type.md). |
| `businessRuleRuntimeType` | enum | — | Çalışma zamanı — [`../enums/business-rule-runtime-type.md`](../enums/business-rule-runtime-type.md): `always` / `firstOpening` / `whenChanging`. |
| `businessRuleConditionType` | enum | — | Koşul birleştirme — [`../enums/business-rule-condition-type.md`](../enums/business-rule-condition-type.md): `and` (VE) / `or` (VEYA). |
| `businessRuleConditions` | List\<BusinessRuleCondition\> | — | Koşul listesi (recursive → `business-rule-condition.md`). |
| `activeViewProfiles` | List\<int\> | FK → ProcessViewProfile.id | Yalnız bu görüntüleme profillerinde çalış. |
| `shouldNotWorkInReadonlyMode` | bool | — | Salt-okunur modda çalışmasın. |

### `businessRuleActionType` değerleri (bu modeldeki rol — frontend etkisi)
Enum tanımı → [`../enums/business-rule-action-type.md`](../enums/business-rule-action-type.md). Bu modelde koşul sağlanınca formda uygulanacak etkiyi belirler:
- `SetViewForProperties` (visible/enabled/required) · `ChangeViewProfile` · `ApplyValidation` · `ShowMessage` ·
  `AssignValueToProperty` · `FillDataSource` · `AssignValueToPropertyAttribute` _(isim teyit)_ ·
  `SetStyle` _(tekil görünüm niteliği — fontSize/titleColor; `../organization-settings/style.md` Style varlığını **seçmez**)_.

> `AssignValueToProperty` değer kaynakları (`ValueAssignType` → [`../enums/value-assign-type.md`](../enums/value-assign-type.md)): `FixedValue` · `PropertyValue` · `FromCalculation` ·
> `FromDataSet` · `Search` · `HttpRequest`.

## İlişkiler
- **N – 1** → `Organization` (`organizationId`), `Service` (`serviceId`).
- **N – N** → `ProcessViewProfile` (`activeViewProfiles`).
- **1 – N** ← `BusinessRuleCondition` (`businessRuleId`).

## Notlar / açık noktalar
- İki-katman sınırı (adım ↔ iş kuralı), `FillDataSource` kaynak tipleri, performans (alan-bağımlı tetikleme) → `../../todo.md`.

*Oluşturma: 2026-07-02.*
