# Process Step Settings — `flovoAi` (Flovo AI)

> **stepType:** `flovoAi` · **Adım:** seçilen Flovo AI'ı bir dosya üzerinde çalıştırıp sonucu **parametre** olarak sonraki adıma taşıyan **otomatik** adım; başarıda `default`, hatada `onFail` aksiyonuyla ilerler.
> **Davranış:** → [`../../../../service-settings/process-step.md`](../../../../service-settings/process-step.md) §3.3 · **Model (§3):** [`../../process-step.md`](../../process-step.md) §3.2 · **İndeks:** [`index.md`](./index.md).
> **Depolama:** `ProcessStep.settings` (JSONB), ayrımlayıcı `stepType`.

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `selectedAi` | string | evet | — | Çalıştırılacak **Flovo AI'ın kimliği** — Flovo'nun geliştirdiği AI listesinden seçilir; bu değer hangi AI motorunun tetikleneceğini ve `aiSettings`'in nasıl yorumlanacağını belirler. Başlangıçta planlanan AI'lar: Masraf · Fatura · Kredi Kartı Ekstresi (üçü de girdi olarak dosya alır). **Kanonik değer seti (enum) henüz kesinleşmedi** → serbest string olarak tutulur (→ [`../../../../todo.md`](../../../../todo.md), "Flovo AI adım ayarları"). |
| `aiSettings` | object | hayır | — | Seçilen AI'a **özel** ayarlar — şekli `selectedAi`'a göre değişen serbest yapı (her AI'ın kendi parametreleri). **Per-AI şeması açık** → içi doğrulanmaz (→ [`../../../../todo.md`](../../../../todo.md)). |
| `fileSourceType` | enum (`thumbnail`·`fileProperty`) | evet | — | AI'ın işleyeceği **dosyanın kaynağı**: `thumbnail` → formun thumbnail dosyası · `fileProperty` → bir **file** alanındaki dosya (→ [`../property-settings/file.md`](../property-settings/file.md)). **Ayrı bir enum dosyasına yükseltilmesi açık** (şimdilik iki-değerli satır-içi enum) → [`../../../../todo.md`](../../../../todo.md). |
| `fileSourcePropertyId` | int? | koşullu | — | `fileSourceType = fileProperty` iken AI'a verilecek dosyayı taşıyan **file property**. `thumbnail` iken kullanılmaz. **`settings` içi referans id** — DB FK'si değil, uygulama-katmanı doğrulaması (§3 not). |

> **Akış yönlendirme `settings`'te DEĞİL:** AI **başarıyla** çalışıp parametre üretince **`default`** kodlu, **hata** durumunda **`onFail`** kodlu `ProcessStepAction` tetiklenir (üretilen parametreler `default` aksiyonla taşınır) → [`../../process-step-action.md`](../../process-step-action.md), motor tarafı [`../../../../architectures/engine-core/flovo-bpm-engine.md`](../../../../architectures/engine-core/flovo-bpm-engine.md) §7.

## 2. Alt-model
- Yok. `aiSettings` **serbest** bir nesnedir (seçilen AI'a göre şekillenir; ortak alt-model tanımlanmaz).

## 3. Ortak alanlar (settings'te değil — `ProcessStep` kolonu)
`code`·`stepType`·`definition`·`order`·`showInHistory`·`skip*`·`environmentRestriction` → [`../../process-step.md`](../../process-step.md) §1.
`settings` içindeki referans id (`fileSourcePropertyId`) **DB FK'si değildir** → uygulama-katmanı doğrulaması + silme koruması (→ [`../../../../todo.md`](../../../../todo.md)).

## 4. JSON Schema
```json
{
  "$id": "process-step-settings/flovoAi",
  "type": "object",
  "additionalProperties": false,
  "required": ["selectedAi", "fileSourceType"],
  "properties": {
    "selectedAi":     { "type": "string", "minLength": 1 },
    "aiSettings":     { "type": "object" },
    "fileSourceType": { "enum": ["thumbnail", "fileProperty"] },
    "fileSourcePropertyId": { "type": "integer" }
  },
  "allOf": [
    {
      "if":   { "properties": { "fileSourceType": { "const": "fileProperty" } } },
      "then": { "required": ["fileSourcePropertyId"] }
    }
  ]
}
```
> Not: `selectedAi` kanonik enum'a, `fileSourceType` ayrı enum dosyasına yükseltildiğinde ve `aiSettings` per-AI şeması netleştiğinde şema **daraltılacaktır** (→ [`../../../../todo.md`](../../../../todo.md)). `aiSettings` içi bilerek **açık** bırakıldı (`additionalProperties` kısıtlanmadı). `fileSourcePropertyId` referansı **uygulama-katmanı** doğrulaması.

## 5. Örnek
```json
{
  "selectedAi": "expense",
  "fileSourceType": "thumbnail",
  "aiSettings": { "currency": "TRY" }
}
```
```json
{
  "selectedAi": "invoice",
  "fileSourceType": "fileProperty",
  "fileSourcePropertyId": 87
}
```

*Oluşturma: 2026-08-28.*
