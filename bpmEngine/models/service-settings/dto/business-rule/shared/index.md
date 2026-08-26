# İş Kuralı — Ortak Yapı Taşları (`shared/`)

> **Amaç:** İş kuralı ailesinde **birden çok yerde** kullanılan temel modeller.
> **Üst indeks:** [`../index.md`](../index.md)

| Döküman | Nerede kullanılır |
|---|---|
| [`assign-value.md`](./assign-value.md) | **AssignValue** — "buraya bir değer gelecek" olan her yer: aksiyon değeri, validasyon/mesaj metni, koşul `fromCalculation`, filtre değeri. **Discriminated union** (`ValueAssignType` + oneOf payload). |
| [`property-appearance.md`](./property-appearance.md) | Alan görünüm bayrakları (`visible`/`enabled`/`required`) — `../actions/set-view-for-properties.md` içinde. |
| [`business-rule-condition-compare-value.md`](./business-rule-condition-compare-value.md) | Koşul tarafı (`referenceValue`/`valueToCompare`) değer kaynağı — `../../../business-rule-condition.md`. **Discriminated union**. |

*Oluşturma: 2026-08-26.*
