# Process Step Settings — `notification` (Bildirim)

> **stepType:** `notification` · **Adım:** seçili alıcılara **Mail / Push / Toast** ile dinamik mesaj gönderen **otomatik** adım; bildirimi atıp **`default`** aksiyonla ilerler.
> **Davranış:** → [`../../../../service-settings/process-step.md`](../../../../service-settings/process-step.md) §3.6 · **Model (§3):** [`../../process-step.md`](../../process-step.md) §3.6 · **İndeks:** [`index.md`](./index.md).
> **Depolama:** `ProcessStep.settings` (JSONB), ayrımlayıcı `stepType`.
>
> **Alt-model kaynağı (paylaşılan):** Bu dosyanın §2'sindeki **`SendNotificationMessages`** ve **`NotificationUserSelection`** (+ alt-parçaları) yalnız Bildirim adımına ait değildir; **`user` / `userGroup` adımlarının adıma-girince-bildirim kısayolu** ve **`timer` timeout bildirimi** de aynı `SendNotificationMessages` yapısını buradan referanslar. Bu yüzden alt-modeller burada **tam** tanımlıdır.

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `messages` | [`SendNotificationMessages`](#2-alt-modeller) | evet | — | **Ne gönderilir:** hedef kanallar + dil-başına başlık/metin + (yalnız Push/Toast) çalışma-zamanı parametreleri (§2). |
| `recipients` | `SendNotificationUsers[]` | evet | — | **Kime gönderilir:** bir veya **birden fazla** alıcı bloğu; her blok bağımsız bir hedef kitle tanımlar (bir bloğu asıl muhatap, diğerini CC yapabilirsiniz). En az bir blok beklenir (§2). |

> **Akış yönlendirme `settings`'te DEĞİL:** Bildirim gönderilip **`default`** kodlu `ProcessStepAction` ile ilerlenir; hedef adım aksiyonun `targetProcessStepId`'sindedir → [`../../process-step-action.md`](../../process-step-action.md).

## 2. Alt-modeller

### 2.1 `SendNotificationMessages` — gönderilecek içerik (paylaşılan)
Bir bildirimin **kanallarını** ve **çok-dilli metnini** taşır. Aynı içerik tanımı `user`/`userGroup` adımlarının adıma-girince-bildirimi ve `timer` timeout bildiriminde de kullanılır.

| Alan | Tip | Zorunlu | Açıklama |
|---|---|---|---|
| `channels` | [`NotificationChannel`](../../../enums/notification-channel.md)`[]` | evet | Bildirimin **hangi kanallardan** gideceği — `mail` · `push` · `toast`. Dinamik liste; aynı bildirimde birden fazla kanal seçilebilir. |
| `items` | `NotificationMessageItem[]` | evet | **Dil-başına** başlık/metin (§2.2). Alıcının diline uyan kayıt gösterilir; sabit TR/EN alan çiftleri yerine dinamik liste. |
| `parameters` | [`DynamicParameter`](./http-request.md#2-alt-model--dynamicparameter)`[]` | hayır | **Yalnız Push/Toast** — bildirimle taşınan çalışma-zamanı parametreleri. **UI'da gösterilmez**; frontendde veriyi güncellemek içindir (ör. `instanceId` + değişen alan değerleri → form anında güncellenir). **Mail'de kullanılmaz.** Parametre yapısı `DynamicParameter` (`name` + `value` = ValueAssignType kaynağı) → [`http-request.md`](./http-request.md) §2. |

### 2.2 `NotificationMessageItem` — tek dilin başlık/metni
`SendNotificationMessages.items` listesindeki her kayıt bir dil için içeriktir.

| Alan | Tip | Zorunlu | Açıklama |
|---|---|---|---|
| `languageCode` | string | evet | Dil kodu (ör. `tr` / `en`); alıcının diline göre eşleştirilir. |
| `title` | string | evet | Bildirim başlığı. |
| `text` | string | evet | Bildirim gövdesi. **Dinamik değişken** taşıyabilir: `#ProcessCreator` · `#ProcessState` · `#ProcessStartDate` · `#ServiceName` (+ form property referansları) çalışma-zamanında yerlerine konur. |

### 2.3 `SendNotificationUsers` — bir alıcı bloğu (paylaşılan)
Her blok tek bir **hedef türü** tanımlar; `recipients` bunlardan birden fazlasını içerebilir.

| Alan | Tip | Zorunlu | Açıklama |
|---|---|---|---|
| `recipientType` | [`NotificationRecipientType`](../../../enums/notification-recipient-type.md) | evet | Bloğun kimi hedeflediği — `user` (bir kullanıcı, `userSelection` ile çözülür) · `userGroup` (grup, `userGroupIds`) · `takeUsersWhoTookActionBefore` (süreçte daha önce aksiyon alanlar; ek alan gerektirmez). |
| `userSelection` | `NotificationUserSelection?` | koşullu | **`recipientType = user`** ise: kullanıcının nasıl belirleneceği (§2.4). Diğer türlerde boş. |
| `userGroupIds` | int[]? | koşullu | **`recipientType = userGroup`** ise: hedef kullanıcı grubu/grupları (UserGroup id'leri; `settings` içi mantıksal referans, DB FK'si değil). |
| `addToCc` | bool | hayır | `true` → bu blok **asıl muhatap değil, CC** (bilgi kopyası) olarak eklenir (mail/bildirim kopyası). `false`/yok → birincil alıcı. |

### 2.4 `NotificationUserSelection` — `user` alıcısının çözümü (paylaşılan)
`recipientType = user` olan blokta, kullanıcının **hangi yöntemle** belirleneceğini taşır.

| Alan | Tip | Zorunlu | Açıklama |
|---|---|---|---|
| `userType` | [`NotificationUserType`](../../../enums/notification-user-type.md) | evet | Belirleme yöntemi — `processStarter` (süreci başlatan) · `fixedUser` (sabit liste) · `variableUsers` (önceki adımların aksiyon alanları) · `formProperty` (formdaki bir alanda seçili kullanıcılar). |
| `fixedUserIds` | int[]? | koşullu | **`fixedUser`** ise: sabit seçilen kullanıcı id'leri. |
| `variableUserProcessStepIds` | int[]? | koşullu | **`variableUsers`** ise: hangi adımların aksiyon alanlarının hedefleneceği — kaynak `ProcessStep` id'leri. |
| `propertyId` | int? | koşullu | **`formProperty`** ise: kullanıcı(lar)ı taşıyan form property id'si. |

> **Koşullu alanlar (discriminator):** `SendNotificationUsers`'ta `recipientType`, `NotificationUserSelection`'da `userType` **ayrımlayıcıdır**; hangi ek alanın dolacağını belirler. Zorunluluk ve id referanslarının geçerliliği **uygulama-katmanında** doğrulanır (JSON Schema `additionalProperties:false` ile kapalı tutar, koşulu prose ile kurar).

## 3. Ortak alanlar (settings'te değil — `ProcessStep` kolonu)
`code`·`stepType`·`definition`·`order`·`showInHistory`·`skip*`·`environmentRestriction` → [`../../process-step.md`](../../process-step.md) §1.

## 4. JSON Schema
```json
{
  "$id": "process-step-settings/notification",
  "type": "object",
  "additionalProperties": false,
  "required": ["messages", "recipients"],
  "properties": {
    "messages":   { "$ref": "#/$defs/sendNotificationMessages" },
    "recipients": { "type": "array", "minItems": 1, "items": { "$ref": "#/$defs/sendNotificationUsers" } }
  },
  "$defs": {
    "sendNotificationMessages": {
      "type": "object",
      "additionalProperties": false,
      "required": ["channels", "items"],
      "properties": {
        "channels":   { "type": "array", "minItems": 1, "items": { "enum": ["mail", "push", "toast"] } },
        "items":      { "type": "array", "minItems": 1, "items": { "$ref": "#/$defs/notificationMessageItem" } },
        "parameters": { "type": "array", "items": { "$ref": "#/$defs/dynamicParameter" }, "default": [] }
      }
    },
    "notificationMessageItem": {
      "type": "object",
      "additionalProperties": false,
      "required": ["languageCode", "title", "text"],
      "properties": {
        "languageCode": { "type": "string", "minLength": 1 },
        "title":        { "type": "string" },
        "text":         { "type": "string" }
      }
    },
    "sendNotificationUsers": {
      "type": "object",
      "additionalProperties": false,
      "required": ["recipientType"],
      "properties": {
        "recipientType": { "enum": ["user", "userGroup", "takeUsersWhoTookActionBefore"] },
        "userSelection": { "$ref": "#/$defs/notificationUserSelection" },
        "userGroupIds":  { "type": "array", "items": { "type": "integer" } },
        "addToCc":       { "type": "boolean", "default": false }
      }
    },
    "notificationUserSelection": {
      "type": "object",
      "additionalProperties": false,
      "required": ["userType"],
      "properties": {
        "userType":                   { "enum": ["processStarter", "fixedUser", "variableUsers", "formProperty"] },
        "fixedUserIds":               { "type": "array", "items": { "type": "integer" } },
        "variableUserProcessStepIds": { "type": "array", "items": { "type": "integer" } },
        "propertyId":                 { "type": "integer" }
      }
    },
    "dynamicParameter": {
      "type": "object",
      "additionalProperties": false,
      "required": ["name", "value"],
      "properties": {
        "name":  { "type": "string", "minLength": 1 },
        "value": { "type": "object" }
      }
    }
  }
}
```
> Not: `dynamicParameter.value`'nun tam şeması **ValueAssignType** discriminated-union'ıdır (`fixedValue`/`propertyValue`/`fromCalculation` → [`../../../enums/value-assign-type.md`](../../../enums/value-assign-type.md)); ortak tanım [`http-request.md`](./http-request.md) §2/§4. `recipientType`↔ek-alan ve `userType`↔ek-alan koşulları, `userGroupIds`/`fixedUserIds`/`propertyId` referansları **uygulama-katmanı** doğrulaması.

## 5. Örnek
```json
{
  "messages": {
    "channels": ["mail", "push"],
    "items": [
      { "languageCode": "tr", "title": "Masraf onayınızda", "text": "#ProcessCreator tarafından açılan masraf onayınızı bekliyor." },
      { "languageCode": "en", "title": "Expense awaiting you", "text": "An expense opened by #ProcessCreator is awaiting your approval." }
    ],
    "parameters": [
      { "name": "instanceId", "value": { "valueAssignType": "propertyValue", "propertyValue": { "propertyId": 7 } } }
    ]
  },
  "recipients": [
    { "recipientType": "user", "userSelection": { "userType": "processStarter" }, "addToCc": false },
    { "recipientType": "userGroup", "userGroupIds": [12, 15], "addToCc": true }
  ]
}
```

*Oluşturma: 2026-08-28.*
