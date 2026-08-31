# Flovo BPM Motoru — Zamanlayıcı & Uyandırma (scheduler · WorkflowTimer · timeout · cron · lider-seçim)

> **Durum:** 📝 TASLAK v0.44 — **onay bekliyor**. Kararlar **R7, R14**, açık sorular **Q14–Q16, Q20** → [`engine-runtime-plan.md`](./engine-runtime-plan.md).
> **Kapsam:** [`engine-runtime.md`](./engine-runtime.md) §7'nin tam spesifikasyonu; `flovo-bpm-engine.md` §5.2/§6.2, `process-step.md` §3.7–§3.9 (Timer ailesi) ve
> §3.15/§3.16/§3.22 `timeout` bloğu, `service-trigger.md` `timer` (cron) runtime karşılığı.
> **Modeller:** [`WorkflowTimer`](./models/processInstances/workflow-timer.md) · [`WorkflowEvent`](./models/processInstances/workflow-event.md) (`timerFired`) ·
> [`WorkflowProjection`](./models/processInstances/workflow-projection.md) · enum [`WorkflowTimerKind`](./models/enums/workflow-timer-kind.md) / [`WorkflowTimerStatus`](./models/enums/workflow-timer-status.md).

---

## 0. İlke
Zaman, motorda **bir tablodur**: uyanması gereken her şey `workflow_timer`'da `armed` bir satırdır (`dueAt`). **Scheduler** bu tabloyu tarar,
dolan satırları **Postgres'te claim eder** (`FOR UPDATE SKIP LOCKED`), aynı TX'te `timerFired` olayını yazar ve `resume.v1` yayınlar. Bekleyen süreç
hiçbir kaynak tutmaz; scheduler **durumsuz ve yatay ölçeklenir** — **lider seçimi gerekmez** (R7). Cron (ServiceTrigger `timer`) de aynı tabloda
"bir sonraki tetik" satırı olarak durur.

## 1. Bileşen & çalışma modeli (R7)
```
her T=1s:
  BEGIN
    rows = SELECT * FROM workflow_timer
           WHERE status IN ('armed','deferred') AND dueAt <= now()
           ORDER BY dueAt LIMIT 100
           FOR UPDATE SKIP LOCKED                      -- N scheduler kopyası çakışmaz
    for r in rows:
      apply(r)                                         -- §4: olay yaz / defer / cancel  (aynı TX)
  COMMIT
  publish(dispatch of written events)                  -- hızlı yol; kaçarsa relay (outbox-in-event)
```
- **Neden lider seçimi yok:** `SKIP LOCKED` ile her dolan satırı **tam olarak bir** kopya alır; iki kopya aynı timer'ı uygulayamaz. Kopya çökse kilit
  TX ile düşer, satır bir sonraki turda başkasına gider. **At-most-once uygulama** = satır kilidi + `timerFired.messageId = timer:{id}` (UNIQUE).
- **Advisory lock nerede kalır:** yalnız **singleton housekeeping** (§7 — pruning, stuck detector, tutarlılık denetimi): `pg_try_advisory_lock(key)`;
  alamayan kopya o işi atlar. NATS KV lock **alternatif** olarak notlandı, gerekmedi (Q20).
- **Ölçek:** claim `LIMIT 100`/tur/kopya; gecikme metriği `now() - dueAt` (p95 hedef < 2 s). Kopya sayısı = gecikmeye göre (K8s replica).
- **Cron'un kendisi yok:** scheduler cron ifadesi **değerlendirmez**; her `serviceTriggerCron` satırı önceden hesaplanmış bir `dueAt` taşır (§5).

## 2. Kurulum (arm) — kim, ne zaman
| Tetikleyen | `kind` | Kim yazar | Ne zaman |
|---|---|---|---|
| **Timer adımına girildi** (§3.7) | `stepTimer` (`armedBy=stepEntry`) | worker | adım `suspended(waitReason=timer)` olurken — süreç **burada bekler** |
| **`timerStart`** (§3.8) | `stepTimer` (`armedBy=timerStart`, `processStepId = selectedTimerProcessStepId`) | worker | Start adımı koşar, timer'ı kurar, **`default` ile ilerler** (süreç beklemez) |
| **İnsan adımı askıya alındı** + `settings.timeout.timeoutActive` | `taskTimeout` | worker | `suspended(waitReason=humanTask)` ile aynı TX |
| **`stepFailed(retryable)`** | `retry` (`attempt+1`) | worker | aynı TX; `dueAt = now() + backoff` (→ errors §2) |
| **ServiceTrigger `timer` oluştu / aktifleşti** | `serviceTriggerCron` | settings-api (yazma anı) | `dueAt = next(cron, now)` |
| **Cron tetiği uygulandı** | `serviceTriggerCron` (yeni satır) | scheduler | `dueAt = next(cron, firedDueAt)` |

- **Yeniden kurma:** aynı `(processStepInstanceId, kind)` için `armed` varken yeni kurulum → eski `cancelled(rearmed)`, yeni satır.
- **Kurulum idempotency:** `messageId` = kuran olayın idempotency anahtarı; aynı olay iki kez işlense ikinci timer **kurulmaz**.

## 3. İptal (cancel)
| Olay | İptal edilen | `cancelReason` |
|---|---|---|
| Bekleyen insan adımında **aksiyon alındı** (`actionTaken`) | o `processStepInstanceId`'nin `taskTimeout`'u | `actionTaken` |
| **`timerEnd`** (§3.9) koştu | `processStepId = selectedTimerProcessStepId` olan **tüm `armed` `stepTimer`**'lar (bu süreçte) | `timerEnd` |
| Süreç **`ended`** | sürecin tüm `armed`/`deferred` timer'ları | `processEnded` |
| Süreç **`cancelled`** / `failed` | tümü (kurtarma yeniden kurar) | `processCancelled` |
| Admin **`retry now`** | `retry` timer'ı | `rearmed` |
| ServiceTrigger `active=false` / silindi | o trigger'ın `armed` cron satırı | `triggerDisabled` |

## 4. Uygulama (fire) — türe göre semantik
Scheduler `apply(r)` için sürecin `WorkflowProjection`'ını okur (`FOR UPDATE`), `executionState`/`waitReason`'a bakar:

### 4.1 Ön koşul — "tek aktif kol" korunur (R14)
| Süreç durumu | `stepTimer` / `taskTimeout` | `retry` |
|---|---|---|
| `waiting` (uygun `waitReason`) | **uygula** | `waitReason = retry` ise uygula |
| `running` | **`deferred`**: `dueAt = now() + 30 s`, `deferCount++` (otomatik zincir bitince uygulanır) | olmaz (retry yalnız waiting'de kurulur) |
| `done` / `cancelled` / `failed` | `cancelled(processEnded)` | `cancelled` |
| `waiting` ama **başka** adımda (timer kuranın adımı kapanmış, ör. `timerStart` sonrası süreç başka insan adımında) | `stepTimer`: **uygula** (tasarım gereği — bkz. 4.2) · `taskTimeout`: `cancelled(actionTaken)` (zaten geçilmiş) | — |

`deferCount` üst sınırı (öneri **20** ≈ 10 dk) aşılırsa alarm; uygulama **denenmeye devam eder** (Q14).

### 4.2 `stepTimer` — Timer adımının `default` aksiyonu
1. Version+1: **`timerFired{ workflowTimerId, preemptedProcessStepInstanceId = aktif PSI }`**.
2. Süreç Timer adımının **kendisinde** bekliyorsa (`waitReason=timer`): o PSI kapatılır (`actionTriggerDate`, `processStepActionId = default`), `default` hedefi için `step_ready`.
3. Süreç **başka bir insan adımında** bekliyorsa (`timerStart` ile kurulmuş "süreçten bağımsız" Timer): bekleyen PSI **kapatılır** (aktör yok — sistem; `processStepActionId = null`),
   `InstanceAwaitingUser` temizlenir, Timer adımı için yeni PSI açılır ve `default` aksiyonuyla (`stepCompleted`) hedefe `step_ready`. Bu, "X süre içinde tamamlanmazsa
   şu adıma git" kalıbının runtime karşılığıdır (timeout'un genelleştirilmişi).
4. Timer'ın `timeoutNotificationActive` bildirimi (varsa) aynı turda **Bildirim adımı yürütücüsüyle** gönderilir (ayrı adım açılmaz).

### 4.3 `taskTimeout` — insan adımı zaman aşımı (§6.2 · §3.15)
1. `timerFired{ preemptedProcessStepInstanceId }` · bekleyen PSI kapatılır (sistem) · `InstanceAwaitingUser` temizlenir.
2. `payload.notify` ise timeout bildirimi gönderilir.
3. **Timeout aksiyonu** (`settings.timeout` içinde belirlenen aksiyon kodu — Timer ailesi şemasıyla aynı; aksiyon yoksa `default`) seçilir → hedef adım için `step_ready`
   (**eskalasyon = hedef adım** — v0.32 kararı; ayrı mekanizma yok).

### 4.4 `retry`
`timerFired` → `resume.v1{source=retry}` → worker aynı adımı **`attempt+1`** ile koşar (`stepStarted`). Projeksiyon `waitReason=null`, `executionState=running`.

### 4.5 `serviceTriggerCron`
1. Trigger hâlâ `active` ve servis yayında mı (arşivli değil) — değilse `cancelled(triggerDisabled)`.
2. Hedef servis için **yeni ana `ProcessInstance`** (`parentProcessInstanceId = null`, `createdByUserId = null`, `createdByApiKeyId = null` → kaynak `startRequested.payload.source = serviceTrigger`)
   + `startRequested` (v1, `dispatch = step_ready(processStart)`).
3. **Sonraki tetik** satırı: `dueAt = next(cron, scheduledFor)` (kaçırılan tetik politikası §5.3).

## 5. Cron değerlendirme (ServiceTrigger `timer`)
### 5.1 Saat dilimi (Q15)
Organization'da timezone alanı **yok** (v0.33 kararı). Cron, **dağıtım konfigürasyonu** `FLOVO_SCHEDULER_TZ` ile değerlendirilir — varsayılan **`Europe/Istanbul`**
(Türkiye 2016'dan beri **kalıcı UTC+3**, DST yok). `dueAt` **UTC** saklanır; `payload.timezone` + `scheduledFor` (yerel) audit için tutulur.

### 5.2 DST (TZ değişirse geçerli)
Standart cron semantiği: yerel saatte **var olmayan** an (ileri alma) → o tetik **atlanır**; **iki kez oluşan** an (geri alma) → **ilk** oluşum. TR için etkisiz.

### 5.3 Kaçırılan tetikler (sistem kapalıyken)
**"Bir kez yakala, yığın yok":** `dueAt` geçmişte kalan cron satırı ilk turda **bir kez** uygulanır (gecikmeli), sonraki tetik `next(cron, now)` ile hesaplanır —
arada kaçan tetikler **üretilmez** (10 saat kesintide "her saat" trigger'ı 10 süreç açmaz). Tolerans: `dueAt < now() - 24h` ise **uygulanmaz**, yalnız log (Q15).

### 5.4 Geçerlilik
`cronExpression` kaydetme anında (settings-api) doğrulanır; **en sık 1 dk** (saniye alanı yok); `*/1 * * * *`'e izin verilip verilmeyeceği yük politikası (Q15).

## 6. Süre hesabı (`stepTimer` · `taskTimeout`) — `ProcessStepTimerSettings`
→ Şema [`timer.md`](./models/service-settings/jsonTemplateModels/process-step-settings/timer.md).
- **`workCalendar`:** referans an = kurulum anı; organizasyonun **`WorkingSchedule`** (gün/saat) + **`VacationDay`** üzerinden yalnız çalışma zamanı sayılarak `value` ilerletilir.
  Çalışma dışı ana denk gelen sonuç **sonraki çalışma başlangıcına** yuvarlanır.
- **`normalCalendar`:** `day` takvim günü + `workTimeSelection` (`atWorkStart`/`atWorkEnd`) + `postponing` (`hoursBefore`/`hoursAfter` × `postponingHour`).
- **`fixedDateTime`:** `dateTime` ± erteleme; geçmişse **hemen** dolar (kurulum turunda).
- **Sabitleme (Q16):** `dueAt` kurulumda hesaplanır, takvim/ayar sonradan değişse **yeniden hesaplanmaz** (basit, öngörülebilir; istenirse admin `rearm`).
- Hangi organizasyonun takvimi: sürecin `organizationId`'si; kullanıcı-bazlı takvim (atananın `WorkingSchedule`'ı) **yok** (Q16 alt-madde).

## 7. Singleton housekeeping (advisory lock)
Tek kopyada koşması gereken periyodik işler — `pg_try_advisory_lock(hash(jobName))`, alamayan atlar:
| İş | Periyot | Ne yapar |
|---|---|---|
| **Stuck detector** | 1 dk | `WorkflowProjection.executionState='running' AND lastEventAt < now()-5m` → outbox relay tetikle; hâlâ takılıysa alarm |
| **Outbox relay sweep** | 5 s | `workflow_events.dispatch IS NOT NULL AND publishedAt IS NULL AND occurredAt < now()-5s` → yeniden publish (→ workflow-event §3.5) |
| **Timer pruning** | günlük | `fired`/`cancelled` > 30 gün → sil (→ retention §6) |
| **Event retention** | günlük | partition detach/drop (→ retention §3) |
| **Tutarlılık denetimi** | saatlik | örneklem `lastVersion` ↔ `MAX(version)` |

> Relay sweep birden çok kopyada koşsa da zararsızdır (çift yayın idempotent) — advisory lock yalnız **yükü** azaltır.

## 8. NATS etkileşimi
Scheduler yalnız **yayınlar** (`flovo.workflow.resume.v1` · cron'da `step_ready.v1`); NATS'tan tüketmez. Mesaj `messageId = timer:{id}`; worker `workflow_events.messageId`
ile ikinci teslimi atlar. Publish başarısız olursa `publishedAt` null kalır → relay.

## 9. Ölçek · izleme
Metrik: scheduler gecikmesi (`firedAt - dueAt` p95) · `armed` sayısı (org) · `deferred` oranı · cron kaçırma sayısı · claim başına süre.
Alarm: gecikme > 30 s · `deferCount` > 20 · relay sweep sürekli iş buluyor (publish yolu bozuk).

## 10. Açık noktalar → [`engine-runtime-plan.md`](./engine-runtime-plan.md) §3
Q14 defer üst sınırı/politikası · Q15 TZ konfig + DST + kaçırılan tetik toleransı + en sık cron · Q16 takvim değişince yeniden hesap / kullanıcı-bazlı takvim ·
Q20 advisory lock yalnız housekeeping (NATS KV gereksiz) teyidi.

---

*Oluşturma: 2026-08-31 (v0.44). engine-runtime §7 doldurma.*
