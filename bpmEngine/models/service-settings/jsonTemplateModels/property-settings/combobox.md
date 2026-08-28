# Property Settings — `combobox` (Combobox)

> **propertyType:** `combobox` · **Kontrol:** listeden seçim; statik (`propertyItems`) veya dinamik (`dataSource*`) kaynak.
> `isAssociatedCombobox=true` iken başka bir servisin instance'larından seçtirir (ilişki kurar).
> **Değer şekli:** → [`../../../processInstances/propertyValuesTemplates/combobox.md`](../../../processInstances/propertyValuesTemplates/combobox.md) (`LabeledValue` / dizi / ilişkili=id) ·
> **Davranış:** → [`../../../../service-settings/properties.md`](../../../../service-settings/properties.md) §3.3 · **Çekirdek model:** [`../../property.md`](../../property.md) · **İndeks:** [`index.md`](./index.md).

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `isMultiSelect` | bool | hayır | `false` | Çoklu seçim. `true` → değer bir **dizi**dir (değer şekli combobox.md). Değer şeklini etkilediğinden projeksiyon katmanı da okur. |
| `manuelEntry` | bool | hayır | `false` | Listede olmayan **serbest giriş**e izin. |
| `lazyLoading` | bool | hayır | `false` | Seçenekler **tembel** (arama/scroll ile) yüklenir (büyük listeler). |
| `headerText` | string? | hayır | `null` | Seçim **pop-up başlığı**. |
| `isAssociatedCombobox` | bool | hayır | `false` | **Ayrımlayıcı.** `true` → düz liste yerine **başka bir servisin instance'larından** seçtirir ve ilişki kurar; çekirdek `associatedServiceId` **zorunlu** olur (§2). `false` = ilişki kurmayan düz liste. |

## 2. Çekirdek kolonda (settings'e girmez)
- **Dinamik kaynak:** `dataSource` (string) · `dataSourceId` (int?) · `dataSourceValue` (string?) — seçenek kaynağı (§1.4). `dataSourceId` **referans id** → uygulama-katmanı doğrulaması.
- **Statik kaynak:** `propertyItems` — ayrı **`PropertyItem`** alt-tablosunda (settings'e gömülmez → [`../../property-item.md`](../../property-item.md)).
- **`associatedServiceId`** (int?, FK → Service) — `isAssociatedCombobox=true` iken **zorunlu**; combobox'ın seçenek kaynağı servis. Motor/projektör okuduğundan **çekirdek kolonda** (§1.5).
- `hasTranslation` (bool) — seçenek etiketleri çeviri kullanıyor mu (projeksiyon metadata'sı, §1.3).

## 3. Profil-bazlı
- Yok (`combobox` için profil-özel ayar tanımlı değil).

## 4. Ayrımlayıcı davranışı (`isAssociatedCombobox`)
- **`true`:** `associatedServiceId` zorunlu; seçilen instance'ın **id'si** alanın `value`'suna yazılır; her değişimde seçilen instance için **`AssociatedInstance`** kaydı düşer (→ [`../../../processInstances/associated-instance.md`](../../../processInstances/associated-instance.md)). `isMultiSelect` ile **çoklu** ilişki kurulabilir (her seçim ayrı `AssociatedInstance`).
- **`false`:** düz liste seçimi; ilişki kaydı düşmez; değer `LabeledValue`.
- **Çapraz-kısıt (uygulama-katmanı):** `isAssociatedCombobox=true ⟹ associatedServiceId != null`. Ayraç bayrağı `settings`'te, FK çekirdek kolonda olduğundan bu kısıt **JSON Schema ile ifade edilemez** → uygulama-katmanı doğrulaması.

## 5. JSON Schema (`settings`)
```json
{
  "$id": "property-settings/combobox",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "isMultiSelect":        { "type": "boolean", "default": false },
    "manuelEntry":          { "type": "boolean", "default": false },
    "lazyLoading":          { "type": "boolean", "default": false },
    "headerText":           { "type": ["string", "null"], "default": null },
    "isAssociatedCombobox": { "type": "boolean", "default": false }
  }
}
```
> Not: Kaynak alanları (`dataSource*`/`propertyItems`) ve `associatedServiceId` **çekirdek kolon** olduğundan bu şemada **yer almaz**; şema yalnız `settings` JSONB'yi doğrular.

## 6. Örnek
```json
{ "isMultiSelect": false, "manuelEntry": false, "lazyLoading": true, "headerText": "Şirket seçin", "isAssociatedCombobox": true }
```

*Oluşturma: 2026-08-28.*
