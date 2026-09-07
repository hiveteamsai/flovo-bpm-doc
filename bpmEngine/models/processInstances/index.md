# Çalışma-Zamanı (Runtime) Modelleri — İndeks

> **Amaç:** Ayarlardan (`Service`/`ProcessStep`/`Property`…) motor tarafından üretilen **çalışma-zamanı** kayıtları —
> süreç çalıştırma, doldurulmuş form, onay/bekleme ve **form-değer saklama** (JSONB tapu + fihrist projeksiyonları) verisi. 🟢 TANIMLI.

## Dökümanlar

### Süreç & form çekirdeği
| Döküman | Özet |
|---|---|
| [`process-instance.md`](./process-instance.md) | Bir servis sürecinin **çalıştırma örneği** (runtime); tasarımdaki `Service`/`ProcessStep`'in canlı karşılığı. |
| [`process-step-instance.md`](./process-step-instance.md) | **Tek bir süreç adımının çalıştırılması** — hangi adım, hangi aksiyon, kim/ne tarafından, ne zaman. |
| [`instance.md`](./instance.md) | Bir iş akışında oluşturulan **doldurulmuş form** (runtime veri kaydı); mevcut `statusId`. Değerleri **taşımaz** (→ `InstanceValue`). |
| [`instance-awaiting-user.md`](./instance-awaiting-user.md) | Form üzerinde **atanan / aksiyon alabilecek** kullanıcı veya grup (aksiyon/onay kuyruğu). |
| [`associated-instance.md`](./associated-instance.md) | Bir formu **başka bir formla ilişkilendirme** (property boyutuyla). |

### Değer saklama (form değerleri — CQRS + Outbox + NATS)
| Döküman | Özet |
|---|---|
| [`instance-value.md`](./instance-value.md) | **Kaynak-hakikat (tapu)** — Instance ile 1–1; tüm alan değerleri `data` **JSONB, code-keyed** + `version`. |
| [`instance-attr.md`](./instance-attr.md) | **Skaler fihrist** — sorgulanabilir alan → 1 satır (tipli EAV projeksiyonu); `InstanceValue`'dan yeniden üretilebilir. |
| [`instance-list-item.md`](./instance-list-item.md) | **Liste kalemleri fihristi** — liste-of-model (`groupByTax`, key-value) alanları için kalem-bazlı projeksiyon. |
| [`instance-value-outbox.md`](./instance-value-outbox.md) | **Outbox olayı** — değer update'iyle aynı TX'te; relay → NATS → projektör. |
| [`instance-value-change.md`](./instance-value-change.md) | **Değer geçmişi** (append-only audit; `saveChangeLog=true` alanlar) — projeksiyon değil, kaynak kanıt. |
| [`reflection-propagation.md`](./reflection-propagation.md) | **Yansıma yayılım mekanizması** (tablo değil, runtime akış) — `parentProperty` **ilk dolum/temizleme** (§3a: ilişki kurulunca kopya · bağ kalkınca `null`, KARAR v0.45) + `reflectionMode=materialized` (A′) parent→child tazeleme; `AssociatedInstance` + `Property` metadata ile çözülür; `async` (vars.) / `sync`. |
| [`propertyValuesTemplates/`](./propertyValuesTemplates/index.md) | **Değer şablonları (property tipine göre)** — her `propertyType` için `data` içindeki JSONB şekli + `projectToAttr` projeksiyon eşlemesi; **core `labeled-value.md`** (etiketli değer şekli) bu klasördedir. |

### Motor yürütme (event sourcing — runtime state machine) · 📝 TASLAK v0.44, onay bekliyor
> Davranış → [`../../engine-runtime.md`](../../engine-runtime.md) · hata → [`../../engine-runtime-errors.md`](../../engine-runtime-errors.md) · zamanlayıcı →
> [`../../engine-runtime-scheduler.md`](../../engine-runtime-scheduler.md) · saklama → [`../../engine-runtime-retention.md`](../../engine-runtime-retention.md) · kararlar/açık sorular → [`../../engine-runtime-plan.md`](../../engine-runtime-plan.md).

| Döküman | Özet |
|---|---|
| [`workflow-event.md`](./workflow-event.md) | **`WorkflowEvent` (`workflow_events`) — kaynak-hakikat olay günlüğü** (append-only): 12 olay tipi · süreç-başına `version` (optimistic concurrency) · `messageId` (idempotency) · `dispatch`/`publishedAt` (**outbox-in-event**) · aktör kolonları (KVKK) · aylık RANGE partition. |
| [`workflow-projection.md`](./workflow-projection.md) | **`WorkflowProjection` — motor imleci** (1–1 ProcessInstance, türetilmiş): `lastVersion` · `executionState` + `waitReason` · aktif adım · `attempt` · guard sayaçları (`autoStepRun`/`totalSteps`) · `lastError`. Replay ile yeniden kurulur. |
| [`workflow-timer.md`](./workflow-timer.md) | **`WorkflowTimer` — zamanlanmış uyandırma** (4 tür: `stepTimer` · `taskTimeout` · `retry` · `serviceTriggerCron`); scheduler `FOR UPDATE SKIP LOCKED` ile claim eder (lider seçimi yok). `SchedulerJob`'dan (org cron fonksiyonları) ayrı. |

*Oluşturma: 2026-07-13. Güncelleme: 2026-08-31 (v0.44) — motor yürütme modelleri eklendi.*
