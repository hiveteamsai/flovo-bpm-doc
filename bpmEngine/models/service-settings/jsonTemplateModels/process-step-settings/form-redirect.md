# Process Step Settings — `formRedirect` (Form Yönlendirme)

> **stepType:** `formRedirect` · **Adım:** form **create edilmeden önce**, belli bir **karşılaştırma/işlem** yapıp
> **farklı, var olan bir formun** açılmasını sağlayan adım (örn. barkodla var olan formu açma).
> **Davranış:** → [`../../../../service-settings/process-step.md`](../../../../service-settings/process-step.md) §3.19 · **Model (§3.16):** [`../../process-step.md`](../../process-step.md) §3.16 · **İndeks:** [`index.md`](./index.md).
> **Depolama:** `ProcessStep.settings` (JSONB), ayrımlayıcı `stepType`.

## 1. `settings` (JSONB) — **ERTELENDİ** (şema TBD → todo)
Bu adımın tipe-özel `settings` şeması **henüz modellenmedi**. Ayarsız değildir — ileride alan kazanacaktır; ancak alanlar
şu an **tanımsızdır**. Uydurma alan **eklenmez**. İzlenen açık madde:
[`../../../../todo.md`](../../../../todo.md) — *"`triggerProcessStep` / `formRedirect` adım ayarları — henüz modellenmedi (ayarsız grup §3.16)."*

## 2. Adım ne yapar (davranış → §3.19)
Yeni bir form **oluşturulmadan önce** araya girer: bir **karşılaştırma/işlem** yapar ve sonucuna göre, yeni form açmak
yerine **var olan farklı bir formu** açar. Amaç, mükerrer kayıt yerine ilgili mevcut kaydı getirmektir (örn. okunan
barkoda karşılık gelen mevcut formu açma → `sampleProcess/scanBarcode`).

## 3. Aday (henüz şema-dışı) kavramlar
Modelleme açıldığında ele alınacak, **şemaya dahil olmayan** aday kavramlar (todo'da izlenir — burada alan olarak tanımlanmaz):
- **Karşılaştırma/koşul:** hangi ölçüte göre yönlendirme yapılacağı (ör. bir alan/değer eşleşmesi).
- **Hedef form seçimi:** açılacak **var olan** form/instance'ın nasıl çözüleceği (eşleşen kaydın belirlenmesi).
- **Eşleşme yoksa davranış:** kayıt bulunamazsa yeni form akışıyla devam / hata.

> Bunlar **doğrulanmamış adaylardır**; şemaya dahil değildir ve model netleşene dek bağlayıcı değildir.

## 4. JSON Schema — **TBD**
Tipe-özel şema henüz tanımlı olmadığından bağlayıcı bir şema **yayımlanmaz**. Doğrulama kapısı için geçici iskelet
(alansız placeholder; alanlar modellenene dek boş):
```json
{
  "$id": "process-step-settings/formRedirect",
  "type": "object",
  "additionalProperties": false
}
```
> **Not:** Placeholder'dır — modelleme tamamlanınca `properties`/`required` bu dosyada tanımlanacak (→ [`../../../../todo.md`](../../../../todo.md)). Ortak alanlar (`code`·`stepType`·`definition`·`order`·`showInHistory`·`skip*`·`environmentRestriction`) `settings`'te değil, `ProcessStep` kolonundadır (→ [`../../process-step.md`](../../process-step.md) §1).

*Oluşturma: 2026-08-28.*
