# Değer Şablonu — `mapViewer` (Map Viewer)

> **Durum:** 🟡 TASLAK — ilk çıkarım; düzenlenecek.
> **Kapsam:** `mapViewer` değerinin **`InstanceValue.data` içindeki şekli** (yapısal JSON) + **`projectToAttr=true`** iken fihriste yansıması.
> **Alan davranışı:** → [`../../../service-settings/properties.md`](../../../service-settings/properties.md) §3.12 · **model:** [`../../service-settings/property.md`](../../service-settings/property.md) · **değer modeli:** [`../instance-value.md`](../instance-value.md) · [`../instance-attr.md`](../instance-attr.md).

## 1. JSONB değer şekli — `data["<code>"]`
**Yapısal obje** — koordinat + (opsiyonel) adres.

```json
{ "location": { "lat": 41.0082, "lng": 28.9784, "address": "İstanbul, TR" } }
```
- Seçilmemiş: değer **`null`** (anahtar her zaman bulunur — `code` ile; → [`../instance-value.md`](../instance-value.md)).

## 2. Projeksiyon — `projectToAttr=true`
Projekte **edilir** (Q7). Yapısal obje tek `InstanceAttr` satırının skaler kolonlarına tümüyle sığmadığından alt-alan bazlı:

| Alt-alan | Hedef |
|---|---|
| `address` | **InstanceAttr.textValue** (adrese göre arama/sıralama) |
| `lat` / `lng` | `data`'da kalır — eşitlik `GIN`; coğrafi (yakınlık/poligon) **PostGIS** (post-MVP) |

## 3. Notlar
- Coğrafi sorgu (yakınlık/poligon) gerekiyorsa **PostGIS** koşullu geliştirmedir (→ araştırma §22/faz-3); MVP'de `address`→Attr + `data`/GIN yeterli.
- `lat`/`lng`'nin de **indeksli aralık** sorgusu gerekirse `InstanceListItem` (alt-alan satırları) veya PostGIS'e taşınır.

*Oluşturma: 2026-08-06.*
