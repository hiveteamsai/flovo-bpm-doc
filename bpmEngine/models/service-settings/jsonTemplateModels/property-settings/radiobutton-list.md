# Property Settings — `radiobuttonList` (Radiobutton List)

> **propertyType:** `radiobuttonList` · **Kontrol:** **tek** seçimlik liste; her seçenek bir radio düğmesi olarak **satır içi** gösterilir. Kaynak statik (`propertyItems`) veya dinamik (`dataSource*`).
> **Değer şekli:** → [`../../../processInstances/propertyValuesTemplates/radiobutton-list.md`](../../../processInstances/propertyValuesTemplates/radiobutton-list.md) (tek `LabeledValue` — **çoklu değildir**) ·
> **Davranış:** → [`../../../../service-settings/properties.md`](../../../../service-settings/properties.md) §3.7 · **Çekirdek model:** [`../../property.md`](../../property.md) · **İndeks:** [`index.md`](./index.md).

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `manuelEntry` | bool | hayır | `false` | Listede olmayan bir değerin **serbest girilmesine** izin (radio grubuna "diğer/serbest" seçeneği ekler). Yalnız istemci render/giriş davranışı. |
| `lazyLoading` | bool | hayır | `false` | Dinamik kaynaklı (`dataSource*`) listede seçenekler **tembel** (arama/istek anında) yüklenir; büyük seçenek kümeleri için. |

> **Not:** `radiobuttonList` **tekildir** → Combobox'taki `isMultiSelect` **yoktur** (değer her zaman tek `LabeledValue`). Seçenekler **satır içi** gösterildiğinden Combobox'ın seçim **pop-up başlığı** `headerText` de **uygulanmaz**. İlişki kuran `isAssociatedCombobox` yalnız Combobox'a aittir; radiobutton düz tekil seçimdir.

## 2. Çekirdek kolonda (settings'e girmez)
- **Dinamik kaynak:** `dataSource` (string) · `dataSourceId` (int?) · `dataSourceValue` (string?) — seçenek kaynağı (§1.4). `dataSourceId` **referans id** → uygulama-katmanı doğrulaması. Dinamik seçenekler iş kuralı (`fillDataSource`) ile de gelebilir (Combobox ile aynı — properties §2.4).
- **Statik kaynak:** `propertyItems` — ayrı **`PropertyItem`** alt-tablosunda (settings'e gömülmez → [`../../property-item.md`](../../property-item.md)).
- **`defaultValue`** (tek `LabeledValue`) — **varsayılan seçim** (form açılışında önceden seçili radio). Değer alanı olduğundan çekirdek kolonda (§1.3); şekli değer şablonundaki tekli `LabeledValue`.
- `hasTranslation` (bool) — seçenek etiketleri çeviri kullanıyor mu (projeksiyon metadata'sı, §1.3); etiketli seçim `LabeledValue` (`{value, display, translationCode}`) ile yazılır.

## 3. Profil-bazlı
- Yok (`radiobuttonList` için profil-özel ayar tanımlı değil; görünür/düzenlenebilir/zorunlu genel profil alanlarıdır → [`../../view-profile-property.md`](../../view-profile-property.md)).

## 4. JSON Schema (`settings`)
```json
{
  "$id": "property-settings/radiobuttonList",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "manuelEntry": { "type": "boolean", "default": false },
    "lazyLoading": { "type": "boolean", "default": false }
  }
}
```
> Not: Kaynak alanları (`dataSource*`/`propertyItems`), **varsayılan seçim** (`defaultValue`) ve `hasTranslation` **çekirdek kolon** olduğundan bu şemada **yer almaz**; şema yalnız `settings` JSONB'yi doğrular.

## 5. Örnek
```json
{ "manuelEntry": false, "lazyLoading": true }
```

*Oluşturma: 2026-08-28.*
