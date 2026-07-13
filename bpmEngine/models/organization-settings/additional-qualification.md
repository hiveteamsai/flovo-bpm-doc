# Model — AdditionalQualification (Ek Nitelik — organizasyon ayarı)

> **Durum:** 🟡 TASLAK — eski uygulama DTO'sundan türetildi.
> **Kaynak DTO:** `../../research/current-flovo-bpm-engine/organizations/additional-qualifications.md` (`AccountAdditionalQualificationDto`).
> **Dönüşüm:** `account*`→`organization*`; `accountId` (string) → **`organizationId` (int)**; `accountCompanyIds`→`companyIds` (List\<int\>).
> **Amaç:** Standart alanların dışında, organizasyon varlıklarına eklenen **dinamik/özel alanlar** (örn. "SGK No", "Sicil No").

## Alanlar
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Ek nitelik ID'si. |
| `organizationId` | int | FK → `organization.md` | Sahibi organizasyon. |
| `code` | string | — | Nitelik kodu. |
| `definition` | string | — | Nitelik tanımı. |
| `valueType` | enum | — | Değerin **tipi** — `QualificationValueType` ([`../enums/qualification-value-type.md`](../enums/qualification-value-type.md)) (String/Double/DateTime/Combobox); değerin hangi **typed sütuna** yazılacağını belirler. |
| `active` | bool | — | Aktif/pasif — **null olamaz**, varsayılan `true`. `false` = frontend'de **görünür/düzenlenebilir** ama BPM işlemede kullanılmaz. |
| `deleted` | bool | — | Soft-delete — **null olamaz**, varsayılan `false`. `true` = frontend'de **gizli/aktarılmaz/salt** + BPM işlemede kullanılmaz. |
| `companyIds` | List\<int\> | FK → `company.md` (N–N) | Nitelik kapsamındaki şirketler. |

## Alt model — AdditionalQualificationRelation (hangi varlığa uygulanır)
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Kayıt ID'si. |
| `additionalQualificationId` | int | FK → AdditionalQualification | Bağlı nitelik. |
| `relationalType` | enum | — | İlişkilendirilen varlık türü (aşağıda) — [`../enums/relational-type.md`](../enums/relational-type.md). |
| `required` | bool | — | Bu varlık için zorunlu mu. |

### Enum — RelationalType
Enum tanımı → [`../enums/relational-type.md`](../enums/relational-type.md). Bu modelde niteliğin hangi varlığa uygulandığını ve değerin hangi `...QualificationValue` alt modeline yazılacağını belirler.
| Index | Değer | Hedef varlık |
|---|---|---|
| 0 | `Users` | `user.md` |
| 1 | `Departments` | `department.md` |
| 2 | `Professions` | `profession.md` |
| 3 | `CostCenters` | `cost-center.md` |
| 4 | `WorkerLevels` | `worker-level.md` |

### Enum — QualificationValueType
Enum tanımı → [`../enums/qualification-value-type.md`](../enums/qualification-value-type.md). Niteliğin **değer tipi**; value modelinde hangi **typed sütunun** kullanılacağını belirler.
| Index | Değer | Depolanan sütun |
|---|---|---|
| 0 | `String` | `stringValue` (string) |
| 1 | `Double` | `doubleValue` (double) |
| 2 | `DateTime` | `datetimeValue` (datetime) |
| 3 | `Combobox` | `comboboxItemId` + kopya `comboboxCode` / `comboboxDefinition` |

## Alt model — QualificationItem (combobox seçeneği; `valueType = Combobox`)
`valueType=Combobox` olan nitelik, **kendi combobox seçeneklerini** ek nitelik sayfasında **`QualificationItem`** olarak
tanımlar. `PropertyItem` yapısından türetildi **fakat `Property` ile ilişkisi YOKTUR** (`propertyId` yerine
`additionalQualificationId`). Değer atama ekranında (`relationalType`'a göre) bu seçeneklerden **biri seçilir**.

| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Öğe ID'si. |
| `additionalQualificationId` | int | FK → AdditionalQualification | Bağlı ek nitelik (Combobox tipli). |
| `value` | string | — | Seçilen değer; `(additionalQualificationId, value)` **benzersiz**. |
| `code` | string | — | Çeviri eşleşme kodu (→ `translation.md`); öğe metni buradan çözülür. |
| `definition` | string | — | Öğe tanımı (yönetim ekranında görünen ad). |

> Değer atamada seçilen öğenin `code` + `definition`'ı ilgili `...QualificationValue`'nun `comboboxCode` /
> `comboboxDefinition` alanlarına **kopyalanır** (snapshot; anlık gösterim/çeviri, join'siz).

## Değer saklama (varlık başına)
Bir niteliğin **değeri**, hedef varlığın kendi "qualification value" alt modelinde tutulur. Ortak desen —
`{ id, <entity>Id, qualificationId, stringValue, doubleValue, datetimeValue, comboboxItemId, comboboxCode, comboboxDefinition }`:
niteliğin **`valueType`**'ına göre **yalnız ilgili sütun(lar)** doldurulur — String→`stringValue` · Double→`doubleValue` ·
DateTime→`datetimeValue` · **Combobox→`comboboxItemId` + kopya `comboboxCode`/`comboboxDefinition`** (diğerleri `null`).
Value modelleri: `UserQualificationValue` · `DepartmentQualificationValue` · `ProfessionQualificationValue` ·
`CostCenterQualificationValue` · `WorkerLevelQualificationValue`.

## Benzersizlik
> `(organizationId, code)` **benzersiz** — aynı organizasyonda aynı `code`'lu iki kayıt olamaz. **`deleted=true` kayıtlar kontrole dahil değildir** (soft-delete edilenler bu kontrolde sayılmaz).

## İlişkiler
- **N – 1** → `Organization` · **N – N** → `Company` (`companyIds`).
- **1 – N** ← `AdditionalQualificationRelation` (`additionalQualificationId`).
- **1 – N** ← `QualificationItem` (`additionalQualificationId`) — yalnız `valueType=Combobox` (combobox seçenekleri).
- **Değer:** `relationalType`'a göre ilgili varlığın `...QualificationValue` kaydında (`qualificationId` FK).

*Oluşturma: 2026-07-03.*
