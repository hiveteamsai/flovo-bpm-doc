# Property Settings — `barcode` (Barcode)

> **propertyType:** `barcode` · **Kontrol:** bir string `value` tutar; `barcodeFormat`'a göre bu değeri **barkod görseline render eder**. Görselin altında text alanı, sağında kamerayı açan ikon bulunur.
> **Değer şekli:** → [`../../../processInstances/propertyValuesTemplates/barcode.md`](../../../processInstances/propertyValuesTemplates/barcode.md) (düz `string` — ham değer, Attr `textValue`) ·
> **Davranış:** → [`../../../../service-settings/properties.md`](../../../../service-settings/properties.md) §3.10 · **Çekirdek model:** [`../../property.md`](../../property.md) · **İndeks:** [`index.md`](./index.md).

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `barcodeFormat` | [`BarcodeFormat`](../../../enums/barcode-format.md) | hayır | `code128` | Kontrolün **tanıyacağı/tarayacağı ve render edeceği** barkod biçimi (hem render hem okuma — §3.10). Saklanan değer yine ham string'tir; görsel bu biçimle değerden yeniden çizilir (değer şablonu §1). `aztec`·`code39`·`code93`·`ean8`·`ean13`·`code128`·`dataMatrix`·`qr`·`interleaved2of5`·`pdf417`. |
| `scannerActive` | bool | hayır | `false` | **Kamera/tarayıcı ile okuma** açık mı — sağdaki ikon kamerayı açıp taranan değeri `value`'ya yazsın mı. `false` iken değer yalnız alttaki textbox'tan elle girilir. |

## 2. Çekirdek kolonda (settings'e girmez)
- `defaultValue` (string) — başlangıç barkod değeri; şekli bu tipte **string** (§1.3).
- `hint` (string) · `helperText` (string) — yardım metinleri (§1.2).
- Değer-saklama/projeksiyon metadata'sı: `savePropertyToDb` · `projectToAttr` · `saveChangeLog` (§1.3). Tam eşitlik araması çoğunlukla `data` GIN'iyle yeterlidir (`projectToAttr=false` bile bulunur); prefix/sıralama için `projectToAttr=true` → `InstanceAttr.textValue` (değer şablonu §2).

## 3. Profil-bazlı
- Yok (`barcode` için profil-özel ayar tanımlı değil; görünür/düzenlenebilir/zorunlu genel profil alanlarıdır → [`../../view-profile-property.md`](../../view-profile-property.md)).

## 4. İlişkili akış (motor/aksiyon)
- **`scanBarcode` (Barcode Tara) aksiyonu** — kamerayla okunan değeri bu alana yazan no-code aksiyon (→ `../../../../service-settings/process-step-action.md` §3.5). `scannerActive`, alan içi kamera ikonunu; bu aksiyon ise adım-tetikli taramayı sağlar.
- **Custom ID Creator `createWithBarcode`** — instance oluşturulurken kimliği/barkodu üreten seçenek (→ `../../../../service-settings/process-step.md` §3.11); üretilen değer bu tip alanda saklanıp `barcodeFormat` ile render edilir.

## 5. JSON Schema
```json
{
  "$id": "property-settings/barcode",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "barcodeFormat":  { "enum": ["aztec", "code39", "code93", "ean8", "ean13", "code128", "dataMatrix", "qr", "interleaved2of5", "pdf417"], "default": "code128" },
    "scannerActive":  { "type": "boolean", "default": false }
  }
}
```
> Not: `value`/`defaultValue` (string) **çekirdek kolon** olduğundan bu şemada yer almaz; şema yalnız `settings` JSONB'yi doğrular.

## 6. Örnek
```json
{ "barcodeFormat": "ean13", "scannerActive": true }
```

*Oluşturma: 2026-08-28.*
