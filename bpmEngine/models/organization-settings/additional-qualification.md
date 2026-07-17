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
| `translationCode` | string? | çeviri anahtarı | **Çeviri eşleşme anahtarı** (→ [`translation.md`](./translation.md) `code`). `null` = çeviri **es geçilir**, doğrudan `definition` kullanılır. |
| `valueType` | QualificationValueType | — | Değerin **tipi** ([`../enums/qualification-value-type.md`](../enums/qualification-value-type.md)) (string/double/dateTime/combobox); değerin hangi **typed sütuna** yazılacağını belirler. |
| `active` | bool | — | Aktif/pasif — **null olamaz**, varsayılan `true`. `false` = frontend'de **görünür/düzenlenebilir** ama BPM işlemede kullanılmaz. |
| `deleted` | bool | — | Soft-delete — **null olamaz**, varsayılan `false`. `true` = frontend'de **gizli/aktarılmaz/salt** + BPM işlemede kullanılmaz. |
| `companyIds` | List\<int\> | FK → `company.md` (N–N) | Nitelik kapsamındaki şirketler. |

## Alt model — AdditionalQualificationRelation (hangi varlığa uygulanır)
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Kayıt ID'si. |
| `additionalQualificationId` | int | FK → AdditionalQualification | Bağlı nitelik. |
| `relationalType` | RelationalType | — | İlişkilendirilen varlık türü (aşağıda) — [`../enums/relational-type.md`](../enums/relational-type.md). |
| `required` | bool | — | Bu varlık için zorunlu mu. |

### Enum — RelationalType
Enum tanımı → [`../enums/relational-type.md`](../enums/relational-type.md). Bu modelde niteliğin hangi varlığa uygulandığını ve değerin hangi `...QualificationValue` alt modeline yazılacağını belirler.
| Index | Değer | Hedef varlık |
|---|---|---|
| 0 | `users` | `user.md` |
| 1 | `departments` | `department.md` |
| 2 | `professions` | `profession.md` |
| 3 | `costCenters` | `cost-center.md` |
| 4 | `workerLevels` | `worker-level.md` |

### Enum — QualificationValueType
Enum tanımı → [`../enums/qualification-value-type.md`](../enums/qualification-value-type.md). Niteliğin **değer tipi**; value modelinde hangi **typed sütunun** kullanılacağını belirler.
| Index | Değer | Depolanan sütun |
|---|---|---|
| 0 | `string` | `stringValue` (string) |
| 1 | `double` | `doubleValue` (double) |
| 2 | `dateTime` | `datetimeValue` (datetime) |
| 3 | `combobox` | `comboboxItemId` + kopya `comboboxTranslationCode` / `comboboxDefinition` |

## Alt model — QualificationItem (combobox seçeneği; `valueType = combobox`)
`valueType=combobox` olan nitelik, **kendi combobox seçeneklerini** ek nitelik sayfasında **`QualificationItem`** olarak
tanımlar. `PropertyItem` yapısından türetildi **fakat `Property` ile ilişkisi YOKTUR** (`propertyId` yerine
`additionalQualificationId`). Değer atama ekranında (`relationalType`'a göre) bu seçeneklerden **biri seçilir**.

| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Öğe ID'si. |
| `additionalQualificationId` | int | FK → AdditionalQualification | Bağlı ek nitelik (combobox tipli). |
| `value` | string | — | Seçilen değer; `(additionalQualificationId, value)` **benzersiz**. |
| `translationCode` | string? | çeviri anahtarı | **Çeviri eşleşme anahtarı** (→ [`translation.md`](./translation.md) `code`); öğe metni buradan çözülür. `null` = çeviri **es geçilir**, doğrudan `definition` kullanılır. |
| `definition` | string | — | Öğe tanımı — **varsayılan dildeki** metin (yönetim ekranında görünen ad). |

> Değer atamada seçilen öğenin `translationCode` + `definition`'ı ilgili `...QualificationValue`'nun
> `comboboxTranslationCode` / `comboboxDefinition` alanlarına **kopyalanır** (snapshot; anlık gösterim/çeviri, join'siz).
> Snapshot **çeviri anahtarını da taşır** — böylece kopya metin de aktif dile çözülebilir; `comboboxTranslationCode`
> `null` ise `comboboxDefinition` doğrudan kullanılır.

## Değer saklama (varlık başına)
Bir niteliğin **değeri**, hedef varlığın kendi "qualification value" alt modelinde tutulur. Ortak desen —
`{ id, <entity>Id, qualificationId, stringValue, doubleValue, datetimeValue, comboboxItemId, comboboxTranslationCode, comboboxDefinition }`:
niteliğin **`valueType`**'ına göre **yalnız ilgili sütun(lar)** doldurulur — string→`stringValue` · double→`doubleValue` ·
dateTime→`datetimeValue` · **combobox→`comboboxItemId` + kopya `comboboxTranslationCode`/`comboboxDefinition`** (diğerleri `null`).
Value modelleri: `UserQualificationValue` · `DepartmentQualificationValue` · `ProfessionQualificationValue` ·
`CostCenterQualificationValue` · `WorkerLevelQualificationValue`.

## Benzersizlik
> `(organizationId, code)` **benzersiz** — aynı organizasyonda aynı `code`'lu iki kayıt olamaz. **`deleted=true` kayıtlar kontrole dahil değildir** (soft-delete edilenler bu kontrolde sayılmaz).

## İlişkiler
- **N – 1** → `Organization` · **N – N** → `Company` (`companyIds`).
- **1 – N** ← `AdditionalQualificationRelation` (`additionalQualificationId`).
- **1 – N** ← `QualificationItem` (`additionalQualificationId`) — yalnız `valueType=combobox` (combobox seçenekleri).
- **Değer:** `relationalType`'a göre ilgili varlığın `...QualificationValue` kaydında (`qualificationId` FK).

*Oluşturma: 2026-07-03.*
