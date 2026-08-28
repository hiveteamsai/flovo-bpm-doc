# Process Step Settings — `triggerProcessStep` (Süreç Adımı Tetikleme)

> **stepType:** `triggerProcessStep` · **Adım:** formda yer alan **alt servislerin** süreç adımlarını (alt süreç /
> aksiyon) tetiklemek için kullanılan **akış-üzeri** otomatik adım.
> **Davranış:** → [`../../../../service-settings/process-step.md`](../../../../service-settings/process-step.md) §3.5 · **Model (§3.16):** [`../../process-step.md`](../../process-step.md) §3.16 · **İndeks:** [`index.md`](./index.md).
> **Depolama:** `ProcessStep.settings` (JSONB), ayrımlayıcı `stepType`.

## 1. `settings` (JSONB) — **ERTELENDİ** (şema TBD → todo)
Bu adımın tipe-özel `settings` şeması **henüz modellenmedi**. Ayarsız değildir — ileride alan kazanacaktır; ancak alanlar
şu an **tanımsızdır**. Uydurma alan **eklenmez**. İzlenen açık madde:
[`../../../../todo.md`](../../../../todo.md) — *"`triggerProcessStep` / `formRedirect` adım ayarları — henüz modellenmedi (ayarsız grup §3.16)."*

## 2. Adım ne yapar (davranış → §3.5)
Bir formun **alt servislerinin** süreç adımlarını tetikler; adıma girildiğinde ilgili alt süreci/aksiyonu **akış-üzeri**
başlatır. `ServiceTrigger` (akış-**dışı** otomatik olay/cron) ile sınır nettir: `triggerProcessStep` **akış-üzeri** bir
adımdır, girince tetikler; ServiceTrigger olay/zamanla akış-dışı çalışır (→ [`../../service-trigger.md`](../../service-trigger.md)).
Hedeflenen giriş düğümü tipik olarak bir **`subProcessStart`** (§3.20) olabilir.

## 3. Aday (henüz şema-dışı) kavramlar
Modelleme açıldığında ele alınacak, **şemaya dahil olmayan** aday kavramlar (todo'da izlenir — burada alan olarak tanımlanmaz):
- **Hedef seçim:** tetiklenecek alt-servis + hedef alt-süreç giriş adımı (`subProcessStart`) / aksiyon seçimi.
- **İlişkili instance hedefleme:** ilişkili instance'ların (`associatedInstance`) alt süreç/aksiyonunu tetikleme; hangi ilişkili kayıtların kapsanacağı.
- **Bekleme davranışı:** senkron/asenkron ilerleme (hedef sürecin sonuna kadar bekle / bekleme).
- **Girdi taşıma:** tetiklemeye geçirilecek `ActionTransfer` (`parameters`/`changeList`) — çalışma-zamanı girdisi, ayar olmayabilir.

> Bunlar **doğrulanmamış adaylardır**; şemaya dahil değildir ve model netleşene dek bağlayıcı değildir.

## 4. JSON Schema — **TBD**
Tipe-özel şema henüz tanımlı olmadığından bağlayıcı bir şema **yayımlanmaz**. Doğrulama kapısı için geçici iskelet
(alansız placeholder; alanlar modellenene dek boş):
```json
{
  "$id": "process-step-settings/triggerProcessStep",
  "type": "object",
  "additionalProperties": false
}
```
> **Not:** Placeholder'dır — modelleme tamamlanınca `properties`/`required` bu dosyada tanımlanacak (→ [`../../../../todo.md`](../../../../todo.md)). Ortak alanlar (`code`·`stepType`·`definition`·`order`·`showInHistory`·`skip*`·`environmentRestriction`) `settings`'te değil, `ProcessStep` kolonundadır (→ [`../../process-step.md`](../../process-step.md) §1).

*Oluşturma: 2026-08-28.*
