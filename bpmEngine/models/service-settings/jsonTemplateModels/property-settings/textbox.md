# Property Settings — `textbox` (Textbox)

> **propertyType:** `textbox` · **Kontrol:** yazı yazılabilen alan; `minLine`/`maxLine` ile tek-satır ya da çok-satırlı.
> **Değer şekli:** → [`../../../processInstances/propertyValuesTemplates/textbox.md`](../../../processInstances/propertyValuesTemplates/textbox.md) (`string`, Attr `textValue`) ·
> **Davranış:** → [`../../../../service-settings/properties.md`](../../../../service-settings/properties.md) §3.1 · **Çekirdek model:** [`../../property.md`](../../property.md) · **İndeks:** [`index.md`](./index.md).

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `minLine` | int | hayır | `1` | Minimum satır sayısı. `1` = tek satır. `>1` = çok satırlı giriş (ayrı textarea tipi yok). `minLine ≥ 1`. |
| `maxLine` | int | hayır | `null` | Maksimum satır sayısı (`null` = sınırsız). Verilirse `maxLine ≥ minLine`. |
| `charMaxLength` | int | hayır | `null` | Maksimum karakter sayısı (`null` = sınırsız). `≥ 0`. |
| `showCharCount` | bool | hayır | `false` | Karakter sayacı gösterilsin mi (genelde `charMaxLength` ile). |
| `keyboardType` | [`KeyboardType`](../../../enums/keyboard-type.md) | hayır | `default` | Sanal klavye tipi — `default`·`plain`·`text`·`numeric`·`email`·`url`·`telephone`. |

## 2. Çekirdek kolonda (settings'e girmez)
- `hint` (string) · `helperText` (string) — yardım metinleri (§1.2).
- `defaultValue` (string) — başlangıç değeri; şekli bu tipte **string** (§1.3).
- `format` (string) — giriş **maskesi** (varsa); serbest maske deseni (§1.3).
- Değer-saklama/projeksiyon metadata'sı: `savePropertyToDb` · `projectToAttr` · `saveChangeLog` · `hasTranslation` (§1.3).

## 3. Profil-bazlı
- Yok (`textbox` için profil-özel ayar tanımlı değil; görünür/düzenlenebilir/zorunlu genel profil alanlarıdır → [`../../view-profile-property.md`](../../view-profile-property.md)).

## 4. JSON Schema
```json
{
  "$id": "property-settings/textbox",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "minLine":       { "type": "integer", "minimum": 1, "default": 1 },
    "maxLine":       { "type": ["integer", "null"], "minimum": 1, "default": null },
    "charMaxLength": { "type": ["integer", "null"], "minimum": 0, "default": null },
    "showCharCount": { "type": "boolean", "default": false },
    "keyboardType":  { "enum": ["default", "plain", "text", "numeric", "email", "url", "telephone"], "default": "default" }
  }
}
```
> Not: `maxLine ≥ minLine` çapraz-kısıtı JSON Schema ile ifade edilemez → **uygulama-katmanı** doğrulaması.

## 5. Örnek
```json
{ "minLine": 1, "maxLine": 4, "charMaxLength": 250, "showCharCount": true, "keyboardType": "text" }
```

*Oluşturma: 2026-08-28.*
