# Değer Şablonu — `checkbox` (Checkbox)

> **Durum:** 🟡 TASLAK — ilk çıkarım; düzenlenecek.
> **Kapsam:** `checkbox` değerinin **`InstanceValue.data` içindeki şekli** + **`projectToAttr=true`** iken fihriste yansıması.
> **Alan davranışı:** → [`../../../service-settings/properties.md`](../../../service-settings/properties.md) §3.6 · **model:** [`../../service-settings/property.md`](../../service-settings/property.md) · **değer modeli:** [`../instance-value.md`](../instance-value.md) · [`../instance-attr.md`](../instance-attr.md).

## 1. JSONB değer şekli — `data["<code>"]`
Düz **`bool`** (`true`/`false`). `defaultValue` başlangıç değerini belirler.

```json
{ "isUrgent": true }
```
- Girilmemiş: değer **`defaultValue`/`false`** (anahtar her zaman bulunur — `code` ile; → [`../instance-value.md`](../instance-value.md)).

## 2. Projeksiyon — `projectToAttr=true`
| Kaynak | Hedef | Kolon |
|---|---|---|
| `data["<code>"]` (bool) | **InstanceAttr** | `boolValue` |

- Diğer kolonlar = **null**.
- Filtre: `boolValue = true`.

## 3. Notlar
- İki-durumlu olduğundan çeviri/`display` **yoktur**; etiketli değer değildir.

*Oluşturma: 2026-08-06.*
