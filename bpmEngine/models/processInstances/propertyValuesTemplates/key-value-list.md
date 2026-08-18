# Değer Şablonu — `keyValueList` (Key-Value List)

> **Durum:** 🟡 TASLAK — ilk çıkarım; düzenlenecek.
> **Kapsam:** `keyValueList` değerinin **`InstanceValue.data` içindeki şekli** (liste-of-model) + **`projectToAttr=true`** iken fihriste yansıması.
> **Alan davranışı:** → [`../../../service-settings/properties.md`](../../../service-settings/properties.md) §3.18 · **model:** [`../../service-settings/property.md`](../../service-settings/property.md) · **değer modeli:** [`../instance-list-item.md`](../instance-list-item.md) · **şekil:** [`labeled-value.md`](./labeled-value.md).

## 1. JSONB değer şekli — `data["<code>"]`
**Obje dizisi**. Her satır: **`key`** (metin) + **`value`** (combobox seçimi → etiketli `LabeledValue`).

```json
{ "attributes": [
  { "key": "Renk", "value": {"value":"red","display":"Kırmızı","translationCode":"red…"} },
  { "key": "Beden", "value": {"value":"L","display":"L","translationCode":null} }
] }
```
- Boş: değer **`[]`** (anahtar her zaman bulunur — `code` ile; → [`../instance-value.md`](../instance-value.md)).

## 2. Projeksiyon — `projectToAttr=true`
**Satır × alt-alan** → [`InstanceListItem`](../instance-list-item.md). Her satır `itemIndex`:

| `attrCode` | Kolon(lar) |
|---|---|
| `key` | `textValue` |
| `value` | `textValue`=`value` · `display` · `translationCode` |

- `listCode` = alan kodu, `itemIndex` = 0,1,2…
- Value etiketli olduğundan `display`/`translationCode` çözümü → [`labeled-value.md`](./labeled-value.md).

## 3. Notlar
- `value` **combobox** olduğundan etiketli değer kuralları geçerli; `key` düz metin (çeviri yok).

*Oluşturma: 2026-08-06.*
