# Process Step Settings — `switch` (Switch)

> **stepType:** `switch` · **Adım:** seçili bir alanın **değerine göre** dallanan **otomatik** adım; alanın değeri hangi
> aksiyon koduna denk geliyorsa o aksiyonla ilerler, denk gelen yoksa `default` ile.
> **Davranış:** → [`../../../../service-settings/process-step.md`](../../../../service-settings/process-step.md) §3.14 · **Model (§3):** [`../../process-step.md`](../../process-step.md) §3.5 · **İndeks:** [`index.md`](./index.md).
> **Depolama:** `ProcessStep.settings` (JSONB), ayrımlayıcı `stepType`.

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `propertyId` | int | evet | — | Değerine bakılacak **alan** (form property). Bu alanın çalışma-zamanındaki değeri, dallanmayı doğrudan belirler (aşağıya bkz.). |

> **Eşleşme listesi (`cases`) YOK — değer = aksiyon kodu:** Ayrı bir `cases`/eşleme tablosu **tutulmaz**. Alanın
> çalışma-zamanındaki değeri **ne ise, o `code`'a sahip** [`ProcessStepAction`](../../process-step-action.md) tetiklenir
> (ör. alan değeri `"onaylandi"` → `code = "onaylandi"` aksiyonu). Aynı değeri taşıyan aksiyon **yoksa** `default` kodlu
> aksiyon çalışır (**`default` zorunludur**). Böylece dallar `settings`'te değil, aksiyon kümesinde tanımlanır; hangi adıma
> gidileceği `ProcessStepAction.targetProcessStepId`'dedir.

## 3. Ortak alanlar (settings'te değil — `ProcessStep` kolonu)
`code`·`stepType`·`definition`·`order`·`showInHistory`·`skip*`·`environmentRestriction` → [`../../process-step.md`](../../process-step.md) §1.

## 4. JSON Schema
```json
{
  "$id": "process-step-settings/switch",
  "type": "object",
  "additionalProperties": false,
  "required": ["propertyId"],
  "properties": {
    "propertyId": { "type": "integer" }
  }
}
```
> Not: `propertyId`'nin bir form property'sine işaret ettiği **uygulama-katmanı** doğrulamasıdır (DB FK'si değil). Dal
> kümesi (alan değerlerine karşılık gelen aksiyon `code`'ları + `default`) `settings`'te değil; tasarımcı bunları
> `ProcessStepAction` olarak tanımlar → [`../../process-step-action.md`](../../process-step-action.md).

## 5. Örnek
```json
{
  "propertyId": 88
}
```
> Bu alanın değeri çalışma-zamanında `"high"` ise `code = "high"` aksiyonu, hiçbiri eşleşmezse `code = "default"` aksiyonu tetiklenir.

*Oluşturma: 2026-08-28.*
