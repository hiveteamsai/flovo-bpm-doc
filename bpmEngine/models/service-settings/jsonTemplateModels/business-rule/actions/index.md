# İş Kuralı — Aksiyon Konfigleri (`actions/`)

> **Amaç:** `BusinessRule.configuration` (JSONB) alanının, `businessRuleActionType`'a göre aldığı **7 aksiyon şeması** —
> koşul sağlanınca formda uygulanacak etkinin ayarları.
> **Üst indeks:** [`../index.md`](../index.md) · **davranış:** [`../index.md`](../index.md) → `service-settings/business-rule.md` §3

| Döküman | Aksiyon tipi | Ne yapar |
|---|---|---|
| [`set-view-for-properties.md`](./set-view-for-properties.md) | `setViewForProperties` | Alan(lar)ın visible/enabled/required durumu. |
| [`apply-validation.md`](./apply-validation.md) | `applyValidation` | Koşullu validasyon (satır-bazlı destekli). |
| [`show-message.md`](./show-message.md) | `showMessage` | Başlık + gövde dialog. |
| [`assign-value-to-property.md`](./assign-value-to-property.md) | `assignValueToProperty` | Alan **değerine** atama. |
| [`fill-data-source.md`](./fill-data-source.md) | `fillDataSource` | Seçim alanının veri kaynağı (**discriminated union**). |
| [`assign-value-to-property-attribute.md`](./assign-value-to-property-attribute.md) | `assignValueToPropertyAttribute` | Alan **özniteliğine** atama. |
| [`set-style.md`](./set-style.md) | `setStyle` | Tekil görünüm niteliği (fontSize/titleColor). |

> Aksiyonların değer alanları **`../shared/assign-value.md`** (AssignValue), veri kaynakları **`../data-source/`** modellerini kullanır.

*Oluşturma: 2026-08-26.*
