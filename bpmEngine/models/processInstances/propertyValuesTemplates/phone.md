# Değer Şablonu — `phone` (Phone)

> **Durum:** 🟡 TASLAK — ilk çıkarım; düzenlenecek.
> **Kapsam:** `phone` değerinin **`InstanceValue.data` içindeki şekli** + **`projectToAttr=true`** iken fihriste yansıması.
> **Alan davranışı:** → [`../../../service-settings/properties.md`](../../../service-settings/properties.md) §3.11 · **model:** [`../../service-settings/property.md`](../../service-settings/property.md) · **değer modeli:** [`../instance-value.md`](../instance-value.md) · [`../instance-attr.md`](../instance-attr.md).

## 1. JSONB değer şekli — `data["<code>"]`
**Obje** — ülke kodu ve numara **ayrı** tutulur:

| Alan | Tip | Açıklama |
|---|---|---|
| `countryCode` | string | Ülke/arama kodu (ör. `"+90"`). |
| `number` | string | Ülke kodu **dışındaki** numara — **maskeli metin** olarak saklanır (Q9; ör. `"532 123 45 67"`). |

```json
{ "phone": { "countryCode": "+90", "number": "532 123 45 67" } }
```
- Boş/girilmemiş: değer **`null`** (anahtar her zaman bulunur — `code` ile; → [`../instance-value.md`](../instance-value.md)).
- `number` **maskeli (görünen) biçimde** `text` olarak tutulur (Q9) — ham rakama normalize edilmez.

## 2. Projeksiyon — `projectToAttr=true`
| Kaynak | Hedef | Kolon |
|---|---|---|
| `data["<code>"]` (`countryCode`+`number` birleşik) | **InstanceAttr** | `textValue` = **normalize** tam numara (ör. `"+905321234567"`) |

- **Projektör maskeyi soyar:** `number`'daki rakam-dışı karakterler (boşluk/tire/parantez) **atılır** ve `countryCode` ile birleştirilir → yalnız-rakam (E.164 benzeri) tam numara `textValue`'ya yazılır. **Kaynak `data`'daki `number` maskeli kalır** (normalize yalnız fihrist içindir; §1 Q9).
- Diğer kolonlar = **null**.
- Arama normalize numara üzerinden `textValue`; tam eşitlik ayrıca `data` GIN'iyle (alt-alan `countryCode`/`number` bazlı da sorgulanabilir).

## 3. Notlar
- `number` **maskeli metin** olarak saklanır (Q9); arama maskeli değer üzerinden `textValue`.

*Oluşturma: 2026-08-06.*
