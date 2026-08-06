# Model — ProcessInstance (iş akışı çalıştırma kaydı)

> **Durum:** 🟢 TANIMLI (alanlar netleşti)
> **Yeni model.**
> **Amaç:** Bir servisin sürecinin **çalıştırılması** (runtime örneği). Tasarım tarafındaki `Service`/`ProcessStep`
> ayarları kullanılarak motor tarafından üretilen **çalışma-zamanı** kaydı.

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | İş akışı çalıştırma ID'si. |
| `createdByUserId` | int? | FK → User.id | Akışı başlatan kullanıcı. _(kullanıcı **veya** API anahtarı — biri dolu.)_ |
| `createdByApiKeyId` | int? | FK → ApiKey (geçici) | Customer API ile oluşturulan kayıtlarda **kim yaptı** bilgisi — oluşturan doğrudan bir `User` olmadığından. Ad **geçici**; içeriği Customer API erişim mekanizması kesinleşince doğrulanacak. |
| `createdDate` | datetime | — | Oluşturulma zamanı. |
| `serviceId` | int | FK → Service.id | Hangi servisin süreci çalıştırılıyor. |
| `organizationId` | int | (denormalize) | Kiracı — **RLS/tenant izolasyonu** (RLS Pattern B v2: her tenant-tabloda `organizationId`; DB-seviyesi izolasyon). |
| `parentProcessInstanceId` | int? | FK → ProcessInstance.id (self) | **Alt süreç** ise **alt sürecin koştuğu (hedef/host) instance'ın ana `ProcessInstance`** id'si (**tetikleyen** süreç değil). **Null = ana süreç** (üst akış yok). |

## İlişkiler
- **N – 1** → `Service` (`serviceId`), `User` (`createdByUserId`), `ApiKey` (`createdByApiKeyId`),
  `ProcessInstance` (`parentProcessInstanceId`, **self** — alt sürecin üst/ana akışı).
- **1 – N** ← `ProcessStepInstance.processInstanceId`, `Instance.processInstanceId`, `ProcessInstance.parentProcessInstanceId` (üst akışın alt süreç çalıştırmaları).

## Notlar / açık noktalar
- **`createdByApiKeyId` / `ApiKey` (açık soru):** Customer API ile oluşturulan kayıtlarda oluşturan doğrudan bir `User`
  olmadığından, **işlemi kimin yaptığını** kaydetmek için `createdByApiKeyId` alanı kullanılır. Customer API'de `apiKey`
  mekanizması henüz kararlaştırılmadığından hedef **`ApiKey` modeli/adı geçici**; içine gelecek veri **erişim mekanizması
  kesinleşince doğrulanacak** → `../../todo.md`, `../index.md §4` (`ApiKey` henüz modellenmedi).
- `createdByUserId` **veya** `createdByApiKeyId` — biri dolar (kullanıcı ya da API başlatımı).
- **Alt süreç = yeni bir `ProcessInstance` (yeni Instance değil):** **Alt Süreç Başlangıcı** (→ `../../service-settings/process-step.md` §3.20) ile
  başlayan süreçler **yeni bir `ProcessInstance`** olarak oluşur (yeni **Instance/form kaydı** oluşmaz); `parentProcessInstanceId`'ye alt sürecin
  koştuğu **hedef/host instance'ın ana `ProcessInstance` id'si** yazılır (**tetikleyen** süreç değil). Instance'a bağ `parentProcessInstanceId`
  zinciriyle **dolaylı**dır (host instance'ın `processInstanceId`'si bu ana `ProcessInstance`'tır). **Ana süreçlerde** (Süreç Başlangıcı ile başlayan) `parentProcessInstanceId` **null**'dur.
- **`instance` alanı eklenmez + bağ dolaylı (KARAR):** `ProcessInstance`'a ayrı `instanceId`/`instance` alanı **konmaz** — bir Instance
  kendi **`Instance.processInstanceId`**'siyle ana sürecine bağlanır. Bir instance'ın **tek ana süreci** vardır; o ana sürecin
  **birden çok alt süreci** (`parentProcessInstanceId` = ana süreç) olabilir. Alt süreç bu zincir üzerinden instance'a **dolaylı**
  bağlanır; ek alan gerekmez (mevcut FK'ler yeterli → `service-trigger.md` "Alt süreç runtime temsili").
- **Ayrı tablo yok (KARAR):** Alt süreç çalıştırmaları **ayrı bir tabloda/sayfada tutulmaz** — ana süreçlerle **aynı
  `ProcessInstance` tablosunda** durur. Ana↔alt ayrımı yalnız **`parentProcessInstanceId`'nin null olup olmamasıyla**
  yapılır; izolasyon/sorgu/raporlama bu alan + `serviceId` üzerinden çözülür (alt süreç de bir süreçtir, ayrı depolama
  gerektirmez).

*Oluşturma: 2026-07-06.*
