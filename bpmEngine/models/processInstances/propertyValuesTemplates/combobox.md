# Değer Şablonu — `combobox` (Combobox)

> **Durum:** 🟡 TASLAK — ilk çıkarım; düzenlenecek.
> **Kapsam:** `combobox` değerinin **`InstanceValue.data` içindeki şekli** + **`projectToAttr=true`** iken fihriste yansıması. **İki bağımsız boyut (2×2):** seçim adedi (**tekli** / **çoklu**=`isMultiSelect`) × kaynak (**düz liste** / **ilişkili**=`isAssociatedCombobox`) — dört kombinasyon da geçerlidir.
> **Alan davranışı:** → [`../../../service-settings/properties.md`](../../../service-settings/properties.md) §3.3 · **model:** [`../../service-settings/property.md`](../../service-settings/property.md) · **şekil:** [`labeled-value.md`](./labeled-value.md) · **değer modelleri:** [`../instance-attr.md`](../instance-attr.md) · [`../instance-list-item.md`](../instance-list-item.md) · [`../associated-instance.md`](../associated-instance.md).

## 1. JSONB değer şekli — `data["<code>"]`

### 1a. Tekli (varsayılan)
Tek **`LabeledValue`** — `{value, display, translationCode}` (→ [`labeled-value.md`](./labeled-value.md)).
```json
{ "expenseType": { "value": "2", "display": "Ulaşım", "translationCode": "transport…" } }
```

### 1b. Çoklu (`isMultiSelect=true`)
**`LabeledValue` dizisi**.
```json
{ "tags": [
  { "value": "1", "display": "Acil", "translationCode": null },
  { "value": "5", "display": "Onaylı", "translationCode": "approved…" }
] }
```

### 1c. İlişkili (`isAssociatedCombobox=true`, `associatedServiceId` dolu)
Seçilen **instance'ın id'si** `value`'ya yazılır; `display` seçilen instance'ın etiketidir. **Her** seçilen instance için ilişkinin **asıl kaydı** [`AssociatedInstance`](../associated-instance.md)'e düşer (`data`'daki bu kopya **görüntü/hızlı erişim** içindir). İlişkili mod **`isMultiSelect` ile birleşebilir** — o zaman **tek alan birden çok instance'ı ilişkilendirir** (Form List'in bir instance'ı birden çok kayda bağlaması gibi):

- **Tekli · ilişkili:** tek `LabeledValue` (`value`=id) → **1** `AssociatedInstance`.
```json
{ "relatedExpense": { "value": "45821", "display": "Masraf #45821", "translationCode": null } }
```
- **Çoklu · ilişkili** (`isMultiSelect=true`): `LabeledValue` **dizisi** (her `value`=id) → **her id için 1** `AssociatedInstance`.
```json
{ "relatedExpenses": [
  { "value": "45821", "display": "Masraf #45821", "translationCode": null },
  { "value": "45830", "display": "Masraf #45830", "translationCode": null }
] }
```
- Boş/seçilmemiş: değer **`null`** (çoklu modda **`[]`**); anahtar her zaman bulunur — `code` ile (→ [`../instance-value.md`](../instance-value.md)).

## 2. Projeksiyon — `projectToAttr=true`
| Mod | Hedef | Kolon eşlemesi |
|---|---|---|
| **Tekli · düz** | **InstanceAttr** | `textValue`=`value` · `display` · `translationCode` |
| **Çoklu · düz** | **InstanceListItem** | her seçim = `itemIndex`; `attrCode`=`"value"` (sabit) · `textValue`=`value` · `display` · `translationCode` |
| **Tekli · ilişkili** | **InstanceAttr** | `numValue`=id **ve** `textValue`=id (**ikisi birden**) · `display`; ilişki sorguları **`AssociatedInstance`** üzerinden |
| **Çoklu · ilişkili** | **InstanceListItem** | her seçim = `itemIndex`; `attrCode`=`"value"` · `numValue`=id · `textValue`=id · `display`; **her id bir `AssociatedInstance`** kaydı |

- İsimle arama: `display ILIKE '%…%'` (dil çözümü → [`labeled-value.md`](./labeled-value.md) "Okuma kuralı").

## 3. Notlar
- **İki boyut bağımsız (2×2):** `isMultiSelect` (adet) ve `isAssociatedCombobox` (kaynak) **serbestçe birleşir**. **Çoklu + ilişkili** = tek alanla **birden çok instance ilişkilendirme** (Form List'in bir instance'ı birden çok kayda bağlaması gibi); her seçim ayrı bir `AssociatedInstance` kaydıdır.
- **Çoklu seçim** tek `InstanceAttr` satırına sığmadığından **`InstanceListItem`**'a açılır; `attrCode`=`"value"` (sabit — Q1).
- **İlişkili** modda seçilen instance id **hem `numValue` hem `textValue`**'da tutulur (Q2: numerik id-filtre/join + metin); ilişkinin kaynağı `AssociatedInstance`.
- **Statik** liste display'i `PropertyItem.definition`/`translationCode`'dan; **dinamik** (iş kuralı `fillDataSource`/API) listede istekle gelir → [`labeled-value.md`](./labeled-value.md).

*Oluşturma: 2026-08-06.*
