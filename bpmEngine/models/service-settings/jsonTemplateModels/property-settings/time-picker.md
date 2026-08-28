# Property Settings — `timePicker` (Time Picker)

> **propertyType:** `timePicker` · **Kontrol:** günün **saatini** seçtiren alan; değer sabit-genişlikli `"HH:mm"` (tarih bileşeni yok).
> **Değer şekli:** → [`../../../processInstances/propertyValuesTemplates/time-picker.md`](../../../processInstances/propertyValuesTemplates/time-picker.md) (`"HH:mm"` / `"HH:mm:ss"` `string`) ·
> **Davranış:** → [`../../../../service-settings/properties.md`](../../../../service-settings/properties.md) §3.5 · **Çekirdek model:** [`../../property.md`](../../property.md) · **İndeks:** [`index.md`](./index.md).

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `headerText` | string? | hayır | `null` | Saat seçim **pop-up başlığı** — yalnız pop-up açan alanlarda görünür (§2.2 notu). |

> **Not:** `timePicker`'ın kalan iki ayarı (`format`, `defaultValue`) **saf render/değer** olmayıp genel çekirdek kolonlardır → §2. Bu yüzden `settings` yalnız `headerText` taşır.

## 2. Çekirdek kolonda (settings'e girmez)
- `format` (string) — saat **formatı**; `"HH:mm"` (vars.) ya da `"HH:mm:ss"`. Saklanan değer sabit-genişlik olduğundan **metin sıralaması = kronolojik sıralamadır** (`"09:00" < "14:30"`; değer şablonu §2/§3).
- `defaultValue` (string, `"HH:mm"`) — başlangıç saati (§1.3). `hint`/`helperText` yardım metinleri (§1.2).
- Değer-saklama/projeksiyon metadata'sı: `savePropertyToDb` · `projectToAttr` (`true` → **InstanceAttr.textValue**; `timeValue` kolonu yok, sabit-genişlik metin sıralaması kronolojiktir) · `saveChangeLog` (§1.3).

## 3. Profil-bazlı
- Yok (`timePicker` için profil-özel ayar tanımlı değil; görünür/düzenlenebilir/zorunlu genel profil alanlarıdır → [`../../view-profile-property.md`](../../view-profile-property.md)).

## 4. JSON Schema
```json
{
  "$id": "property-settings/timePicker",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "headerText": { "type": ["string", "null"], "default": null }
  }
}
```
> Not: `format` ve `defaultValue` **çekirdek kolon** olduğundan bu şemada **yer almaz**; şema yalnız `settings` JSONB'yi doğrular.

## 5. Örnek
```json
{ "headerText": "Başlangıç saati" }
```

*Oluşturma: 2026-08-28.*
