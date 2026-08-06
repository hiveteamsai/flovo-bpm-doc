# Değer Şablonu — `timePicker` (Time Picker)

> **Durum:** 🟡 TASLAK — ilk çıkarım; düzenlenecek.
> **Kapsam:** `timePicker` değerinin **`InstanceValue.data` içindeki şekli** + **`projectToAttr=true`** iken fihriste yansıması.
> **Alan davranışı:** → [`../../../service-settings/properties.md`](../../../service-settings/properties.md) §3.5 · **model:** [`../../service-settings/property.md`](../../service-settings/property.md) · **değer modeli:** [`../instance-value.md`](../instance-value.md) · [`../instance-attr.md`](../instance-attr.md).

## 1. JSONB değer şekli — `data["<code>"]`
Sabit-genişlikli **`"HH:mm"`** (veya `format`'a göre `"HH:mm:ss"`) **`string`**. Tarih bileşeni yoktur.

```json
{ "startTime": "14:30" }
```
- Boş/girilmemiş: anahtar **yok** ya da `null`.

## 2. Projeksiyon — `projectToAttr=true`
| Kaynak | Hedef | Kolon |
|---|---|---|
| `data["<code>"]` (`"HH:mm"`) | **InstanceAttr** | `textValue` |

- Sabit-genişlik olduğundan `textValue` üzerinde **metin sıralaması = kronolojik sıralamadır** (`"09:00" < "14:30"`).
- Diğer kolonlar = **null**.

## 3. Notlar
- Saat **`textValue`**'da `"HH:mm"` olarak tutulur (Q8) — `timeValue` kolonu **yok**; sabit-genişlik olduğundan metin sıralaması = kronolojik sıralamadır.

*Oluşturma: 2026-08-06.*
