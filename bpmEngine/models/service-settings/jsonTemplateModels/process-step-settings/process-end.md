# Process Step Settings — `processEnd` (Süreç Bitişi)

> **stepType:** `processEnd` · **Adım:** sürecin **son adımı**; kimsenin onayında beklemez, sürecin **bittiği** anlamına gelir.
> Yürütme döngüsünü sonlandırır. **İstisna:** bu adıma da aksiyon bağlanabilir; yalnız **yetkili gruplar** bir geri-taşıma (re-open)
> aksiyonunu görüp tetikleyerek **aynı instance'ı** farklı bir adıma taşıyabilir.
> **Davranış:** → [`../../../../service-settings/process-step.md`](../../../../service-settings/process-step.md) §3.17 · **Model (§3):** [`../../process-step.md`](../../process-step.md) §3.12 · **İndeks:** [`index.md`](./index.md).
> **Depolama:** `ProcessStep.settings` (JSONB), ayrımlayıcı `stepType`.

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `processViewProfileId` | int | evet | — | Süreç bittiğinde formun (rapor/liste üzerinden) **görüntüleneceği profil** (→ [`../../../../service-settings/view-profile.md`](../../../../service-settings/view-profile.md)). |
| `userGroupIds` | int[] | hayır | `[]` | Bitiş sonrası forma **erişip geri-taşıma (re-open) aksiyonu alabilecek** yetkili kullanıcı grupları. **Boş** → geri-taşıma aksiyonu tetikleyebilen grup yok (yalnız görüntüleme erişimi). |

> **Geri-taşıma (re-open) — davranış:** Süreç Bitişi'ne bağlı bir aksiyonu **yalnız** `userGroupIds`'teki gruplar görüntüleyip
> tetikleyebilir; tetiklendiğinde süreç kapanmış sayılmaz, aksiyonun **`targetProcessStepId`**'sindeki adıma **aynı `ProcessInstance`
> üzerinde** ilerler (yeni çalıştırma açılmaz). Aksiyon-hedefi yönlendirme `settings`'te **değil**, `ProcessStepAction`'dadır
> → [`../../process-step-action.md`](../../process-step-action.md).

## 3. Ortak alanlar (settings'te değil — `ProcessStep` kolonu)
`code`·`stepType`·`definition`·`order`·`showInHistory`·`skip*`·`environmentRestriction` → [`../../process-step.md`](../../process-step.md) §1.

## 4. JSON Schema
```json
{
  "$id": "process-step-settings/processEnd",
  "type": "object",
  "additionalProperties": false,
  "required": ["processViewProfileId"],
  "properties": {
    "processViewProfileId": { "type": "integer" },
    "userGroupIds": { "type": "array", "items": { "type": "integer" }, "default": [] }
  }
}
```
> Not: Referans id'ler (`processViewProfileId`·`userGroupIds[]`) DB FK'si değil, **uygulama-katmanı** doğrulaması + silme koruması.

## 5. Örnek
```json
{
  "processViewProfileId": 15,
  "userGroupIds": [2, 5]
}
```

*Oluşturma: 2026-08-28.*
