# Flovo Auth Mekanizması — Token · Yenileme (Refresh) · Oturum

> **Durum:** 🟡 TASLAK (v0.48) — süreler ve refresh mimarisi **kesin** (v0.48 kararı L9); Keycloak-tarafı gerçekleştirme noktaları **🟦 VARSAYIM**
> (`todo.md` Login/Auth K3/K4/K8/K12). **Kararlar / açık noktalar:** [`todo.md`](../../todo.md) Tier 2 "Login / Auth" (K2–K12).
> **Kardeş doküman:** [`flovo-identity-access.md`](./flovo-identity-access.md) — login akışı, organizasyon seçimi, provisioning (bu doküman **mekanizmayı** anlatır).
> **Teknoloji:** [`tech-stack/keycloak.md`](../../tech-stack/keycloak.md) · [`tech-stack/postgresql.md`](../../tech-stack/postgresql.md) (RLS).

---

## 0. Özet (bir paragraf)

Oturum **iki token** ile sürer: **1 saatlik erişim token'ı** (Bearer JWT; her istekte gönderilir, **seçili organizasyonu** taşır) ve **30 günlük
yenileme token'ı** (opak; yalnız yeni erişim token'ı almak için, **her kullanımda döner/rotasyon**). OTP ile açılan **kimlik oturumu** 30 gün
sürer; bu pencere içinde kullanıcı yeniden kod girmez — erişim token'ı dolunca BFF sessizce yeniler. OTP doğrulanır doğrulanmaz **ilk tespit edilen
organizasyon** için token üretilir (seçim ekranı yok); **organizasyon değiştirmek** aynı kimlik oturumu üzerinden, **OTP'siz**, seçilen organizasyon + kullanıcı
bilgisiyle **yeni bir erişim token'ı** almaktır. Token'lar tarayıcıya **çıkmaz** (BFF tutar, httpOnly çerez). Backend her istekte imzayı
doğrular, token'daki `organizationId`'yi **RLS tenant GUC**'una yazar; yetki kararı **Flovo**'da verilir.

---

## 1. Token türleri ve süreler (KARAR L9)

| Token | Biçim | Süre | İçerik | Kullanım |
|---|---|---|---|---|
| **Erişim token'ı (access / Bearer)** | JWT (RS256), Keycloak imzalı | **1 saat** (`exp = iat + 3600`) | kimlik + **seçili organizasyon** + kullanıcı (§2) | Her API isteğinde `Authorization: Bearer …`; org-scoped |
| **Yenileme token'ı (refresh)** | opak / Keycloak refresh JWT (istemci okumaz) | **30 gün** | oturum referansı (`sid`) | Yalnız Keycloak token ucuna; yeni erişim (+ yeni yenileme) token'ı üretir; **rotasyonlu** |
| **Kimlik oturumu** | Keycloak SSO oturumu (`sid`) | **30 gün** | kimlik (`sub`), açılış zamanı, cihaz | Yenileme token'ının yaşam penceresi; dolunca OTP ile yeniden giriş |
| **OTP isteği** | sunucu-tarafı kayıt (`requestId`) | **3 dk** (🟦 K8) | kimlik, kanal, kod hash'i, deneme sayacı | Tek kullanımlık; §5 |

**Kurallar**
- **Erişim token'ı kısa (1 saat)** — sızsa bile etkisi sınırlı; sunucu-tarafı iptal listesi **tutulmaz** (JWT doğal süresinde ölür). Anında iptal gereken
  senaryolar (kullanıcı pasifleştirme) backend'deki **aktiflik kontrolü** ile karşılanır (§4.3).
- **Yenileme token'ı uzun (30 gün) ama tek-kullanımlık:** her yenilemede **yeni** yenileme token'ı verilir, eskisi geçersizleşir (rotasyon). Eski bir yenileme
  token'ının **tekrar** kullanılması = sızıntı sinyali → **oturum tümüyle kapatılır** (reuse detection).
- 🟦 **VARSAYIM (K12): 30 gün mutlak penceredir** (ilk OTP girişinden itibaren; yenileme süreyi **uzatmaz**). 30. günde kullanıcı **OTP ile yeniden giriş** yapar.
  Alternatif "kayan pencere" (her yenileme +30 gün) sürekli kullanan kullanıcının **hiç** yeniden doğrulanmaması demektir; şifresiz modelde önerilmez.
- **Offline token yok** (Keycloak offline_access kapalı). **Uzun ömürlü API anahtarları** ayrı mekanizmadır (⏭️ Customer API, `todo-phase2.md` §13).

---

## 2. Erişim token'ı claim şeması

```jsonc
{
  "iss": "https://auth.flovo.app/realms/flovo",
  "sub": "8f3c…-keycloak-identity-id",          // KİMLİK (kişi) — organizasyon-üstü
  "aud": "flovo-api",
  "azp": "flovo-web",                            // istemci (BFF); mobil: "flovo-mobile"
  "iat": 1757500000, "exp": 1757503600,          // 1 saat
  "jti": "…", "sid": "…",                        // token id · kimlik oturumu id
  "amr": ["otp"],                                // doğrulama yöntemi (şifre yok)
  "identity": { "channel": "email", "value": "a.b@example.com" },   // login'de kullanılan kimlik (normalize) — 🟦 opsiyonel

  "organizationId": 42,                          // SEÇİLİ organizasyon — RLS'in güven kökü (zorunlu)
  "organizationCode": "ACME",                    // dış referans (O6 kararına bağlı)
  "userId": 1078,                                // seçili organizasyondaki User.id (zorunlu)
  "userCode": "E-00123",
  "orgAdmin": false                              // FE ipucu; OTORİTE Flovo hasPermission() (permissions.md)
}
```

- **Zorunlu Flovo claim'leri:** `organizationId` · `userId`. Backend kimlik ve organizasyon bağlamını **yalnız token'dan** okur (L8) — bu iki claim olmadan
  token iş isteği için **geçersizdir** (`TOKEN_INVALID`). OTP doğrulanınca token **doğrudan ilk organizasyon** ile üretildiğinden org claim'siz bir "kimlik
  token'ı" istemciye **verilmez** (yalnız BFF içi ara durum).
- **Yetki listesi token'da taşınmaz.** Yetkiler organizasyonca **dinamik** yönetilir (`adminUserIds` + `*UserGroupId` grupları); token'a gömülse 1 saate kadar
  **bayat** kalır. Backend her istekte (veya kısa süreli önbellekle) çözer. `orgAdmin` yalnız UI ipucudur.
- **Claim'leri kim doldurur?** 🟦 (K4) Keycloak **Custom Token Mapper SPI** — seçili organizasyon bağlamını (a) **Keycloak Organizations** üyeliği/scope'undan
  veya (b) kimlik oturumuna yazılan **aktif-organizasyon niteliğinden** okur; `userId`'yi Flovo'dan (mapper → Flovo lookup ya da oturuma yazılmış nitelik) alır.
- **Mobil** istemci aynı şemayı alır; `azp` farklıdır.

---

## 3. Akışlar

### 3.1 İlk token alma (OTP sonrası — organizasyon seçimi yok)
1. OTP doğrulanır → Keycloak **kimlik oturumu** (30 gün) + **yenileme token'ı**.
2. BFF, kimliğe bağlı aktif `User` listesini alır (sıra: **en eski `User` kaydı önce** — L12); **ilk** kaydın organizasyonu için Keycloak'tan
   **org-scoped erişim token'ı** ister (🟦 K4 mekanizması) → BFF oturumuna yazar. Kullanıcı **ana sayfaya** gider; seçili organizasyon = ilk.
3. Tarayıcıya yalnız **httpOnly oturum çerezi**; token'lar BFF deposunda (§7).

### 3.2 Yenileme (refresh)
```
[BFF]  erişim token'ı dolmak üzere (exp − 5 dk)  ──▶  Keycloak /token  grant_type=refresh_token
                                                          │
                                       ◀── yeni erişim (1 saat) + YENİ yenileme token'ı (rotasyon) ──┘
       eski yenileme token'ı geçersiz; BFF oturumu güncellenir; istemci hiçbir şey fark etmez
```
- **Proaktif:** BFF, `exp − 5 dk` eşiğinde arka planda yeniler (istek sırasında gecikme yok).
- **Reaktif:** backend `401 TOKEN_EXPIRED` dönerse BFF **bir kez** yeniler ve isteği **tekrar** gönderir (tek-uçuşlu tekrar; idempotent olmayan istekler
  için `Idempotency-Key` → `engine-runtime-plan.md` Q17).
- **Eşzamanlılık:** Aynı oturum için yenileme **tekil** (mutex/single-flight); paralel istekler sonucu paylaşır — rotasyonda **çift yenileme = reuse** hatası doğurmasın.
- **Başarısız yenileme** (30 gün doldu · rotasyon ihlali · oturum kapatıldı · kullanıcı tüm org'larda pasif): BFF oturumu **siler** → FE **OTP ile yeniden giriş** ekranı
  (`SESSION_ENDED`).
- **Org bağlamı korunur:** yenilenen erişim token'ı **aynı organizasyon** claim'lerini taşır; organizasyon değişimi ayrı akıştır (§3.3).

### 3.3 Organizasyon değiştirme (yeni token, yeniden OTP doğrulaması yok)
1. FE → `POST /auth/select-organization {organizationCode}`.
2. **Aktiflik doğrulaması (KARAR L13):** BFF, kimliğin o organizasyondaki `User`'ının **hâlâ `active=true` ve `deleted=false`** olduğunu ve organizasyonun
   aktif olduğunu Flovo DB'de doğrular; sağlanmıyorsa geçiş **yapılmaz** → `403 ORGANIZATION_NOT_ALLOWED`, FE listeyi yeniler (organizasyon listeden düşer).
3. BFF, **mevcut kimlik oturumu** üzerinden Keycloak'tan **yeni org-scoped erişim token'ı** (+ yenileme token'ı) alır — 🟦 K4:
   **(a)** Keycloak Organizations: token isteğinde `scope=organization:<code>` → mapper `organizationId/userId` yazar ·
   **(b)** aktif-organizasyon niteliği güncellenir + yenileme → mapper yeni değeri yazar · **(c)** token exchange.
4. BFF oturumundaki **eski token çifti düşürülür**; FE durumu sıfırlar. Eski erişim token'ı (yalnız BFF'deydi) kullanılmaz; sızmış olsa bile ≤1 saat yaşar.
5. Kayıt: uygulama logu `auth.organization_switched` (kim · eski → yeni org · `sid`) — denetim izi ⏭️ Faz 2 (`todo-phase2.md` §3).

### 3.4 Logout
- FE → `POST /auth/logout` → BFF **Keycloak end-session/logout** çağırır (yenileme token'ı + kimlik oturumu **iptal**) → BFF oturumunu siler → çerez düşer.
- Erişim token'ı iptal edilmez; ≤1 saat içinde doğal ölür (BFF dışında kopyası yoktur).
- **Tüm cihazlardan çıkış** (kullanıcı/yönetici): Keycloak kimlik oturumlarının tümü sonlandırılır (Admin API) — pasifleştirme senaryosu §4.3.

### 3.5 Boşta kalma (`Organization.idleTimeoutMinute`)
- Seçili organizasyonun değeri; `0` = kapalı. FE etkinlik izler; süre dolunca **tam logout** (§3.4) — yalnız UI kilidi **değil** (v0.18/v0.33 kararı).
  Böylece 30 günlük yenileme penceresi, organizasyonun boşta kalma politikasını **aşamaz**.
- Organizasyon değişince sayaç **yeni organizasyonun** değeriyle yeniden başlar.

### 3.6 Oturum sonu (30 gün)
- Yenileme reddedilir → `SESSION_ENDED` → OTP ile yeniden giriş → **yeni** kimlik oturumu; giriş yine **en eski `User` kaydının** organizasyonuyla açılır (L12).

---

## 4. Backend doğrulama (her istekte)

### 4.1 Adımlar
1. `Authorization: Bearer` var mı → yoksa `401 TOKEN_MISSING`.
2. **İmza** (Keycloak JWKS, önbellekli; `kid` rotasyonu desteklenir) · `iss` · `aud` · `exp`/`nbf` (±60 sn tolerans) → aksi `401 TOKEN_INVALID` / `401 TOKEN_EXPIRED`.
3. **Flovo claim'leri:** `organizationId` + `userId` zorunlu → yoksa `401 TOKEN_INVALID` (iş isteği için geçersiz token).
4. **Tenant bağlamı:** aynı DB transaction'ında `SET LOCAL app.organization_id = <organizationId>` → **RLS Pattern B v2** (→ `tech-stack/postgresql.md`).
   Bu satır **her isteğin ilk işidir**; RLS'siz sorgu yolu yoktur.
5. **Kullanıcı bağlamı:** `userId`'nin **o organizasyona ait, `active=true`, `deleted=false`** olduğu doğrulanır (§4.3) → aksi `403 USER_INACTIVE`.
   Organizasyon pasifse `403 ORGANIZATION_INACTIVE`.
6. **Yetki:** istek gerektiriyorsa `hasPermission(userId, organizationId, …)` (`permissions.md`) → `403 FORBIDDEN`.

### 4.2 URL'deki organizasyon ile token'daki organizasyon
İstek yolunda/gövdesinde organizasyon belirten bir alan **varsa** token ile **eşleşmek zorundadır** (`403 ORGANIZATION_MISMATCH`). Tasarım kuralı: iş uçları
organizasyonu **token'dan** alır, **parametre olarak istemez** (L7'nin API karşılığı).

### 4.3 Aktiflik kontrolü ve önbellek
- `userId`/organizasyon aktiflik kontrolü her istekte **DB**'den (tek satır, PK) ya da **kısa TTL önbellekle** (≤60 sn) yapılır. Pasifleştirme en geç 60 sn içinde
  etkili olur; erişim token'ının 1 saatlik ömrünü **beklemez**.
- Kullanıcı **tüm** organizasyonlarda pasifleştirilirse: Keycloak kimlik oturumları **sonlandırılır** (Admin API) → yenileme de durur.

---

## 5. OTP politikası (🟦 VARSAYIM K8 — sayısal değerler karara açık)

| Kural | Değer | Not |
|---|---|---|
| Kod | **6 hane**, CSPRNG | Sabit uzunluk (L4). |
| Ömür | **3 dk** | Süre dolunca yeni istek gerekir. |
| Tek kullanım | evet | Doğru kod kullanıldığı an geçersiz. |
| Yanlış deneme | **5** → kimlik **15 dk** kilit | Deneme sayacı `requestId` + kimlik bazlı. |
| Yeniden gönderim | **60 sn** bekleme | `resendAfterSec` yanıtta döner. |
| Hız sınırı | **5 kod / saat / kimlik** + IP bazlı ek sınır | Aşımda `429 OTP_RATE_LIMITED`. |
| Saklama | kod **hash**'lenir; düz metin loglanmaz | Sunucu tarafı. |
| Kanal | girilen kimliğin kanalı (e-posta / SMS) | Sağlayıcı (SMS gateway · e-posta servisi) **tech-stack kararı** (🟦). |
| Mesaj | çok-dilli şablon ("Flovo giriş kodunuz: 123456 — 3 dk geçerli"); kullanıcının dili `User.language`? / istemci dili | Şablon Translation havuzundan (🟦). |
| Kullanıcı bulunamadı | kimlik hiçbir org'da aktif değilse kod **gönderilmez**, **açık hata** `404 USER_NOT_FOUND` ("kullanıcı bulunamadı") | ✅ L10 — numaralandırma riski kabul edildi; hız sınırı ile sınırlanır (§9) |

---

## 6. Hata sözleşmesi (auth)

| HTTP | Kod | Anlam | İstemci davranışı |
|---|---|---|---|
| 401 | `TOKEN_MISSING` | Bearer yok | Oturum ekranı |
| 401 | `TOKEN_INVALID` | İmza/iss/aud hatalı | Oturumu sil → OTP |
| 401 | `TOKEN_EXPIRED` | `exp` geçti | BFF yeniler ve **bir kez** tekrar dener |
| 401 | `SESSION_ENDED` | Yenileme reddedildi (30 gün · rotasyon ihlali · logout · pasif) | OTP ile yeniden giriş |
| 404 | `USER_NOT_FOUND` | OTP isteğinde kimlik hiçbir org'da aktif değil ("kullanıcı bulunamadı") | Mesajı göster; kayıt yolu yok |
| 403 | `ORGANIZATION_NOT_ALLOWED` | Geçiş isteğinde hedef `User` pasif/silinmiş veya org pasif (L13) | Listeyi yenile (org düşer); mevcut org'da kal |
| 403 | `ORGANIZATION_INACTIVE` / `USER_INACTIVE` | Org veya kullanıcı pasif | Listeye dön / giriş engeli |
| 403 | `ORGANIZATION_MISMATCH` | İstekteki org ≠ token org | İstek reddi (istemci hatası) |
| 403 | `FORBIDDEN` | Yetki yok (`hasPermission`) | UI'da gizle/engelle |
| 400 | `OTP_INVALID` / `OTP_EXPIRED` | Kod yanlış / süresi dolmuş | Tekrar dene / yeniden gönder |
| 423 | `OTP_LOCKED` | Deneme limiti | Süre sonunda tekrar |
| 429 | `OTP_RATE_LIMITED` | Hız sınırı | Bekle |

> Zarf biçimi (`{ code, message, details }`) **Settings API ortak hata sözleşmesi** ile aynı olacak (`todo.md` Settings API kalanlar); burada yalnız **kodlar** tanımlıdır.

---

## 7. Saklama ve taşıma

- **Web:** token'lar **BFF sunucu deposunda** (oturum id → {erişim, yenileme, org bağlamı}); tarayıcıda **httpOnly · Secure · SameSite=Lax** çerez. JS erişemez;
  `localStorage`/`sessionStorage`'da **asla** token yok. Durum-değiştiren isteklerde **CSRF** koruması (SameSite + istek başlığı). 🟦 Depo: Redis
  (tech-stack'te 🟡, pilotta kurulmadı) — pilotta sunucu-içi bellek/PG; yatay ölçekte Redis.
- **Mobil (ileride):** erişim + yenileme token'ı **secure storage** (Keychain / Keystore); aynı yenileme ve rotasyon kuralları istemcide uygulanır.
- **Taşıma:** yalnız TLS; `Authorization: Bearer` başlığı; token URL'de **taşınmaz**.

---

## 8. Keycloak yapılandırma özeti (🟦 K3/K4/K12 varsayımlarıyla)

| Ayar | Değer |
|---|---|
| Access Token Lifespan | **60 dk** |
| SSO Session Idle / Max | **30 gün / 30 gün** (mutlak pencere — K12) |
| Client Session Idle / Max | ≤ SSO değerleri (aynı) |
| Revoke Refresh Token / Max Reuse | **açık / 0** (rotasyon + reuse detection) |
| Offline Access | **kapalı** |
| Doğrulama akışı | **Şifresiz OTP authenticator** (custom Authenticator SPI; e-posta/SMS) — browser + direct-grant benzeri (BFF) varyantı (K3-a) |
| Token mapper | **Custom Token Mapper SPI** → `organizationId` · `organizationCode` · `userId` · `userCode` · `orgAdmin` (K4) |
| Organizasyon bağlamı | K4-a: **Keycloak Organizations** (26.x, `organization:<code>` scope) **veya** K4-b: kimlik oturumu niteliği "activeOrganization" |
| Kullanıcı kaynağı | Flovo `User` tablosu tek kaynak; Keycloak kimliği **push** ile (K2-a); AD/LDAP federasyonu ⏭️ MVP-sonrası (K7) |
| İstemciler | `flovo-web` (confidential, BFF) · `flovo-mobile` (public + PKCE, ileride) |

---

## 9. Güvenlik notları

- **Kullanıcı numaralandırma (enumeration):** "kullanıcı bulunamadı" açık hatası (L10) kimliğin kayıtlı olup olmadığını dışarı sızdırır — **bilinçli kabul**;
  kimlik + IP bazlı hız sınırı (§5) ve gecikme ile taramalar yavaşlatılır.
- **Şifre yok → OTP tek faktör.** Kod politikası (§5) ve hız sınırları **zorunlu**; kod SMS/e-posta ile taşındığından kanal güvenliği (SIM swap, e-posta ele
  geçirme) risk kabulüdür; MFA ⏭️ MVP-sonrası (K7).
- **Kısa erişim + rotasyonlu yenileme** → sızan erişim token'ı ≤1 saat; sızan yenileme token'ı ilk **çift kullanımda** tüm oturumu kapatır.
- **RLS güven kökü = token claim'i.** Mapper ve imza doğrulama kritik; claim'i **istemci** belirleyemez (org değişimi yalnız sunucu-tarafı akışla).
- **Denetim olayları:** `auth.otp_requested` · `auth.otp_failed` · `auth.login` · `auth.organization_switched` · `auth.refresh_reuse_detected` · `auth.logout` —
  MVP'de uygulama logu; denetim izi/saklama ⏭️ Faz 2 (`todo-phase2.md` §3).
- **Kişisel veri:** kimlik claim'i (`identity.value`) token'da opsiyoneldir; KVKK açısından `sub` + `userId` yeterliyse **konmaz** (🟦).

---

## 10. Varsayımlar ve açık kararlar (plan §6 eşlemesi)

| Etiket | Varsayım | Karar |
|---|---|---|
| ✅ L9 | Erişim 1 saat · yenileme 30 gün · refresh mimarisi, rotasyon | karar |
| 🟦 K12 | 30 gün **mutlak** pencere (kayan değil) | todo Login/Auth K12 |
| 🟦 K3 | OTP = Keycloak şifresiz authenticator SPI | todo Login/Auth K3 |
| 🟦 K4 | Org bağlamı: Organizations scope (a) ↔ aktif-org niteliği (b) ↔ token exchange (c) | todo Login/Auth K4 |
| 🟦 K8 | OTP sayısal politikası (§5) | todo Login/Auth K8 |
| ✅ L10 | "Kullanıcı bulunamadı" açık hatası, kod yok | karar L10 |
| ✅ L11 | OTP sonrası ilk organizasyonla token, seçim ekranı yok; değiştirme OTP'siz | karar L11 |
| ✅ L12 | İlk = en eski `User` kaydı; cihaz hatırlaması yok | karar L12 |
| ✅ L13 | Geçişte hedef `User` aktiflik doğrulaması; pasif/silinmiş org listeden düşer | karar L13 |
| 🟦 — | BFF oturum deposu (Redis ↔ PG/bellek) · `identity.value` claim'i konsun mu · SMS/e-posta sağlayıcısı | tech-stack |

---

## 11. İlgili dosyalar

- [`flovo-identity-access.md`](./flovo-identity-access.md) — login akışı, organizasyon seçimi, provisioning.
- [`../../todo.md`](../../todo.md) Tier 2 "Login / Auth" — açık kararlar (K2–K12) ve kalan model işleri.
- [`tech-stack/keycloak.md`](../../tech-stack/keycloak.md) · [`tech-stack/postgresql.md`](../../tech-stack/postgresql.md) · [`tech-stack/redis.md`](../../tech-stack/redis.md).
- [`organization-settings/permissions.md`](../../organization-settings/permissions.md) — `hasPermission()`.
- [`engine-runtime-plan.md`](../engine-runtime/engine-runtime-plan.md) Q17 — `Idempotency-Key`.

*Oluşturma: 2026-09-10 (v0.48). Güncelleme: aynı gün — L10/L11 düzeltmesi (açık hata · ilk organizasyon otomatik).*
