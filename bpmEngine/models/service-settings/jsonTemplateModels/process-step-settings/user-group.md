# Process Step Settings — `userGroup` (Kullanıcı Grubu)

> **stepType:** `userGroup` · **Adım:** **birden fazla kullanıcıya** aksiyon-alınabilir durumda iletilen **insan-görev** adımı;
> kümedeki **bir** üye aksiyon alınca süreç ilerler.
> **Davranış:** → [`../../../../service-settings/process-step.md`](../../../../service-settings/process-step.md) §3.16 · **Model (§3):** [`../../process-step.md`](../../process-step.md) §3.11 · **İndeks:** [`index.md`](./index.md).
> **Depolama:** `ProcessStep.settings` (JSONB), ayrımlayıcı `stepType`.

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `userGroupType` | [`ProcessStepUserGroupType`](../../../enums/process-step-user-group-type.md) | evet | — | Forma gidecek **kullanıcı kümesinin belirlenme yöntemi**. Seçime göre aşağıdaki id alanı dolar. |
| `userGroupId` | int? | koşullu | — | `userGroupType = fixedUserGroup` ise: aksiyona gidecek **sabit** kullanıcı grubu. |
| `dynamicUserListPropertyId` | int? | koşullu | — | `userGroupType = dynamicUserList` (property'deki **kullanıcılar**) **veya** `dynamicUserGroup` (property'deki **kullanıcı grubu**) ise: kümeyi **çalışma-zamanında taşıyan** form alanı (property). |
| `processViewProfileId` | int | evet | — | Onaya gidecek kullanıcıların formu **göreceği/düzenleyeceği görüntüleme profili** (→ [`../../../../service-settings/view-profile.md`](../../../../service-settings/view-profile.md)). |
| `sendNotificationOnStep` | `SendNotificationMessages`? | hayır | — | Adıma girildiğinde **küme üyelerine** gönderilecek bildirim kısayolu (yalnız mesaj/kanal bloğu; alıcı = bu adımın atananları). Yapı → **§2**. |
| `timeout` | `ProcessStepTimerSettings`? | hayır | — | Adıma girildiğinde başlayan **otomatik süre**; dolunca **timeout aksiyonuna** düşer (eskalasyon, no-code). Yapı → **§2**. |

> **`userGroupType` → dolacak id alanı:** `fixedUserGroup` → `userGroupId` · `dynamicUserList` / `dynamicUserGroup` → `dynamicUserListPropertyId`.

> **Politika (KARAR v0.32):** **Grup-onay eşiği YOK** — gruba iletilen formda **bir** üye aksiyon alınca süreç ilerler; quorum /
> "hepsi onaylar" / çoğunluk yoktur (tek üye yeterli — kalıcı). **Üyelik dinamiktir:** aksiyon alabilenler
> `InstanceAwaitingUser.userGroupId`'den **okuma-zamanında** çözülür → gruba sonradan eklenen/çıkan üye otomatik yansır.
> **Atama çözülemezse** (dinamik yöntemde küme boş) → **hata/fallback** (§3.16, `user` §1 ile aynı kural).

## 2. Gömülü bloklar (cross-ref — burada yeniden tanımlanmaz)
Bu adımın iki opsiyonel bloğu, **başka dosyalarda tanımlı ortak modelleri** gömülü kullanır:

| Alan | Ortak model | Tanım |
|---|---|---|
| `sendNotificationOnStep` | `SendNotificationMessages` (kanal + dil-başına başlık/mesaj + parametreler) | → [`./notification.md`](./notification.md) |
| `timeout` | `ProcessStepTimerSettings` (`timeoutActive` + süre hesap stili + timeout bildirimi) | → [`./timer.md`](./timer.md) |

> `sendNotificationOnStep` yalnız **mesaj bloğunu** taşır (alıcı seçimi yok); alıcı **bu adımın atanan üyeleridir**.
> `timeout`, Timer ailesinin **timeout** kullanımıdır (adıma girince başlar, dolunca timeout aksiyonu = eskalasyon hedefi).

## 3. Ortak alanlar (settings'te değil — `ProcessStep` kolonu)
`code`·`stepType`·`definition`·`order`·`showInHistory`·`skip*`·`environmentRestriction` → [`../../process-step.md`](../../process-step.md) §1.

## 4. JSON Schema
```json
{
  "$id": "process-step-settings/userGroup",
  "type": "object",
  "additionalProperties": false,
  "required": ["userGroupType", "processViewProfileId"],
  "properties": {
    "userGroupType": { "enum": ["fixedUserGroup", "dynamicUserList", "dynamicUserGroup"] },
    "userGroupId":               { "type": "integer" },
    "dynamicUserListPropertyId": { "type": "integer" },
    "processViewProfileId": { "type": "integer" },
    "sendNotificationOnStep": { "type": "object" },
    "timeout":                { "type": "object" }
  }
}
```
> Not: `userGroupType`'a **karşılık gelen** id alanının varlığı **koşulludur** — **uygulama-katmanı** doğrulaması.
> `sendNotificationOnStep`/`timeout` tam şeması sırasıyla `notification.md` (`SendNotificationMessages`) ve `timer.md`
> (`ProcessStepTimerSettings`) içinde; buradaki `type:object` yalnız gömülü blok yeridir. Referans id'ler
> (`userGroupId`·`dynamicUserListPropertyId`·`processViewProfileId`) DB FK'si değil, **uygulama-katmanı** doğrulaması.

## 5. Örnek
```json
{
  "userGroupType": "fixedUserGroup",
  "userGroupId": 4,
  "processViewProfileId": 12,
  "sendNotificationOnStep": {
    "channels": ["mail"],
    "items": [ { "languageCode": "tr", "title": "Grup onayı", "text": "Form, grubunuzun onayına iletildi." } ]
  }
}
```
> _(Gömülü blokların tam alan seti → `notification.md` / `timer.md`.)_

*Oluşturma: 2026-08-28.*
