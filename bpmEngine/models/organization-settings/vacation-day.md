# Model — VacationDay (Tatil Günü — organizasyon ayarı)

> **Durum:** 🟢 Gözden geçirildi (v0.36)
> **Amaç:** Resmi tatil / çalışılmayan günler. `WorkingSchedule` ile birlikte **iş günü/süre** hesaplamalarında kullanılır.

## Alanlar
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Tatil ID'si. |
| `organizationId` | int | FK → `organization.md` | Sahibi organizasyon. |
| `code` | string | — | Tatil kodu. |
| `startingDate` | datetime | — | Başlangıç tarihi. |
| `endingDate` | datetime | — | Bitiş tarihi. |
| `startHalf` | bool | — | Başlangıç günü yarım mı (gün hesabında 0.5). |
| `endHalf` | bool | — | Bitiş günü yarım mı (0.5). |
| `definition` | string | — | Tatil tanımı/adı. |
| `translationCode` | string? | çeviri anahtarı | **Çeviri eşleşme anahtarı** (→ [`translation.md`](./translation.md) `code`). `null` = çeviri **es geçilir**, doğrudan `definition` kullanılır. |
| `active` | bool | — | Aktif/pasif — **null olamaz**, varsayılan `true`. `false` = frontend'de **görünür/düzenlenebilir** ama BPM işlemede kullanılmaz. |
| `deleted` | bool | — | Soft-delete — **null olamaz**, varsayılan `false`. `true` = frontend'de **gizli/aktarılmaz/salt** + BPM işlemede kullanılmaz. |
| `synchronizationStatus` | [SyncStatus](../enums/sync-status.md) | — | Harici sistemle (ERP/muhasebe) **senkron durumu** — `synced` / `pending` / `error`. |

## Benzersizlik
> `(organizationId, code)` **benzersiz** — aynı organizasyonda aynı `code`'lu iki kayıt olamaz. **`deleted=true` kayıtlar kontrole dahil değildir.**

## İlişkiler
- **N – 1** → `Organization`.
- **Kullanım:** `WorkingSchedule` süre hesabı (`checkHoliday`: 0=değil, 1=tam, 2=yarım) → BPM Timer/zaman aşımı bu günleri atlar.

> **Yarım gün modeli:** Tek `halfDay` yerine ayrı `startHalf` + `endHalf` — aralığın başı ve/veya sonu yarım gün olabilir
> (gün hesabında 0.5). Tekrarlayan yıllık tatiller **açık tarih aralığıyla** (her yıl ayrı kayıt) temsil edilir; ayrı yinelenme alanı yoktur.

*Oluşturma: 2026-07-03. Güncelleme: 2026-08-28 — `synchronizationStatus` → `SyncStatus` enum; süreç-artefaktı notları temizlendi; gözden geçirildi (TASLAK kaldırıldı).*
