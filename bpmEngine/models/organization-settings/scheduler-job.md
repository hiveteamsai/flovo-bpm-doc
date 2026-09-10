# Model — SchedulerJob (Zamanlanmış Görev — organizasyon ayarı)

> **Durum:** 🟢 Gözden geçirildi (v0.36)
> **Amaç:** Cron tabanlı **arka plan görevleri**. BPM'in zaman tabanlı otomasyonlarını (hatırlatma, zaman aşımı işleme, toplu işlem) besler.

## Alanlar
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Görev ID'si. |
| `organizationId` | int | FK → `organization.md` | Sahibi organizasyon. |
| `functionName` | string | — | Çalıştırılan fonksiyon adı. |
| `cronExpression` | string | — | Zamanlama (cron). |
| `description` | string | — | Açıklama. |
| `category` | string | — | Görev kategorisi. |
| `isEnabled` | bool | — | Aktif/pasif. |
| `lastRunAt` | datetime? | — | Son çalışma zamanı. **Hiç çalışmamış görevde `null`.** |
| `lastRunStatus` | string? | — | Son çalışma durumu. **Hiç çalışmamış görevde `null`.** |
| `createdAt` / `updatedAt` | datetime | — | Oluşturma/güncelleme. |
| `supportsManualInvoke` | bool | — | Manuel tetikleme desteği. |

### Alt model — SchedulerJobLog (çalışma geçmişi)
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Log ID'si. |
| `schedulerJobId` | int | FK → SchedulerJob | Bağlı görev. |
| `startTime` / `endTime` | datetime | — | Başlangıç/bitiş. |
| `status` | string | — | Çalışma durumu. |
| `errorMessage` | string | — | Hata mesajı (başarısızsa). |
| `triggeredBy` | string | — | Tetikleyen (zamanlayıcı / manuel). |
| `triggeredByUserId` | int? | FK → `user.md` | Manuel tetikleyen kullanıcı. |
| `durationSeconds` | double | — | Çalışma süresi. |

## İlişkiler
- **N – 1** → `Organization` · **1 – N** ← `SchedulerJobLog`.

## Notlar
- **Altyapı modeli (erteleme):** `...At`/`...Time` alan adlandırma birliği + alan detayları sonra netleşecek → `../../todo.md`.
- **`WorkflowTimer` ile sınır (📝 v0.44):** `SchedulerJob` = organizasyon-düzeyi **cron'lu arka plan fonksiyonları** (`functionName`; bakım, toplu işlem, hatırlatma job'ları).
  Süreç-örneği düzeyindeki **tek-atımlık uyandırmalar** (Timer adımı süresi · insan-görev timeout · retry backoff · ServiceTrigger cron sonraki tetik) **bu tabloda değil**,
  [`../processInstances/workflow-timer.md`](../processInstances/workflow-timer.md)'da tutulur ve motor scheduler'ı tarafından claim edilir (→ [`../../architectures/engine-runtime/engine-runtime-scheduler.md`](../../architectures/engine-runtime/engine-runtime-scheduler.md)).
  Motor housekeeping işleri (partition/retention · relay sweep · stuck detector) ileride `SchedulerJob` kaydı olarak **görünür kılınabilir** (öneri; karar sonra).

*Oluşturma: 2026-07-03.*
