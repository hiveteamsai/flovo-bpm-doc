# Model — WorkingSchedule (Çalışma Takvimi — organizasyon ayarı)

> **Durum:** 🟡 TASLAK
> **Amaç:** Haftalık çalışma saatleri (7 gün, 2 periyot). BPM **Timer / zaman aşımı** "çalışma takvimine göre" hesaplamalarının temeli.

## Alanlar
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Takvim ID'si. |
| `organizationId` | int | FK → `organization.md` | Sahibi organizasyon. |
| `code` | string | — | Takvim kodu. |
| `definition` | string | — | Takvim adı/tanımı. |
| `translationCode` | string? | çeviri anahtarı | **Çeviri eşleşme anahtarı** (→ [`translation.md`](./translation.md) `code`). `null` = çeviri **es geçilir**, doğrudan `definition` kullanılır. |
| `active` | bool | — | Aktif/pasif — **null olamaz**, varsayılan `true`. `false` = frontend'de **görünür/düzenlenebilir** ama BPM işlemede kullanılmaz. |
| `deleted` | bool | — | Soft-delete — **null olamaz**, varsayılan `false`. `true` = frontend'de **gizli/aktarılmaz/salt** + BPM işlemede kullanılmaz. |
| `isDefaultSchedule` | bool | — | Varsayılan takvim mi. |

### Alt model — WorkingScheduleDay (haftanın günü)
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Kayıt ID'si. |
| `workingScheduleId` | int | FK → WorkingSchedule | Bağlı takvim. |
| `active` | bool | — | O gün çalışılıyor mu. |
| `day` | int | — | Gün (1=Pazartesi … 7=Pazar). |
| `period1Start` / `period1End` | datetime | — | 1. periyot başlangıç/bitiş. |
| `period2Start` / `period2End` | datetime? | — | 2. periyot (opsiyonel). |

## Benzersizlik
> `(organizationId, code)` **benzersiz** — aynı organizasyonda aynı `code`'lu iki kayıt olamaz. **`deleted=true` kayıtlar kontrole dahil değildir** (soft-delete edilenler bu kontrolde sayılmaz).

## İlişkiler
- **N – 1** → `Organization` · **1 – N** ← `WorkingScheduleDay`.
- **1 – N** ← `User` (`workingScheduleId`).
- **Kullanım:** `VacationDay` ile birlikte iş günü/saat ve BPM Timer zaman aşımı hesabı (`TimerCalculationType.workCalendar` → [`../enums/timer-calculation-type.md`](../enums/timer-calculation-type.md)).

*Oluşturma: 2026-07-03.*
