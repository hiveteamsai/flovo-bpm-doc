# Property Settings — `text` (Text — statik)

> **propertyType:** `text` · **Kontrol:** başlık/açıklama gösteren **statik label** — **girdi değildir**; kullanıcı değer üretmez.
> **Değer şekli:** → [`../../../processInstances/propertyValuesTemplates/text.md`](../../../processInstances/propertyValuesTemplates/text.md) (**değer yok**; `data`'da anahtar bulunmaz — istisna) ·
> **Davranış:** → [`../../../../service-settings/properties.md`](../../../../service-settings/properties.md) §3.9 · **Çekirdek model:** [`../../property.md`](../../property.md) · **İndeks:** [`index.md`](./index.md).

## 1. `settings` (JSONB) — tipe-özel tipografi/yerleşim ayarları
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `fontSize` | number? | hayır | `null` | Etiket **yazı boyutu** (punto). `null` = tema/varsayılan boyut. `> 0`. |
| `iconSize` | number? | hayır | `null` | Etiketin (varsa) **ikon boyutu**. `null` = tema/varsayılan. `> 0`. |
| `isBold` | bool | hayır | `false` | Metin **kalın** gösterilsin mi. |
| `textAlignment` | [`TextAlignment`](../../../enums/text-alignment.md) | hayır | `left` | Metin **yatay hizalaması** — `left`·`center`·`right`. |
| `stiky` | bool | hayır | `false` | Başlık **yapışkan/sabit** kalsın mı — form kaydırılırken üstte sabitlenen bölüm başlığı için. |

## 2. Çekirdek kolonda (settings'e girmez)
- `defaultValue` (string) — **gösterilecek statik metin** (tasarım-zamanı; §1.3). `text` bir değer üretmediğinden bu, başlangıç değeri değil **görüntülenen içeriktir** (değer şablonu §1). Fiziksel **çekirdek `Property.defaultValue`** kolonunu kullanır (tüm tiplerde ortak kolon); render-only olsa da ayrı bir `settings` anahtarına kopyalanmaz — İndeks (`index.md`) text `settings` özeti de yalnız 5 tipografi alanını listeler.
- `translationCode` (Property) — `defaultValue` çevrilecekse **statik etiket çevirisi** buradan çözülür; bu, **değer** değil **tanım** çevirisidir (değer şablonu §3).
- **Değer-saklama:** `savePropertyToDb=false` · `projectToAttr=false` — text saklanan/aranan bir değer üretmez (anlamsız; değer şablonu §2).

## 3. Profil-bazlı
- Yok (`text` için profil-özel ayar tanımlı değil).

## 4. JSON Schema
```json
{
  "$id": "property-settings/text",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "fontSize":      { "type": ["number", "null"], "exclusiveMinimum": 0, "default": null },
    "iconSize":      { "type": ["number", "null"], "exclusiveMinimum": 0, "default": null },
    "isBold":        { "type": "boolean", "default": false },
    "textAlignment": { "enum": ["left", "center", "right"], "default": "left" },
    "stiky":         { "type": "boolean", "default": false }
  }
}
```
> Not: `textAlignment` değer kümesi **TextAlignment** enum'undadır ([`../../../enums/text-alignment.md`](../../../enums/text-alignment.md)); JSON Schema'da değerler ayrıca **satır-içi** listelenir. `defaultValue` **çekirdek kolon** olduğundan (gösterilecek statik metin) bu şemada **yer almaz**.

## 5. Örnek
```json
{ "fontSize": 18, "iconSize": 20, "isBold": true, "textAlignment": "center", "stiky": true }
```

*Oluşturma: 2026-08-28.*
