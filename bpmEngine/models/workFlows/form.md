# Model — Form (doldurulmuş form / süreç örneği)

> **Durum:** 🟢 TANIMLI (form-düzeyi alanlar netleşti; **property value depolaması** sonraya bırakıldı)
> **Amaç:** Bir iş akışında oluşturulan **doldurulmuş form** (runtime veri kaydı). `Property` tanımlarına göre
> girilen form değerlerinin sahibi/örneği; mevcut `Status`'u taşır.
> **Oluşturulma:** Form, **FormCreator** süreç adımı tarafından oluşturulur.
> **Eski karşılığı:** `ServiceInstances` (isim eşlemesi → `../../research/compare/new-vs-current-names.md` §15.2).

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Form ID'si. |
| `serviceId` | int | FK → Service.id | Formun ait olduğu servis. |
| `workFlowId` | int | FK → WorkFlow.id | Formu oluşturan iş akışı. |
| `creatorUserId` | int | FK → User.id | Formu oluşturan kullanıcı. |
| `createdDate` | datetime | — | **FormCreator** adımının formu **oluşturduğu** tarih. |
| `delete` | bool | — | **Soft-delete** işareti. `true` = kayıt silinmiş sayılır (fiziksel silme yok). |
| `statusId` | int | FK → Status.id | Formun **mevcut durumu** (organizasyon havuzu Status). |

## İlişkiler
- **N – 1** → `Service` (`serviceId`), `WorkFlow` (`workFlowId`), `User` (`creatorUserId`), `Status` (`statusId`).
- **1 – N** ← `FormAwaitingUser.formId`, `ProcessStepExecution.formId`, `RelatedForm.formId` / `.relatedFormId`.

## Notlar / açık noktalar
- **Property value depolaması (sonraya bırakıldı):** Form **alan değerlerinin** nerede/nasıl tutulacağı (bu modelde mi,
  ayrı value tablolarında mı) daha detaylı araştırma sonrası kararlaştırılacak; alan-düzeyi tanımlar burada değil, ayrı
  **değer dokümantasyonunda** yapılacak → `../../form-value-scenarios.md` (§12) · `../../todo.md`.
- **`delete` = soft-delete** işaretidir (fiziksel silme yapılmaz); `delete` alanı içeren tüm modellerde aynı kural geçerlidir.
- **Validasyon durumu (açık soru):** validasyonları workflow'dan **sürekli tekrar yapmamak** ve iş kuralı (`ApplyValidation`)
  validasyonlarıyla **tutarsızlığı önlemek** için `Form`'a **`validated` (bool)** alanı mı eklenmeli, yoksa ayrı bir
  **`FormValidation`** tablosu mu oluşturulmalı? → `../../todo.md`.

*Oluşturma: 2026-07-06.*
