# Model — WorkFlow (iş akışı çalıştırma kaydı)

> **Durum:** 🟢 TANIMLI (alanlar netleşti)
> **Eski karşılığı:** yok — **yeni model**.
> **Amaç:** Bir servisin sürecinin **çalıştırılması** (runtime örneği). Tasarım tarafındaki `Service`/`ProcessStep`
> ayarları kullanılarak motor tarafından üretilen **çalışma-zamanı** kaydı.

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | İş akışı çalıştırma ID'si. |
| `createdByUserId` | int (null olabilir) | FK → User.id | Akışı başlatan kullanıcı. _(kullanıcı **veya** API anahtarı — biri dolu.)_ |
| `createdByApiKeyId` | int (null olabilir) | FK → ApiKey (geçici) | Customer API ile oluşturulan kayıtlarda **kim yaptı** bilgisi — oluşturan doğrudan bir `User` olmadığından. Ad **geçici**; içeriği Customer API erişim mekanizması kesinleşince doğrulanacak. |
| `createdDate` | datetime | — | Oluşturulma zamanı. |
| `serviceId` | int | FK → Service.id | Hangi servisin süreci çalıştırılıyor. |
| `parentWorkFlowId` | int (null olabilir) | FK → WorkFlow.id (self) | **Alt süreç** ise tetikleyen **ana sürecin `WorkFlow`** id'si. **Null = ana süreç** (üst akış yok). |

## İlişkiler
- **N – 1** → `Service` (`serviceId`), `User` (`createdByUserId`), `ApiKey` (`createdByApiKeyId`),
  `WorkFlow` (`parentWorkFlowId`, **self** — alt sürecin üst/ana akışı).
- **1 – N** ← `ProcessStepExecution.workFlowId`, `Form.workFlowId`, `WorkFlow.parentWorkFlowId` (üst akışın alt süreç çalıştırmaları).

## Notlar / açık noktalar
- **`createdByApiKeyId` / `ApiKey` (açık soru):** Customer API ile oluşturulan kayıtlarda oluşturan doğrudan bir `User`
  olmadığından, **işlemi kimin yaptığını** kaydetmek için `createdByApiKeyId` alanı kullanılır. Customer API'de `apiKey`
  mekanizması henüz kararlaştırılmadığından hedef **`ApiKey` modeli/adı geçici**; içine gelecek veri **erişim mekanizması
  kesinleşince doğrulanacak** → `../../todo.md`, `../models.md §4` (`ApiKey` henüz modellenmedi).
- `createdByUserId` **veya** `createdByApiKeyId` — biri dolar (kullanıcı ya da API başlatımı).
- **Alt süreç = bağımsız yeni `WorkFlow`:** **Alt Süreç Başlangıcı** (→ `../../service-settings/process-step.md` §3.20) ile
  başlayan süreçler ana süreçten **bağımsız, yeni bir `WorkFlow`** olarak oluşur; `parentWorkFlowId`'ye **tetikleyen ana sürecin
  `WorkFlow` id'si** yazılır. **Ana süreçlerde** (Süreç Başlangıcı ile başlayan) `parentWorkFlowId` **null**'dur.

*Oluşturma: 2026-07-06.*
