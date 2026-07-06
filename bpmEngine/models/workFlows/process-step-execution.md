# Model — ProcessStepExecution (adım çalıştırma kaydı)

> **Durum:** 🟢 TANIMLI (alanlar netleşti)
> **Amaç:** Bir iş akışında **tek bir süreç adımının çalıştırılması**. Hangi adımın, hangi aksiyonla, kim/ne tarafından,
> ne zaman tetiklendiğinin runtime kaydı.
> **Eski karşılığı:** `ServiceInstanceRequests` (isim eşlemesi → `../../research/compare/new-vs-current-names.md` §15.1).

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Adım çalıştırma ID'si. |
| `workFlowId` | int | FK → WorkFlow.id | Ait olduğu iş akışı. |
| `formId` | int (null olabilir) | FK → Form.id | İlgili form. **Null olabilir:** yeni form oluşturulmadan başka bir workflow'a yönlendiren adımlarda (bkz. aşağıdaki not — Form Yönlendirme). |
| `processStepId` | int | FK → ProcessStep.id | Çalıştırılan tasarım adımı. |
| `atUserId` | int (null olabilir) | FK → User.id | **Aksiyonu tetikleyen kullanıcı** (AT = ActionTrigger). Aksiyon tetiklendiğinde dolar. |
| `atApiKeyId` | int (null olabilir) | FK → ApiKey | **Aksiyonu tetikleyen API anahtarı** (kullanıcı yerine API başlatımı). Aksiyon tetiklendiğinde dolar. |
| `executionDate` | datetime | — | Bu adıma **ilk girildiği / çalıştığı** tarih. |
| `actionTriggerDate` | datetime (null olabilir) | — | **Aksiyonun tetiklendiği** zaman. Aksiyon tetiklendiğinde dolar. |
| `processStepActionId` | int (null olabilir) | FK → ProcessStepAction.id | Adım **bir aksiyon tetiklenerek** çalıştığında, **hangi aksiyonun** tetiklendiği. |
| `processStepActionParameter` | string (null olabilir) | — | **Sonraki aksiyona taşınan `ActionTransfer` modelinin JSON kaydı.** Aksiyon tetiklendiğinde dolar. |
| `atDelegateUserId` | int (null olabilir) | FK → User.id | **Vekaleten** aksiyon alınması durumunda, **vekaleten onaylayan** kişi. |

## İlişkiler
- **N – 1** → `WorkFlow` (`workFlowId`), `Form` (`formId`), `ProcessStep` (`processStepId`),
  `ProcessStepAction` (`processStepActionId`), `User` (`atUserId`, `atDelegateUserId`), `ApiKey` (`atApiKeyId`).
- **1 – N** ← `FormAwaitingUser.processStepExecutionId`.

## Aksiyon tetiklendiğinde dolan alanlar
Adım **bir aksiyon tetiklenerek** ilerlediğinde şu alanlar birlikte dolar:
- **`processStepActionId`** — tetiklenen adım-aksiyon.
- **`atUserId`** / **`atApiKeyId`** — aksiyonu tetikleyen kullanıcı ya da API anahtarı.
- **`actionTriggerDate`** — tetikleme zamanı.
- **`processStepActionParameter`** — sonraki aksiyona taşınan **`ActionTransfer`** verisinin JSON kaydı (= aksiyon veri
  aktarım paketi `parameters`/`changeList`/`action` → `../../service-settings/process-step-action.md` §2).
- **`atDelegateUserId`** — yalnız **vekaleten** aksiyon alındıysa (vekaleten onaylayan kişi).

## Notlar / açık noktalar
- **`formId` neden null olabilir:** Yeni form oluşturmak istemediğimizde, **daha önce oluşturulmuş bir forma yönlendiren**
  adımlarda oluşan iş akışında **yeni form create edilmez**; `formId`'si olan **farklı bir workflow'a** yönlendirilir; bu
  yüzden bu execution kaydında `formId` boş kalır. Örnek: `../../sampleProcess/scanBarcode/` — `redirect` (Form Yönlendirme) adımı.
- **`AT` ön eki** = **ActionTrigger**.
- **`ActionTransfer`** = aksiyonla sonraki adıma taşınan **veri aktarım paketi** (`parameters`/`changeList`/`action`);
  `processStepActionParameter` bu paketin JSON kaydıdır → `../../service-settings/process-step-action.md` §2.
- `atDelegateUserId` ↔ yetkilendirme **impersonation/vekalet** ilişkisi → `../../organization-settings/permissions.md`.

*Oluşturma: 2026-07-06.*
