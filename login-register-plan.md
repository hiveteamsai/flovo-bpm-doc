# Login / Register (Kimlik & Erişim) — Çalışma Planı

> **Durum:** 🟡 AÇIK — planlama tamam, yazım başlamadı. Kararlar bekleniyor (§6).
> **Amaç:** Login/register/kimlik-erişim **işleyişini** BPM motoru dökümantasyonuna eklemek.
> **Nasıl devam edilir:** Önce §6'daki kararları ver → sonra §5 Faz 1'den (`flovo-identity-access.md`) yazmaya başla.
> **Oluşturma:** 2026-08-25. **Bağlam:** İki keşif ajanının bulguları §2–§3'e işlendi (yeniden araştırma gerekmez).

---

## 0. Bu dosya ne için?

Login/register konusu **değerlendirildi** ama yazıma henüz geçilmedi. Bu dosya, konunun **tüm bağlamını + yol haritasını + açık
kararları** tek yerde tutar; kullanıcı bu konuya daha sonra dönecek. Devam ederken buradan başla.

> **Not (konvansiyon):** Projede açık sorular normalde yalnız `bpmEngine/todo.md`'de tutulur. Bu dosya **geçici bir çalışma/plan
> dosyasıdır**; §6'daki kararlar netleşince ilgili maddeler `todo.md`'ye ve tasarım dökümanlarına taşınıp bu dosya kapatılabilir.

---

## 1. Amaç & kapsam

- **Var olan:** Kimlik-erişim **modelleri** kısmen var (`User`, `Organization`, `UserGroup`), auth **teknoloji katmanı** kararlı (Keycloak).
- **Eksik olan:** **İşleyiş/akış** — login, kayıt/provisioning, oturum, doğrulama, impersonation, çok-tenant geçişi, Customer API kimliği (ApiKey) hiçbir dökümanda **akış olarak** yazılı değil.
- **Bu planın hedefi:** Bu işleyişi yeni bir kök döküman (`flovo-identity-access.md`) + model tamamlamaları ile yazmak.

---

## 2. Mevcut durum (değerlendirme)

### 2.1 Karar verilmiş (sağlam zemin)
- **Kimlik doğrulama (authN) = Keycloak'a devredilmiş.** Kaynak: `bpmEngine/tech-stack/keycloak.md` (🟢 · Keycloak 25).
  - OIDC/OAuth2 + SAML + JWT; **AD/LDAP User Federation** (Enterprise'da zorunlu); SSO.
  - **Custom Token Mapper SPI** → JWT'ye `organizationId` + rol/yetki claim'i gömer.
  - Akış: FE (Next.js) → Keycloak OIDC login → access token (JWT) → Go backend doğrular → **PostgreSQL RLS Pattern B** (`SET app.organization_id`).
- **Yetkilendirme (authZ) = Flovo'da, org-bazlı dinamik.** Kaynak: `bpmEngine/organization-settings/permissions.md` (🟢) — `hasPermission()`, admin + grup-bazlı.
- **Oturum kilidi:** `Organization.idleTimeoutMinute` — boşta kalınca kilit + **yeniden login** (v0.18 kararı).

### 2.2 Modellenmiş olan (hepsi 🟡 TASLAK)
| Model | Dosya | Auth-ilgili kritik alanlar |
|---|---|---|
| **User** | `bpmEngine/models/organization-settings/user.md` | `email?`/`phone?` = **giriş kimliği** (CHECK: en az biri dolu), `code`, `organizationId` (tenant FK), `active`/`deleted` (bool), `managerUserId`. **Şifre/hash YOK · token YOK · userName YOK · rol alanı YOK.** Benzersiz: `(orgId,email)`, `(orgId,phone)`, `(orgId,code)` |
| **Organization** | `bpmEngine/models/organization-settings/organization.md` | `idleTimeoutMinute`, `adminUserIds`, 4 yetki-grubu FK: `impersonationUserGroupId`, `organizationSettingsUserGroupId`, `serviceSettingsUserGroupId`, `viewAllReportsUserGroupId` |
| **UserGroup + UserGroupMember** | `bpmEngine/models/organization-settings/user-group.md` | `UserGroupMember{ userGroupId, userId, companyId }` = grup **üyeliği** |
| **ApiKey** | *(modellenmemiş — sadece FK olarak geçiyor)* | `ProcessInstance.createdByApiKeyId`, `ProcessStepInstance.atApiKeyId`, `InstanceValueChange.changedByApiKeyId`. Ad geçici, alanlar tanımsız |

- **Auth enum'u YOK** (`bpmEngine/models/enums/`): kullanıcı-durumu / doğrulama-tipi / oturum-tipi enum'u yok. Kullanıcı durumu `active`/`deleted` **bool**.

### 2.3 Boşluklar (model VAR ama işleyiş YOK)
1. **Kayıt/self-signup akışı yok** — User nasıl oluşuyor/kaydoluyor yazılı değil. `keycloak.md` "kullanıcı-provisioning ve `organizationId` atama akışı onboarding'de netleştirilmeli" diyor → **User ↔ Keycloak provisioning açık.**
2. **Login'in Flovo-tarafı ayrıntısı yok** — yalnız Keycloak referansı var; token doğrulama/refresh yaşam döngüsü Flovo dökümanlarında yok.
3. **Session/oturum modeli yok** — `idleTimeoutMinute` var, token/refresh yaşam döngüsü Keycloak'a devredilmiş, Flovo tarafı yazılmamış.
4. **ApiKey modellenmemiş** — 3 runtime modeli FK veriyor; model/alan/yaşam döngüsü (oluşturma, kapsam, rotasyon) yok. (`todo.md`'de açık.)
5. **Davet/Invitation akışı yok** — ne model ne döküman.
6. **Organizasyon üyeliği** yalnız grup üyeliği (`UserGroupMember`) olarak var; org üyeliği `User.organizationId` + `adminUserIds` ile örtük — ayrı join/katılma akışı yok.
7. **E-posta/telefon doğrulama (verification)** modeli/akışı/enum'u yok.
8. **Impersonation** yetki alanı (`impersonationUserGroupId`) var, **kapsam/akış/audit açık** (`todo.md`).
9. **Password/credential** Flovo'da bilinçli yok (Keycloak sahibi) — ama tek satırla belirtilmiş.

### 2.4 İlgili `todo.md` açık maddeleri (mevcut)
- Customer API — kimlik/yetki (token kapsam/süre/yenileme); webhook güvenliği + idempotency (kimlik = Keycloak token).
- `apiKeyId` içeriği/adı — Customer API erişim mekanizması kesinleşince doğrulanacak.
- Yetkilendirme açık kalanlar: `ProcessStepAction.authorizationLevel`, impersonation kapsamı.
- `idleTimeoutMinute` alt/üst sınır + Organization sonraki alanlar (kilit davranışı çözüldü: yeniden login).
- Merkezi-kimlik: Keycloak AD/LDAP ile giderildi; kalan minör: saf-on-prem'de **sosyal-login** kapsamı.
- **Vekalet (proxy) sistemi** — görev-devri yerine kalıcı vekalet (impersonation ile kavramsal komşu; §6.5'e bak).

---

## 3. Eski app referansı (özet — bağlam korunsun diye)

> Eski app'ten salt-referans özet (kaynak-kod yolu tutulmaz; gerekirse kullanıcı verir). Yeni tasarım kendi başına yazılır.

- **Login:** e-posta/telefon → **OTP** (`sendverificationcode` + `CheckVerificationCode`, 6 hane) → `AccountDto.authenticationType`'a göre dallanma:
  - `no` = şifresiz (sadece OTP) · `client-eba` = kul.adı+şifre · `azure-adb2c` = Azure AD B2C (backend'de; mobil sadece credential toplar).
  - **Token:** JWT `accessToken` + `refreshToken` (`UserDto` içinde). Refresh: 401 + `TOKEN_EXPIRED` → `RefreshToken` endpoint, tek-uçuşlu. `Authorization: Bearer`.
- **"Register" = gerçek kayıt değil, ŞİFRE ATAMA** (davetli/provizyonlu kullanıcıya). **Self-servis şirket-kurma/hesap-açma YOK** → model **davet/provizyon-tabanlı**.
- **Şifre:** ilk-belirleme/değiştirme aynı `Register` endpoint'i (`isPasswordMustChange`). Klasik "şifremi unuttum" endpoint'i **yok** (dolaylı: OTP + yeniden set).
- **Oturum:** idle timeout (varsayılan 12 saat), logout (yerel temizlik + `logout`), **QR ile giriş** (SignalR, çoklu cihaz).
- **Multi-tenant:** hesap e-posta/telefondan tek belirleniyor; **admin hesap değiştirme** (`GetAdminAccounts` / `GetLoginResponseAdminUserByAccount`); **impersonation** (`changeUser`/`undoChangeUser`, shadow-pref + Splash'ta geri-alma → kırılgan).
- **SSO/MFA:** gerçek interaktif SSO **yok** (Google/MS/Apple/SAML paketi yok), TOTP/authenticator MFA **yok**, cihaz biyometrisi **yok** (PEP'teki "biometric" = KYC rıza onayı, giriş yöntemi değil).
- **Taşınırken dersler:** (1) auth tenant'a göre **policy-driven** olmalı; (2) token güvenliği (eski app mobilde düz SharedPreferences → yeni: secure storage); (3) "register≠signup"; self-servis kayıt + ayrık parola-sıfırlama **yeni yetenek** olarak tasarlanmalı; (4) multi-tenant + impersonation **token-scoped + audit'li** olmalı; (5) gerçek OIDC/OAuth2 (PKCE) + opsiyonel MFA baştan planlanmalı.

---

## 4. Önerilen dökümantasyon yapısı (nereye)

İşleyiş (akış) için **yeni kök döküman** — `flovo-bpm-engine.md` / `flovo-customer-api.md` ile kardeş:

| Katman | Dosya | Ne anlatır | Durum |
|---|---|---|---|
| **İşleyiş (YENİ)** | `bpmEngine/flovo-identity-access.md` | Login · kayıt/provisioning · oturum · doğrulama · impersonation · çok-tenant · ApiKey **akışları** (sequence) | ⚪ yazılacak |
| Teknoloji | `bpmEngine/tech-stack/keycloak.md` | Keycloak katmanı — link verilir, tekrar yazılmaz | 🟢 var |
| Yetki | `bpmEngine/organization-settings/permissions.md` | authZ — link | 🟢 var |
| Modeller | `bpmEngine/models/organization-settings/` | `user.md`/`organization.md` güncelle + **yeni:** `api-key.md`, (karara göre) `invitation.md` | 🟡/⚪ |
| Enum | `bpmEngine/models/enums/` | (karara göre) `authentication-type`, `invitation-status`, `verification-channel` | ⚪ |

> Kök `bpmEngine/index.md` ve `models/index.md`'ye yeni doküman/model satırları eklenecek.

---

## 5. Fazlı yol haritası (checklist)

### Faz 1 — Ana işleyiş dökümanı (`flovo-identity-access.md`) — *en büyük değer*
- [ ] Mimari sınır: **authN=Keycloak / authZ=Flovo** (net çizgi + `keycloak.md` & `permissions.md` linkleri)
- [ ] **Login akışı** (sequence): FE → Keycloak OIDC → JWT (`organizationId` claim) → Go backend doğrulama → RLS
- [ ] **Kayıt/provisioning akışı** (User ↔ Keycloak; §6.1–§6.2 kararına göre)
- [ ] **Oturum yaşam döngüsü**: token/refresh (Keycloak sahibi) + `idleTimeoutMinute` (Flovo) + logout — sınır belirt
- [ ] **Doğrulama** (email/phone — §6.3 kararına göre sahibi)
- [ ] **Impersonation** akışı (özet + §6.5) + **Vekalet** ile sınır notu
- [ ] **Çok-tenant** organizasyon seçimi/geçişi
- [ ] **Customer API kimliği (ApiKey)** — özet, detay Faz 2'ye link
- [ ] `bpmEngine/index.md`'ye doküman satırı ekle

### Faz 2 — Model tamamlama
- [ ] **`api-key.md`** (yeni model): alanlar (kapsam, süre, rotasyon, `organizationId`, oluşturan), 3 FK bağı (`createdByApiKeyId`/`atApiKeyId`/`changedByApiKeyId`)
- [ ] **`user.md`** güncelle: Keycloak bağ alanı (ör. `keycloakUserId` / `externalSubject`) + provisioning notu
- [ ] (§6.1 self-signup/davet kararına göre) **`invitation.md`** + `InvitationStatus` enum
- [ ] (§6.3 kararına göre) doğrulama enum'u / modeli — ya da "Keycloak sahibi" notuyla kapat
- [ ] Gerekirse `authentication-type` enum (policy-driven auth için)
- [ ] `models/index.md` ilişki haritasına yeni model(ler)i ekle

### Faz 3 — Çapraz bağ & todo temizliği
- [ ] `keycloak.md` ↔ `flovo-identity-access.md` çapraz link
- [ ] `flovo-customer-api.md` ↔ `api-key.md` bağ
- [ ] `todo.md` ilgili maddeleri güncelle/kapat (§2.4)
- [ ] `research/compare/new-vs-current.md`'ye auth farkını ekle (eski davet/provizyon + OTP-dallanma → yeni Keycloak-federasyon)
- [ ] commitNote (`v0-X.md`) + commit/push (kullanıcı isteyince)

---

## 6. Karar bekleyen açık sorular (yazımdan önce) — numaralı + öneri

> Kullanıcı bunlara karar verince Faz 1 yazımı başlar. "Önerilerin uygun" → önerilen varsayılanlarla ilerlenir.

1. **Kayıt modeli:** Self-servis "şirket kur/hesap aç" **var mı**, yoksa **davet/provizyon-tabanlı** (org'a katılma) mı?
   → *Öneri: davet/provizyon-tabanlı (Enterprise + AD/LDAP gerektiriyor); self-signup post-MVP.*
2. **Kullanıcı provisioning (User ↔ Keycloak):** (a) ilk login'de **JIT** (Flovo `User` otomatik) · (b) admin oluşturur → Keycloak push · (c) SCIM/senkron?
   → *Öneri: (a) JIT + admin-daveti melezi.*
3. **Doğrulama (email/phone) sahibi:** Keycloak mı (federasyon/OIDC), yoksa Flovo OTP mi?
   → *Öneri: Keycloak sahibi; Flovo doğrulanmış claim'e güvenir.*
4. **Oturum/token:** Session modeli Flovo'da tutulmasın (Keycloak sahibi), Flovo yalnız `idleTimeoutMinute` uygulasın — "sınır + referans" olarak mı yazayım?
   → *Öneri: evet.*
5. **Impersonation:** Auth doc'ta **özet** + detay ayrı açık madde (kapsam/audit henüz açık) mı? Ayrıca **Vekalet** ile sınır çizilsin mi (impersonation=admin geçici tam-taklit ↔ vekalet=kullanıcının verdiği süreli onay yetkisi)?
   → *Öneri: özet + todo'ya detay; vekalet sınırı çizilsin.*
6. **ApiKey:** Şimdi iskelet model mi, yoksa Customer API erişim mekanizması kesinleşene kadar **yer tutucu** mu?
   → *Öneri: şimdi iskelet + detay Customer API fazına bağlı.*
7. **SSO/MFA kapsamı (MVP):** Sosyal login + MFA/biyometri MVP'de mi, post-MVP mi?
   → *Öneri: MVP=OIDC+AD/LDAP; sosyal login + MFA post-MVP.*

---

## 7. İlgili dosyalar / kaynaklar

- `bpmEngine/tech-stack/keycloak.md` — auth teknoloji katmanı (🟢, temel).
- `bpmEngine/organization-settings/permissions.md` — authZ (🟢).
- `bpmEngine/models/organization-settings/user.md` · `organization.md` · `user-group.md` — modeller (🟡).
- `bpmEngine/flovo-customer-api.md` — ApiKey/token bağı (🟡).
- `bpmEngine/models/index.md` §4 — ApiKey FK'leri.
- `bpmEngine/todo.md` — §2.4 açık maddeler.

---

## 8. Sonraki adım (devam noktası)

➡️ **§6'daki 7 kararı ver** (ya da "önerilerin uygun" de) → ardından **Faz 1**: `bpmEngine/flovo-identity-access.md`'i yaz.

*Oluşturma: 2026-08-25. Bu plan dosyası ana dizindedir; konuya dönünce buradan başla.*
