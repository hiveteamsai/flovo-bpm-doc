# DTO — ActionTransfer

> **Tür:** **DTO** (Data Transfer Object) — **DB tablosu değildir.** Bir aksiyon tetiklendiğinde sonraki adıma taşınan
> **veri aktarım paketi**. Kalıcı biçimi: `ProcessStepInstance.processStepActionParameter` alanında **JSON string** olarak
> saklanır (ayrı tablo / PK / FK yok).
> **Davranış/kullanım:** → [`../../../service-settings/process-step-action.md`](../../../service-settings/process-step-action.md) §2
> ("Aksiyon Veri Aktarım Modeli").

## 0. Nedir?
Bir aksiyon tetiklendiğinde taşıdığı veri **3 alandan** oluşur — **üçü de opsiyonel**, boş olabilir:

| Alan | Tip | Ne için |
|---|---|---|
| `parameters` | obje-map `{ key: value }` | Adımdan adıma taşınan **geçici** veri (**forma yazılmaz**); anahtar **serbest**. `mergeParameter` ile zincir boyunca birikebilir (§2.1). |
| `changeList` | obje-map `{ Property.code: value }` | **Forma yazılan kalıcı** alan değerleri; her adım iş yapmadan **önce** forma merge edilir (`InstanceValue.data = data \|\| changeList`). Anahtar = yazılan servisin **yazılabilir** `Property.code`'u. |
| `action` | `string?` | **HTTP Request** adımının **response**'undan gelen **aksiyon kodu** (opsiyonel/nullable). **Doluysa** → adıma bağlı aksiyonlardan **aynı `code`'lu** olan tetiklenir; **boş/null** → **`default`** kodlu aksiyon tetiklenir. |

## 1. Yapı (JSON)
```jsonc
{
  "parameters": { /* geçici, adımdan adıma  — obje-map, serbest anahtar             — opsiyonel */ },
  "changeList": { /* kalıcı, forma yazılır  — obje-map { "Property.code": value }    — opsiyonel */ },
  "action":     "approve"  /* string? — tetiklenecek aksiyon KODU (response'tan); boş/null → `default` — opsiyonel */
}
```

## 2. Değer modeli (ortak değer dili)
`parameters` ve `changeList` içindeki değerler, **`InstanceValue.data` ile aynı değer-modelini** kullanır — yani
**`propertyValuesTemplates`** şekilleri (skaler · `LabeledValue {value, display, translationCode}` · user-ref
`{userId, nameSurname}` · phone `{countryCode, number}` · list-of-model …). Değer **kayıpsız** akar; forma yazmak = düz
JSONB merge, adıma taşımak = aynı objeyi geçirmek. Ayrıntı (tablo · yazılamaz alanlar · bütünsel taşıma · JSON Schema
kapısı) → [`../../../service-settings/process-step-action.md`](../../../service-settings/process-step-action.md) §2.2 ·
değer şablonları → [`../../processInstances/propertyValuesTemplates/index.md`](../../processInstances/propertyValuesTemplates/index.md).

## 3. Kullanım / kalıcılık
- **Üretim:** Bir aksiyon (`ProcessStepAction`) tetiklendiğinde bu paket üretilir; `mergeParameter` binding'i `parameters`
  birikimini yönetir (davranış → `process-step-action.md` §2.1).
- **Kalıcılık:** `ProcessStepInstance.processStepActionParameter` (string?) = bu ActionTransfer'in **JSON kaydı**
  (→ [`../../processInstances/process-step-instance.md`](../../processInstances/process-step-instance.md)).
- **Tetikleme girdisi:** **Süreç Adımı Tetikleme** adımının girdisi bir ActionTransfer'dir
  (→ [`../../../service-settings/process-step.md`](../../../service-settings/process-step.md) §3.5).

## 4. Kararlar / açık noktalar
- ✅ **`action` alanının şekli — ÇÖZÜLDÜ (v0.33): `string?` (aksiyon kodu).** Bir obje değil, **kod string'idir**; **doluysa**
  adıma bağlı **aynı `code`'lu** aksiyon tetiklenir, **boş/null** ise **`default`** kodlu aksiyon tetiklenir (→ §0/§1).
- [ ] **`user` alanı eklenmeli mi** *(AÇIK → [`../../../todo.md`](../../../todo.md))* — aksiyon/parametre verisinden
  `Instance.creatorUserId`'yi **opsiyonel** set etmek için. _(process-step-action §2 · process-step §3.12)_

*Oluşturma: 2026-08-25.*
