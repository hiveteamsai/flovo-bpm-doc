# Model — Instance (doldurulmuş form / süreç örneği)

> **Durum:** 🟢 TANIMLI (form-düzeyi alanlar netleşti; **property value depolaması** sonraya bırakıldı)
> **Amaç:** Bir iş akışında oluşturulan **doldurulmuş form** (runtime veri kaydı). `Property` tanımlarına göre
> girilen form değerlerinin sahibi/örneği; mevcut `Status`'u taşır.
> **Oluşturulma:** Instance, **Instance Creator** süreç adımı tarafından oluşturulur.

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Instance ID'si. |
| `serviceId` | int | FK → Service.id | Formun ait olduğu servis. |
| `processInstanceId` | int | FK → ProcessInstance.id | Formu oluşturan iş akışı. |
| `creatorUserId` | int? | FK → User.id | Instance sahibi / oluşturan kullanıcı. **Null olabilir:** **`parameter` tipi** serviste her zaman boş (sahipsiz veri-kaynağı); **`form` tipinde** ise süreç **API/webhook ile** (tek oluşturan kullanıcı olmadan) başlatılırsa boş kalabilir — başlatan `ProcessInstance.createdByApiKeyId` ile izlenir (→ `../service-settings/service.md` `formType`). |
| `createdDate` | datetime | — | **Instance Creator** adımının formu **oluşturduğu** tarih. |
| `deleted` | bool | — | **Soft-delete** işareti. `true` = kayıt silinmiş sayılır (fiziksel silme yok). |
| `statusId` | int | FK → Status.id | Formun **mevcut durumu** (organizasyon havuzu Status). |

## İlişkiler
- **N – 1** → `Service` (`serviceId`), `ProcessInstance` (`processInstanceId`), `User` (`creatorUserId`), `Status` (`statusId`).
- **1 – N** ← `InstanceAwaitingUser.instanceId`, `ProcessStepInstance.instanceId`, `AssociatedInstance.instanceId` / `.associatedInstanceId`.

## Notlar / açık noktalar
- **Servis `formType`'ına göre oluşma (→ `../service-settings/service.md`):** **`form`** → akışla oluşur, `creatorUserId`
  **genelde dolu** ama **zorunlu değil** — süreç API/webhook ile (tek sahip olmadan) başlatılırsa **null olabilir**
  (başlatan → `ProcessInstance.createdByApiKeyId`; örn. `../../sampleProcess/referred`), `InstanceAwaitingUser` olabilir
  (onay akışı); **`parameter`** → oluşur ama `creatorUserId` **null** (sahipsiz veri-kaynağı), `InstanceAwaitingUser`'a
  **bakılmadan** yetkili kullanıcı işlem yapar; **`eventForm`** → **`Instance` oluşmaz** (pop-up değerleri `parameters` ile taşınır).
- **Property value depolaması (sonraya bırakıldı):** Instance **alan değerlerinin** nerede/nasıl tutulacağı (bu modelde mi,
  ayrı value tablolarında mı) daha detaylı araştırma sonrası kararlaştırılacak; alan-düzeyi tanımlar burada değil, ayrı
  **değer dokümantasyonunda** yapılacak → `../../research/property-value-storage/form-value-scenarios.md` (§12) · `../../todo.md`.
- **`deleted` = soft-delete** işaretidir (fiziksel silme yapılmaz); `deleted` alanı içeren tüm modellerde aynı kural geçerlidir (organizasyon-ayar modelleriyle **tek/kanonik isim** — `delete` kullanılmaz).
- **Validasyon durumu (açık soru):** validasyonları iş akışından **sürekli tekrar yapmamak** ve iş kuralı (`applyValidation`)
  validasyonlarıyla **tutarsızlığı önlemek** için `Instance`'a **`validated` (bool)** alanı mı eklenmeli, yoksa ayrı bir
  **`FormValidation`** tablosu mu oluşturulmalı? → `../../todo.md`.

*Oluşturma: 2026-07-06.*
