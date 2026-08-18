# Değer Şablonu — `groupByTaxReceipt` (Group By Tax Receipt)

> **Durum:** 🟡 TASLAK — ilk çıkarım; düzenlenecek.
> **Kapsam:** `groupByTaxReceipt` değerinin **`InstanceValue.data` içindeki şekli** (liste-of-model) + **`projectToAttr=true`** iken fihriste yansıması.
> **Alan davranışı:** → [`../../../service-settings/properties.md`](../../../service-settings/properties.md) §3.17 · **model:** [`../../service-settings/property.md`](../../service-settings/property.md) · **değer modeli:** [`../instance-list-item.md`](../instance-list-item.md) · **şekil:** [`labeled-value.md`](./labeled-value.md).

## 1. JSONB değer şekli — `data["<code>"]`
**Obje dizisi** (kalem listesi). Her kalem: **gider türü** (`expenseType` — etiketli seçim, şirketin gider türü listesinden; `PropertyItem` gibi `translationCode`'lu) + **vergi oranı** (`taxRate` — **sayısal**, oran değerini tutar, ör. `18`) + **tutar** (`amount` — sayı) + (opsiyonel) **KKEG işareti** (`isKkeg` — bool). Kalem/vergi toplamları **türetilir** (saklanmaz veya türetilmiş alan olarak).

```json
{ "groupByTax": [
  { "expenseType": {"value":"yemek","display":"Yemek","translationCode":"meal…"},
    "taxRate": 18,
    "amount": 1000,
    "isKkeg": false },
  { "expenseType": {"value":"ulasim","display":"Ulaşım","translationCode":"transport…"},
    "taxRate": 8,
    "amount": 800 }
] }
```
- Boş: değer **`[]`** (anahtar her zaman bulunur — `code` ile; → [`../instance-value.md`](../instance-value.md)).

## 2. Projeksiyon — `projectToAttr=true`
**Kalem × alt-alan** → [`InstanceListItem`](../instance-list-item.md). Her kalem `itemIndex`, her alt-alan `attrCode`:

| `attrCode` | Kolon(lar) |
|---|---|
| `expenseType` | `textValue`=`value` · `display` · `translationCode` (etiketli — gider türü listesi) |
| `taxRate` | `numValue` (oran değeri; **etiketsiz** — `display`/`translationCode` **yok**) |
| `amount` | `numValue` |
| `isKkeg` | `boolValue` |

- `listCode` = alan kodu (`groupByTax`), `itemIndex` = 0,1,2…
- Kalem-bazlı rapor (`SUM(amount) GROUP BY taxRate`) ListItem üzerinden; dosya/binary **MinIO'da** (yalnız URL).

## 3. Notlar
- Kalem alt-alan şeması (`expenseType` · `taxRate` · `amount` · `isKkeg`) **kesinleşti** — eksik/fazla yok (Q3). **Tipler:** `expenseType` **etiketli** (`LabeledValue` + `translationCode` — şirketin gider türü listesinden, combobox `dataSource`/`propertyItem` gibi) · `taxRate` **sayısal** (oran değeri; etiketsiz) · `amount` sayı · `isKkeg` bool.
- **Toplamlar (dip toplam) `data`'da saklanmaz** — kalem/vergi toplamları **gerektiğinde hesaplanır** (türetilir) (Q4).

*Oluşturma: 2026-08-06.*
