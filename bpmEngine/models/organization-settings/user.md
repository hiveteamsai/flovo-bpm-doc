# Model — User (Kullanıcı — organizasyon ayarı)

> **Durum:** 🟢 Gözden geçirildi (v0.36)
> **Amaç:** Organizasyondaki **kişiler**. BPM onay mercilerinin (kullanıcı / kullanıcının yöneticisi / departman yöneticisi) temeli.

## Alanlar — temel
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Kullanıcı ID'si. |
| `organizationId` | int | FK → `organization.md` | Sahibi organizasyon. |
| `email` | string? | — | E-posta (giriş kimliği + bildirim). **`phone` ile birlikte ikisi birden null olamaz** (↓ Kimlik alanları). |
| `phone` | string? | — | Telefon numarası (giriş kimliği + bildirim). **`email` ile birlikte ikisi birden null olamaz** (↓ Kimlik alanları). |
| `code` | string | — | Kullanıcı kodu. |
| `firstName` / `lastName` | string | — | Ad / Soyad. _(fullName = getter, saklanmaz.)_ |
| `profilePhoto` | string? | — | Profil fotoğrafı URL. |
| `active` | bool | — | Aktif/pasif — **null olamaz**, varsayılan `true`. `false` = frontend'de **görünür/düzenlenebilir** ama BPM işlemede kullanılmaz. |
| `deleted` | bool | — | Soft-delete — **null olamaz**, varsayılan `false`. `true` = frontend'de **gizli/aktarılmaz/salt** + BPM işlemede kullanılmaz. |
| `employmentStartDate` | datetime? | — | İşe başlama tarihi. |
| `synchronizationStatus` | [SyncStatus](../enums/sync-status.md) | — | Harici sistemle (ERP/muhasebe) **senkron durumu** — `synced` / `pending` / `error`. |

> **Kimlik alanları (`email` / `phone`):** ikisi de **nullable**, fakat **en az biri dolu olmak zorundadır** —
> `email IS NOT NULL OR phone IS NOT NULL` (CHECK kısıtı). Kullanıcı **e-posta ile, telefon ile veya ikisiyle** tanımlanabilir;
> **hiçbiri olmadan** tanımlanamaz (giriş kimliği ve bildirim kanalları bunlara dayanır → [`../enums/notification-channel.md`](../enums/notification-channel.md)).

> **Yetki:** Yetkiler **organizasyon bazında** (admin + grup-bazlı) **dinamik** yönetilir → `../../organization-settings/permissions.md`.
> (Kullanıcıda ayrı bir yetki-seviyesi alanı tutulmaz.)

## Alanlar — organizasyon bağlantıları
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `departmentId` | int? | FK → `department.md` | Departman. |
| `professionId` | int? | FK → `profession.md` | Ünvan/meslek. |
| `managerUserId` | int? | FK → User (self-ref) | **Yönetici** — kullanıcının doğrudan yöneticisi (`usersManager` atamasında kullanılır). |
| `costCenterId` | int? | FK → `cost-center.md` | Masraf yeri. |
| `workerLevelId` | int? | FK → `worker-level.md` | Çalışan seviyesi. |
| `workingScheduleId` | int? | FK → `working-schedule.md` | Çalışma takvimi. |
| `companyIds` | List\<int\> (boş olabilir) | FK → `company.md` (N–N) | İlişkili şirketler. |
| `primaryCompanyId` | uuid? | FK → `company.md` (**bileşik**: `(userId, primaryCompanyId)` → `user_company`) | **Kullanıcının "1. şirketi"** — `companyIds` üyeliklerinden **biri**. Üyelik dışından değer atanamaz (garanti **deklaratif**: bileşik FK; uygulama kontrolü değil). Üyelik kaldırılırsa alan **NULL**'a düşer (`ON DELETE SET NULL`). |

> **Tüm organizasyon bağlantıları opsiyoneldir** (nullable); kullanıcı bunların hiçbirine bağlı olmadan da tanımlanabilir.

> **⚠️ Durum (2026-09-10) · `primaryCompanyId`:** bu alan ÜRÜNE HENÜZ İNMEDİ. Yukarıdaki satır **tasarımı** anlatır. Göç ve bileşik FK taslak PR'da (#353/AC-2); **#408 göç kapısı ⊕ iş sahibi ack'i** bekliyor. Bugün ürün veritabanında ne `primary_company_id` sütunu ne o FK vardır — *"üyelik dışından değer atanamaz"* ve *"üyelik kaldırılırsa NULL'a düşer"* ifadeleri **tasarım gereğidir, yürürlükte olan bir garanti değildir.** Yürürlüğe girdiğinde bu not kalkar.
>
> **Ölçümün adresi — ✅ bugün `origin/main`'de doğrulanabilir:**
> `org_users.id` UUID ⟹ `supabase/migrations/20260820110000_org_users.sql:30` ·
> `org_companies.id` UUID ⟹ `20260706120000_org_companies.sql:15` ·
> `user_company` ⟹ `20260820110000_org_users.sql:83-88` (`:84` user_id UUID→org_users(id) ·
> `:85` company_id UUID→org_companies(id) · `:87` **PRIMARY KEY (user_id, company_id)** — bileşik
> FK'nın hedefi olabilmesinin şartı).
>
> **⚠️ Yalnız taslak PR'da (bugün main'de YOK):** `feat/353-ac2-primary-company` ⟹
> `supabase/migrations/20260909180000_org_users_primary_company.sql:47` (ADD COLUMN … UUID) ⊕
> **`:58-61`** (kısıt adı · `FOREIGN KEY (id, primary_company_id)` · `REFERENCES user_company
> (user_id, company_id)` · `ON DELETE SET NULL (primary_company_id)`) — kolon **listeli** SET NULL;
> listesiz hâli `id`'yi de NULL'lamaya çalışırdı ⊕ ⚠️ PG 15+ gerektirir (pilot 16.15).

> **⚠️ `primaryCompanyId` `isDefaultCompany` ile AYNI ŞEY DEĞİLDİR ve ona fallback YAPILMAZ.** `company.md`'deki `isDefaultCompany` **organizasyon** seviyesinde bir varsayılandır; `primaryCompanyId` **kullanıcı** seviyesindedir. `primaryCompanyId` boşsa **boş görünür** — organizasyon varsayılanına düşmez. *(Karşılaştırma: `position.md`'de `companyId` boş bırakılırsa varsayılan şirket kullanılır; **burada o desen kasıtlı olarak izlenmez** — "boş" bir cevaptır, "bilinmiyor"un yerine bir değer konmaz.)*

> **Neden kullanıcı seviyesinde:** `userInfo` değer-seçicisinde "Şirket" anahtarı, süreç çalışırken kullanıcının **kendi** birincil şirketini vermek zorundadır; organizasyon varsayılanı çok-şirketli bir kullanıcıda yanlış cevap üretir. (İş sahibi onayı: 2026-09-08 · #353)

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
| `comboboxTranslationCode` | string? | çeviri anahtarı | Seçilen öğenin **kopya `translationCode`**'u (çeviri; `null` ise `comboboxDefinition` doğrudan kullanılır). |
| `comboboxDefinition` | string? | — | Seçilen öğenin **kopya `definition`**'ı. |

> **Kredi kartları:** `CreditCard.userId` üzerinden bağlanır (bkz. `credit-card.md`).

## Benzersizlik
> `(organizationId, code)` · `(organizationId, email)` · `(organizationId, phone)` **benzersiz** — aynı organizasyonda aynı
> `code` / `email` / `phone`'lu iki kullanıcı olamaz. **Farklı organizasyonlarda aynı e-posta/telefon kullanılabilir**
> (organizasyon bazında benzersiz, global değil). **`deleted=true` kayıtlar kontrole dahil değildir**.
> **`email`/`phone` null ise benzersizlik kontrolüne girmez** — dolayısıyla aynı organizasyonda `email`'i null olan birden
> çok kullanıcı olabilir (aynısı `phone` için).

## İlişkiler
- **N – 1** → `Organization`, `Department`, `Profession`, `CostCenter`, `WorkerLevel`, `WorkingSchedule`, `User` (`managerUserId`, self-ref).
- **N – N** → `Company` (`companyIds`), `UserGroup` (üyelik → `UserGroupMember`).
- **1 – N** ← `UserSolution`, `UserQualificationValue`, `CreditCard` (`userId`).
- **1 – 1** ← `Staff` (`userId`) — kullanıcının **pozisyon/kadro** ataması; User'da depolanmaz, salt-okunur yansıma (→ `position.md`).
- **BPM:** onay merci atamaları (süreci başlatan / sabit kullanıcı / kullanıcının yöneticisi / departman yöneticisi / değişken kullanıcı → `../enums/process-step-user-type.md`).

*Oluşturma: 2026-07-03.*
