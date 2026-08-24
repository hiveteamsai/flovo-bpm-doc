# Model — VacationDay (Tatil Günü — organizasyon ayarı)

> **Durum:** 🟡 TASLAK
> **Amaç:** Resmi tatil / çalışılmayan günler. `WorkingSchedule` ile birlikte **iş günü/süre** hesaplamalarında kullanılır.
> **⚠️ v-next align (2026-08-24, product-as-reference):** mevcut-çalışan-ürün (FE) referans alınarak canonical text-entity + tarih-aralığı alanları eklendi (BO-directive: working-product = org-settings referansı). Değişiklikler `[YENİ]`/`[DEĞİŞİM]` ile işaretli; özet CHANGES.md'de.

## Alanlar
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Tatil ID'si. |
| `organizationId` | int | FK → `organization.md` | Sahibi organizasyon. |
| `code` | string | — | **[YENİ]** Tatil kodu (canonical entity-code). |
| `startingDate` | datetime | — | Başlangıç tarihi. |
| `endingDate` | datetime | — | Bitiş tarihi. |
| `startHalf` | bool | — | **[DEĞİŞİM: eski `halfDay` bölündü]** Başlangıç günü yarım mı (gün hesabında 0.5). |
| `endHalf` | bool | — | **[YENİ: `halfDay` bölünmesinin ikinci yarısı]** Bitiş günü yarım mı (0.5). |
| `definition` | string | — | Tatil tanımı/adı. |
| `translationCode` | string? | çeviri anahtarı | **Çeviri eşleşme anahtarı** (→ [`translation.md`](./translation.md) `code`). `null` = çeviri **es geçilir**, doğrudan `definition` kullanılır. |
| `active` | bool | — | **[YENİ]** Aktif/pasif — **null olamaz**, varsayılan `true`. `false` = frontend'de **görünür/düzenlenebilir** ama BPM işlemede kullanılmaz. |
| `deleted` | bool | — | **[YENİ]** Soft-delete — **null olamaz**, varsayılan `false`. `true` = frontend'de **gizli/aktarılmaz/salt** + BPM işlemede kullanılmaz. |
| `synchronizationStatus` | SyncStatus (enum) | — | **[YENİ, tip: James-SA-catch]** Harici ERP/muhasebe senkron durumu — **3-state string-enum** (`synced` / `pending` / `error`), bool DEĞİL (FE-gerçeği, Emma cross-cutting-inventory). |

## Benzersizlik
> **[YENİ]** `(organizationId, code)` **benzersiz** — aynı organizasyonda aynı `code`'lu iki kayıt olamaz. **`deleted=true` kayıtlar kontrole dahil değildir.**

## İlişkiler
- **N – 1** → `Organization`.
- **Kullanım:** `WorkingSchedule` süre hesabı (`checkHoliday`: 0=değil, 1=tam, 2=yarım) → BPM Timer/zaman aşımı bu günleri atlar.

## v-next gerekçesi (review: Osmancan Güven + BO)
Mevcut-çalışan-ürün VacationDay'i **canonical text-entity + tarih-aralığı** olarak modelliyor: `code` · `active` · `deleted` · `synchronizationStatus` + per-endpoint `startHalf`/`endHalf` (eski tek `halfDay` yerine). BO-directive (2026-08-24): org-settings için **working-product = referans**; analiz-doc buna hizalanır. Bu güncelleme §7.2 VAC-cluster'ını (`AC-VAC-02/05/06/07`) CONFORM'a çevirir. **Review-notu:** eski `halfDay` (tek bool) → `startHalf`+`endHalf`; okuma-geriye-uyum gerekirse migration'da eşleme belirtilecek (BE-lane, bu doc dışı).

*Oluşturma: 2026-07-03. v-next align: 2026-08-24.*
