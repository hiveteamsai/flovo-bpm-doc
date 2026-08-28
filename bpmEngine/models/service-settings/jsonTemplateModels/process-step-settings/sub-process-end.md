# Process Step Settings — `subProcessEnd` (Alt Süreç Bitişi)

> **stepType:** `subProcessEnd` · **Adım:** bir **alt sürecin son adımı** — ana sürecin **Süreç Bitişi (§3.17)**'nin
> alt-süreç karşılığı; motor bu adıma ulaşınca alt süreç yürütmesi **sonlanır** (yürütme döngüsünün çıkış düğümü).
> **Davranış:** → [`../../../../service-settings/process-step.md`](../../../../service-settings/process-step.md) §3.21 · **Model (§3.16):** [`../../process-step.md`](../../process-step.md) §3.16 · **İndeks:** [`index.md`](./index.md).
> **Depolama:** `ProcessStep.settings` (JSONB), ayrımlayıcı `stepType`.

## 1. `settings` (JSONB) — **AYARSIZ** (`settings = {}`)
Bu adımın **tipe-özel ayarı yoktur**; `settings` **boş nesnedir** (`{}`).

**Neden ayarsız:** Alt Süreç Bitişi yalnızca alt süreç kolunun **açık çıkış düğümüdür**. Alt süreç bağımsız ve yardımcı bir
koldur; **kimseyi onayda bekletmez** ve **geri-taşıma / re-open yoktur**. Bu yüzden Süreç Bitişi'nin (§3.17)
bitiş-sonrası erişim ayarları — `processViewProfileId` / `userGroupIds` — **burada yoktur**. Adımın tek işi kolu tanımlı bir
biçimde sonlandırmaktır; seçilecek bir parametre taşımaz.

## 2. Neden ayrı adım tipi (bilgi)
Alt Süreç Başlangıcı (§3.20) alt sürecin girişini açık bir süreç adımı yaptı; simetrik biçimde Alt Süreç Bitişi de **çıkışı**
açık bir düğüm yapar. Böylece "aksiyonu olmayan otomatik adımın kolu ima yoluyla bitirmesi" belirsizliği ortadan kalkar; her
alt süreç kolunun **tanımlı bir sonu** olur. Bu adımda **giden aksiyon (`ProcessStepAction`) yoktur** — kol burada biter.

## 3. Ortak alanlar (settings'te değil — `ProcessStep` kolonu)
`code`·`stepType`·`definition`·`order`·`showInHistory`·`skip*`·`environmentRestriction` → [`../../process-step.md`](../../process-step.md) §1.

## 4. JSON Schema
```json
{
  "$id": "process-step-settings/subProcessEnd",
  "type": "object",
  "additionalProperties": false,
  "properties": {}
}
```
> Boş nesne (`{}`) dışında hiçbir alan kabul edilmez (`additionalProperties: false`).

*Oluşturma: 2026-08-28.*
