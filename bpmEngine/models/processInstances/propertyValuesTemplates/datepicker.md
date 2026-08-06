# Değer Şablonu — `datepicker` (Datepicker)

> **Durum:** 🟡 TASLAK — ilk çıkarım; düzenlenecek.
> **Kapsam:** `datepicker` değerinin **`InstanceValue.data` içindeki şekli** + **`projectToAttr=true`** iken fihriste yansıması.
> **Alan davranışı:** → [`../../../service-settings/properties.md`](../../../service-settings/properties.md) §3.4 · **model:** [`../../service-settings/property.md`](../../service-settings/property.md) · **değer modeli:** [`../instance-value.md`](../instance-value.md) · [`../instance-attr.md`](../instance-attr.md).

## 1. JSONB değer şekli — `data["<code>"]`
**ISO-8601 `string`** (UTC). Yalnız tarih veya tarih+saat (`format`/opsiyona göre). Görünüm formatı (`format`) sunumdadır; saklanan değer **kanonik ISO**'dur.

```json
{ "invoiceDate": "2026-08-06T00:00:00Z" }
```
- Boş/girilmemiş: anahtar **yok** ya da `null`.

## 2. Projeksiyon — `projectToAttr=true`
| Kaynak | Hedef | Kolon |
|---|---|---|
| `data["<code>"]` (ISO string) | **InstanceAttr** | `dateValue` (timestamptz) |

- Diğer kolonlar = **null**.
- Aralık/sıralama (`BETWEEN`, `ORDER BY`) `dateValue` btree ile.

## 3. Notlar
- Saklama **UTC**; görüntüleme kullanıcının/organizasyonun saat dilimine göre çözülür (sunum katmanı).

*Oluşturma: 2026-08-06.*
