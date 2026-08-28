# Process Step Settings — `user` (Kullanıcı)

> **stepType:** `user` · **Adım:** **tek kullanıcının** onayına giden **insan-görev** adımı; atanan kişi formu görür/düzenler,
> form **aksiyon-alınabilir** olur ve kişi adımın aksiyonlarından birini **manuel** tetikler.
> **Davranış:** → [`../../../../service-settings/process-step.md`](../../../../service-settings/process-step.md) §3.15 · **Model (§3):** [`../../process-step.md`](../../process-step.md) §3.10 · **İndeks:** [`index.md`](./index.md).
> **Depolama:** `ProcessStep.settings` (JSONB), ayrımlayıcı `stepType`.

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `userType` | [`ProcessStepUserType`](../../../enums/process-step-user-type.md) | evet | — | Aksiyonu alacak **tek kullanıcının belirlenme yöntemi**. Seçime göre aşağıdaki id alanlarından **biri** dolar (`processStarter`'da ek alan gerekmez). |
| `fixedUserId` | int? | koşullu | — | `userType = fixedUser` ise: aksiyonu alacak **sabit** kullanıcı (tasarım anında seçilir). |
| `userAdministratorSourceProcessStepId` | int? | koşullu | — | `userType = usersManager` ise: aksiyon sahibi, **bu kaynak adımda son onayı veren** kullanıcının **yöneticisidir**; alan o adımı işaret eder ("yönetici" muğlak kalmasın diye belirli bir adımın onaylayanına bağlanır). |
| `departmentManagerDepartmentId` | int? | koşullu | — | `userType = departmentManager` ise: yöneticisi aksiyonu alacak **hedef departman**. |
| `variableUserPropertyId` | int? | koşullu | — | `userType = variableUser` ise: aksiyonu alacak kullanıcıyı **çalışma-zamanında taşıyan** form alanı (property). |
| `processViewProfileId` | int | evet | — | Atanan kullanıcının formu **göreceği/düzenleyeceği görüntüleme profili** (→ [`../../../../service-settings/view-profile.md`](../../../../service-settings/view-profile.md)). |
| `sendNotificationOnStep` | `SendNotificationMessages`? | hayır | — | Adıma girildiğinde **atanan kullanıcıya** gönderilecek bildirim kısayolu (yalnız mesaj/kanal bloğu; alıcı = bu adımın atananı). Yapı → **§2**. |
| `timeout` | `ProcessStepTimerSettings`? | hayır | — | Adıma girildiğinde başlayan **otomatik süre**; dolunca **timeout aksiyonuna** düşer (eskalasyon, no-code). Yapı → **§2**. |

> **`userType` → dolacak id alanı:** `processStarter` (ek alan yok) · `fixedUser` → `fixedUserId` · `usersManager` → `userAdministratorSourceProcessStepId` · `departmentManager` → `departmentManagerDepartmentId` · `variableUser` → `variableUserPropertyId`.

> **Atama çözülemezse → hata/fallback (KARAR):** Dinamik yöntem (`usersManager`/`departmentManager`/`variableUser`) **boş** dönerse
> (yönetici tanımsız, property boş vb.) atanan **belirlenemez**; adım **sessizce beklemez** → **hata** üretir ve `onFail`/fallback
> akışına düşer (→ [`../../../../service-settings/process-step.md`](../../../../service-settings/process-step.md) §3.15).

## 2. Gömülü bloklar (cross-ref — burada yeniden tanımlanmaz)
Bu adımın iki opsiyonel bloğu, **başka dosyalarda tanımlı ortak modelleri** gömülü kullanır:

| Alan | Ortak model | Tanım |
|---|---|---|
| `sendNotificationOnStep` | `SendNotificationMessages` (kanal + dil-başına başlık/mesaj + parametreler) | → [`./notification.md`](./notification.md) |
| `timeout` | `ProcessStepTimerSettings` (`timeoutActive` + süre hesap stili + timeout bildirimi) | → [`./timer.md`](./timer.md) |

> `sendNotificationOnStep` yalnız **mesaj bloğunu** taşır (alıcı seçimi yok); alıcı **bu adımın atanan kullanıcısıdır**.
> `timeout`, Timer ailesinin **timeout** kullanımıdır (adıma girince başlar, dolunca timeout aksiyonu = eskalasyon hedefi).

## 3. Ortak alanlar (settings'te değil — `ProcessStep` kolonu)
`code`·`stepType`·`definition`·`order`·`showInHistory`·`skip*`·`environmentRestriction` → [`../../process-step.md`](../../process-step.md) §1.

## 4. JSON Schema
```json
{
  "$id": "process-step-settings/user",
  "type": "object",
  "additionalProperties": false,
  "required": ["userType", "processViewProfileId"],
  "properties": {
    "userType": { "enum": ["processStarter", "fixedUser", "usersManager", "departmentManager", "variableUser"] },
    "fixedUserId":                          { "type": "integer" },
    "userAdministratorSourceProcessStepId": { "type": "integer" },
    "departmentManagerDepartmentId":        { "type": "integer" },
    "variableUserPropertyId":               { "type": "integer" },
    "processViewProfileId": { "type": "integer" },
    "sendNotificationOnStep": { "type": "object" },
    "timeout":                { "type": "object" }
  }
}
```
> Not: `userType`'a **karşılık gelen** id alanının varlığı **koşulludur** (`processStarter` hariç) — **uygulama-katmanı** doğrulaması.
> `sendNotificationOnStep`/`timeout` tam şeması sırasıyla `notification.md` (`SendNotificationMessages`) ve `timer.md` (`ProcessStepTimerSettings`)
> içinde; buradaki `type:object` yalnız gömülü blok yeridir. Referans id'ler (`fixedUserId`·`userAdministratorSourceProcessStepId`·
> `departmentManagerDepartmentId`·`variableUserPropertyId`·`processViewProfileId`) DB FK'si değil, **uygulama-katmanı** doğrulaması.

## 5. Örnek
```json
{
  "userType": "departmentManager",
  "departmentManagerDepartmentId": 7,
  "processViewProfileId": 12,
  "sendNotificationOnStep": {
    "channels": ["push"],
    "items": [ { "languageCode": "tr", "title": "Onayınız bekleniyor", "text": "Masraf formu onayınıza düştü." } ]
  },
  "timeout": { "timeoutActive": true, "workStyle": "normalCalendar" }
}
```
> _(Gömülü blokların tam alan seti → `notification.md` / `timer.md`.)_

*Oluşturma: 2026-08-28.*
