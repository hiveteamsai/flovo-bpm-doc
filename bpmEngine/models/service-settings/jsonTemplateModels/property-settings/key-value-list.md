# Property Settings — `keyValueList` (Key-Value List)

> **propertyType:** `keyValueList` · **Kontrol:** iki sütunlu (**Key** / **Value**) anahtar-değer listesi; kullanıcı **artı** butonuyla satır ekler, **Value** bir **combobox**'tan seçilir.
> **Değer şekli:** → [`../../../processInstances/propertyValuesTemplates/key-value-list.md`](../../../processInstances/propertyValuesTemplates/key-value-list.md) (**obje dizisi**: her satır `key` metni + `value` etiketli seçim [`LabeledValue`]) ·
> **Davranış:** → [`../../../../service-settings/properties.md`](../../../../service-settings/properties.md) §3.18 · **Çekirdek model:** [`../../property.md`](../../property.md) · **Değer modeli:** [`../../../processInstances/instance-list-item.md`](../../../processInstances/instance-list-item.md) · **İndeks:** [`index.md`](./index.md).

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `addNewEnabled` | bool | hayır | `true` | Kullanıcı **yeni satır ekleyebilir** mi (artı butonu). `false` = liste sabit; yalnız `keyValueItems`'tan gelen satırlar düzenlenir. |
| `deleteEnabled` | bool | hayır | `true` | Kullanıcı **satır silebilir** mi. `false` = satırlar kaldırılamaz. |
| `keyDescription` | string? | hayır | `null` | **Key** sütununun başlığı (arayüzde gösterilen etiket). `null` = varsayılan başlık. |
| `valueDescription` | string? | hayır | `null` | **Value** sütununun başlığı. `null` = varsayılan başlık. |
| `comboBoxItems` | array\<obje\> | hayır | `[]` | **Value combobox'ının seçenek kaynağı** — her satırdaki Value hücresinde seçilebilecek sabit seçenekler. Öğe şekli: `{ value, definition, translationCode }` (PropertyItem konvansiyonu; `definition` = varsayılan dil metni, `translationCode` = çeviri anahtarı → [`../../property-item.md`](../../property-item.md)). **İstisna:** combobox statik seçenekleri normalde ayrı `PropertyItem` alt-tablosunda tutulur; `keyValueList`'te Value seçenekleri **`settings`'e gömülüdür** (alanın kendi iç combobox'ı olduğundan). |
| `keyValueItems` | array\<obje\> | hayır | `[]` | **Başlangıç (seed) çiftleri** — alan ilk açıldığında dolu gelecek satırlar. Öğe şekli: `{ key, value }`; `value` bir etiketli seçim (`{ value, display, translationCode }` — `comboBoxItems`'tan biri) veya `null`. Boş liste = alan boş başlar. |

## 2. Çekirdek kolonda (settings'e girmez)
- **Değer** = satır listesi (`key` metni + `value` etiketli seçim) → `InstanceValue.data`'da **obje dizisi** (değer şablonu §1).
- **Projeksiyon** (`projectToAttr=true`): **satır × alt-alan** → [`InstanceListItem`](../../../processInstances/instance-list-item.md) (`key` → `textValue`; `value` → `textValue`=`value` + `display` + `translationCode`) — değer şablonu §2.
- `savePropertyToDb` · `saveChangeLog` · **`hasTranslation`** (Value etiketli olduğundan seçenek metinleri çeviri kullanabilir) (§1.3).

## 3. Profil-bazlı
- Yok (`keyValueList` için profil-özel ayar tanımlı değil; görünür/düzenlenebilir/zorunlu genel profil alanlarıdır → [`../../view-profile-property.md`](../../view-profile-property.md)).

## 4. Zorunluluk (required) davranışı
- Alan **required** ise (profilde `required=true`): **en az bir** satır bulunmalı **ve tüm satırlar dolu** olmalıdır — `key` boş değil **ve** `value` seçili. Eksik satır varken form geçerli sayılmaz (properties §3.18).

## 5. JSON Schema (`settings`)
```json
{
  "$id": "property-settings/key-value-list",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "addNewEnabled":    { "type": "boolean", "default": true },
    "deleteEnabled":    { "type": "boolean", "default": true },
    "keyDescription":   { "type": ["string", "null"], "default": null },
    "valueDescription": { "type": ["string", "null"], "default": null },
    "comboBoxItems": {
      "type": "array",
      "default": [],
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["value"],
        "properties": {
          "value":           { "type": "string" },
          "definition":      { "type": "string" },
          "translationCode": { "type": ["string", "null"], "default": null }
        }
      }
    },
    "keyValueItems": {
      "type": "array",
      "default": [],
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["key"],
        "properties": {
          "key": { "type": "string" },
          "value": {
            "type": ["object", "null"],
            "additionalProperties": false,
            "required": ["value"],
            "properties": {
              "value":           { "type": "string" },
              "display":         { "type": "string" },
              "translationCode": { "type": ["string", "null"], "default": null }
            }
          }
        }
      }
    }
  }
}
```
> Not: Çalışma-zamanı **değeri** (girilen satırlar) çekirdek/değer katmanındadır; bu şema yalnız alan-düzeyi `settings` (sütun başlıkları · ekleme/silme izni · Value seçenek kaynağı · seed satırlar) JSONB'sini doğrular. `comboBoxItems` içindeki `value` referanslarının seçili değerlerle tutarlılığı **uygulama-katmanı** doğrulamasıdır.

## 6. Örnek
```json
{
  "addNewEnabled": true,
  "deleteEnabled": true,
  "keyDescription": "Özellik",
  "valueDescription": "Değer",
  "comboBoxItems": [
    { "value": "red", "definition": "Kırmızı", "translationCode": "color.red" },
    { "value": "L",   "definition": "L",       "translationCode": null }
  ],
  "keyValueItems": [
    { "key": "Renk", "value": { "value": "red", "display": "Kırmızı", "translationCode": "color.red" } }
  ]
}
```

*Oluşturma: 2026-08-28.*
