# Property Settings — `checkbox` (Checkbox)

> **propertyType:** `checkbox` · **Kontrol:** iki-durumlu tikleme alanı (işaretli/işaretsiz).
> **Değer şekli:** → [`../../../processInstances/propertyValuesTemplates/checkbox.md`](../../../processInstances/propertyValuesTemplates/checkbox.md) (düz `bool`, Attr `boolValue`) ·
> **Davranış:** → [`../../../../service-settings/properties.md`](../../../../service-settings/properties.md) §3.6 · **Çekirdek model:** [`../../property.md`](../../property.md) · **İndeks:** [`index.md`](./index.md).

## 1. `settings` (JSONB) — tipe-özel ayarlar
**Tipe-özel `settings` yoktur (boş obje).** Checkbox'ın tek ayarı `defaultValue`'dur (başlangıçta işaretli mi) ve o da **çekirdek kolonda** durur (§2) — değer şeklini/başlangıcını belirleyen metadata olduğundan render-dışı katman da okur. Bu yüzden bu tipte `settings` **boş kalır**; kapalı-set kuralı gereği bilinmeyen anahtar yine reddedilir.

| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| _(yok)_ | — | — | — | Tipe-özel render ayarı tanımlı değil. |

## 2. Çekirdek kolonda (settings'e girmez)
- `defaultValue` (bool) — başlangıç işaret durumu; girilmezse instance değeri `defaultValue`/`false` olur (değer şablonu §1). Şekli bu tipte **bool** (§1.3).
- `hint` (string) · `helperText` (string) — yardım/etiket metinleri (§1.2).
- Değer-saklama/projeksiyon metadata'sı: `savePropertyToDb` · `projectToAttr` · `saveChangeLog` (§1.3). `projectToAttr=true` → `InstanceAttr.boolValue` (filtre: `boolValue = true`, değer şablonu §2).
- `hasTranslation` **uygulanmaz:** iki-durumlu olduğundan çeviri/`display` yoktur; etiketli değer değildir (değer şablonu §3).

## 3. Profil-bazlı
- Yok (`checkbox` için profil-özel ayar tanımlı değil; görünür/düzenlenebilir/zorunlu genel profil alanlarıdır → [`../../view-profile-property.md`](../../view-profile-property.md)).

## 4. JSON Schema
```json
{
  "$id": "property-settings/checkbox",
  "type": "object",
  "additionalProperties": false,
  "properties": {}
}
```
> Not: `defaultValue` (bool) **çekirdek kolon** olduğundan bu şemada **yer almaz**; şema yalnız (boş) `settings` JSONB'yi doğrular — yani `settings` için `{}` dışında herhangi bir anahtar reddedilir.

## 5. Örnek
```json
{}
```

*Oluşturma: 2026-08-28.*
