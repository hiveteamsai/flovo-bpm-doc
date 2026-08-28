# Property Settings — `phone` (Phone)

> **propertyType:** `phone` · **Kontrol:** telefon numarası girişi; **ülke kodu + numara** ayrı tutulur.
> **Değer şekli:** → [`../../../processInstances/propertyValuesTemplates/phone.md`](../../../processInstances/propertyValuesTemplates/phone.md) (obje `{countryCode, number}`; projeksiyonda normalize `textValue`) ·
> **Davranış:** → [`../../../../service-settings/properties.md`](../../../../service-settings/properties.md) §3.11 · **Çekirdek model:** [`../../property.md`](../../property.md) · **İndeks:** [`index.md`](./index.md).

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `keyboardType` | [`KeyboardType`](../../../enums/keyboard-type.md) | hayır | `telephone` | Numara girişinde açılacak **sanal klavye** — telefon alanında tipik olarak `telephone` (numara tuş takımı). Yalnız render/istemci davranışı. `default`·`plain`·`text`·`numeric`·`email`·`url`·`telephone`. |

## 2. Çekirdek kolonda (settings'e girmez)
- `format` (string) — **numara maskesi** (ör. `"### ### ## ##"`); numara **maskeli (görünen) biçimde** saklanır (değer şablonu §1, Q9), ham rakama normalize edilmez. Maske çekirdek `format` kolonundadır (§1.3).
- `defaultValue` (obje) — başlangıç değeri; şekli bu tipte **`{countryCode, number}`** (değer şablonu §1). Örn. varsayılan ülke kodu bu obje ile verilir (ayrı bir "varsayılan ülke kodu" ayarı yoktur).
- `hint` (string) · `helperText` (string) — yardım metinleri (§1.2).
- Değer-saklama/projeksiyon metadata'sı: `savePropertyToDb` · `projectToAttr` · `saveChangeLog` (§1.3). `projectToAttr=true` iken **projektör maskeyi soyar** ve `countryCode`+`number`'ı birleştirip **yalnız-rakam** (E.164 benzeri, ör. `"+905321234567"`) `InstanceAttr.textValue`'ya yazar; kaynak `data`'daki `number` maskeli kalır (değer şablonu §2).

## 3. Profil-bazlı
- Yok (`phone` için profil-özel ayar tanımlı değil; görünür/düzenlenebilir/zorunlu genel profil alanlarıdır → [`../../view-profile-property.md`](../../view-profile-property.md)).

## 4. JSON Schema
```json
{
  "$id": "property-settings/phone",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "keyboardType": { "enum": ["default", "plain", "text", "numeric", "email", "url", "telephone"], "default": "telephone" }
  }
}
```
> Not: `format` (maske) ve `defaultValue` (`{countryCode, number}`) **çekirdek kolon** olduğundan bu şemada yer almaz; şema yalnız `settings` JSONB'yi doğrular. `keyboardType` saf render davranışı olduğundan (sınır kuralı) `textbox` ile tutarlı biçimde `settings`'tedir.

## 5. Örnek
```json
{ "keyboardType": "telephone" }
```

*Oluşturma: 2026-08-28.*
