# Process Step Settings — `timer` · `timerStart` · `timerEnd` (Timer ailesi)

> **stepType:** `timer` · `timerStart` · `timerEnd` · **Adım:** zamanlayıcı ailesi — bir süre kurulur, süre dolunca **`default`** aksiyonla ilerlenir; Start/End adımları var-olan bir Timer'ı **başlatır/sonlandırır**.
> **Davranış:** → [`../../../../service-settings/process-step.md`](../../../../service-settings/process-step.md) §3.7 (Timer) · §3.8 (Timer Start) · §3.9 (Timer End) · **Model (§3):** [`../../process-step.md`](../../process-step.md) §3.7 · **İndeks:** [`index.md`](./index.md).
> **Depolama:** `ProcessStep.settings` (JSONB), ayrımlayıcı `stepType`.
>
> **Paylaşım notu (önemli):** Aynı `ProcessStepTimerSettings` yapısı, **`user` / `userGroup` (ve `parentInstanceUser`) insan-görev adımlarının `timeout` bloğunda gömülü** kullanılır (adıma girildiğinde otomatik süre başlatma). O adımlarda `settings.timeout` = **bu şemanın tamamı**; oradaki "timeout dolunca" davranışı, buradaki Timer davranışının aynısıdır. Bu yüzden yapı burada bütün olarak tanımlanır.

## 1. `settings` (JSONB) — tipe-özel ayarlar
Üç `stepType` **tek şemayı** paylaşır; her tip alanların **farklı alt-kümesini** doldurur (→ §1.1).

| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `timeoutActive` | bool | hayır | `false` | Zamanlayıcının/timeout'un **kurulu (armed)** olup olmadığı. `timer` adımında süre bu bayrakla etkinleşir; `timeout` bloğunda ise adıma girince timeout'un uygulanıp uygulanmayacağını belirler. |
| `workStyle` | [`TimerCalculationType`](../../../enums/timer-calculation-type.md) | koşullu | — | Sürenin **nasıl hesaplanacağı** — `workCalendar` (iş günü + çalışma saatleri) · `normalCalendar` (takvim günleri, erteleme opsiyonlu) · `fixedDateTime` (belirli tarih/saat). Seçilen değere göre aşağıdaki **üç bloktan biri** dolar. (`timer` + `timeout` içindir; Start/End'de kullanılmaz.) |
| `workCalendarSchedule` | `TimerWorkSchedule?` | koşullu | — | `workStyle = workCalendar` ise süre bloğu (§2.1). |
| `normalCalendarSchedule` | `TimerNormalSchedule?` | koşullu | — | `workStyle = normalCalendar` ise süre bloğu (§2.2). |
| `fixedDateTimeSchedule` | `TimerFixedSchedule?` | koşullu | — | `workStyle = fixedDateTime` ise süre bloğu (§2.3). |
| `timeoutNotificationActive` | bool | hayır | `false` | Süre dolunca **bildirim gönderilsin mi**. |
| `timeoutNotification` | [`SendNotificationMessages`](./notification.md#21-sendnotificationmessages--gönderilecek-içerik-paylaşılan)`?` | koşullu | — | `timeoutNotificationActive = true` ise gönderilecek bildirim — kanal + çok-dilli metin (Bildirim adımıyla **aynı** içerik modeli → [`notification.md`](./notification.md) §2.1). |
| `selectedTimerProcessStepId` | int? | koşullu | — | **Yalnız `timerStart` / `timerEnd`** için: başlatılacak/sonlandırılacak **hedef Timer adımı**nın `ProcessStep` id'si (`settings` içi mantıksal referans, DB FK'si değil → uygulama-katmanı doğrulaması). |

> **Akış yönlendirme `settings`'te DEĞİL:** Üç adım da işini yapıp **`default`** kodlu `ProcessStepAction` ile ilerler (Timer'da süre dolunca; Start/End'de anında). Hedef adım aksiyonun `targetProcessStepId`'sindedir → [`../../process-step-action.md`](../../process-step-action.md).

### 1.1 Üç `stepType` — hangi alanları kullanır
| `stepType` | Ne yapar | Dolan alanlar | Kullanılmayan |
|---|---|---|---|
| `timer` | **Süreçten bağımsız** kurulan zamanlayıcı (cron benzeri dinamik süre); süre dolunca `default` ile ilerler, opsiyonel timeout bildirimi atar. | `timeoutActive` · `workStyle` + ilgili `*Schedule` bloğu · `timeoutNotificationActive`/`timeoutNotification` | `selectedTimerProcessStepId` |
| `timerStart` | Seçili Timer adımının süresini **başlatır**; işini yapıp `default` ile ilerler. | `selectedTimerProcessStepId` | süre/bildirim alanları |
| `timerEnd` | **Daha önce başlatılmış** Timer'ı **sonlandırır**; işini yapıp `default` ile ilerler. | `selectedTimerProcessStepId` | süre/bildirim alanları |

> **Neden Start/End ayrı adım:** `timer` süreyi **tanımlar**; `timerStart`/`timerEnd` ise akışın belirli noktalarında o süreyi **kontrol eder** (aç/kapat). Böylece "bir işe X süre tanı, ara adımda tamamlandıysa iptal et" gibi kalıplar no-code kurulur — hedef timer `selectedTimerProcessStepId` ile işaret edilir.

## 2. Alt-modeller — süre blokları
`workStyle`'a karşılık gelen üç bloktan yalnız **biri** doldurulur.

### 2.1 `TimerWorkSchedule` — çalışma takvimine göre (`workCalendar`)
İş günü + çalışma saatleri (organizasyonun çalışma takvimi) üzerinden hesaplanan süre.

| Alan | Tip | Zorunlu | Açıklama |
|---|---|---|---|
| `value` | string | evet | Çalışma takvimine göre **süre miktarı** (referans andan itibaren, yalnız çalışma zamanı sayılarak ilerletilir). |

### 2.2 `TimerNormalSchedule` — normal takvime göre (`normalCalendar`)
Takvim günleri üzerinden hesap; opsiyonel **erteleme** (saat önce/sonra) alır.

| Alan | Tip | Zorunlu | Açıklama |
|---|---|---|---|
| `day` | string | evet | Süre — **takvim günü** cinsinden miktar. |
| `workTimeSelection` | [`WorkTimeSelection`](../../../enums/work-time-selection.md) | evet | Referans anın çalışma gününün **başı mı (`atWorkStart`) sonu mu (`atWorkEnd`)** sayılacağı. |
| `postponing` | bool | hayır | Hesaplanan zamana **erteleme** uygulanacak mı. |
| `timeAdjustmentOption` | [`TimeAdjustmentOption`](../../../enums/time-adjustment-option.md) | koşullu | Erteleme yönü — `hoursAfter` (sonra, ekle) / `hoursBefore` (önce, çıkar). `postponing = true` iken anlamlı. |
| `postponingHour` | string | koşullu | Erteleme **miktarı** (saat); `postponing = true` iken kullanılır. |

### 2.3 `TimerFixedSchedule` — sabit zaman (`fixedDateTime`)
Belirli bir tarih/saatte tetiklenir; yine opsiyonel erteleme alabilir.

| Alan | Tip | Zorunlu | Açıklama |
|---|---|---|---|
| `dateTime` | string | evet | Hedef **tarih/saat**. |
| `postponing` | bool | hayır | Hesaplanan zamana **erteleme** uygulanacak mı. |
| `timeAdjustmentOption` | [`TimeAdjustmentOption`](../../../enums/time-adjustment-option.md) | koşullu | Erteleme yönü — `hoursAfter` / `hoursBefore`. `postponing = true` iken anlamlı. |
| `postponingHour` | string | koşullu | Erteleme **miktarı** (saat); `postponing = true` iken kullanılır. |

## 3. Ortak alanlar (settings'te değil — `ProcessStep` kolonu)
`code`·`stepType`·`definition`·`order`·`showInHistory`·`skip*`·`environmentRestriction` → [`../../process-step.md`](../../process-step.md) §1.

## 4. JSON Schema
```json
{
  "$id": "process-step-settings/timer",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "timeoutActive":             { "type": "boolean", "default": false },
    "workStyle":                 { "enum": ["workCalendar", "normalCalendar", "fixedDateTime"] },
    "workCalendarSchedule":      { "$ref": "#/$defs/timerWorkSchedule" },
    "normalCalendarSchedule":    { "$ref": "#/$defs/timerNormalSchedule" },
    "fixedDateTimeSchedule":     { "$ref": "#/$defs/timerFixedSchedule" },
    "timeoutNotificationActive": { "type": "boolean", "default": false },
    "timeoutNotification":       { "$ref": "process-step-settings/notification#/$defs/sendNotificationMessages" },
    "selectedTimerProcessStepId":{ "type": "integer" }
  },
  "$defs": {
    "timerWorkSchedule": {
      "type": "object",
      "additionalProperties": false,
      "required": ["value"],
      "properties": {
        "value": { "type": "string", "minLength": 1 }
      }
    },
    "timerNormalSchedule": {
      "type": "object",
      "additionalProperties": false,
      "required": ["day", "workTimeSelection"],
      "properties": {
        "day":                  { "type": "string", "minLength": 1 },
        "workTimeSelection":    { "enum": ["atWorkStart", "atWorkEnd"] },
        "postponing":           { "type": "boolean", "default": false },
        "timeAdjustmentOption": { "enum": ["hoursAfter", "hoursBefore"] },
        "postponingHour":       { "type": "string" }
      }
    },
    "timerFixedSchedule": {
      "type": "object",
      "additionalProperties": false,
      "required": ["dateTime"],
      "properties": {
        "dateTime":             { "type": "string", "minLength": 1 },
        "postponing":           { "type": "boolean", "default": false },
        "timeAdjustmentOption": { "enum": ["hoursAfter", "hoursBefore"] },
        "postponingHour":       { "type": "string" }
      }
    }
  }
}
```
> Not: `timeoutNotification`, Bildirim adımının **paylaşılan** `sendNotificationMessages` tanımına `$ref` ile bağlanır (kanonik şema → [`notification.md`](./notification.md) §4). Tek şema üç `stepType`'ı da kapsadığından **zorunluluklar koşulludur** (§1.1) ve uygulama-katmanında doğrulanır: `timer`/`timeout` → `workStyle` + eşleşen `*Schedule` bloğu; `timerStart`/`timerEnd` → `selectedTimerProcessStepId`. `selectedTimerProcessStepId`'nin gerçekten bir `timer` adımını işaret ettiği de uygulama-katmanı denetimidir.

## 5. Örnek
**a) `timer` — normal takvime göre 2 gün, çalışma sonu referanslı, timeout bildirimi:**
```json
{
  "timeoutActive": true,
  "workStyle": "normalCalendar",
  "normalCalendarSchedule": {
    "day": "2",
    "workTimeSelection": "atWorkEnd",
    "postponing": true,
    "timeAdjustmentOption": "hoursBefore",
    "postponingHour": "3"
  },
  "timeoutNotificationActive": true,
  "timeoutNotification": {
    "channels": ["mail"],
    "items": [ { "languageCode": "tr", "title": "Süre doldu", "text": "İşlem süresi doldu." } ]
  }
}
```
**b) `timerStart` / `timerEnd` — hedef timer'ı başlat/sonlandır:**
```json
{ "selectedTimerProcessStepId": 88 }
```

*Oluşturma: 2026-08-28.*
