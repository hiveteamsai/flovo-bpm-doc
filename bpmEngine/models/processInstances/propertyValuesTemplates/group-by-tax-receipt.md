# Değer Şablonu — `groupByTaxReceipt` (Group By Tax Receipt)

> **Durum:** 🟡 TASLAK — ilk çıkarım; düzenlenecek.
> **Kapsam:** `groupByTaxReceipt` değerinin **`InstanceValue.data` içindeki şekli** (liste-of-model) + **`projectToAttr=true`** iken fihriste yansıması.
> **Alan davranışı:** → [`../../../service-settings/properties.md`](../../../service-settings/properties.md) §3.17 · **model:** [`../../service-settings/property.md`](../../service-settings/property.md) · **değer modeli:** [`../instance-list-item.md`](../instance-list-item.md) · **şekil:** [`labeled-value.md`](./labeled-value.md).

## 1. JSONB değer şekli — `data["<code>"]`
**Obje dizisi** (kalem listesi). Her kalem: **gider türü** (etiketli seçim) + **vergi oranı** (etiketli/sayısal) + **tutar** (sayı) + (opsiyonel) **KKEG işareti**. Kalem/vergi toplamları **türetilir** (saklanmaz veya türetilmiş alan olarak).

```json
{ "groupByTax": [
  { "expenseType": {"value":"yemek","display":"Yemek","translationCode":"meal…"},
    "taxRate": {"value":"18","display":"%18","translationCode":null},
    "amount": 1000,
    "isKkeg": false },
  { "expenseType": {"value":"ulasim","display":"Ulaşım","translationCode":"transport…"},
    "taxRate": {"value":"8","display":"%8","translationCode":null},
    "amount": 800 }
] }
```
- Boş: anahtar **yok** ya da `[]`.

## 2. Projeksiyon — `projectToAttr=true`
**Kalem × alt-alan** → [`InstanceListItem`](../instance-list-item.md). Her kalem `itemIndex`, her alt-alan `attrCode`:

| `attrCode` | Kolon(lar) |
|---|---|
| `expenseType` | `textValue`=`value` · `display` · `translationCode` |
| `taxRate` | `textValue`/`numValue` (etiketli/sayısal) · `display` |
| `amount` | `numValue` |
| `isKkeg` | `boolValue` |

- `listCode` = alan kodu (`groupByTax`), `itemIndex` = 0,1,2…
- Kalem-bazlı rapor (`SUM(amount) GROUP BY taxRate`) ListItem üzerinden; dosya/binary **MinIO'da** (yalnız URL).

## 3. Notlar
- Kalem alt-alan şeması (`expenseType` · `taxRate` · `amount` · `isKkeg`) **kesinleşti** — eksik/fazla yok (Q3).
- **Toplamlar (dip toplam) `data`'da saklanmaz** — kalem/vergi toplamları **gerektiğinde hesaplanır** (türetilir) (Q4).

*Oluşturma: 2026-08-06.*
