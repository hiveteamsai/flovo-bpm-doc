# Model — WorkerLevel (Çalışan Seviyesi — organizasyon ayarı)

> **Durum:** 🟡 TASLAK
> **Amaç:** Personel **kademe/seviye** tanımları (örn. Uzman, Kıdemli Uzman). Kullanıcılara atanır.
> **⚠️ v-next align (2026-08-24, product-as-reference):** mevcut-çalışan-ürün `synchronizationStatus` taşıyor; analiz-doc'a eklendi (BO-directive: working-product = org-settings referansı). `[YENİ]` işaretli.

## Alanlar
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Seviye ID'si. |
| `organizationId` | int | FK → `organization.md` | Sahibi organizasyon. |
| `code` | string | — | Kod. |
| `definition` | string | — | Ad/tanım. |
| `translationCode` | string? | çeviri anahtarı | **Çeviri eşleşme anahtarı** (→ [`translation.md`](./translation.md) `code`). `null` = çeviri **es geçilir**, doğrudan `definition` kullanılır. |
| `active` | bool | — | Aktif/pasif — **null olamaz**, varsayılan `true`. `false` = frontend'de **görünür/düzenlenebilir** ama BPM işlemede kullanılmaz. |
| `deleted` | bool | — | Soft-delete — **null olamaz**, varsayılan `false`. `true` = frontend'de **gizli/aktarılmaz/salt** + BPM işlemede kullanılmaz. |
| `synchronizationStatus` | bool | — | **[YENİ]** Harici ERP/muhasebe ile senkron durumu. |

### Alt model — WorkerLevelQualificationValue
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Kayıt ID'si. |
| `workerLevelId` | int | FK → WorkerLevel | Bağlı seviye. |
| `qualificationId` | int | FK → `additional-qualification.md` | Ek nitelik. |
| `stringValue` | string? | — | `valueType=string` ise değer burada. |
| `doubleValue` | double? | — | `valueType=double` ise değer burada. |
| `datetimeValue` | datetime? | — | `valueType=dateTime` ise değer burada. |
| `comboboxItemId` | int? | FK → `additional-qualification.md` (QualificationItem) | `valueType=combobox` ise **seçilen öğe**. |
| `comboboxTranslationCode` | string? | çeviri anahtarı | Seçilen öğenin **kopya `translationCode`**'u (çeviri; `null` ise `comboboxDefinition` doğrudan kullanılır). |
| `comboboxDefinition` | string? | — | Seçilen öğenin **kopya `definition`**'ı. |

## Benzersizlik
> `(organizationId, code)` **benzersiz** — aynı organizasyonda aynı `code`'lu iki kayıt olamaz. **`deleted=true` kayıtlar kontrole dahil değildir** (soft-delete edilenler bu kontrolde sayılmaz).

## İlişkiler
- **N – 1** → `Organization`.
- **1 – N** ← `User` (`workerLevelId`).
- **Ek nitelikler:** `AdditionalQualification` (`RelationalType=workerLevels`).

## v-next gerekçesi (review: Osmancan Güven + BO)
Mevcut-çalışan-ürün WorkerLevel'da `synchronizationStatus` alanını taşıyor (canonical entity-pattern); analiz-doc buna hizalandı. **Review-notu:** syncStatus bir çok canonical-entity'de var (companies dahil); WorkerLevel'da FE-carries → product-as-reference ile eklendi. Genuine-requirement mı yoksa FE-boilerplate mı — Osmancan/BO teyit eder (düşük-risk, additive-optional).

*Oluşturma: 2026-07-03. v-next align: 2026-08-24.*
