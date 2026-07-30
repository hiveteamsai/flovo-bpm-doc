# Model — Profession (organizasyon ayarı)

> **Durum:** 🟡 TASLAK
> **Amaç:** Çalışan **görev/meslek** (ünvan) tanımları; kullanıcıya `professionId` ile atanır. BPM'de **ek nitelik** (`AdditionalQualification`, `RelationalType=professions`) üzerinden tüketilir.

## Alanlar
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Profession ID'si. |
| `organizationId` | int | FK → `organization.md` | Sahibi organizasyon. |
| `code` | string | — | Kod. |
| `definition` | string | — | Ad/tanım. |
| `translationCode` | string? | çeviri anahtarı | **Çeviri eşleşme anahtarı** (→ [`translation.md`](./translation.md) `code`). `null` = çeviri **es geçilir**, doğrudan `definition` kullanılır. |
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
| `stringValue` | string? | — | `valueType=string` ise değer burada. |
| `doubleValue` | double? | — | `valueType=double` ise değer burada. |
| `datetimeValue` | datetime? | — | `valueType=dateTime` ise değer burada. |
| `comboboxItemId` | int? | FK → `additional-qualification.md` (QualificationItem) | `valueType=combobox` ise **seçilen öğe**. |
| `comboboxTranslationCode` | string? | çeviri anahtarı | Seçilen öğenin **kopya `translationCode`**'u (çeviri; `null` ise `comboboxDefinition` doğrudan kullanılır). |
| `comboboxDefinition` | string? | — | Seçilen öğenin **kopya `definition`**'ı. |

## Benzersizlik
> `(organizationId, code)` **benzersiz** — aynı organizasyonda aynı `code`'lu iki kayıt olamaz. **`deleted=true` kayıtlar kontrole dahil değildir** (soft-delete edilenler bu kontrolde sayılmaz).

## İlişkiler
- **N – 1** → `Organization` · **N – N** → `Company` (`companyIds`).
- **1 – N** ← `User` (`professionId`).
- **Ek nitelikler:** `AdditionalQualification` (`RelationalType=professions`) → değerler `ProfessionQualificationValue`.

*Oluşturma: 2026-07-03.*
