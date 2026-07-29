# Enum — ServiceTriggerType

> **Kullanan model:** [`../service-settings/service-trigger.md`](../service-settings/service-trigger.md) — **ServiceTrigger** modeli, alan `serviceTriggerType`, tip **ServiceTriggerType**
> **Amaç:** Bir **ServiceTrigger**'ın **hangi olayla** ateşleneceğini belirler — bir zaman/süre dolduğunda mı, yoksa servis instance'ına bir **ilişki (associate) eklendiğinde/kaldırıldığında** mı.

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `timer` | Zaman/süre tetiklemesi | **`cronExpression`** ile belirlenen takvime göre ateşlenir; **`processStart`** (ana süreç başlangıcı) çalıştırılıp **yeni bağımsız bir ana süreç** başlatılır (alt süreç değil; kaynak instance yok). |
| `whenAddedAssociate` | İlişki **eklenince** | İzlenen ilişki alanına (**`targetPropertyId`**) bir **`AssociatedInstance`** eklendiğinde (ör. Form List'e kayıt eklenmesi, `isAssociatedCombobox` seçimi) ateşlenir. |
| `whenRemoveAssociate` | İlişki **kaldırılınca** | İzlenen ilişki alanından (**`targetPropertyId`**) bir **`AssociatedInstance`** kaldırıldığında ateşlenir. |

## Notlar
- İlişki (associate) kaydının **ne zaman düştüğü** → [`../processInstances/associated-instance.md`](../processInstances/associated-instance.md) (Form List → liste ekleme; Combobox → `isAssociatedCombobox=true` + değer değişimi).
- **Tespit noktası (çekirdek):** `whenAddedAssociate`/`whenRemoveAssociate`, **`AssociatedInstance` tablosuna yazım (AddOrUpdate/silme) sırasında** — DB güncelleme katmanında — tespit edilir; ilişki kuran her yerde ayrıca ele alınmaz. Eşleşme: **`AssociatedInstance.associatedPropertyId == trigger.targetPropertyId`** → kaynak instance = `associatedInstanceId` (→ [`../service-settings/service-trigger.md`](../service-settings/service-trigger.md) "Çalışma zamanı").
- Bu enum, süreç adımı tipi **ProcessStepType** ile **karıştırılmamalı**: ServiceTrigger **olay/zaman-güdümlü** (akış dışı) otomatik başlatıcıdır; `triggerProcessStep` ise **akış üzerindeki** bir süreç adımıdır.

*Oluşturma: 2026-07-29.*
