# Model — User (Kullanıcı — organizasyon ayarı)

> **Durum:** 🟡 TASLAK — eski uygulama DTO'sundan türetildi.
> **Kaynak DTO:** `../../research/current-flovo-bpm-engine/organizations/users.md` (`AccountUserDto`).
> **Dönüşüm:** `account*`→`organization*`; `accountId` (string) → **`organizationId` (int)**; `userId`→`id`;
> string FK'ler int'e: `departmantId`→`departmentId`, `unvanId`→`professionId`, `yoneticiUserId`→`managerUserId`,
> `masrafYeriId`→`costCenterId`.
> **Amaç:** Organizasyondaki **kişiler**. BPM onay mercilerinin (kullanıcı / yönetici / yönetici zinciri / departman yöneticisi) temeli.

## Alanlar — temel
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Kullanıcı ID'si. |
| `organizationId` | int | FK → `organization.md` | Sahibi organizasyon. |
| `email` | string | — | E-posta (giriş kimliği + bildirim). |
| `phone` | string | — | Telefon numarası. |
| `code` | string | — | Kullanıcı kodu. |
| `firstName` / `lastName` | string | — | Ad / Soyad. _(fullName = getter, saklanmaz.)_ |
| `profilePhoto` | string | — | Profil fotoğrafı URL. |
| `active` | bool | — | Aktif/pasif — **null olamaz**, varsayılan `true`. `false` = frontend'de **görünür/düzenlenebilir** ama BPM işlemede kullanılmaz. |
| `deleted` | bool | — | Soft-delete — **null olamaz**, varsayılan `false`. `true` = frontend'de **gizli/aktarılmaz/salt** + BPM işlemede kullanılmaz. |
| `employmentStartDate` | datetime | — | İşe başlama tarihi. |
| `synchronizationStatus` | bool | — | Senkron durumu. |
| `facebook` / `instagram` / `linkedin` / `twitter` | string | — | Sosyal medya. |

> **Yetki:** Eski `authorizationLevel` (sayısal) **kaldırıldı**; yetkiler artık **organizasyon bazında** (admin + grup-bazlı)
> yönetilir → `../../organization-settings/permissions.md`.

## Alanlar — organizasyon bağlantıları
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `departmentId` | int? | FK → `department.md` | Departman. |
| `professionId` | int? | FK → `profession.md` | Ünvan/meslek. |
| `managerUserId` | int? | FK → User (self-ref) | **Yönetici** (yönetici zinciri). |
| `costCenterId` | int? | FK → `cost-center.md` | Masraf yeri. |
| `workerLevelId` | int? | FK → `worker-level.md` | Çalışan seviyesi. |
| `workingScheduleId` | int? | FK → `working-schedule.md` | Çalışma takvimi. |
| `companyIds` | List\<int\> (boş olabilir) | FK → `company.md` (N–N) | İlişkili şirketler. |

> **Tüm organizasyon bağlantıları opsiyoneldir** (nullable); kullanıcı bunların hiçbirine bağlı olmadan da tanımlanabilir.

## Alt modeller
### UserSolution (çözüm erişimi)
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Kayıt ID'si. |
| `userId` | int | FK → User | Bağlı kullanıcı. |
| `solutionId` | int | FK → `../service-settings/solution.md` | Erişilen çözüm. |

### UserQualificationValue (ek nitelik değeri)
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Kayıt ID'si. |
| `userId` | int | FK → User | Bağlı kullanıcı. |
| `qualificationId` | int | FK → `additional-qualification.md` | Ek nitelik. |
| `stringValue` | string? | — | `valueType=string` ise değer burada. |
| `doubleValue` | double? | — | `valueType=double` ise değer burada. |
| `datetimeValue` | datetime? | — | `valueType=dateTime` ise değer burada. |
| `comboboxItemId` | int? | FK → `additional-qualification.md` (QualificationItem) | `valueType=combobox` ise **seçilen öğe**. |
| `comboboxCode` | string? | — | Seçilen öğenin **kopya `code`**'u (çeviri). |
| `comboboxDefinition` | string? | — | Seçilen öğenin **kopya `definition`**'ı. |

> **Kredi kartları:** `CreditCard.userId` üzerinden bağlanır (bkz. `credit-card.md`).

## Benzersizlik
> `(organizationId, code)` · `(organizationId, email)` · `(organizationId, phone)` **benzersiz** — aynı organizasyonda aynı
> `code` / `email` / `phone`'lu iki kullanıcı olamaz. **Farklı organizasyonlarda aynı e-posta/telefon kullanılabilir**
> (organizasyon bazında benzersiz, global değil). **`deleted=true` kayıtlar kontrole dahil değildir**.

## İlişkiler
- **N – 1** → `Organization`, `Department`, `Profession`, `CostCenter`, `WorkerLevel`, `WorkingSchedule`, `User` (`managerUserId`, self-ref).
- **N – N** → `Company` (`companyIds`), `UserGroup` (üyelik → `UserGroupMember`).
- **1 – N** ← `UserSolution`, `UserQualificationValue`, `CreditCard` (`userId`).
- **1 – 1** ← `Staff` (`userId`) — kullanıcının **pozisyon/kadro** ataması; User'da depolanmaz, salt-okunur yansıma (→ `position.md`).
- **BPM:** onay merci atamaları (kullanıcı / yönetici / yönetici zinciri / departman yöneticisi / ünvana göre yönetici).

*Oluşturma: 2026-07-03.*
