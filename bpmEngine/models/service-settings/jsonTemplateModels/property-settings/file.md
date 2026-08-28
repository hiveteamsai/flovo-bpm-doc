# Property Settings — `file` (File)

> **propertyType:** `file` · **Kontrol:** dosya/görsel **yükleme** alanı; değer her zaman **dizidir** (URL + `fileInfo`), binary MinIO'da.
> **Değer şekli:** → [`../../../processInstances/propertyValuesTemplates/file.md`](../../../processInstances/propertyValuesTemplates/file.md) (`list-of-model`; tekil = tek elemanlı dizi) ·
> **Davranış:** → [`../../../../service-settings/properties.md`](../../../../service-settings/properties.md) §3.8 · **Çekirdek model:** [`../../property.md`](../../property.md) · **İndeks:** [`index.md`](./index.md).

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `allowMultiple` | bool | hayır | `false` | Birden fazla dosya yüklenebilsin mi. **Yalnız UI sınırı** — değer şekli `false` iken de **dizidir** (tekil = tek elemanlı; tekil/çoklu için özel-durum kodu gerekmez → değer şablonu §1/§3). |
| `isCropActive` | bool | hayır | `false` | Görsel yüklerken **kırpma (crop)** aracı açılsın mı — foto/tarama çerçeveleme-düzeltme için. |
| `lazyLoading` | bool | hayır | `false` | Dosya/önizleme **tembel** yüklensin mi (büyük ekler istekle/görünürlükte indirilir; ilk açılışta ağ yükünü azaltır). |

## 2. Çekirdek kolonda (settings'e girmez)
- `savePropertyToDb` (bool) — dosya **referans + meta**'sının (`url` + `fileInfo`) `InstanceValue.data`'ya yazılıp yazılmayacağı. Projektör okuduğundan **çekirdek metadata**'dır (§1.3); binary **JSONB'ye gömülmez**, MinIO'da tutulur, `data` yalnız referans taşır (değer şablonu §3).
- `projectToAttr` — çoğunlukla **`false`** (dosya nadiren aranır); gerekirse **InstanceListItem** (her dosya = `itemIndex`) olarak yansır (değer şablonu §2). `saveChangeLog` · `hasTranslation` (§1.3).
- Yardım/görünüm: `hint` · `helperText` · `leadingView`/`trailingView` (§1.2).

> **Flovo AI kaynağı (çapraz-atıf):** Flovo AI adımı (→ [`../../../../service-settings/process-step.md`](../../../../service-settings/process-step.md) §3.3) işleyeceği dosyayı formun **thumbnail'inden** ya da **bir `file` alanından** alır (Masraf · Fatura · Kredi Kartı Ekstresi AI'ları dosyayı parametre olarak alır → properties.md §3.8). Bu kaynak seçimi **adım ayarıdır** (`ProcessStep`'te), bu alanın `settings`'inde tutulmaz.

## 3. Profil-bazlı
- Yok (`file` için profil-özel ayar tanımlı değil; görünür/düzenlenebilir/zorunlu genel profil alanlarıdır → [`../../view-profile-property.md`](../../view-profile-property.md)).

## 4. JSON Schema
```json
{
  "$id": "property-settings/file",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "allowMultiple": { "type": "boolean", "default": false },
    "isCropActive":  { "type": "boolean", "default": false },
    "lazyLoading":   { "type": "boolean", "default": false }
  }
}
```
> Not: `savePropertyToDb`/`projectToAttr` **çekirdek kolon** olduğundan bu şemada **yer almaz**; şema yalnız `settings` JSONB'yi doğrular.

## 5. Örnek
```json
{ "allowMultiple": true, "isCropActive": false, "lazyLoading": true }
```

*Oluşturma: 2026-08-28.*
