# Property Settings — `mapViewer` (Map Viewer)

> **propertyType:** `mapViewer` · **Kontrol:** harita üzerinde **konum seçme ve görüntüleme**; değer bir koordinat (+opsiyonel adres).
> **Değer şekli:** → [`../../../processInstances/propertyValuesTemplates/map-viewer.md`](../../../processInstances/propertyValuesTemplates/map-viewer.md) (yapısal obje: `{ location: { lat, lng, address } }`) ·
> **Davranış:** → [`../../../../service-settings/properties.md`](../../../../service-settings/properties.md) §3.12 · **Çekirdek model:** [`../../property.md`](../../property.md) · **İndeks:** [`index.md`](./index.md).

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `mapPinIconUrl` | string? | hayır | `null` | Konumu haritada işaretleyen **pin/marker ikonu**nun URL'i (**görüntüleme** ayarı). `null` = varsayılan marker. Yalnız render; değeri (koordinat) etkilemez. |

> _Konum **seçme/gösterme** dışında saf render ayarı yalnız marker ikonudur; alanın düzenlenebilir mi yoksa salt-görüntüleme mi olduğu genel profil alanı `enabled` ile (→ [`../../view-profile-property.md`](../../view-profile-property.md)), "yalnız kendi konumu" kısıtı ise **profil-bazlı** `editOnlyOwnPosition` ile (§3) belirlenir._

## 2. Çekirdek kolonda (settings'e girmez)
- `hint` (string) · `helperText` (string) — yardım metinleri (§1.2).
- `defaultValue` — başlangıç konumu; şekli bu tipte **yapısal obje** (`{ location: { lat, lng, address } }`, değer şablonuyla aynı) (§1.3).
- Değer-saklama/projeksiyon metadata'sı: `savePropertyToDb` · `projectToAttr` · `saveChangeLog` (§1.3). `projectToAttr=true` iken `address` → `InstanceAttr.textValue`; `lat`/`lng` `data`'da kalır (eşitlik GIN; coğrafi sorgu PostGIS, post-MVP) → değer şablonu §2.

## 3. Profil-bazlı
Görüntüleme profiline göre değişen tipe-özel ayar → [`../../view-profile-property.md`](../../view-profile-property.md) (`ProcessViewProfilePropertySetting {key, value}`):

| key | value tipi | Ne yapar |
|---|---|---|
| `editOnlyOwnPosition` | bool | Kullanıcı haritada **yalnız kendi konumunu** düzenleyebilir mi (başkalarının işaretlediği konumlar salt-okunur). **Profil-bazlı** olmasının nedeni: aynı alan bir profilde serbest, başka profilde (örn. saha ekibi) yalnız kendi konumuyla sınırlı olabilir (**KARAR v0.33**). Belirtilmezse `Property` varsayılanı. |

## 4. JSON Schema (`settings`)
```json
{
  "$id": "property-settings/map-viewer",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "mapPinIconUrl": { "type": ["string", "null"], "default": null }
  }
}
```
> Not: `editOnlyOwnPosition` **profil-bazlı** (`ProcessViewProfilePropertySetting`) olduğundan bu `settings` şemasında **yer almaz**; şema yalnız alan-düzeyi `settings` JSONB'yi doğrular.

## 5. Örnek
```json
{ "mapPinIconUrl": "https://cdn.example.com/pins/expense.png" }
```

*Oluşturma: 2026-08-28.*
