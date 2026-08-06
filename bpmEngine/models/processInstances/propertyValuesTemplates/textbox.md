# Değer Şablonu — `textbox` (Textbox)

> **Durum:** 🟡 TASLAK — ilk çıkarım; düzenlenecek.
> **Kapsam:** `textbox` değerinin **`InstanceValue.data` içindeki şekli** + **`projectToAttr=true`** iken fihriste yansıması.
> **Alan davranışı:** → [`../../../service-settings/properties.md`](../../../service-settings/properties.md) §3.1 · **model:** [`../../service-settings/property.md`](../../service-settings/property.md) · **değer modeli:** [`../instance-value.md`](../instance-value.md) · [`../instance-attr.md`](../instance-attr.md).

## 1. JSONB değer şekli — `data["<code>"]`
Düz **`string`**. `minLine`/`maxLine` yalnız görünümü (tek/çok satır) değiştirir; tip yine string'tir.

```json
{ "note": "Ödeme açıklaması...\nİkinci satır" }
```
- Boş/girilmemiş: anahtar **yok** ya da `null`.

## 2. Projeksiyon — `projectToAttr=true`
| Kaynak | Hedef | Kolon |
|---|---|---|
| `data["<code>"]` (string) | **InstanceAttr** | `textValue` |

- Diğer kolonlar (`numValue`/`dateValue`/`boolValue`/`display`/`translationCode`) = **null** (etiketsiz skaler).
- İsimle/parçayla arama: `textValue` üzerinde **trigram (pg_trgm) GIN** → `ILIKE '%…%'`; tam eşitlik ayrıca `data` GIN'iyle de bulunur.

## 3. Notlar
- Uzun / nadiren aranan metinler (açıklama, imza notu) için **`projectToAttr=false`** önerilir — fihristi şişirmez, eşitlik yine `data` GIN'iyle çözülür.

*Oluşturma: 2026-08-06.*
