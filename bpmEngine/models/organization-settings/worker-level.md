# Model — WorkerLevel (Çalışan Seviyesi — organizasyon ayarı)

> **Durum:** 🟡 TASLAK — eski uygulama DTO'sundan türetildi.
> **Kaynak DTO:** `../../research/current-flovo-bpm-engine/organizations/worker-levels.md` (`AccountWorkerLevelDto`).
> **Dönüşüm:** `account*`→`organization*`; `accountId` (string) → **`organizationId` (int)**.
> **Amaç:** Personel **kademe/seviye** tanımları (örn. Uzman, Kıdemli Uzman). Kullanıcılara atanır.

## Alanlar
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Seviye ID'si. |
| `organizationId` | int | FK → `organization.md` | Sahibi organizasyon. |
| `code` | string | — | Kod. |
| `definition` | string | — | Ad/tanım. |
| `active` | bool | — | Aktif/pasif — **null olamaz**, varsayılan `true`. `false` = frontend'de **görünür/düzenlenebilir** ama BPM işlemede kullanılmaz. |
| `deleted` | bool | — | Soft-delete — **null olamaz**, varsayılan `false`. `true` = frontend'de **gizli/aktarılmaz/salt** + BPM işlemede kullanılmaz. |

### Alt model — WorkerLevelQualificationValue
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Kayıt ID'si. |
| `workerLevelId` | int | FK → WorkerLevel | Bağlı seviye. |
| `qualificationId` | int | FK → `additional-qualification.md` | Ek nitelik. |
| `stringValue` | string (null olabilir) | — | `valueType=String` ise değer burada. |
| `doubleValue` | double (null olabilir) | — | `valueType=Double` ise değer burada. |
| `datetimeValue` | datetime (null olabilir) | — | `valueType=DateTime` ise değer burada. |
| `comboboxItemId` | int (null olabilir) | FK → `additional-qualification.md` (QualificationItem) | `valueType=Combobox` ise **seçilen öğe**. |
| `comboboxCode` | string (null olabilir) | — | Seçilen öğenin **kopya `code`**'u (çeviri). |
| `comboboxDefinition` | string (null olabilir) | — | Seçilen öğenin **kopya `definition`**'ı. |

## Benzersizlik
> `(organizationId, code)` **benzersiz** — aynı organizasyonda aynı `code`'lu iki kayıt olamaz. **`deleted=true` kayıtlar kontrole dahil değildir** (soft-delete edilenler bu kontrolde sayılmaz).

## İlişkiler
- **N – 1** → `Organization`.
- **1 – N** ← `User` (`workerLevelId`).
- **Ek nitelikler:** `AdditionalQualification` (`RelationalType=WorkerLevels`).

*Oluşturma: 2026-07-03.*
