# Model — Instance (doldurulmuş form / süreç örneği)

> **Durum:** 🟢 TANIMLI (form-düzeyi alanlar netleşti; **property value depolaması** → `InstanceValue` (1–1) ile modellendi)
> **Amaç:** Bir iş akışında oluşturulan **doldurulmuş form** (runtime veri kaydı). `Property` tanımlarına göre
> girilen form değerlerinin sahibi/örneği; mevcut `Status`'u taşır.
> **Oluşturulma:** Instance, **Instance Creator** süreç adımı tarafından oluşturulur.

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Instance ID'si. |
| `serviceId` | int | FK → Service.id | Formun ait olduğu servis. |
| `organizationId` | int | (denormalize) | Kiracı — **RLS/tenant izolasyonu** (RLS Pattern B v2: her tenant-tabloda `organizationId`; DB-seviyesi izolasyon). |
| `processInstanceId` | int | FK → ProcessInstance.id | Formu oluşturan iş akışı. |
| `creatorUserId` | int? | FK → User.id | Instance sahibi / oluşturan kullanıcı. **Null olabilir:** **`parameter` tipi** serviste her zaman boş (sahipsiz veri-kaynağı); **`form` tipinde** ise süreç **API/webhook ile** (tek oluşturan kullanıcı olmadan) başlatılırsa boş kalabilir — başlatan `ProcessInstance.createdByApiKeyId` ile izlenir (→ `../service-settings/service.md` `formType`). |
| `createdDate` | datetime | — | **Instance Creator** adımının formu **oluşturduğu** tarih. |
| `deleted` | bool | — | **Soft-delete** işareti. `true` = kayıt silinmiş sayılır (fiziksel silme yok). |
| `statusId` | int | FK → Status.id | Formun **mevcut durumu** (organizasyon havuzu Status). |

## İlişkiler
- **N – 1** → `Service` (`serviceId`), `ProcessInstance` (`processInstanceId`), `User` (`creatorUserId`), `Status` (`statusId`).
- **1 – 1** ↔ `InstanceValue` (`instanceId` — **alan değerlerinin JSONB tapusu**).
- **1 – N** ← `InstanceAwaitingUser.instanceId`, `ProcessStepInstance.instanceId`, `AssociatedInstance.instanceId` / `.associatedInstanceId`,
  `InstanceAttr.instanceId`, `InstanceListItem.instanceId`, `InstanceValueChange.instanceId`, `InstanceValueOutbox.instanceId`.
  _(A′ yansıma yayılımı ayrı bir bağ tablosu kullanmaz; parent↔child `AssociatedInstance` üzerinden çözülür → [`reflection-propagation.md`](./reflection-propagation.md).)_

## Notlar / açık noktalar
- **Servis `formType`'ına göre oluşma (→ `../service-settings/service.md`):** **`form`** → akışla oluşur, `creatorUserId`
  **genelde dolu** ama **zorunlu değil** — süreç API/webhook ile (tek sahip olmadan) başlatılırsa **null olabilir**
  (başlatan → `ProcessInstance.createdByApiKeyId`; örn. `../../sampleProcess/referred`), `InstanceAwaitingUser` olabilir
  (onay akışı); **`parameter`** → oluşur ama `creatorUserId` **null** (sahipsiz veri-kaynağı), `InstanceAwaitingUser`'a
  **bakılmadan** yetkili kullanıcı işlem yapar; **`eventForm`** → **`Instance` oluşmaz** (pop-up değerleri `parameters` ile taşınır).
- **Property value depolaması → `InstanceValue` (1–1):** Instance **alan değerlerini taşımaz**; değerler ayrı bir kaynak-hakikat
  tablosunda (`InstanceValue.data`, **JSONB, code-keyed**) tutulur ve buradan `InstanceAttr`/`InstanceListItem` fihristlerine
  yansıtılır (CQRS + Outbox + NATS). Değer modelleri → [`instance-value.md`](./instance-value.md) · [`instance-attr.md`](./instance-attr.md) ·
  [`instance-list-item.md`](./instance-list-item.md) · [`instance-value-outbox.md`](./instance-value-outbox.md) · [`instance-value-change.md`](./instance-value-change.md) ·
  [`labeled-value.md`](./propertyValuesTemplates/labeled-value.md) (+ A′ yansıma yayılım mekanizması → [`reflection-propagation.md`](./reflection-propagation.md)). Kaynak mimari →
  `../../research/property-value-storage/form-deger-saklama-v2.html`.
- **`statusId` neden `InstanceValue.data`'da değil:** Form durumu **sık değişir** (her onayda). JSONB'de olsa her status
  değişiminde tüm `data` yeniden yazılır (MVCC) + rapor bayatlardı; bu yüzden `statusId` **kolonda** tutulur (hem canlı hem indeksli).
- **`deleted` = soft-delete** işaretidir (fiziksel silme yapılmaz); `deleted` alanı içeren tüm modellerde aynı kural geçerlidir (organizasyon-ayar modelleriyle **tek/kanonik isim** — `delete` kullanılmaz).
- **Validasyon durumu (açık soru):** validasyonları iş akışından **sürekli tekrar yapmamak** ve iş kuralı (`applyValidation`)
  validasyonlarıyla **tutarsızlığı önlemek** için `Instance`'a **`validated` (bool)** alanı mı eklenmeli, yoksa ayrı bir
  **`FormValidation`** tablosu mu oluşturulmalı? → `../../todo.md`.

*Oluşturma: 2026-07-06.*
