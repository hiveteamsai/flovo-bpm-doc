# Model — VacationDay (Tatil Günü — organizasyon ayarı)

> **Durum:** 🟡 TASLAK
> **Amaç:** Resmi tatil / çalışılmayan günler. `WorkingSchedule` ile birlikte **iş günü/süre** hesaplamalarında kullanılır.

## Alanlar
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Tatil ID'si. |
| `organizationId` | int | FK → `organization.md` | Sahibi organizasyon. |
| `startingDate` | datetime | — | Başlangıç tarihi. |
| `endingDate` | datetime | — | Bitiş tarihi. |
| `halfDay` | bool | — | Yarım gün mü (gün hesabında 0.5). |
| `definition` | string | — | Tatil tanımı/adı. |
| `translationCode` | string? | çeviri anahtarı | **Çeviri eşleşme anahtarı** (→ [`translation.md`](./translation.md) `code`). `null` = çeviri **es geçilir**, doğrudan `definition` kullanılır. |

## İlişkiler
- **N – 1** → `Organization`.
- **Kullanım:** `WorkingSchedule` süre hesabı (`checkHoliday`: 0=değil, 1=tam, 2=yarım) → BPM Timer/zaman aşımı bu günleri atlar.

*Oluşturma: 2026-07-03.*
