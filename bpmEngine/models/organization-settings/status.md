# Model — Status

> **Durum:** 🟡 TASLAK (ilk çıkarım — gözden geçirilecek)
> **Amaç:** BPM sürecindeki bir kaydın **mevcut aşamasını** temsil eden etiket (örn. *Beklemede*, *Onaylandı*).
> Görsel gösterim, filtreleme ve raporlama için.
> **Davranış/kullanım:** → `../../organization-settings/status.md`

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Durum ID'si. |
| `organizationId` | int | FK → Organization.id | Sahibi organizasyon. **Organizasyon havuzu**: o organizasyonun **tüm servislerinde** kullanılabilir. |
| `code` | string | benzersiz | Durum **kodu** — yalnız tanımlayıcı (çeviri için kullanılmaz → `translationCode`). |
| `definition` | string | — | Durum **adı** — kullanıcıya görünen; **varsayılan dildeki** metin (çeviri: `translationCode` → Translation). Frontend'de metin rengi `styleId`.`fontColor`'dan gelir. |
| `translationCode` | string? | çeviri anahtarı | **Çeviri eşleşme anahtarı** (→ [`translation.md`](./translation.md) `code`). `null` = çeviri **es geçilir**, doğrudan `definition` kullanılır. |
| `icon` | string | — | İkon. Frontend'de ikon rengi `styleId`.`fontColor`'dan gelir. |
| `styleId` | int | FK → Style.id | Renk/görünüm: `bgColor` = etiket arka planı; **`fontColor` = `definition` metni + `icon` rengi**. |

## Benzersizlik
> `(organizationId, code)` **benzersiz** — aynı organizasyonda aynı `code`'lu iki durum olamaz.

## İlişkiler
- **N – 1** → `Organization` (`organizationId`), `Style` (`styleId`).
- **1 – N** ← `ProcessStepAction.changeStatusId` (herhangi bir servisin adım-aksiyonu bu organizasyon havuzundaki durumu atayabilir).

## Notlar / açık noktalar
- **Çözüldü:** `icon` ve `definition` frontend'de `styleId`.`fontColor`'ı kullanır (ayrı renk alanı yok).
- Raporlama için **kategori/grup** boyutu gerekli mi? → `../../todo.md`.

*Oluşturma: 2026-07-02.*
