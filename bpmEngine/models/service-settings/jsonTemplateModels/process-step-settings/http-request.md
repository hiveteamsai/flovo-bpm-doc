# Process Step Settings — `httpRequest` (HTTP Request)

> **stepType:** `httpRequest` · **Adım:** dış endpoint'e HTTP isteği atan **otomatik** adım; yanıttaki `action` koduyla ilerler
> (boş/`async` ise `default`).
> **Davranış:** → [`../../../../service-settings/process-step.md`](../../../../service-settings/process-step.md) §3.2 · **Model (§3):** [`../../process-step.md`](../../process-step.md) §3.1 · **İndeks:** [`index.md`](./index.md).
> **Depolama:** `ProcessStep.settings` (JSONB), ayrımlayıcı `stepType`.

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `endpoint` | string | evet | — | İstek atılacak **URL**. `templateParameters` ile `{name}` yer tutucuları doldurulur (path/şablon). |
| `method` | [`HttpMethod`](../../../enums/http-method.md) | evet | — | HTTP metodu — `get`·`post`·`put`·`delete`. |
| `templateParameters` | `DynamicParameter[]` | hayır | `[]` | **URL şablon/path** parametreleri — `endpoint`'teki `{name}` yer tutucularını doldurur (§2). |
| `queryParameters` | `DynamicParameter[]` | hayır | `[]` | **Query string** parametreleri (`?name=value`). |
| `headers` | `DynamicParameter[]` | hayır | `[]` | İstek **başlıkları** (ör. `Authorization`, `Content-Type`). |
| `body` | `DynamicParameter[]` | hayır | `[]` | **Gövde** parametreleri (POST/PUT için). |
| `async` | bool | hayır | `false` | `true` → yanıt **beklenmez**, doğrudan `default` aksiyonla ilerlenir (fire-and-forget); `false` → yanıt beklenir, dönen `action` koduyla ilerlenir. |

> **Akış yönlendirme `settings`'te DEĞİL:** İlerlenecek adım, yanıttaki `action` koduyla **aynı kodlu** `ProcessStepAction` üzerinden belirlenir (başarısızlıkta `onFail`) → [`../../process-step-action.md`](../../process-step-action.md).

## 2. Alt-model — `DynamicParameter`
Bir parametrenin **adı** ve **değer kaynağını** taşır; tüm parametre gruplarında (`templateParameters`/`queryParameters`/`headers`/`body`) ortak.

| Alan | Tip | Zorunlu | Açıklama |
|---|---|---|---|
| `name` | string | evet | Parametre adı (URL yer tutucusu / query anahtarı / header adı / body alanı). |
| `value` | `ValueAssignType`-değeri | evet | Değer **kaynağı** (→ [`../../../enums/value-assign-type.md`](../../../enums/value-assign-type.md)): `fixedValue` (sabit) · `propertyValue` (form alanından) · `fromCalculation` (ifade) + ilgili değer. |

> Not: Çalışma-zamanında hesaplanan gönderilecek değer (`parameterValue`) **ayar değildir**, kaydedilen `settings`'e girmez.

## 3. Ortak alanlar (settings'te değil — `ProcessStep` kolonu)
`code`·`stepType`·`definition`·`order`·`showInHistory`·`skip*`·`environmentRestriction` → [`../../process-step.md`](../../process-step.md) §1.

## 4. JSON Schema
```json
{
  "$id": "process-step-settings/httpRequest",
  "type": "object",
  "additionalProperties": false,
  "required": ["endpoint", "method"],
  "properties": {
    "endpoint": { "type": "string", "minLength": 1 },
    "method":   { "enum": ["get", "post", "put", "delete"] },
    "templateParameters": { "type": "array", "items": { "$ref": "#/$defs/dynamicParameter" }, "default": [] },
    "queryParameters":    { "type": "array", "items": { "$ref": "#/$defs/dynamicParameter" }, "default": [] },
    "headers":            { "type": "array", "items": { "$ref": "#/$defs/dynamicParameter" }, "default": [] },
    "body":               { "type": "array", "items": { "$ref": "#/$defs/dynamicParameter" }, "default": [] },
    "async":  { "type": "boolean", "default": false }
  },
  "$defs": {
    "dynamicParameter": {
      "type": "object",
      "additionalProperties": false,
      "required": ["name", "value"],
      "properties": {
        "name":  { "type": "string", "minLength": 1 },
        "value": { "type": "object" }
      }
    }
  }
}
```
> Not: `value`'nun tam şeması **ValueAssignType** discriminated-union'ıdır (`fixedValue`/`propertyValue`/`fromCalculation`); ortak tanım → `value-assign-type.md`. `name` içindeki URL/query/header referansları ve `propertyValue.propertyId` **uygulama-katmanı** doğrulaması.

## 5. Örnek
```json
{
  "endpoint": "https://api.example.com/orders/{orderId}",
  "method": "post",
  "templateParameters": [ { "name": "orderId", "value": { "valueAssignType": "propertyValue", "propertyValue": { "propertyId": 42 } } } ],
  "headers": [ { "name": "Authorization", "value": { "valueAssignType": "fixedValue", "fixedValue": { "value": "Bearer xyz" } } } ],
  "body": [ { "name": "total", "value": { "valueAssignType": "fromCalculation", "fromCalculation": { "expression": "#TUTAR * #KUR" } } } ],
  "async": false
}
```

*Oluşturma: 2026-08-28.*
