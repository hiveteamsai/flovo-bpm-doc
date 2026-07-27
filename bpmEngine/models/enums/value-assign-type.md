# Enum — ValueAssignType

> **Kullanan model:** [`business-rule.md`](../service-settings/business-rule.md) (`assignValueToProperty` aksiyonu) · süreç adımı **Değer Atama** [`process-step.md`](../service-settings/process-step.md) — alan `valueAssignType`, tip **ValueAssignType**
> **Amaç:** Bir alana atanacak değerin **nereden geleceğini** (kaynağını) belirler.

## Değerler
| Değer | Anlam | Ne için | Geçerli bağlam |
|---|---|---|---|
| `fixedValue` | Sabit, elle girilen değer. | Bilinen sabit bir değeri yazmak. | **İş kuralı + Değer Atama** |
| `propertyValue` | Başka bir alanın değeri. | Alandan alana değer taşımak/yansıtmak. | **İş kuralı + Değer Atama** |
| `fromCalculation` | Bir ifade/hesaplama sonucu. | Formül ile türetilen değer. | **İş kuralı + Değer Atama** |
| `fromDataSet` | Bir veri kümesinden çekilen değer. | Kayıtlı veri setinden değer getirmek. | Yalnız iş kuralı |
| `search` | Arama sonucu seçilen değer. | Kullanıcının aramayla bulduğu kaydı atamak. | Yalnız iş kuralı |
| `httpRequest` | Dış HTTP isteğinin dönüşü. | Entegrasyondan gelen değeri atamak. | Yalnız iş kuralı |

## Notlar
- **Bağlama göre geçerli alt-küme (KARAR, v0.18):** Bu tek enum **iki bağlamda** paylaşılır (aynı kavram = *değer kaynağı*),
  fakat geçerli değer kümesi bağlama göre değişir: **iş kuralı `assignValueToProperty`** **6 değerin tümünü** kullanır; süreç
  adımı **Değer Atama** ise yalnız **`fixedValue` · `propertyValue` · `fromCalculation`** alt-kümesini kabul eder
  (`fromDataSet`/`search`/`httpRequest` Değer Atama'da **geçerli değil**). **Ayrı enum açılmadı** — aynı kavram için iki enum
  tekrar/bakım eşleşmesi yaratırdı; kısıt, adım `settings` JSONB'sinin **tip-başına JSON Schema**'sıyla (uygulama-katmanı
  doğrulama) uygulanır. → [`../service-settings/process-step.md`](../service-settings/process-step.md) §3.3 (Değer Atama).
- **Alan adı ayrıştırıldı (v0.18):** Süreç adımı Değer Atama alanı **`valueAssignType`** (tip **bu** enum — **ValueAssignType**); [`additional-qualification.md`](../organization-settings/additional-qualification.md)'deki **`valueType`** ise [`qualification-value-type.md`](./qualification-value-type.md)'dir (**QualificationValueType**). Artık **alan adları farklı** — çakışma yok.

*Oluşturma: 2026-07-10.*
