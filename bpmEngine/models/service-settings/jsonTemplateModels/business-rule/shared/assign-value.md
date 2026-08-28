# DTO — AssignValue

> **Tür:** DTO — **DB tablosu değildir.** İş kuralı aksiyon konfiglerinin içinde, `BusinessRule.configuration` **JSONB**
> gövdesinde iç-içe yaşar.
> **Amaç:** **"Buraya bir değer gelecek"** olan her yerde kullanılan **merkezi değer-çözümleme** modeli.
> **Aile / davranış:** [`index.md`](../index.md) · [`../../../../../service-settings/business-rule.md`](../../../../../service-settings/business-rule.md) §3.1 · kaynak enum → [`../../../../enums/value-assign-type.md`](../../../../enums/value-assign-type.md)

## Nedir?
Değerin **nereden** geleceğini `valueAssignType` **ayrımlayıcısı** ile seçer; yalnız o kaynağın **payload**'ı dolu olur
(**discriminated union / oneOf**). Her tip **yalnız kendi alanlarını** taşır — kullanan taraf ilgisiz alan görmez.

> **Nerede:** `assignValueToProperty` değeri · `applyValidation`/`showMessage` metni · koşul `fromCalculation` tarafı ·
> veri seti/organizasyon filtre değerleri (→ [`fill-data-source-parameter.md`](../data-source/fill-data-source-parameter.md) · [`assign-value-from-dataset-parameter.md`](../data-source/assign-value-from-dataset-parameter.md)).

## Yapı (ayrımlayıcı + oneOf payload)
| Alan | Tip | Zorunlu | Açıklama |
|---|---|:---:|---|
| `valueAssignType` | ValueAssignType | ✔ | **Ayrımlayıcı** — dolu payload'ı belirler ([`../../../../enums/value-assign-type.md`](../../../../enums/value-assign-type.md)). |
| `fixedValue` | `{ value: string, translationCode?: string }` | oneOf | Sabit değer (+ çok-dilli metin için çeviri anahtarı → [`../../../../organization-settings/translation.md`](../../../../organization-settings/translation.md)). |
| `propertyValue` | `{ propertyId: int, useDisplay?: bool }` | oneOf | Başka bir alanın değeri; `useDisplay` = value yerine görünen metin. |
| `fromCalculation` | `{ expression: string, localizedExpressions?: [{ languageCode, expression }] }` | oneOf | İfade sonucu. `expression` = **default** (eksik dillerde kullanılır); `localizedExpressions` = **dile-özel** ifadeler (kayıt-başına-dil → [`../../../../../service-settings/business-rule.md`](../../../../../service-settings/business-rule.md) §5). |
| `fromDataSet` | AssignValueFromDataSet | oneOf | Başka servisin instance'larından (→ [`assign-value-from-dataset.md`](../data-source/assign-value-from-dataset.md)). |
| `httpRequest` | HTTP Request konfigi | oneOf | Dış çağrı. **Konfig** (`endpoint`/`HttpMethod`/`DynamicParameter[]`) `process-step` HTTP Request'i paylaşır; **yanıt→değer çıkarımı** (`responseParameter` + liste için `valueField`/`displayField`) iş-kuralına özeldir → [`../../../../../service-settings/business-rule-engine.md`](../../../../../service-settings/business-rule-engine.md) §7. |
| `search` | *(açık → todo)* | oneOf | Arama sonucu seçilen değer. |

> **oneOf kısıtı:** Yalnız `valueAssignType`'a **karşılık gelen** payload alanı dolu olmalıdır; diğerleri **bulunmaz**.

## Örnek (JSON)
```jsonc
// başka alanın değeri
{ "valueAssignType": "propertyValue", "propertyValue": { "propertyId": 55 } }

// sabit + çok-dilli metin
{ "valueAssignType": "fixedValue", "fixedValue": { "value": "Onaylandı", "translationCode": "APPROVED" } }

// hesaplama (dil-agnostik)
{ "valueAssignType": "fromCalculation", "fromCalculation": { "expression": "#TUTAR * #KUR" } }

// çok-dilli hesaplama — default + dile-özel (eksik dilde default kullanılır)
{ "valueAssignType": "fromCalculation",
  "fromCalculation": {
    "expression": "isHoliday(#TARIH)==1 ? 'Tatil' : 'İş Günü'",              // default
    "localizedExpressions": [
      { "languageCode": "en", "expression": "isHoliday(#TARIH)==1 ? 'Holiday' : 'Workday'" }
    ]
  }
}
```

## Nasıl çalışır
- Motor `valueAssignType`'a bakar, **yalnız** o payload'ı okur.
- Asenkron kaynaklar (`fromDataSet` lazy · `httpRequest` · async `fromCalculation`) çözülünce değer atanır.

## İlişkili / Notlar
- **SOLID (discriminated union):** her kaynak **yalnız kendi payload**'ını taşır (ISP); **yeni kaynak** = yeni `ValueAssignType` değeri + yeni payload alanı, mevcut payload'lar **değişmez** (OCP). `BusinessRuleConditionCompareValue` ve `FillDataSource` aynı konvansiyonu izler.
- **Dil alanları `...En` — iki AYRI yol (aynı sepete konmaz):**
  - eski **`fixedValueEn`** (sabit metin) → **`fixedValue.translationCode`** → Translation (statik değerler, kayıt-başına-dil, §10). ✓
  - eski **`fromCalculationValueEn`** (ifade) → **Translation'a indirgenemez** (dinamik hesaplama). Yerine `fromCalculation` içinde **çok-dilli ifade listesi**: `expression` (**default**) + `localizedExpressions: [{ languageCode, expression }]`. Böylece **TR/EN kısıtı kalkar** (N dil); bir dil listede yoksa **`expression` (default)** kullanılır. _(Bildirim mesajı `{languageCode, text}` deseninin ifade karşılığı.)_
- Eski adı `AssignValueToFieldDto` (düz-opsiyonel alanlar); yeni motorda payload-gruplu.

*Oluşturma: 2026-08-26 · Güncelleme: 2026-08-26 (SOLID — discriminated union).*
