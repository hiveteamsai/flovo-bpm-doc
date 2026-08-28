# Process Step Settings — `instanceDeleter` (Instance Deleter)

> **stepType:** `instanceDeleter` · **Adım:** sürecin instance'ını (ve seçime göre ilişkili instance'ları) silen
> **otomatik** adım; silme yumuşaktır (`deleted = true`).
> **Davranış:** → [`../../../../service-settings/process-step.md`](../../../../service-settings/process-step.md) §3.10 · **Model (§3):** [`../../process-step.md`](../../process-step.md) §3.15 · **İndeks:** [`index.md`](./index.md).
> **Depolama:** `ProcessStep.settings` (JSONB), ayrımlayıcı `stepType`.

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `deleteMode` | [`InstanceDeleteMode`](../../../enums/instance-delete-mode.md) | evet | — | İlişkili formların silmeden nasıl etkileneceğini belirler — `withRelated` (ilişkilileri de sil) · `unlinkRelated` (yalnız ilişkiyi kopar). Amaç farkı aşağıda. |

**`deleteMode` seçeneklerinin amacı:**
- **`withRelated` — *formu ve ilişkili formları birlikte tasfiye et:*** sürecin instance'ı **ve** ona bağlı tüm ilişkili
  instance'lar `deleted = true` yapılır. Ana kayıt ile ona bağımlı alt kayıtların **tek parça** olduğu, birlikte var olup
  birlikte kaldırılması gereken durumlar için.
- **`unlinkRelated` — *ana kaydı sil, ilişkilileri yaşat:*** yalnız sürecin instance'ı `deleted = true` yapılır; ilişkiyi
  taşıyan `AssociatedInstance` kayıtları **silinir** (bağ kopar) ama **ilişkili instance'ların `deleted` durumuna dokunulmaz**.
  İlişkili kayıtların bağımsız/paylaşılan olduğu, ana kayıt gitse de yaşamaya devam etmesi gereken durumlar için.

> **Akış yönlendirme `settings`'te DEĞİL:** Silme sonrası ilerleme, otomatik adımın tek çıkışı olan `default` kodlu
> [`ProcessStepAction`](../../process-step-action.md) ile belirlenir (hedef adım orada).

## 3. Ortak alanlar (settings'te değil — `ProcessStep` kolonu)
`code`·`stepType`·`definition`·`order`·`showInHistory`·`skip*`·`environmentRestriction` → [`../../process-step.md`](../../process-step.md) §1.

## 4. JSON Schema
```json
{
  "$id": "process-step-settings/instanceDeleter",
  "type": "object",
  "additionalProperties": false,
  "required": ["deleteMode"],
  "properties": {
    "deleteMode": { "enum": ["withRelated", "unlinkRelated"] }
  }
}
```
> Not: Formlar arası ilişki `AssociatedInstance` üzerinden tutulur; hangi kayıtların silineceği/koparılacağı **uygulama-katmanında** çözülür (→ [`../../../processInstances/index.md`](../../../processInstances/index.md)).

## 5. Örnek
```json
{
  "deleteMode": "withRelated"
}
```

*Oluşturma: 2026-08-28.*
