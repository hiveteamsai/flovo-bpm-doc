# Değer Şablonu — `datepicker` (Datepicker)

> **Durum:** 🟡 TASLAK — ilk çıkarım; düzenlenecek.
> **Kapsam:** `datepicker` değerinin **`InstanceValue.data` içindeki şekli** + **`projectToAttr=true`** iken fihriste yansıması.
> **Alan davranışı:** → [`../../../service-settings/properties.md`](../../../service-settings/properties.md) §3.4 · **model:** [`../../service-settings/property.md`](../../service-settings/property.md) · **değer modeli:** [`../instance-value.md`](../instance-value.md) · [`../instance-attr.md`](../instance-attr.md).

## 1. JSONB değer şekli — `data["<code>"]`
**Sadece-tarih ISO string** — `"YYYY-MM-DD"`; **saat bileşeni YOKTUR.** Datepicker yalnız **takvim günü** tutar. Saat ayrıca gerekiyorsa **ayrı bir `timePicker`** alanında tutulur (tarih + saat = iki ayrı property). Görünüm formatı (`format`) sunumdadır; saklanan değer **kanonik `YYYY-MM-DD`**'dir.

```json
{ "invoiceDate": "2026-08-06" }
```
- Boş/girilmemiş: değer **`null`** (anahtar her zaman bulunur — `code` ile; → [`../instance-value.md`](../instance-value.md)).

## 2. Projeksiyon — `projectToAttr=true`
| Kaynak | Hedef | Kolon |
|---|---|---|
| `data["<code>"]` (`YYYY-MM-DD`) | **InstanceAttr** | `dateValue` (**takvim tarihi** — `date`; saat/tz **yok**) |

- Diğer kolonlar = **null**.
- Aralık/sıralama (`BETWEEN`, `ORDER BY`) `dateValue` btree ile — **takvim günü** karşılaştırması.

## 3. Notlar
- **Saat dilimi dönüşümü YOK:** sadece-tarih olduğundan değer **olduğu gibi** (takvim günü) gösterilir; UTC↔yerel dönüşümü yapılmaz → **gün kayması olmaz**.
- **Saat gerekliyse ayrı `timePicker`** alanı kullanılır — datepicker saat taşımaz.

*Oluşturma: 2026-08-06.*
