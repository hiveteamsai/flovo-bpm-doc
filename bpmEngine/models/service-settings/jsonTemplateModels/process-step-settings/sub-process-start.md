# Process Step Settings — `subProcessStart` (Alt Süreç Başlangıcı)

> **stepType:** `subProcessStart` · **Adım:** ana akıştan **bağımsız**, aynı servise hizmet eden yardımcı bir **alt sürecin
> giriş düğümü**; tetiklendiğinde kullanıcı beklenmeden **`default`** aksiyonuyla otomatik ilerler.
> **Davranış:** → [`../../../../service-settings/process-step.md`](../../../../service-settings/process-step.md) §3.20 · **Model (§3.16):** [`../../process-step.md`](../../process-step.md) §3.16 · **İndeks:** [`index.md`](./index.md).
> **Depolama:** `ProcessStep.settings` (JSONB), ayrımlayıcı `stepType`.

## 1. `settings` (JSONB) — **AYARSIZ** (`settings = {}`)
Bu adımın **tipe-özel ayarı yoktur**; `settings` **boş nesnedir** (`{}`).

**Neden ayarsız:** Alt Süreç Başlangıcı yalnızca bir alt sürecin **giriş düğümü** olarak var olur — kimlik/topoloji dışında
seçilecek bir davranış parametresi taşımaz. Adım tetiklendiğinde otomatik olarak **`default`** aksiyonu çalışır; hangi adıma
ilerleneceği bu adıma bağlı **`ProcessStepAction`** üzerinden belirlenir, `settings`'te değil. Tetikleme **girdisi**
(`ActionTransfer`: `parameters`/`changeList`) çalışma-zamanı verisidir, ayar değildir.

## 2. Tetikleme kaynağı (ayar değil — bilgi)
Adım **üç yolla** tetiklenir; hiçbiri `settings`'te tutulmaz (davranış → §3.20):
1. **Dış — Webhook:** Flovo Customer API ile; "kim tetikledi" → `ProcessStepInstance.atApiKeyId`.
2. **İç — Süreç Adımı Tetikleme:** Başka bir sürecin `triggerProcessStep` (§3.5) adımı.
3. **Otomatik — ServiceTrigger (associate):** İlişki alanı değişince `whenAddedAssociate`/`whenRemoveAssociate` trigger'ı **akış-dışı** çalıştırır (→ [`../../service-trigger.md`](../../service-trigger.md)).

> Webhook'u tutan aksiyon bu adıma bağlı **`default`** aksiyonuna dönüşür; güvenlik (secret/imza) + idempotency ayarları webhook aksiyonu tarafında tutulur (→ [`../../process-step-action.md`](../../process-step-action.md) §3.6).

## 3. Ortak alanlar (settings'te değil — `ProcessStep` kolonu)
`code`·`stepType`·`definition`·`order`·`showInHistory`·`skip*`·`environmentRestriction` → [`../../process-step.md`](../../process-step.md) §1.

## 4. JSON Schema
```json
{
  "$id": "process-step-settings/subProcessStart",
  "type": "object",
  "additionalProperties": false,
  "properties": {}
}
```
> Boş nesne (`{}`) dışında hiçbir alan kabul edilmez (`additionalProperties: false`).

*Oluşturma: 2026-08-28.*
