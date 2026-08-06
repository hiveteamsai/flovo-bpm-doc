# Değer Şablonu — `combobox` (Combobox)

> **Durum:** 🟡 TASLAK — ilk çıkarım; düzenlenecek.
> **Kapsam:** `combobox` değerinin **`InstanceValue.data` içindeki şekli** + **`projectToAttr=true`** iken fihriste yansıması. Üç mod: **tekli** · **çoklu** (`isMultiSelect`) · **ilişkili** (`isAssociatedCombobox`).
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
Seçilen **instance'ın id'si** `value`'ya yazılır; `display` seçilen instance'ın etiketidir. İlişkinin **asıl kaydı** ayrıca [`AssociatedInstance`](../associated-instance.md)'e düşer (`data`'daki bu kopya **görüntü/hızlı erişim** içindir).
```json
{ "relatedExpense": { "value": "45821", "display": "Masraf #45821", "translationCode": null } }
```
- Boş/seçilmemiş: anahtar **yok** ya da `null` (dizi modunda `[]`).

## 2. Projeksiyon — `projectToAttr=true`
| Mod | Hedef | Kolon eşlemesi |
|---|---|---|
| **Tekli** | **InstanceAttr** | `textValue`=`value` · `display` · `translationCode` |
| **Çoklu** | **InstanceListItem** | her seçim = `itemIndex` satırı; `attrCode`=`"value"` (sabit) · `textValue`=`value` · `display` · `translationCode` |
| **İlişkili** | **InstanceAttr** | `numValue`=instance id **ve** `textValue`=instance id (**ikisi birden**) · `display` (instance etiketi); ilişki sorguları **`AssociatedInstance`** üzerinden |

- İsimle arama: `display ILIKE '%…%'` (dil çözümü → [`labeled-value.md`](./labeled-value.md) "Okuma kuralı").

## 3. Notlar
- **Çoklu seçim** tek `InstanceAttr` satırına sığmadığından **`InstanceListItem`**'a açılır; `attrCode`=`"value"` (sabit — Q1).
- **İlişkili** modda seçilen instance id **hem `numValue` hem `textValue`**'da tutulur (Q2: numerik id-filtre/join + metin); ilişkinin kaynağı `AssociatedInstance`.
- **Statik** liste display'i `PropertyItem.definition`/`translationCode`'dan; **dinamik** (iş kuralı `fillDataSource`/API) listede istekle gelir → [`labeled-value.md`](./labeled-value.md).

*Oluşturma: 2026-08-06.*
