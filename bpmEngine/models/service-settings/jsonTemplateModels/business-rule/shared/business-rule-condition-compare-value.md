# DTO — BusinessRuleConditionCompareValue

> **Tür:** DTO — **DB tablosu değildir.** `BusinessRuleCondition.referenceValue` / `valueToCompare` alanlarının şeklidir
> (JSONB olarak saklanır).
> **Aile / davranış:** [`index.md`](../index.md) · [`../../../../../service-settings/business-rule.md`](../../../../../service-settings/business-rule.md) §4

## Nedir?
Bir koşulun **sol** (`referenceValue`) veya **sağ** (`valueToCompare`) tarafındaki değerin **nereden geleceğini** tanımlar.
`compareType` **ayrımlayıcısı** kaynağı seçer; yalnız o kaynağın **payload**'ı dolu olur (**discriminated union / oneOf**).

> **Örnek senaryo:** *"`#TUTAR` (form alanı) **>** `1000` (sabit)"* → sol `propertyValue`, sağ `fixedValue`.

## Yapı (ayrımlayıcı + oneOf payload)
| Alan | Tip | Zorunlu | Açıklama |
|---|---|:---:|---|
| `compareType` | BusinessRuleConditionCompareType | ✔ | **Ayrımlayıcı** — kaynak (`propertyValue`/`viewProfile`/`fixedValue`/`fromCalculation` → [`../../../../enums/business-rule-condition-compare-type.md`](../../../../enums/business-rule-condition-compare-type.md)). |
| `propertyValue` | `{ propertyId: int, valueTypeOfList?: ValueTypeOfList }` | oneOf | Form alanının değeri; liste-tipli kontrolde `valueTypeOfList` ile hangi değer (→ [`../../../../enums/value-type-of-list.md`](../../../../enums/value-type-of-list.md)). |
| `fixedValue` | `{ value: string }` | oneOf | Sabit karşılaştırma değeri. |
| `fromCalculation` | `{ expression: string }` | oneOf | İfade/hesaplama sonucu. |
| `viewProfile` | *(payload yok)* | oneOf | Aktif görüntüleme profilinin kodu (ayrımlayıcı tek başına yeter). |

> **oneOf kısıtı:** Yalnız `compareType`'a karşılık gelen payload dolu olur; `viewProfile` için ek alan gerekmez.

## Örnek (JSON)
```jsonc
// sol: #TUTAR alanı
{ "compareType": "propertyValue", "propertyValue": { "propertyId": 73 } }
// sağ: sabit 1000
{ "compareType": "fixedValue", "fixedValue": { "value": "1000" } }
```

## İlişkili / Notlar
- Koşul modeli: [`../../../business-rule-condition.md`](../../../business-rule-condition.md) · operatör: [`../../../../enums/criterion-type.md`](../../../../enums/criterion-type.md).
- **SOLID:** `AssignValue` / `FillDataSource` ile aynı discriminated-union konvansiyonu (ISP/OCP).
- Eski adı `WorkRuleConditionCompareValueDto` (düz-opsiyonel alanlar); yeni motorda payload-gruplu. Koşul tarafı, tam `AssignValue` esnekliği yerine **sade** kaynak kümesini taşır (SRP).

*Oluşturma: 2026-08-26 · Güncelleme: 2026-08-26 (SOLID — discriminated union).*
