# Property Settings — `numericTextbox` (Numeric Textbox)

> **propertyType:** `numericTextbox` · **Kontrol:** yalnız sayı girilen alan; ondalık/negatif/binlik-ayraç giriş kısıtlarıyla.
> **Değer şekli:** → [`../../../processInstances/propertyValuesTemplates/numeric-textbox.md`](../../../processInstances/propertyValuesTemplates/numeric-textbox.md) (düz `number`, Attr `numValue`) ·
> **Davranış:** → [`../../../../service-settings/properties.md`](../../../../service-settings/properties.md) §3.2 · **Çekirdek model:** [`../../property.md`](../../property.md) · **İndeks:** [`index.md`](./index.md).

## 1. `settings` (JSONB) — tipe-özel ayarlar
> Hepsi **giriş kısıtı/görünüm** ayarıdır — saklanan değer her zaman **ham sayı**dır (§2, değer şablonu §1). Bu yüzden hiçbiri projeksiyonu değiştirmez; yalnız render/istemci davranışıdır.

| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `maxDecimalDigits` | int | hayır | `2` | İzin verilen **maksimum ondalık basamak** sayısı. Yalnız giriş/gösterim kısıtı; ham sayı tam duyarlıkla saklanır. `≥ 0`. `integerActive=true` iken **yok sayılır** (0 kabul edilir). |
| `enableNegative` | bool | hayır | `false` | **Negatif** değere izin. `false` = yalnız `≥ 0`. Giriş doğrulama kısıtı. |
| `enableGroupSeperator` | bool | hayır | `false` | **Binlik ayraç** (ör. `1.800,50`) gösterilsin mi. Yalnız **görünüm**dür; `data`'ya ham sayı (`1800.5`) yazılır (değer şablonu §1). |
| `integerActive` | bool | hayır | `false` | **Tam sayı** modu — ondalık girişi kapatır. `true` iken `maxDecimalDigits` etkisizdir. |

## 2. Çekirdek kolonda (settings'e girmez)
- `defaultValue` (number) — başlangıç değeri; şekli bu tipte **number** (§1.3).
- `hint` (string) · `helperText` (string) — yardım metinleri (§1.2).
- Değer-saklama/projeksiyon metadata'sı: `savePropertyToDb` · `projectToAttr` · `saveChangeLog` (§1.3). Para/oran/miktar gibi rapor-filtre alanları tipik olarak `projectToAttr=true` → `InstanceAttr.numValue` (btree; aralık/sıra/`SUM`, değer şablonu §2).

## 3. Profil-bazlı
- Yok (`numericTextbox` için profil-özel ayar tanımlı değil; görünür/düzenlenebilir/zorunlu genel profil alanlarıdır → [`../../view-profile-property.md`](../../view-profile-property.md)).

## 4. JSON Schema
```json
{
  "$id": "property-settings/numericTextbox",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "maxDecimalDigits":     { "type": "integer", "minimum": 0, "default": 2 },
    "enableNegative":       { "type": "boolean", "default": false },
    "enableGroupSeperator": { "type": "boolean", "default": false },
    "integerActive":        { "type": "boolean", "default": false }
  }
}
```
> Not: `integerActive=true ⟹ maxDecimalDigits` yok sayılır çapraz-etkisi JSON Schema ile ifade edilmez → **uygulama-katmanı** yorumu (render + doğrulama).

## 5. Örnek
```json
{ "maxDecimalDigits": 2, "enableNegative": false, "enableGroupSeperator": true, "integerActive": false }
```

*Oluşturma: 2026-08-28.*
