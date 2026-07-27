# Model — Organization

> **Durum:** 🟡 TASLAK (ilk çıkarım — gözden geçirilecek)
> **Amaç:** Flovo'yu kullanan **kurumu (tenant)** temsil eder. Verinin en üst kapsayıcısıdır; kullanıcı/servis/çeviri/
> durum vb. bir organizasyona bağlıdır. Organizasyonlar birbirinden **izoledir**.
> **Davranış/kullanım:** → `../../organization-settings/organization.md`

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Organizasyon ID'si. Diğer modeller `organizationId` ile buraya bağlanır. |
| `code` | string | Unique | Organizasyon **kodu**; **benzersiz**. **Dış referanslarda** (API/entegrasyon) `id` yerine bu kullanılır. |
| `name` | string | — | Organizasyon **adı** (kullanıcıya görünen). |
| `defaultLang` | string | — | **Varsayılan dil**; **sabit set** `tr`/`en`/`de` içinden. Çeviri çözümlemesinde aktif dilin başlangıcı. |
| `logoUrl` | string? | — | Organizasyon **logosu** (görsel URL). Başlık/rapor/bildirimlerde marka. |
| `idleTimeoutMinute` | int | — | **Boşta kalma zaman aşımı** (dk). **null olamaz, varsayılan `0`**. `0` = disable; `>0` iken süre dolunca oturum kilitlenir → **yeniden giriş (login) gerekir**. |
| `adminUserIds` | List\<int\> | FK → `user.md` | **Organizasyon adminleri** (**en az 1 aktif**). Yetki yapılandırmasını yalnız bunlar değiştirir; **tüm yetkilere** sahiptir. |

## Yetkilendirme (Permissions)
Yetkiler **organizasyon bazında** yönetilir (eski `User.authorizationLevel` kaldırıldı). Her yetki için Organization'da
**tek bir kullanıcı grubu** alanı vardır; seçilen grubun üyeleri o yetkiyi alır. Davranış → `../../organization-settings/permissions.md`.

| Alan | Tip | Anahtar | Yetki |
|---|---|---|---|
| `impersonationUserGroupId` | int? | FK → `user-group.md` | Kullanıcı yerine geçme |
| `organizationSettingsUserGroupId` | int? | FK → `user-group.md` | Organizasyon (yapısal) ayarları erişimi |
| `serviceSettingsUserGroupId` | int? | FK → `user-group.md` | Servis ayarları erişimi |
| `viewAllReportsUserGroupId` | int? | FK → `user-group.md` | Tüm raporları görme |

> **Çözümleme:** kullanıcı **admin** (`adminUserIds`) ise tüm yetkilere sahiptir; değilse ilgili `*UserGroupId` grubunun
> üyesiyse o yetkiye sahiptir. Yetki yapılandırmasını (**`adminUserIds`** + bu grup alanları) **yalnız adminler** düzenler.

## İlişkiler
- **1 – N** → `Solution` (`solution.organizationId`) — servisler bu solution'lar altında oluşturulur.
- **1 – N** → `Translation`, `Style`, `Action`, `Status` (hepsi `organizationId`) — **organizasyon havuzu**; o
  organizasyonun tüm servislerinde kullanılabilir.
- **N – N** → `User` (`adminUserIds`) — organizasyon adminleri.
- **N – 1** → `UserGroup` (`impersonationUserGroupId`, `organizationSettingsUserGroupId`, `serviceSettingsUserGroupId`, `viewAllReportsUserGroupId`) — grup-bazlı 4 yetki (→ `../../organization-settings/permissions.md`).
- `organizationId = null` olan Translation/Style kayıtları **ortak/sistem** kabul edilir (organizasyon değil, Flovo sahibi).

## Notlar / açık noktalar
- `idleTimeoutMinute` **alt/üst sınırı** → `../../todo.md`. _(Kilit davranışı **çözüldü** (v0.18): süre dolunca oturum kilitlenir, **yeniden giriş/login** gerekir.)_
- Sonraki alanlar: plan/abonelik, timezone, para birimi, bölge, güvenlik → `../../todo.md`.

*Oluşturma: 2026-07-02.*
