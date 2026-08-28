# Process Step Settings — `instanceCreator` (Instance Creator)

> **stepType:** `instanceCreator` · **Adım:** hedef serviste **yeni form/instance üreten** otomatik adım; yeni kaydın
> başlangıç alanları, adımı tetikleyen aksiyonun `parameters`'ından eşlenir.
> **Davranış:** → [`../../../../service-settings/process-step.md`](../../../../service-settings/process-step.md) §3.12 · **Model (§3):** [`../../process-step.md`](../../process-step.md) §3.9 · **İndeks:** [`index.md`](./index.md).
> **Depolama:** `ProcessStep.settings` (JSONB), ayrımlayıcı `stepType`.

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `targetServiceId` | int | evet | — | Yeni instance'ın **oluşturulacağı hedef form/servis**. |
| `initValues` | `InstanceInitValue[]` | hayır | `[]` | Yeni instance'a yazılacak **başlangıç (init) değer eşlemeleri** — hangi parametrenin hangi alana kopyalanacağı (§2). |
| `thumbnailParameterName` | string? | hayır | — | Yeni instance'ın **thumbnail URL**'sini taşıyan parametre adı (kaynak `parameters` anahtarı). |

> **Akış yönlendirme `settings`'te DEĞİL:** Oluşturma sonrası ilerleme, otomatik adımın `default` kodlu
> [`ProcessStepAction`](../../process-step-action.md) ile belirlenir (hedef adım orada).

## 2. Alt-model — `InstanceInitValue`
Adımı tetikleyen aksiyondan gelen bir **parametrenin değerini**, yeni instance'ın bir **alanına (property)** kopyalar.

| Alan | Tip | Zorunlu | Açıklama |
|---|---|---|---|
| `targetPropertyId` | int | evet | Değerin yazılacağı **hedef property** (yeni instance içinde). |
| `parameterName` | string | evet | **Kaynak** — aksiyondan gelen `parameters` anahtarı; bu anahtarın değeri `targetPropertyId`'ye yazılır. |

> **Detay sonra genişletilecek:** Init değer eşleme modeli (ör. sabit/hesaplanan kaynaklar, çoklu-değer/alt-servis eşlemeleri)
> ilerleyen sürümde detaylandırılacaktır → [`../../../../todo.md`](../../../../todo.md).

## 3. Ortak alanlar (settings'te değil — `ProcessStep` kolonu)
`code`·`stepType`·`definition`·`order`·`showInHistory`·`skip*`·`environmentRestriction` → [`../../process-step.md`](../../process-step.md) §1.

## 4. JSON Schema
```json
{
  "$id": "process-step-settings/instanceCreator",
  "type": "object",
  "additionalProperties": false,
  "required": ["targetServiceId"],
  "properties": {
    "targetServiceId":        { "type": "integer" },
    "initValues":             { "type": "array", "items": { "$ref": "#/$defs/instanceInitValue" }, "default": [] },
    "thumbnailParameterName": { "type": "string" }
  },
  "$defs": {
    "instanceInitValue": {
      "type": "object",
      "additionalProperties": false,
      "required": ["targetPropertyId", "parameterName"],
      "properties": {
        "targetPropertyId": { "type": "integer" },
        "parameterName":    { "type": "string", "minLength": 1 }
      }
    }
  }
}
```
> Not: `targetServiceId` ve `initValues[].targetPropertyId` referansları DB FK'si değil, **uygulama-katmanı** doğrulamasıdır; `parameterName` ve `thumbnailParameterName`'in gelen `parameters` anahtarlarıyla eşleşmesi de çalışma-zamanında çözülür. Init eşleme modeli **genişlemeye açıktır** (→ todo).

## 5. Örnek
```json
{
  "targetServiceId": 12,
  "initValues": [
    { "targetPropertyId": 101, "parameterName": "barcode" },
    { "targetPropertyId": 102, "parameterName": "orderNo" }
  ],
  "thumbnailParameterName": "thumbnailUrl"
}
```

*Oluşturma: 2026-08-28.*
