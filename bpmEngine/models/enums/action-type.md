# Enum — ActionType

> **Kullanan model:** [`action.md`](../organization-settings/action.md) — alan `actionType`, tip **ActionType** · binding: [`process-step-action.md`](../service-settings/process-step-action.md)
> **Amaç:** Bir **aksiyonun tetiklenme/çalışma türünü** belirler — kullanıcı aksiyona bastığında ne olacağını (manuel onay mı, cihaz eylemi mi, otomatik mi, pop-up form mu) tanımlar.
> **Davranış kataloğu:** → [`../../service-settings/process-step-action.md`](../../service-settings/process-step-action.md) §3.

## Değerler
| Kod | Anlam | Ne için |
|---|---|---|
| `manual` | Manuel — kullanıcının elle bastığı standart aksiyon. | Onayla/Reddet/İleri gibi akışı ilerleten manuel adım eylemleri. |
| `eventForm` | Aksiyon anında, `formType=eventForm` bir servisin seçili görüntüleme profili **pop-up** olarak açılır; sonuç `parameters` ile döner. | Akış/instance oluşturmadan, aksiyon sırasında ek veri toplamak. |
| `takePhoto` | Fotoğraf Çek — aksiyon cihaz kamerasını açar. | Aksiyona fotoğraf ekletmek. |
| `selectFile` | Dosya Seç — aksiyon dosya seçiciyi açar. | Aksiyona dosya/ek iliştirmek. |
| `scanBarcode` | Barcode Tara — aksiyon barkod/QR tarayıcıyı açar. | Aksiyonu tarama sonucuyla tetiklemek. |
| `webhook` | Webhook — aksiyon dış bir uç noktaya HTTP çağrısı yapar. | Entegrasyon/dış sistem tetikleme. |
| `autoAction` | Autoaction — kullanıcı etkileşimi olmadan koşul sağlanınca otomatik çalışır. | Otomatik ilerleme/sistem aksiyonu. |
| `delete` | Sil (kaydırmalı) — aksiyon alınınca form **UI'dan kaldırılır**; **card görünümünde** bu tipteki aksiyon **swipe item** olarak render edilir. | Kart listesinde kaydırarak (swipe) formu görünümden silme. |

## Notlar
- **İsim ayrımı:** Bu enum **`Action.actionType`**'tır; iş kuralı etkisi olan [`business-rule-action-type.md`](./business-rule-action-type.md) ise **`BusinessRule.businessRuleActionType`** (v0.7'de karışmayı önlemek için yeniden adlandırıldı). Ayrı enum'lardır.
- Kodlar **camelCase** olarak normalize edildi (v0.7); görünen Türkçe ad "Anlam" sütunundadır.
- **`delete` (v0.33):** aksiyon alınınca ilgili **form UI'dan kaldırılır**; **card (kart) görünümünde** bu tipteki aksiyon **swipe item** (kaydırmalı aksiyon) olarak gösterilir. Swipe **ayrı bir `actionDisplayType` değildir** — doğrudan **`delete` türüne** bağlı bir sunum davranışıdır (`actionDisplayType` görünürlük bağlamını ayrıca yönetmeye devam eder). Davranış → [`../../service-settings/process-step-action.md`](../../service-settings/process-step-action.md) §3.8.

*Oluşturma: 2026-07-10.*
