# Değer Şablonu — `numericTextbox` (Numeric Textbox)

> **Durum:** 🟡 TASLAK — ilk çıkarım; düzenlenecek.
> **Kapsam:** `numericTextbox` değerinin **`InstanceValue.data` içindeki şekli** + **`projectToAttr=true`** iken fihriste yansıması.
> **Alan davranışı:** → [`../../../service-settings/properties.md`](../../../service-settings/properties.md) §3.2 · **model:** [`../../service-settings/property.md`](../../service-settings/property.md) · **değer modeli:** [`../instance-value.md`](../instance-value.md) · [`../instance-attr.md`](../instance-attr.md).

## 1. JSONB değer şekli — `data["<code>"]`
Düz **`number`** (tam sayı veya ondalık). `maxDecimalDigits`/`enableNegative`/`integerActive` yalnız **giriş kısıtıdır**; saklanan değer sayıdır. Binlik ayraç (`enableGroupSeperator`) yalnız görünümdür — **ham sayı** saklanır.

```json
{ "amount": 1800.50 }
```
- Boş/girilmemiş: anahtar **yok** ya da `null`.

## 2. Projeksiyon — `projectToAttr=true`
| Kaynak | Hedef | Kolon |
|---|---|---|
| `data["<code>"]` (number) | **InstanceAttr** | `numValue` (numeric) |

- Diğer kolonlar = **null**.
- **Aralık/sıralama/toplam** doğrudan `numValue` btree ile (`> 1000`, `ORDER BY`, `SUM`). Tip kaybı yok (`9 < 10` doğru).

## 3. Notlar
- Para/oran/miktar gibi rapor-filtre alanları tipik olarak **`projectToAttr=true`**.

*Oluşturma: 2026-08-06.*
