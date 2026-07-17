# Model — Solution (çözüm)

> **Durum:** 🟡 TASLAK (alanlar başlangıç — detaylandırılacak)
> **Amaç:** Bir organizasyona ait, **servisleri gruplamak** için kullanılan tanım. Bir organizasyonda **birden çok
> solution** olabilir; servisler bir solution **altında** oluşturulur.
> **Hiyerarşi:** `Organization → Solution → Service`.

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Solution ID'si. |
| `organizationId` | int | FK → Organization.id | Sahibi organizasyon. |
| `code` | string | benzersiz | Solution kodu (izolasyon başlığı `solutionId`; dış referans). |
| `definition` | string | — | Solution adı/tanımı (kullanıcıya görünen). |
| `translationCode` | string? | çeviri anahtarı | **Çeviri eşleşme anahtarı** (→ [`../organization-settings/translation.md`](../organization-settings/translation.md) `code`). `null` = çeviri **es geçilir**, doğrudan `definition` kullanılır. |

## İlişkiler
- **N – 1** → `Organization` (`organizationId`).
- **1 – N** ← `Service` (`solutionId`).

## Notlar / açık noktalar
- Ek alanlar (açıklama, ikon, sıralama, yetki) detaylandırılacak → `../../todo.md`.

*Oluşturma: 2026-07-02.*
