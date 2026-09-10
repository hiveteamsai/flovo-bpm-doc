# Flovo Kimlik & Erişim — Login Akışı (Identity & Access)

> **Durum:** 🟡 TASLAK (v0.48) — işlevsel kararlar **kesin** (v0.48 kararları L1–L13); teknik gerçekleştirme noktaları **🟦 VARSAYIM** etiketiyle
> yazıldı, `todo.md` Login/Auth maddesindeki karar (K#) verilince kesinleşir. **Kararlar / açık noktalar:** [`todo.md`](../../todo.md) Tier 2 "Login / Auth" (K2–K12).
> **Kardeş doküman:** [`flovo-auth-mechanism.md`](./flovo-auth-mechanism.md) — token / refresh / oturum mekanizması (bu doküman **akışı**, o doküman **mekanizmayı** anlatır).
> **Teknoloji:** [`tech-stack/keycloak.md`](../../tech-stack/keycloak.md) · **Yetki:** [`organization-settings/permissions.md`](../../organization-settings/permissions.md) ·
> **Modeller:** [`models/organization-settings/user.md`](../../models/organization-settings/user.md) · [`organization.md`](../../models/organization-settings/organization.md).

---

## 0. Özet (bir paragraf)

Flovo'ya **şifre yoktur**. Kullanıcı **e-posta veya telefon** girer; kimlik hiçbir organizasyonda bulunamazsa **"kullanıcı bulunamadı"** hatası alır;
bulunduysa girilen kanala **6 haneli tek-kullanımlık kod (OTP)** gönderilir. Kod doğrulanınca kullanıcı **doğrudan ana sayfaya** yönlendirilir: aynı kimlik
birden çok organizasyonda birer **`User`** kaydına sahip olabilir; **ilk tespit edilen** kullanıcının organizasyonu ile **org-kapsamlı (org-scoped) erişim
token'ı** üretilir ve **seçili organizasyon** o olur. Diğer organizasyonlar ana sayfada listelenir; kullanıcı **istediği zaman, yeniden OTP girmeden**
organizasyon değiştirir — token, seçilen organizasyon ve kullanıcı bilgisiyle **yeniden üretilir**. Kullanıcı yalnız **seçili organizasyonun** formlarını görür
ve orada işlem yapar. **Kayıt (register) ve
organizasyon oluşturma yoktur** — kullanıcılar ve organizasyonlar **Flovo tarafından** provizyon edilir. Kimlik doğrulama **Keycloak**'ta, yetki **Flovo**'da,
oturum **1 saatlik erişim token'ı + 30 günlük yenileme token'ı** ile sürer (→ `flovo-auth-mechanism.md`).

---

## 1. Kavramlar

| Kavram | Tanım | Nerede yaşar |
|---|---|---|
| **Kimlik (identity)** | Bir **kişiyi** tanımlayan giriş anahtarı: **normalize edilmiş e-posta** veya **telefon (E.164)**. **Organizasyon-üstüdür** (global). | Keycloak kullanıcı kaydı (`sub`) + Flovo `User.email`/`User.phone` (eşleme) |
| **Kullanıcı (`User`)** | Bir kimliğin **bir organizasyondaki** kaydı: kod, ad, departman, yönetici, yetki grupları… **Organizasyon-içidir.** | Flovo `User` (`organizationId` FK) |
| **Organizasyon** | Kiracı (tenant). Tüm iş verisi ve yetkiler organizasyona bağlıdır; DB'de **RLS** ile izole. | Flovo `Organization` |
| **Aktif organizasyon** | Kullanıcının **o an seçili** organizasyonu = token'daki `organizationId`. Tek seferde **yalnız bir** aktif organizasyon olur. | Erişim token'ı claim'i (+ FE durumu) |
| **Kimlik oturumu** | OTP ile açılan, **30 gün** süren oturum; bu süre içinde yeniden kod istenmez (yenileme token'ı ile sürer). | Keycloak SSO oturumu ↔ BFF oturumu |

**Kural (K-1):** *Aynı kişi = N `User`.* Bir kimlik her organizasyonda **en fazla bir** `User`'a bağlanır (`(organizationId, email)` / `(organizationId, phone)`
benzersiz → `user.md` §Benzersizlik). Farklı organizasyonlarda aynı e-posta/telefon **serbesttir**; login bunları **tek listede** birleştirir.

**Kural (K-2):** *Normalizasyon.* E-posta **küçük harf + trim**; telefon **E.164** (`+90…`). Aynı fonksiyon **hem provizyonda (yazım) hem login'de (arama)**
kullanılır; aksi hâlde organizasyonlar arası eşleşme kırılır. 🟦 VARSAYIM (K9): varsayılan ülke kodu organizasyona değil **platforma** aittir (`+90`).

---

## 2. Mimari sınır

```
[Tarayıcı/Mobil]  ──(1) kimlik + kod──▶  [Flovo BFF / API — auth uçları]  ──(2) OTP akışı / token isteği──▶  [Keycloak]
                                            │                                                     │
                                            │◀──(3) kimlik oturumu + token'lar (org-scoped JWT)────┘
                                            ▼
                                     [Go backend]  ── JWT doğrula → organizationId → RLS tenant GUC ──▶ [PostgreSQL]
```

- **authN = Keycloak.** Kimliği doğrular, oturumu tutar, JWT üretir (imza, süre, claim'ler). Şifre **yoktur**; doğrulama **OTP authenticator** ile.
  🟦 VARSAYIM (K3-a): OTP'yi Keycloak'taki **şifresiz authenticator (custom Authenticator SPI)** üretir/doğrular; e-posta/SMS gönderimi bu akışta.
- **authZ = Flovo.** "Bu kullanıcı bu organizasyonda bunu yapabilir mi?" her istekte Flovo'da çözülür (`permissions.md` `hasPermission()`); token yalnız
  **kim + hangi organizasyon** taşır. (Kaba rol ipuçları — ör. `orgAdmin` — FE için token'a konabilir; **otorite Flovo'dur**.)
- **BFF (Next.js route handler'ları).** Token'lar **tarayıcıya çıkmaz**; BFF, Keycloak ile konuşur, token'ları sunucu tarafında tutar, tarayıcıya yalnız
  **httpOnly oturum çerezi** verir ve backend'e `Authorization: Bearer` enjekte eder (pilotta canlı → `implementation-status.md`). Mobil istemci
  ileride token'ları **secure storage**'da tutar.
- **DB izolasyonu.** Token'daki `organizationId` → backend her istekte tenant GUC'unu set eder → **RLS Pattern B v2**. "Yalnız seçili organizasyon" (L7)
  böylece UI kuralı değil, **veritabanı kuralıdır**.

---

## 3. Login akışı (OTP → ana sayfa; ilk organizasyon otomatik)

### 3.1 Sıralı akış

```mermaid
sequenceDiagram
    autonumber
    participant U as Kullanıcı
    participant FE as Frontend
    participant BFF as Flovo BFF/API
    participant KC as Keycloak
    participant DB as Flovo DB
    U->>FE: e-posta veya telefon girer
    FE->>BFF: POST /auth/otp/request {identity}
    BFF->>BFF: normalize et (K-2)
    BFF->>DB: kimlik → aktif User kayıtları (tüm organizasyonlar)
    alt kullanıcı bulunamadı
        BFF-->>FE: 404 USER_NOT_FOUND ("kullanıcı bulunamadı") — kod gönderilmez
    else kullanıcı(lar) bulundu
        BFF->>KC: OTP akışını başlat (identity)
        KC-->>U: 6 haneli kod (e-posta / SMS)
        BFF-->>FE: 200 {requestId, channel, resendAfterSec}
    end
    U->>FE: kodu girer
    FE->>BFF: POST /auth/otp/verify {requestId, code}
    BFF->>KC: kodu doğrula → kimlik oturumu (30 gün) + yenileme token'ı
    BFF->>DB: kimliğe bağlı User/Organization listesi (sıralı)
    BFF->>KC: İLK organizasyon için org-scoped erişim token'ı
    KC-->>BFF: erişim token'ı (userId + organizationId)
    BFF-->>FE: giriş tamam → ANA SAYFA (aktif org = ilk; diğerleri listede)
    U->>FE: (istediği zaman) listeden başka organizasyon seçer — OTP yok
    FE->>BFF: POST /auth/select-organization {organizationCode}
    BFF->>KC: yeni org-scoped erişim token'ı (seçilen org + o org'daki User)
    BFF-->>FE: aktif organizasyon güncellendi
    FE->>BFF: iş istekleri (oturum çerezi)
    BFF->>DB: Authorization: Bearer <org-scoped JWT> → RLS
```

### 3.2 Adımlar (KARAR — kullanıcı, 2026-09-10)

1. **Login ekranı:** kullanıcı **e-posta veya telefon numarası** girer (tek alan; 🟦 K9: tür otomatik algılanır, normalize edilir).
2. **Kullanıcı tespiti:** kimlik, **tüm organizasyonlardaki** `User` kayıtlarında aranır (`email = :identity OR phone = :identity`, `active=true`, `deleted=false`,
   organizasyon aktif). **Tespit edilemezse** → **"kullanıcı bulunamadı"** hatası (`404 USER_NOT_FOUND`); **kod gönderilmez**. Kayıt yolu **yoktur** (L1).
3. **Kod gönderimi:** kullanıcı(lar) tespit edildiyse girilen kanala **6 haneli doğrulama kodu** gönderilir (politika → `flovo-auth-mechanism.md` §5).
4. **Kod doğrulama:** kullanıcı kodu doğru girer → Keycloak **kimlik oturumu** (30 gün) açılır.
5. **İlk organizasyon ile token:** tespit edilen kullanıcı listesinin **ilk** kaydının organizasyonu ile **bearer (erişim) token'ı** üretilir
   (`userId` + `organizationId` claim'leri); **seçili organizasyon** artık odur. **Organizasyon seçim ekranı yoktur.**
   *"İlk" sırası (KARAR L12):* **en eski kullanıcı kaydı** önceliklidir — `User.id` artan (oluşturma sırası). Cihaz-bazlı "son kullanılan organizasyon"
   hatırlaması **yoktur**. Sıra deterministiktir; kullanıcı ana sayfadan değiştirebilir.
6. **Ana sayfaya yönlendirme:** kullanıcı doğrudan **ana sayfaya** gider. Ana sayfada **aktif organizasyon** ve **diğer organizasyonlar** listelenir.
7. **Organizasyon değiştirme (OTP yok):** kullanıcı listeden başka organizasyonu seçer → **bearer token yeniden üretilir**; yeni token **seçilen organizasyonu ve
   o organizasyondaki kullanıcı bilgisini** taşır (→ §4).
8. **Token içeriği:** her bearer token **kullanıcı (`userId`) + organizasyon (`organizationId`)** bilgisini taşır; backend doğrulamayı **yalnız token'dan**
   yapar (imza + claim'ler → RLS; ek DB kontrolü yalnız aktiflik için, önbellekli) → `flovo-auth-mechanism.md` §2 · §4.

### 3.3 Kenar durumlar

| Durum | Davranış |
|---|---|
| Kimlik hiçbir org'da yok | **`404 USER_NOT_FOUND`** ("kullanıcı bulunamadı"); kod gönderilmez. Hız sınırı (kimlik + IP) numaralandırma denemelerini yavaşlatır (→ mekanizma §9). |
| Kimlik var ama tüm `User`'ları pasif/silinmiş | Aynı: "kullanıcı bulunamadı" (aktif kayıt yok). |
| Kimlik hem e-posta hem telefonla kayıtlı | İki kimlik anahtarı **aynı `User`**'a gider; hangisi girildiyse kod **o kanala** gider. |
| Aynı org'da biri e-postalı, biri telefonlu **iki ayrı** `User` aynı kişiye aitse | Modelde iki farklı kayıttır; login e-postayla girince yalnız e-postalı `User` bulunur. **Provizyon kuralı:** aynı kişi için tek `User`, ikisi de doldurulur. |
| Birden çok organizasyon | **En eski `User` kaydının** organizasyonu ile giriş (adım 5, L12); diğerleri ana sayfa listesinde; değiştirme OTP'siz (§4). |
| Kod yanlış / süresi doldu | Yeniden gönderim (bekleme süresi sonunda); deneme limiti dolunca geçici kilit (mekanizma §5). |
| Kod doğrulanırken tek kullanıcı pasifleştirildi (yarış) | Erişilebilir organizasyon kalmadıysa oturum kapatılır, "kullanıcı bulunamadı". |
| Aktif org'daki `User` sonradan pasifleştirildi | Sonraki istekte **403 `USER_INACTIVE`** → FE listeden erişilebilir bir organizasyona geçirir; hiç kalmadıysa logout. |
| Organizasyon pasifleştirildi | Listede görünmez; aktif org ise **403 `ORGANIZATION_INACTIVE`** → aynı davranış. |
| Cihaz/oturum 30 günü doldurdu | Yenileme başarısız → **tam yeniden giriş (OTP)**. |

---

## 4. Aktif organizasyon ve değiştirme

### 4.1 Kural (L6/L7)
- Kullanıcı her an **tam olarak bir** aktif organizasyona sahiptir; **yalnız onun** formlarını, listelerini, aksiyonlarını görür ve kullanır.
- Yetkiler (`permissions.md`), boşta kalma süresi (`Organization.idleTimeoutMinute`), görüntüleme profilleri **seçili organizasyonun** `User`'ı ve ayarlarıyla çözülür.
- Başka organizasyonda işlem = **önce değiştir**. Aynı tarayıcıda **iki organizasyon aynı anda** açık **değildir** (tek aktif token). 🟦 VARSAYIM: çok-sekme
  senaryosunda değişim tüm sekmelere yansır (BFF oturumu tek).

### 4.2 Değiştirme akışı (yeniden OTP yok; aktiflik doğrulamalı)
1. Ana sayfadaki **organizasyon listesi** (§4.3) → kullanıcı **istediği zaman** seçer.
2. FE → `POST /auth/select-organization {organizationCode}`.
3. **Aktiflik doğrulaması (KARAR L13):** BFF, kimliğin hedef organizasyondaki `User`'ının **hâlâ `active=true` ve `deleted=false`** olduğunu ve organizasyonun
   aktif olduğunu **DB'den** doğrular. Sağlanmıyorsa geçiş **yapılmaz** → `403 ORGANIZATION_NOT_ALLOWED`; FE organizasyon listesini **yeniler**, o organizasyon
   listeden **düşer**; kullanıcı mevcut organizasyonda kalır.
4. Doğrulama geçtiyse BFF, **kimlik oturumunu yeniden açtırmadan** (**OTP doğrulaması yok**) Keycloak'tan **yeni bearer token** alır; token **seçilen organizasyon +
   o organizasyondaki kullanıcı** bilgisini taşır; eski token BFF oturumundan **düşürülür** (mekanizma → `flovo-auth-mechanism.md` §3.3).
5. FE, uygulama durumunu **sıfırlar** (açık form, liste filtreleri, önbellek) ve yeni organizasyonun ana sayfasına gider.
6. **Denetim:** değişim `auditLog`'a düşer (kim · hangi org'dan hangi org'a · ne zaman) — 🟦 loglama Faz 2 (`todo-phase2.md` §3); MVP'de en az uygulama logu.

### 4.3 Organizasyon listesi (canlı; pasif/silinmiş düşer — KARAR L13)
- Liste her seferinde **DB'den canlı** hesaplanır: kimliğe bağlı `User` kayıtları içinden **`active=true` · `deleted=false` · organizasyonu aktif** olanlar;
  sıra = **en eski kayıt önce** (L12). Önbellek **yoktur**.
- Bir organizasyonda kullanıcı **pasife alınmış veya silinmişse** o organizasyon **listeden kaldırılır**; ana sayfa açılışında, `GET /auth/organizations`
  çağrısında ve başarısız bir geçişten (`ORGANIZATION_NOT_ALLOWED`) sonra liste yenilenir.
- **Aktif organizasyon** bu duruma düşerse sonraki istekte `403 USER_INACTIVE` → FE listeyi yeniler ve **listedeki ilk** (en eski) erişilebilir organizasyona geçer;
  hiç kalmadıysa **logout**.
- Cihaz-bazlı hatırlama **yoktur** (L12): her login **en eski kayıt** ile açılır.

---

## 5. Provisioning (kullanıcı ve organizasyonun sisteme dahil edilmesi)

- **Organizasyon:** yalnız **Flovo (platform)** açar — onboarding (L2). Açılışta **en az bir organizasyon admini** (`adminUserIds`) tanımlanır.
- **Kullanıcı:** self-servis kayıt **yoktur** (L1). Kullanıcı, **Settings API** organizasyon-ayarı kaynağıyla oluşturulur (`settings-api.md` §4 `/organization/users`).
  🟦 VARSAYIM (K2b): oluşturma yetkisi **Flovo (platform)** ve **organizasyon yöneticisi**nde (admin veya `organizationSettingsUserGroupId` üyesi); toplu senkron ⏭️ Faz 2.
- **Kimlik alanları zorunluluğu:** `email` veya `phone`'dan **en az biri** (CHECK) — aksi hâlde kullanıcı **giriş yapamaz**. Provizyon ekranı normalize eder (K-2).
- **Keycloak eşleme.** 🟦 VARSAYIM (K2-a): `User` oluşturulunca BFF/backend **Keycloak Admin API** ile kimliği **push** eder — kimlik (normalize e-posta/telefon)
  Keycloak'ta **yoksa oluşturulur**, **varsa** yeni `User` ona **bağlanır** (aynı kişi, yeni organizasyon). `User.externalSubject` = Keycloak `sub`
  (→ `user.md` güncellemesi, plan §5 Faz 2). Günlük **mutabakat (reconcile)** işi Flovo ↔ Keycloak sapmalarını kapatır.
- **Kimlik alanı değişirse** (`User.email`/`phone` güncellenir): aynı kişinin **diğer organizasyonlardaki** `User`'ları değişmez (org-içi kayıt) — Keycloak kimliği
  ise **kişiye** aittir; değişiklik Keycloak'a da yansıtılır ve **tüm** organizasyonlarda geçerli olur. 🟦 Bu iki davranış çelişir → **karar (K2c):**
  kimlik değişikliği yalnız **Flovo platform** yetkisinde ve **tüm `User`'larda birlikte** uygulanır (öneri).
- **Pasifleştirme / silme.** `User.active=false` → o organizasyonda giriş/işlem **durur**, diğer org'lar etkilenmez. Kimliğin **hiçbir** aktif `User`'ı
  kalmadıysa Keycloak oturumları **sonlandırılır** (kod da gönderilmez). `deleted=true` aynı; benzersizlik kontrolünden düşer (`user.md`).
- **Davet e-postası/SMS'i.** Kayıt olmadığından "davet linki" **yoktur**; kullanıcıya yalnız bilgilendirme ("Flovo'da hesabınız açıldı, e-posta/telefonunuzla giriş yapın") gönderilir — 🟦 opsiyonel, Bildirim altyapısıyla.

---

## 6. Oturum yaşam döngüsü (özet — ayrıntı kardeş dokümanda)

| Öğe | Süre / kural | Sahip |
|---|---|---|
| **Erişim token'ı (Bearer, JWT)** | **1 saat**; org-scoped; her istekte backend doğrular | Keycloak üretir, BFF taşır |
| **Yenileme token'ı** | **30 gün**; **rotasyonlu**; kimlik oturumunu sürdürür, yeni erişim token'ı üretir | Keycloak |
| **Kimlik oturumu** | 30 gün (yenileme token'ının penceresi); dolunca **OTP ile yeniden giriş** | Keycloak SSO oturumu |
| **Boşta kalma (`idleTimeoutMinute`)** | Seçili organizasyonun değeri; `0` = kapalı; dolunca **tam logout** (oturum sonlandırılır) | Flovo (FE + BFF) |
| **Logout** | BFF oturumu + Keycloak oturumu **birlikte** kapanır; yenileme token'ı iptal | BFF → Keycloak |

→ Mekanizma, claim şeması, hata sözleşmesi, güvenlik: [`flovo-auth-mechanism.md`](./flovo-auth-mechanism.md).

---

## 7. Auth uçları (BFF/API sözleşmesi — özet)

| Uç | Girdi | Çıktı | Not |
|---|---|---|---|
| `POST /auth/otp/request` | `{ identity }` | `200 { requestId, channel: "email"\|"sms", resendAfterSec }` · **`404 USER_NOT_FOUND`** | Kimlik hiçbir org'da aktif değilse **açık hata**, kod gönderilmez. Rate limit. |
| `POST /auth/otp/verify` | `{ requestId, code }` | `200 { active: { organizationCode, userId }, organizations: [{ code, definition, userId }] }` | Kimlik oturumu açılır (çerez); **ilk organizasyon** ile bearer token üretilir; FE ana sayfaya gider. |
| `GET /auth/organizations` | — | `{ active: code, organizations: […] }` | Ana sayfa listesi; **canlı** hesaplanır — pasif/silinmiş `User` ve pasif org **listede yok** (L13); sıra en eski kayıt önce (L12). |
| `POST /auth/select-organization` | `{ organizationCode }` | `{ user: {…}, organization: {…} }` · **`403 ORGANIZATION_NOT_ALLOWED`** | **OTP'siz** değiştirme; önce hedef `User` **aktiflik doğrulaması** (L13); geçtiyse bearer token yeniden üretilir, FE durumu sıfırlar; geçmediyse liste yenilenir. |
| `GET /auth/me` | — | `{ identity, user, organization, permissionsSummary }` | Aktif bağlam (token'dan). |
| `POST /auth/logout` | — | 204 | BFF + Keycloak oturumu kapanır. |
| *(BFF-içi)* yenileme | — | — | Kullanıcıya açık uç **değil**; BFF erişim token'ı dolmadan/401'de yeniler (mekanizma §3.2). |

> Request/response şemaları ve hata kodları → `flovo-auth-mechanism.md` §6. Sözleşme **Settings API ortak hata/sayfalama sözleşmesi** ile hizalanacak (`todo.md`).

---

## 8. Kapsam dışı / Faz 2 bağları

- **Impersonation** (yönetici bir kullanıcının yerine geçer) — yetki alanı var (`impersonationUserGroupId`); akış/audit ⏭️ [`todo-phase2.md`](../../todo-phase2.md) §1.
  **Vekalet** (`UserDelegate`, kullanıcının verdiği süreli yetki) ⏭️ §2. **Sınır:** impersonation = admin **geçici tam-taklit**; vekalet = **kullanıcı-verili** yetki;
  ikisi de token'a **ayrı claim** olarak düşecek (tasarım Faz 2).
- **Customer API / ApiKey** (dış sistem kimliği) ⏭️ §13; MVP'de `ApiKey` iskelet.
- **SSO / MFA / AD-LDAP federasyonu / sosyal login / QR ile giriş** — 🟦 (K7) MVP-sonrası.
- **Self-servis kayıt · organizasyon oluşturma · davet linki** — **yok** (L1/L2), planlanmıyor.

---

## 9. Varsayımlar ve açık kararlar (plan §6 eşlemesi)

| Etiket | Bu dokümandaki varsayım | Karar |
|---|---|---|
| K2 | Provisioning **push** (Admin API) + mutabakat; `User.externalSubject` | todo Login/Auth K2 |
| K2b | Kullanıcıyı Flovo **ve** org yöneticisi ekleyebilir | todo Login/Auth K2 |
| K2c | Kimlik değişikliği platform yetkisinde, tüm `User`'larda birlikte | **yeni** (bu doküman §5) |
| K3 | OTP = Keycloak şifresiz authenticator SPI | todo Login/Auth K3 |
| K4 | Org-scoped token mekanizması (Organizations scope ↔ mapper+nitelik) | todo Login/Auth K4 · mekanizma §3 |
| K7 | SSO/MFA/AD-LDAP/QR MVP-sonrası | todo Login/Auth K7 |
| K8 | OTP politikası (3 dk · 5 deneme · 60 sn · 5/saat) | todo Login/Auth K8 |
| K9 | Tek alan + otomatik algılama; E.164; varsayılan `+90` | todo Login/Auth K9 |
| ✅ L10 | Kullanıcı bulunamazsa **açık hata** "kullanıcı bulunamadı"; kod yok | karar L10 (karar; K10 kapandı) |
| ✅ L11 | OTP sonrası **seçim ekranı yok**: ilk tespit edilen organizasyonla token, ana sayfa; değiştirme OTP'siz | karar L11 (karar) |
| ✅ L12 | "İlk" = **en eski `User` kaydı** (`User.id` artan); cihaz hatırlaması yok | karar L12 (karar) |
| ✅ L13 | Geçişte hedef `User` **aktiflik doğrulaması**; pasif/silinmiş organizasyon **listeden düşer** | karar L13 (karar) |
| ✅ L9 | Erişim token'ı **1 saat**, yenileme token'ı **30 gün**, refresh mimarisi | karar L9 (karar) |

---

## 10. İlgili dosyalar

- [`flovo-auth-mechanism.md`](./flovo-auth-mechanism.md) — token/refresh/oturum mekanizması.
- [`../../todo.md`](../../todo.md) Tier 2 "Login / Auth" — açık kararlar (K2–K12) ve kalan model işleri.
- [`tech-stack/keycloak.md`](../../tech-stack/keycloak.md) · [`tech-stack/postgresql.md`](../../tech-stack/postgresql.md) — authN katmanı, RLS.
- [`organization-settings/permissions.md`](../../organization-settings/permissions.md) — authZ.
- [`models/organization-settings/user.md`](../../models/organization-settings/user.md) · [`organization.md`](../../models/organization-settings/organization.md).
- [`settings-api.md`](../api/settings-api.md) §4 — kullanıcı oluşturma ucu.

*Oluşturma: 2026-09-10 (v0.48). Güncelleme: aynı gün — kullanıcı düzeltmeleri: açık "kullanıcı bulunamadı" hatası · seçim ekranı yok, ilk organizasyon otomatik (L10/L11) · en eski kayıt önce, geçişte aktiflik doğrulaması, pasif/silinmiş org listeden düşer (L12/L13).*
