# Model — ProcessStepInstance (adım çalıştırma kaydı)

> **Durum:** 🟢 TANIMLI (alanlar netleşti)
> **Amaç:** Bir iş akışında **tek bir süreç adımının çalıştırılması**. Hangi adımın, hangi aksiyonla, kim/ne tarafından,
> ne zaman tetiklendiğinin runtime kaydı.

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Adım çalıştırma ID'si. |
| `processInstanceId` | int | FK → ProcessInstance.id | Ait olduğu iş akışı. |
| `instanceId` | int? | FK → Instance.id | İlgili form. **Null olabilir:** yeni form oluşturulmadan başka bir iş akışına yönlendiren adımlarda (bkz. aşağıdaki not — Form Yönlendirme). |
| `processStepId` | int | FK → ProcessStep.id | Çalıştırılan tasarım adımı. |
| `atUserId` | int? | FK → User.id | **Aksiyonu tetikleyen kullanıcı** (AT = ActionTrigger). Aksiyon tetiklendiğinde dolar. |
| `atApiKeyId` | int? | FK → ApiKey | **Aksiyonu tetikleyen API anahtarı** (kullanıcı yerine API başlatımı). Aksiyon tetiklendiğinde dolar. |
| `executionDate` | datetime | — | Bu adıma **ilk girildiği / çalıştığı** tarih. |
| `actionTriggerDate` | datetime? | — | **Aksiyonun tetiklendiği** zaman. Aksiyon tetiklendiğinde dolar. |
| `processStepActionId` | int? | FK → ProcessStepAction.id | Adım **bir aksiyon tetiklenerek** çalıştığında, **hangi aksiyonun** tetiklendiği. |
| `processStepActionParameter` | string? | — | **Sonraki aksiyona taşınan `ActionTransfer` modelinin JSON kaydı.** Aksiyon tetiklendiğinde dolar. |
| `atDelegateUserId` | int? | FK → User.id | **Vekaleten** aksiyon alınması durumunda, **vekaleten onaylayan** kişi. |

## İlişkiler
- **N – 1** → `ProcessInstance` (`processInstanceId`), `Instance` (`instanceId`), `ProcessStep` (`processStepId`),
  `ProcessStepAction` (`processStepActionId`), `User` (`atUserId`, `atDelegateUserId`), `ApiKey` (`atApiKeyId`).
- **1 – N** ← `InstanceAwaitingUser.processStepInstanceId`.

## Aksiyon tetiklendiğinde dolan alanlar
Adım **bir aksiyon tetiklenerek** ilerlediğinde şu alanlar birlikte dolar:
- **`processStepActionId`** — tetiklenen adım-aksiyon.
- **`atUserId`** / **`atApiKeyId`** — aksiyonu tetikleyen kullanıcı ya da API anahtarı.
- **`actionTriggerDate`** — tetikleme zamanı.
- **`processStepActionParameter`** — sonraki aksiyona taşınan **`ActionTransfer`** verisinin JSON kaydı (= aksiyon veri
  aktarım paketi `parameters`/`changeList`/`action` → `../../service-settings/process-step-action.md` §2).
- **`atDelegateUserId`** — yalnız **vekaleten** aksiyon alındıysa (vekaleten onaylayan kişi).

## Notlar / açık noktalar
- **`instanceId` neden null olabilir:** Yeni form oluşturmak istemediğimizde, **daha önce oluşturulmuş bir forma yönlendiren**
  adımlarda oluşan iş akışında **yeni form create edilmez**; `instanceId`'si olan **farklı bir iş akışına** yönlendirilir; bu
  yüzden bu execution kaydında `instanceId` boş kalır. Örnek: `../../sampleProcess/scanBarcode/` — `redirect` (Form Yönlendirme) adımı.
- **`AT` ön eki** = **ActionTrigger**.
- **Bağımsız alt süreç & `processStepId`:** Dışarıdan (webhook / Customer API) veya **Süreç Adımı Tetikleme** ile başlayan
  bağımsız alt süreçlerin giriş düğümü bir **süreç adımıdır** (**Alt Süreç Başlangıcı** → `../../service-settings/process-step.md`
  §3.20); bu sayede alt süreç yürütmesi de **geçerli bir `processStepId` ile** kaydedilir (webhook'un bir adıma bağlı
  olmama sorunu çözüldü). Alt süreç **yeni bir `ProcessInstance`** olarak çalışır (`processInstanceId` = o yeni akış;
  `ProcessInstance.parentProcessInstanceId` = alt sürecin koştuğu **hedef/host instance'ın ana süreci** — **tetikleyen** değil → `process-instance.md`).
- **`ActionTransfer`** = aksiyonla sonraki adıma taşınan **veri aktarım paketi** (`parameters`/`changeList`/`action`);
  `processStepActionParameter` bu paketin JSON kaydıdır → `../../service-settings/process-step-action.md` §2.
- `atDelegateUserId` ↔ yetkilendirme **impersonation/vekalet** ilişkisi → `../../organization-settings/permissions.md`.

*Oluşturma: 2026-07-06.*
