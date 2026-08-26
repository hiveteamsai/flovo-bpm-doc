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
| `translationCode` | string? | çeviri anahtarı | **Çeviri eşleşme anahtarı** (→ [`../organization-settings/translation.md`](../organization-settings/translation.md) `code`). `null` = çeviri **es geçilir**, doğrudan `definition` kullanılır. |
| `icon` | string | — | İkon. |
| `environmentRestriction` | string | — | Ortam kısıtı. |
| `businessRuleActionType` | BusinessRuleActionType | — | Kural aksiyonu (aşağıda) — [`../enums/business-rule-action-type.md`](../enums/business-rule-action-type.md). |
| `configuration` | jsonb | — | **Aksiyon konfigürasyonu** — `businessRuleActionType`'a göre şekillenen **yapısal JSONB** (ayrımlayıcı = aksiyon tipi). Alt-şemalar → [`dto/business-rule/`](./dto/business-rule/index.md). _(Eski motorun `value` string-içinde-JSON alanının yerini alır; v0.34.)_ |
| `businessRuleRuntimeType` | BusinessRuleRuntimeType | — | Çalışma zamanı — [`../enums/business-rule-runtime-type.md`](../enums/business-rule-runtime-type.md): `always` / `firstOpening` / `whenChanging`. |
| `businessRuleConditionType` | BusinessRuleConditionType | — | Koşul birleştirme — [`../enums/business-rule-condition-type.md`](../enums/business-rule-condition-type.md): `and` (VE) / `or` (VEYA). |
| `businessRuleConditions` | List\<BusinessRuleCondition\> | — | Koşul listesi (recursive → `business-rule-condition.md`). |
| `activeViewProfiles` | List\<int\> | FK → ProcessViewProfile.id | Yalnız bu görüntüleme profillerinde çalış. |
| `shouldNotWorkInReadonlyMode` | bool | — | Salt-okunur modda çalışmasın. |
| `priority` | int | — | Kural **çalışma sırası/önceliği** (küçük = önce çalışır). Aynı alana yazan kurallarda belirleyicidir. _(Eski motorda öncelik yoktu → "son yazan kazanır"; v0.34'te eklendi.)_ |

### `businessRuleActionType` değerleri (bu modeldeki rol — frontend etkisi)
Enum tanımı → [`../enums/business-rule-action-type.md`](../enums/business-rule-action-type.md). Bu modelde koşul sağlanınca formda uygulanacak etkiyi belirler:
- `setViewForProperties` (visible/enabled/required) · `applyValidation` · `showMessage` ·
  `assignValueToProperty` · `fillDataSource` · `assignValueToPropertyAttribute` ·
  `setStyle` _(tekil görünüm niteliği — fontSize/titleColor; `../organization-settings/style.md` Style varlığını **seçmez**)_.

> `assignValueToProperty` değer kaynakları (`ValueAssignType` → [`../enums/value-assign-type.md`](../enums/value-assign-type.md)): `fixedValue` · `propertyValue` · `fromCalculation` ·
> `fromDataSet` · `search` · `httpRequest`.

### `configuration` — aksiyon-tipine göre JSONB şeması
`configuration` alanının şekli `businessRuleActionType`'a göre belirlenir (alt-şemalar → [`dto/business-rule/`](./dto/business-rule/index.md)):

| `businessRuleActionType` | `configuration` şeması (DTO) |
|---|---|
| `setViewForProperties` | [`SetViewForProperties`](./dto/business-rule/actions/set-view-for-properties.md) |
| `applyValidation` | [`ApplyValidation`](./dto/business-rule/actions/apply-validation.md) |
| `showMessage` | [`ShowMessage`](./dto/business-rule/actions/show-message.md) |
| `assignValueToProperty` | [`AssignValueToProperty`](./dto/business-rule/actions/assign-value-to-property.md) |
| `fillDataSource` | [`FillDataSource`](./dto/business-rule/actions/fill-data-source.md) |
| `assignValueToPropertyAttribute` | [`AssignValueToPropertyAttribute`](./dto/business-rule/actions/assign-value-to-property-attribute.md) |
| `setStyle` | [`SetStyle`](./dto/business-rule/actions/set-style.md) |

Ortak alt-modeller: **[`AssignValue`](./dto/business-rule/shared/assign-value.md)** (merkezi değer çözümleme) · **[`PropertyAppearance`](./dto/business-rule/shared/property-appearance.md)** · **[`AssignValueFromDataSet`](./dto/business-rule/data-source/assign-value-from-dataset.md)** (+ parametre) · **[`FillDataSourceUser`](./dto/business-rule/data-source/fill-data-source-user.md)**.

## İlişkiler
- **N – 1** → `Organization` (`organizationId`), `Service` (`serviceId`).
- **N – N** → `ProcessViewProfile` (`activeViewProfiles`).
- **1 – N** ← `BusinessRuleCondition` (`businessRuleId`).

## Notlar / açık noktalar
- **Çalışma yeri (KARAR v0.34):** iş kuralları **tam frontend** çalışır — kurallar servise gömülü gelir, her client kendi motorunu yürütür (realtime UX).
- **Aksiyon konfigi (KARAR v0.34):** `configuration` = **yapısal JSONB** (aksiyon-tipine göre şema; string-içinde-JSON değil).
- **Tetikleme kapsamı (KARAR v0.34):** değişim tetiklemesi yalnız **koşul** alanlarına değil, aksiyon/ifade alanlarına da bakar (eski motorda yalnız koşul alanları tetiklerdi).
- **`priority` (KARAR v0.34):** açık kural sırası eklendi (eski "son yazan kazanır" belirsizliği giderildi).
- **Açık:** iki-katman sınırı (adım ↔ iş kuralı) · ifade dilinin somut seçimi + katalog · `fillDataSource` `organizationData` kaynak kapsamı · `search` değer kaynağı · döngü/derinlik limiti + hata görünürlüğü → [`../../todo.md`](../../todo.md).

*Oluşturma: 2026-07-02.*
