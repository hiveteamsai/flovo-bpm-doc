# Değer Şablonu — `barcode` (Barcode)

> **Durum:** 🟡 TASLAK — ilk çıkarım; düzenlenecek.
> **Kapsam:** `barcode` değerinin **`InstanceValue.data` içindeki şekli** + **`projectToAttr=true`** iken fihriste yansıması.
> **Alan davranışı:** → [`../../../service-settings/properties.md`](../../../service-settings/properties.md) §3.10 · **model:** [`../../service-settings/property.md`](../../service-settings/property.md) · **değer modeli:** [`../instance-value.md`](../instance-value.md) · [`../instance-attr.md`](../instance-attr.md).

## 1. JSONB değer şekli — `data["<code>"]`
Düz **`string`** — barkodun **ham değeri**. `barcodeFormat` yalnız render/okuma biçimidir, saklanan değer string'tir (görsel saklanmaz; değerden yeniden render edilir).

```json
{ "barcode": "8690123456789" }
```
- Boş/girilmemiş: anahtar **yok** ya da `null`.

## 2. Projeksiyon — `projectToAttr=true`
| Kaynak | Hedef | Kolon |
|---|---|---|
| `data["<code>"]` (string) | **InstanceAttr** | `textValue` |

- Diğer kolonlar = **null**.
- Barkodla **tam eşitlik** araması çoğunlukla `data` **GIN**'iyle yeterlidir (`projectToAttr=false` bile bulunur); prefix/sıralama gerekiyorsa `textValue`.

## 3. Notlar
- İlgili: Custom ID Creator `createWithBarcode` · `scanBarcode` aksiyonu (→ properties §3.10).

*Oluşturma: 2026-08-06.*
