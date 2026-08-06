# Değer Şablonu — `radiobuttonList` (Radiobutton List)

> **Durum:** 🟡 TASLAK — ilk çıkarım; düzenlenecek.
> **Kapsam:** `radiobuttonList` değerinin **`InstanceValue.data` içindeki şekli** + **`projectToAttr=true`** iken fihriste yansıması.
> **Alan davranışı:** → [`../../../service-settings/properties.md`](../../../service-settings/properties.md) §3.7 · **model:** [`../../service-settings/property.md`](../../service-settings/property.md) · **şekil:** [`labeled-value.md`](./labeled-value.md) · **değer modeli:** [`../instance-attr.md`](../instance-attr.md).

## 1. JSONB değer şekli — `data["<code>"]`
**Tekli seçim** → tek **`LabeledValue`** (`{value, display, translationCode}`). (Combobox tekli mod ile aynı şekil; radiobutton **çoklu değildir**.)

```json
{ "priority": { "value": "1", "display": "Yüksek", "translationCode": "high…" } }
```
- Seçilmemiş: anahtar **yok** ya da `null`.

## 2. Projeksiyon — `projectToAttr=true`
| Kaynak | Hedef | Kolon eşlemesi |
|---|---|---|
| `data["<code>"]` (LabeledValue) | **InstanceAttr** | `textValue`=`value` · `display` · `translationCode` |

- İsimle arama/sıralama: `display` (dil çözümü → [`labeled-value.md`](./labeled-value.md)); kodla filtre: `textValue`.

## 3. Notlar
- Seçenek kaynağı statik `PropertyItem` **veya** dinamik iş kuralı (`fillDataSource`) — Combobox ile aynı (→ properties §2.4).

*Oluşturma: 2026-08-06.*
