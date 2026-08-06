# Model — InstanceValueChange (değer geçmişi / append-only audit)

> **Durum:** 🟡 TASLAK — değer-saklama mimarisinden türetildi (→ `../../research/property-value-storage/form-deger-saklama-v2.html`); alanlar gözden geçirilecek.
> **Yeni model.**
> **Amaç:** `Property.saveChangeLog=true` alanlarda her değer değişiminde **kim, ne zaman, eski→yeni** kaydını tutan
> **append-only** geçmiş. Denetim/KVKK kanıtıdır.

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Değişim kaydı ID'si. |
| `instanceId` | int | FK → Instance.id | Hangi form. |
| `serviceId` | int | FK → Service.id | Hangi servis (izolasyon/partition). |
| `organizationId` | int | (denormalize) | Kiracı — RLS/tenant izolasyonu. |
| `propertyCode` | string | — | Değişen alan (`Property.code`) — **`code`-keyed**. |
| `oldValue` | jsonb? | — | Eski değer (skaler veya obje). İlk yazımda null. |
| `newValue` | jsonb? | — | Yeni değer. |
| `changedByUserId` | int? | FK → User.id | Değişikliği yapan kullanıcı. _(kullanıcı **veya** API anahtarı — biri dolu.)_ |
| `changedByApiKeyId` | int? | FK → ApiKey (geçici) | Customer API ile yapılan değişimde "kim yaptı". **Ad geçici** (→ `../index.md §4`). |
| `occurredDate` | datetime | — | Değişim zamanı. |
| `processStepInstanceId` | int? | FK → ProcessStepInstance.id | Değişime yol açan süreç adımı çalıştırması (varsa). |

## İlişkiler
- **N – 1** → `Instance` (`instanceId`), `Service` (`serviceId`), `User` (`changedByUserId`), `ApiKey` (`changedByApiKeyId`),
  `ProcessStepInstance` (`processStepInstanceId`).

## Notlar / açık noktalar
- **Projeksiyon DEĞİLDİR:** `InstanceAttr`/`InstanceListItem` yeniden üretilebilir fihristlerdir; `InstanceValueChange` ise
  **kaynak hakikatin parçası** (tarihsel kanıt) — yeniden üretilemez, yedeklenir.
- **Yazım:** değer TX'inde (`InstanceValue` update ile aynı transaction), yalnız `saveChangeLog=true` alanlar için satır düşer.
- **`changedByUserId` **veya** `changedByApiKeyId`** — biri dolar (kullanıcı ya da API kaynaklı değişim).
- **Saklama/pruning + KVKK:** partition + retention politikası gerekir; "denetim silinmez" ↔ silme hakkı gerilimi **hukuki
  karar** (→ `../../todo.md` loglama/KVKK). **Ayar değişiklik logu** (`SettingsLog`) **ayrı** konudur, karıştırılmaz.
- **Kaynak mimari:** → `../../research/property-value-storage/form-deger-saklama-v2.html` (§18 değer geçmişi).

*Oluşturma: 2026-08-04.*
