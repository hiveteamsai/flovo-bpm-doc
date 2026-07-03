# Model — Profession (organizasyon ayarı)

> **Durum:** 🟡 TASLAK — eski uygulama DTO'sundan türetildi.
> **Kaynak DTO:** `../../research/current-flovo-bpm-engine/organizations/titles.md` (`AccountProfessionDto`).
> **Adlandırma:** Eski "Ünvan/Title" → **`Profession`** (kod içinde de `Profession`).
> **Dönüşüm:** `account*`→`organization*`; `accountId` (string) → **`organizationId` (int)**; `kod`/`tanim`→`code`/`definition`.
> **Amaç:** Çalışan **görev/meslek** tanımları. BPM'de **"ünvana göre yönetici"** atamalarında kullanılır.

## Alanlar
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Profession ID'si. |
| `organizationId` | int | FK → `organization.md` | Sahibi organizasyon. |
| `code` | string | — | Kod. |
| `definition` | string | — | Ad/tanım. |
| `active` | bool | — | Aktif/pasif — **null olamaz**, varsayılan `true`. `false` = frontend'de **görünür/düzenlenebilir** ama BPM işlemede kullanılmaz. |
| `deleted` | bool | — | Soft-delete — **null olamaz**, varsayılan `false`. `true` = frontend'de **gizli/aktarılmaz/salt** + BPM işlemede kullanılmaz. |
| `synchronizationStatus` | bool | — | Senkron durumu. |
| `companyIds` | List\<int\> | FK → `company.md` (N–N) | İlişkili şirketler. |

### Alt model — ProfessionQualificationValue (ek nitelik değeri)
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Kayıt ID'si. |
| `professionId` | int | FK → Profession | Bağlı profession. |
| `qualificationId` | int | FK → `additional-qualification.md` | Ek nitelik tanımı. |
| `stringValue` | string (null olabilir) | — | `valueType=String` ise değer burada. |
| `doubleValue` | double (null olabilir) | — | `valueType=Double` ise değer burada. |
| `datetimeValue` | datetime (null olabilir) | — | `valueType=DateTime` ise değer burada. |
| `comboboxItemId` | int (null olabilir) | FK → `additional-qualification.md` (QualificationItem) | `valueType=Combobox` ise **seçilen öğe**. |
| `comboboxCode` | string (null olabilir) | — | Seçilen öğenin **kopya `code`**'u (çeviri). |
| `comboboxDefinition` | string (null olabilir) | — | Seçilen öğenin **kopya `definition`**'ı. |

## Benzersizlik
> `(organizationId, code)` **benzersiz** — aynı organizasyonda aynı `code`'lu iki kayıt olamaz. **`deleted=true` kayıtlar kontrole dahil değildir** (soft-delete edilenler bu kontrolde sayılmaz).

## İlişkiler
- **N – 1** → `Organization` · **N – N** → `Company` (`companyIds`).
- **1 – N** ← `User` (`professionId`).
- **Ek nitelikler:** `AdditionalQualification` (`RelationalType=Professions`) → değerler `ProfessionQualificationValue`.

*Oluşturma: 2026-07-03.*
