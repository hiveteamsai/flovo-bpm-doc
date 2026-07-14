# Model — SchedulerJob (Zamanlanmış Görev — organizasyon ayarı)

> **Durum:** 🟡 TASLAK — eski uygulama DTO'sundan türetildi.
> **Kaynak DTO:** `../../research/current-flovo-bpm-engine/organizations/scheduler-jobs.md` (`SchedulerJobDto`).
> **Dönüşüm:** `account*`→`organization*`; `accountCode` → **`organizationId` (int)** (kiracı sahipliği);
> `triggeredByUserId` (string) → int.
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
| `lastRunAt` | datetime | — | Son çalışma zamanı. |
| `lastRunStatus` | string | — | Son çalışma durumu. |
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

*Oluşturma: 2026-07-03.*
