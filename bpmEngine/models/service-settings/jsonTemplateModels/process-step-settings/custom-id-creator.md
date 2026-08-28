# Process Step Settings — `customIdCreator` (Custom ID Creator)

> **stepType:** `customIdCreator` · **Adım:** verilen formata göre **benzersiz bir ID/numara** üretip bir property'ye yazan (isteğe bağlı olarak barkod görseli de oluşturan) **otomatik** adım; işini yapıp `default` aksiyonla ilerler.
> **Davranış:** → [`../../../../service-settings/process-step.md`](../../../../service-settings/process-step.md) §3.11 · **Model (§3):** [`../../process-step.md`](../../process-step.md) §3.8 · **İndeks:** [`index.md`](./index.md).
> **Depolama:** `ProcessStep.settings` (JSONB), ayrımlayıcı `stepType`.

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `customId` | string | evet | — | Üretilecek ID'nin **format şablonu** — ön ek + sıra no + tarih gibi parçalardan oluşan, motor-tanımlı yer tutucular içeren metin. Her çalıştırmada bu şablondan benzersiz bir değer türetilir. |
| `targetPropertyId` | int | evet | — | Üretilen ID'nin **yazılacağı property** (ör. bir textbox veya `barcode` alanı; `barcode` alanında değer `barcodeFormat`'a göre görsele render edilir → [`../property-settings/barcode.md`](../property-settings/barcode.md)). **`settings` içi referans id** (§3). |
| `createWithBarcode` | bool | hayır | `false` | `true` → ID ile birlikte bir **barkod görseli** de üretilip `targetFilePropertyId`'deki file alanına yazılır (§2). `false` → yalnız ID değeri üretilir. |
| `targetFilePropertyId` | int? | koşullu | — | `createWithBarcode = true` iken barkod **görselinin yazılacağı file property** (→ [`../property-settings/file.md`](../property-settings/file.md)). **`settings` içi referans id** (§3). |

> **Akış yönlendirme `settings`'te DEĞİL:** ID üretilip yazıldıktan sonra **`default`** kodlu `ProcessStepAction` tetiklenir → [`../../process-step-action.md`](../../process-step-action.md).

## 2. Barkod ilişkisi (`createWithBarcode` · `targetFilePropertyId`)
`createWithBarcode = true` iken adım iki çıktı üretir:
1. **ID değeri** → `targetPropertyId`'deki property'ye yazılır. Bu property bir **`barcode`** alanıysa, değer o alanın `barcodeFormat` ayarına göre ekranda barkod olarak **render edilir** (görsel render alan tarafındadır → [`../property-settings/barcode.md`](../property-settings/barcode.md) §4).
2. **Barkod görseli (dosya)** → `targetFilePropertyId`'deki **file** property'ye yazılır (dosya/görsel olarak saklanmak istendiğinde; → [`../property-settings/file.md`](../property-settings/file.md)).

> Yani `targetPropertyId` ID **değerini** (barcode alanında canlı render), `targetFilePropertyId` ise üretilen barkodun **dosya halini** tutar; ikisi farklı amaçlara hizmet eder ve `createWithBarcode` açıkken birlikte doldurulur.

## 3. Ortak alanlar (settings'te değil — `ProcessStep` kolonu)
`code`·`stepType`·`definition`·`order`·`showInHistory`·`skip*`·`environmentRestriction` → [`../../process-step.md`](../../process-step.md) §1.
`settings` içindeki referans id'ler (`targetPropertyId`·`targetFilePropertyId`) **DB FK'si değildir** → uygulama-katmanı doğrulaması + silme koruması (→ [`../../../../todo.md`](../../../../todo.md)).

## 4. JSON Schema
```json
{
  "$id": "process-step-settings/customIdCreator",
  "type": "object",
  "additionalProperties": false,
  "required": ["customId", "targetPropertyId"],
  "properties": {
    "customId":         { "type": "string", "minLength": 1 },
    "targetPropertyId": { "type": "integer" },
    "createWithBarcode":    { "type": "boolean", "default": false },
    "targetFilePropertyId": { "type": "integer" }
  },
  "allOf": [
    {
      "if":   { "properties": { "createWithBarcode": { "const": true } }, "required": ["createWithBarcode"] },
      "then": { "required": ["targetFilePropertyId"] }
    }
  ]
}
```
> Not: `targetPropertyId` / `targetFilePropertyId` referanslarının varlığı ve tip uyumu (özellikle `targetFilePropertyId`'nin bir **file** alanı olması) **uygulama-katmanı** doğrulamasıdır. `customId` şablonundaki yer tutucu sözdizimi motor tarafında yorumlanır.

## 5. Örnek
```json
{
  "customId": "EXP-{seq}-{yyyy}",
  "targetPropertyId": 42,
  "createWithBarcode": false
}
```
```json
{
  "customId": "SVK-{seq}",
  "targetPropertyId": 42,
  "createWithBarcode": true,
  "targetFilePropertyId": 71
}
```

*Oluşturma: 2026-08-28.*
