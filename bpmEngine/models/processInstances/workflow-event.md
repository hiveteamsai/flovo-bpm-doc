# Model — WorkflowEvent (`workflow_events` — süreç yürütme günlüğü, append-only)

> **Durum:** 📝 TASLAK v0.44 — **onay bekliyor** (kararlar + açık noktalar → [`../../engine-runtime-plan.md`](../../engine-runtime-plan.md) §2/§3).
> **Yeni model.** Runtime davranış → [`../../engine-runtime.md`](../../engine-runtime.md) §1/§4/§5 · hata/retry → [`../../engine-runtime-errors.md`](../../engine-runtime-errors.md) ·
> zamanlayıcı → [`../../engine-runtime-scheduler.md`](../../engine-runtime-scheduler.md) · saklama/KVKK → [`../../engine-runtime-retention.md`](../../engine-runtime-retention.md).
> **Amaç:** Bir `ProcessInstance`'ın **her yürütme geçişini** (başlatma · adım başladı/bitti · askı · aksiyon · timer · hata · bitiş)
> **değiştirilemez ve sıralı** kayıt olarak tutan **kaynak-hakikat** (Partial Event Sourcing). `ProcessInstance.executionState`,
> [`WorkflowProjection`](./workflow-projection.md) ve `ProcessStepInstance`'ın motor alanları bu günlükten **türetilir / yeniden kurulabilir**.
> Tek tabloda dört iş: **kaynak log** · **idempotency** (`messageId`) · **optimistic concurrency** (`version`) · **outbox** (`dispatch`).

## 0. Adlandırma
Model adı **`WorkflowEvent`**; tablo, tech-stack/engine-runtime dokümanlarında yerleşik **`workflow_events`** adıyla anılır. Konvansiyon
(model adının snake_case'i → `workflow_event`) ile bu yerleşik ad arasındaki seçim **açık** (→ plan **Q1**); bu doküman boyunca `workflow_events` kullanılır.

## 1. Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | bigint | PK | Global sıra (identity). Zaman-sıralı okuma + `causationId` hedefi. |
| `processInstanceId` | int | FK → ProcessInstance.id | Olayın ait olduğu süreç. Her zaman dolu (`startRequested` süreci **açar**; cron tetiği önce `ProcessInstance` yaratır). |
| `organizationId` | int | (denormalize) | Kiracı — RLS Pattern B v2. |
| `version` | int | **UNIQUE** (`processInstanceId`, `version`) | Süreç-içi **monoton sayaç** (1'den başlar, boşluksuz). **Optimistic concurrency:** yazan `expectedVersion + 1` ile INSERT eder; UNIQUE ihlali = **çakışma** (→ engine-runtime §5). |
| `eventType` | [`WorkflowEventType`](../enums/workflow-event-type.md) | — | Geçiş türü (12 değer). |
| `processStepInstanceId` | int? | FK → ProcessStepInstance.id | İlgili adım çalıştırması. `startRequested`/`ended`/`failed`/`cancelled`'da null olabilir. |
| `processStepId` | int? | FK → ProcessStep.id | Adım tasarımı (**denormalize**: replay/audit `ProcessStepInstance`'a bağımlı kalmaz). |
| `processStepActionId` | int? | FK → ProcessStepAction.id | Seçilen/alınan aksiyon (`stepCompleted` · `actionTaken` · `stepSkipped` · `timerFired` · `recovered(skip)`). |
| `attempt` | int | — | Adımın **deneme sayısı** (1 = ilk). `stepStarted`/`stepCompleted`/`stepFailed`'da anlamlı; diğerlerinde `0`. |
| `actorUserId` | int? | FK → User.id | Olayı tetikleyen **kullanıcı** (`actionTaken`; `recovered`/`cancelled`'da admin). **Kolonda tutulur** — KVKK anonimleştirme kolon-hedefli çalışır (§7). |
| `actorApiKeyId` | int? | FK → ApiKey (geçici) | Aktör API anahtarı ise (webhook / Customer API). `actorUserId` ile **biri** dolu; sistem olaylarında (`timerFired`, `stepCompleted`) ikisi de null. |
| `actorDelegateUserId` | int? | FK → User.id | **Vekaleten** alınmışsa vekil (`ProcessStepInstance.atDelegateUserId` ile aynı anlam). |
| `payload` | JSONB | — | Tipe-özel içerik (§2) — `ActionTransfer` snapshot, hata detayı, timer bilgisi… Kişisel veri barındırabilecek yollar §7'de listelenir. |
| `messageId` | string? | **UNIQUE** (partial: `WHERE messageId IS NOT NULL`) | Olaya yol açan **gelen mesajın** kimliği: NATS `Nats-Msg-Id` (job) **veya** API `Idempotency-Key` (kullanıcı aksiyonu) **veya** `timer:{workflowTimerId}`. Aynı mesaj ikinci kez gelirse → **zaten işlendi, atla**. Sistem-içi olaylarda (ör. `suspended`) null. |
| `causationId` | bigint? | FK → WorkflowEvent.id (self) | Bu olayı **doğuran** önceki olay (`stepStarted → stepCompleted`, `timerFired → suspended` …). Zincir izi; ilk olayda null. |
| `correlationId` | int | FK → ProcessInstance.id | **Kök ana süreç** — alt süreç zincirinde en üst `ProcessInstance` (`parentProcessInstanceId` zinciri boyunca). Ana süreçte `= processInstanceId`. Bir işin **tüm alt süreç olaylarını** tek sorguda toplar. |
| `dispatch` | JSONB? | — | **Outbox-in-event (§3):** bu olay commit edildikten sonra yayınlanacak NATS mesajı `{ subject, messageId, body }` (ör. `stepCompleted` → `flovo.workflow.step_ready.v1`). Yayınlanacak bir şey yoksa null. |
| `publishedAt` | datetime? | — | `dispatch` yayınlandı mı. `null` + `dispatch` dolu = **relay** yeniden yayınlar (crash kurtarma). |
| `occurredAt` | datetime | — | Olay zamanı (**UTC**, sunucu saati). **Partition anahtarı** (§4). |

> **Değişmezlik:** satırlar **yalnız INSERT** edilir; tek istisna `publishedAt` (outbox işareti) ve KVKK **anonimleştirme** (`actor*` kolonları +
> `payload` içindeki kişisel yollar; → retention §4). Başka UPDATE/DELETE **yoktur**; saklama süresi dolan partition **bütünüyle** düşer.

## 2. `payload` — olay tipine göre içerik
Şekil **tip-başına sabittir** (JSON Schema ile doğrulanır; `additionalProperties: false`). Ortak: `payload.stepCode` (adımın `code`'u — okunabilir audit).

| `eventType` | `payload` alanları | Not |
|---|---|---|
| `startRequested` | `{ source: "processStart" \| "subProcessStart" \| "serviceTrigger", serviceTriggerId?, parentProcessInstanceId?, initialActionTransfer? }` | Alt süreçte host instance bağı `ProcessInstance.parentProcessInstanceId`'de; burada yalnız kaynak. |
| `stepStarted` | `{ stepCode, stepType, incomingActionTransfer? }` | Adıma **gelen** paket (`changeList` merge'i bu olayla aynı TX'te uygulanır → §3.2). |
| `stepCompleted` | `{ stepCode, stepType, selectedActionCode, outgoingActionTransfer, durationMs }` | `outgoingActionTransfer` = adımın ürettiği + `mergeParameter` birleşimi (**kaynak**; `ProcessStepInstance.processStepActionParameter` bunun **kopyası**). |
| `stepSkipped` | `{ stepCode, skipRule: "preApproved" \| "processStarter", skippedForUserId, selectedActionCode }` | |
| `suspended` | `{ stepCode, waitReason, awaiting: [{userId?, userGroupId?}], timerId?, nextRetryAt? }` | `awaiting` = `InstanceAwaitingUser` **snapshot**'ı (grup üyeliği dinamik → yalnız grup id). |
| `actionTaken` | `{ stepCode, actionCode, actionTransfer, source: "user" \| "api" \| "webhook", idempotencyKey?, expectedProcessStepInstanceId? }` | Aktör kolonlarda; `actionTransfer` = taşınan paket (**kaynak**). |
| `timerFired` | `{ workflowTimerId, kind, dueAt, firedAt, preemptedProcessStepInstanceId?, selectedActionCode? }` | `preempted…` = timer dolduğunda kapatılan bekleme adımı (timeout/stepTimer). |
| `stepFailed` | `{ stepCode, errorClass, errorCode, message, detail?, httpStatus?, retryable, nextRetryAt?, maxAttempts }` | `detail` **kişisel veri içermemeli** (ham response gövdesi → MinIO/log; JSONB'de yalnız kısaltılmış özet ≤ 2 KB). |
| `failed` | `{ stepCode, errorClass, errorCode, message, attempts, reason: "noOnFail" \| "retryExhausted" \| "design" \| "guard" \| "inDoubt" }` | Dead-letter özeti; admin listesi bunu gösterir. |
| `recovered` | `{ mode: "retry" \| "skip", stepCode, selectedActionCode?, note? }` | `note` = admin açıklaması (opsiyonel). |
| `cancelled` | `{ stepCode?, note?, previousExecutionState }` | |
| `ended` | `{ stepCode, endType: "processEnd" \| "subProcessEnd" \| "terminalStep" }` | |

## 3. Yazma kuralları (motor sözleşmesi)
### 3.1 Tek TX'te ne yazılır
Her geçiş **bir** transaction'dır: `INSERT workflow_events` (+ aynı TX'te **senkron projeksiyonlar**: `WorkflowProjection` upsert ·
`ProcessInstance.executionState` · `ProcessStepInstance` ekle/güncelle · `InstanceAwaitingUser` senkron · `WorkflowTimer` kur/iptal ·
gerekiyorsa `InstanceValue` merge + `InstanceValueOutbox`). Olay **kaynak**, diğerleri **türetilmiş** (replay ile yeniden kurulabilir);
aynı TX'te yazıldıkları için "olay var, projeksiyon yok" durumu oluşmaz (Partial ES'in "senkron projeksiyon" kolu).

### 3.2 Otomatik adım = iki TX
1. **TX-A (`stepStarted`):** version+1 · `ProcessStepInstance` (executionDate) · gelen `changeList` → `InstanceValue` merge · projeksiyon `attempt`.
   **Commit** → sonra yan etki (HTTP çağrısı vb.) yapılır.
2. **TX-B (`stepCompleted` | `stepFailed`):** version+1 · sonuç · `dispatch` (sonraki `step_ready`) · projeksiyon.
   Worker TX-A'dan sonra çökerse redelivery'de `stepStarted` görülür → **in-doubt** kuralı (→ errors §3).

> **Neden iki TX:** tek TX'te yan etkiyi "gördüğümüz" bir kayıt kalmaz; ERP'ye giden POST iki kez tekrarlanabilir. Maliyet = adım başına **bir ek küçük INSERT**.

### 3.3 Optimistic concurrency
Yazan taraf (worker · API handler · scheduler) sürecin `WorkflowProjection.lastVersion`'ını okur, `version = lastVersion + 1` ile INSERT eder.
UNIQUE ihlali → TX geri alınır → **çakışma**: worker/scheduler için "başkası ilerletti → ACK ve atla"; API için **409** (→ engine-runtime §5.2).

### 3.4 Idempotency (`messageId`)
Gelen her job/istek bir `messageId` taşır. INSERT öncesi `SELECT 1 WHERE messageId = ?` (ya da partial UNIQUE ihlali) → **zaten işlendi**:
worker ACK'ler; API **aynı sonucu** (200, güncel durum) döner. `messageId` **kaynaktan** gelir: NATS `Nats-Msg-Id` (`step_ready`/`resume` job'ı) ·
API `Idempotency-Key` header'ı · scheduler `timer:{workflowTimerId}`.

### 3.5 Outbox-in-event (`dispatch` · `publishedAt`)
Postgres commit ↔ NATS publish **atomik değildir**; commit sonrası çökme = kuyrukta iş yok, süreç `running`'de takılır. Çözüm ayrı outbox
tablosu **değil**, olayın kendisidir: yayınlanacak mesaj `dispatch`'e yazılır (aynı TX) → commit → **hızlı yol:** yazan hemen publish eder,
`publishedAt` set eder → **relay (sweeper):** `dispatch IS NOT NULL AND publishedAt IS NULL AND occurredAt < now() - 5s` satırlarını yeniden
yayınlar. Çift yayın **zararsızdır** (tüketici `messageId` ile atlar). `InstanceValueOutbox` ile **aynı ilke**, ayrı tablo yok.

## 4. İndeksler · partition · RLS
| Nesne | Tanım | Ne için |
|---|---|---|
| PK | `id` | sıra |
| UNIQUE | (`processInstanceId`, `version`) | optimistic concurrency + süreç akışı okuma |
| UNIQUE (partial) | (`messageId`) `WHERE messageId IS NOT NULL` | idempotency |
| B-tree | (`organizationId`, `occurredAt`) | tenant + zaman (rapor, saklama) |
| B-tree | (`correlationId`, `occurredAt`) | kök süreç → tüm alt süreç olayları |
| B-tree (partial) | (`occurredAt`) `WHERE dispatch IS NOT NULL AND publishedAt IS NULL` | relay sweep (küçük kalır) |
| **Partition** | **`RANGE (occurredAt)` — aylık** | saklama = partition **drop** (DELETE yok); değer tablolarındaki `HASH(service_id)`'den **bilinçli farklı** (→ plan Q2) |
| RLS | `organizationId` = tenant GUC | Pattern B v2 |

> **Boyut tahmini:** adım başına ~2–3 olay × ~1 KB; 1M adım/ay ≈ 3 GB/ay (payload `detail` sınırıyla). Aylık partition + soğuk arşiv (→ retention §2).

## 5. Türetilenler (bu günlükten kurulanlar)
| Türetilen | Nasıl | Yeniden kurma |
|---|---|---|
| [`WorkflowProjection`](./workflow-projection.md) | son olaydan `executionState`/`waitReason`/`lastVersion`/aktif adım/`attempt` | `TRUNCATE` + süreç-başına replay |
| `ProcessInstance.executionState` | aynı değer (liste sorguları için kopya) | replay |
| `ProcessStepInstance` motor alanları (`executionDate`, `actionTriggerDate`, `processStepActionId`, `processStepActionParameter`, `at*`) | `stepStarted`/`actionTaken`/`stepCompleted`'dan | replay (**iş alanları** — `instanceId` — kaynaktan) |
| `InstanceAwaitingUser` | son `suspended.payload.awaiting` | replay |
| `WorkflowTimer` `armed` seti | son `suspended`/`stepFailed` (timer kurulumu) | replay + yeniden kurma |
| `flovo.workflow.*` NATS olayları | `dispatch` | relay |

## 6. İlişkiler
- **N – 1** → `ProcessInstance` (`processInstanceId`, `correlationId`), `ProcessStepInstance` (`processStepInstanceId`), `ProcessStep` (`processStepId`),
  `ProcessStepAction` (`processStepActionId`), `User` (`actorUserId`, `actorDelegateUserId`), `ApiKey` (`actorApiKeyId`), `WorkflowEvent` (`causationId`, self).
- **1 – 1** → `WorkflowProjection` (süreç başına; `lastEventId` bu tabloya işaret eder).

## 7. Notlar / kararlar (öneri, onay bekliyor) / açık noktalar
- **Payload snapshot (öneri R2):** `ActionTransfer` olayda **tam kopya** taşınır (kaynak); `ProcessStepInstance.processStepActionParameter` **okuma kopyası**dır.
  Gerekçe: replay değişebilir tablolara bağımlı olmamalı; paket küçüktür (form değeri değil, delta).
- **Aktör kolonda (öneri R3):** KVKK "silme hakkı" geldiğinde `UPDATE … SET actorUserId = <tombstone>` kolon-hedefli çalışır; payload'da kişisel veri
  taşıyan yollar (`actionTransfer.parameters.*` içindeki user-ref `{userId, nameSurname}`, `awaiting[].userId`) **tip-başına listelenir** ve
  aynı işlemde temizlenir (→ retention §4).
- **`stepStarted` iki-TX modeli (öneri R4)** → §3.2.
- **Outbox-in-event (öneri R5)** → §3.5.
- **Açık:** fiziksel ad (Q1) · partition stratejisi (Q2) · `payload.detail` boyut sınırı ve ham gövde için MinIO eşiği (Q3) · `correlationId` alt süreçlerde
  **tetikleyen** mi **host** mu (şu an host zinciri = `parentProcessInstanceId`; Q4). → [`../../engine-runtime-plan.md`](../../engine-runtime-plan.md) §3.

*Oluşturma: 2026-08-31.*
