# Process Step Settings — `processing` (Processing)

> **stepType:** `processing` · **Adım:** formu **bir kullanıcıya "tamamlanmasını bekleyenler"** olarak gösteren bekleme adımı; üzerinde **işlem alınamaz**. Adımda **`default` kodlu `autoAction`** varsa otomatik ilerler, **yoksa** dış (webhook) aksiyon beklenir.
> **Davranış:** → [`../../../../service-settings/process-step.md`](../../../../service-settings/process-step.md) §3.18 · **Model (§3):** [`../../process-step.md`](../../process-step.md) §3.13 · **İndeks:** [`index.md`](./index.md).
> **Depolama:** `ProcessStep.settings` (JSONB), ayrımlayıcı `stepType`.

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `showLoading` | bool | hayır | `false` | Formun **görünürlüğünü** kontrol eder. `true` → adımdayken form **detayına giriş** ve **alan değerlerinin görüntülenmesi** engellenir; kullanıcı formu **"yükleniyor"** olarak görür (arka planda bir iş sürerken içerik gizlenir). `false` → form **normal** görünür (genelde bir durum güncellemesiyle kullanıcıya güncel bilgi verilir). |

> **Otomatik ilerleme `settings`'te DEĞİL — `default autoAction` ilişkisi:** Processing'in ilerleyip ilerlemeyeceği bu adımın `settings`'inde değil, adıma bağlı **aksiyonlarla** belirlenir:
> - Adımda **`code = default`, `actionType = autoAction`** bir `ProcessStepAction` **varsa** → manuel aksiyon beklenmeden onunla **otomatik ilerler** (motorda otomatik adım gibi davranır; ör. "yükleniyor" gösterip bir sonraki otomatik adıma geçer).
> - **Yoksa** → süreç bu adımda **bekler**; ilerleme, adıma tanımlı bir **webhook** (ya da başka dış) aksiyonun dışarıdan tetiklenmesiyle olur.
>
> Yani `showLoading` yalnız **görünümü**; ilerleme davranışı **aksiyon tarafındadır** → [`../../process-step-action.md`](../../process-step-action.md) (`autoAction` / `webhook`). Hedef adım da aksiyonun `targetProcessStepId`'sindedir.

> **Status (durum) bu adımda değişmez:** Processing'in kendine özel bir durum değişimi yoktur; durum, her adımdaki gibi **aksiyon ilerlerken** (`ProcessStepAction.changeStatusId`) değişir — adımın içinde değil. `showLoading = false`'daki "güncel bilgi", bu adıma **girişi sağlayan** aksiyonun `changeStatusId`'siyle iletilir.

## 2. Alt-modeller
Yok — `settings` tek `bool` alandan ibarettir.

## 3. Ortak alanlar (settings'te değil — `ProcessStep` kolonu)
`code`·`stepType`·`definition`·`order`·`showInHistory`·`skip*`·`environmentRestriction` → [`../../process-step.md`](../../process-step.md) §1.

## 4. JSON Schema
```json
{
  "$id": "process-step-settings/processing",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "showLoading": { "type": "boolean", "default": false }
  }
}
```

## 5. Örnek
```json
{ "showLoading": true }
```

*Oluşturma: 2026-08-28.*
