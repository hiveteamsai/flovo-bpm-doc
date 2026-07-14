# Keycloak — Kimlik Doğrulama & Yetkilendirme (Flovo iBPM v2)

> **Rol:** Merkezi kimlik doğrulama (authentication) ve token üretimi; kurumsal dizinlerle (AD/LDAP) federasyon ve tenant kimliğini taşıyan JWT'yi üretir.
> **Karar:** Keycloak **25** · ✅ canlı (F-Infra SI.3) · tam gerekçe/karşılaştırma → [`../research/tech-stack/tech_rating.md`](../research/tech-stack/tech_rating.md)

## Ne için kullanıyoruz?

Flovo bir **çok-kiracılı (multi-tenant) kurumsal** BPM platformu; müşteriler kendi kullanıcılarını genelde **kendi Active Directory / LDAP** sistemlerinde yönetir. Keycloak bu noktada:

- Kullanıcı **login/logout, token refresh, oturum yönetimi**ni sağlar — bu altyapıyı sıfırdan yazmayız.
- Müşterinin **kurumsal dizinine (AD/LDAP) federasyon** ile bağlanır; kullanıcılar mevcut kurumsal hesaplarıyla girer (Türkiye Enterprise satışında **zorunlu** bir gereksinim).
- Ürettiği **JWT**'ye Flovo'ya özgü claim'leri (özellikle `organizationId`) gömerek, tüm backend ve DB katmanının **tenant izolasyonunu** bu tek kaynaktan almasını sağlar.

## Sürüm & bileşenler

- **Keycloak 25** (self-host, on-prem uyumlu).
- **AD/LDAP User Federation** — kurumsal dizin entegrasyonu.
- **Custom Token Mapper SPI** — Flovo'nun yazdığı, JWT'ye tenant/rol claim'i ekleyen eklenti (Java SPI).
- Protokoller: **OpenID Connect (OAuth2) + SAML + JWT**; SSO.

## Projemizde kullanım

- **Kimlik akışı:** FE (Next.js) → Keycloak OIDC login → access token (JWT). FE bu token'ı Flovo API'ye taşır; Go backend token'ı doğrular.
- **Tenant kimliği token'da:** Custom Token Mapper SPI, JWT'ye **`organizationId`** ve **rol/yetki claim'leri** ekler. Böylece "kullanıcı hangi organizasyona ait" bilgisi her istekte token'dan gelir — ayrı sorgu gerekmez.
- **DB tenant izolasyonuyla bağ (kritik):** Token'daki `organizationId`, PostgreSQL **RLS Pattern B**'yi besler — backend, oturum değişkenine (`SET app.organization_id`) token'daki değeri yazar; DB satır bazında yalnız o organizasyonun verisini döndürür. Detay → [`./postgresql.md`](./postgresql.md).
- **Yetkilendirme:** Kimlik-doğrulama Keycloak'ta; ancak **iş yetkileri organizasyon bazında** Flovo tarafında yönetilir (bkz. `organization.md` — `User.authorizationLevel` kaldırıldı, yetkiler Organization'da). Keycloak rolleri kaba erişim (ör. admin/user), ince yetki Flovo modeli.

## Konfigürasyon / desen notları

- **Realm stratejisi:** kimlik federasyonu müşteri dizinine bağlı; tenant ayrımı JWT `organizationId` claim'i + Flovo RLS ile sağlanır (realm-per-tenant zorunlu değil).
- **Custom Token Mapper SPI** Flovo'ya özel; claim şeması Flovo `User` ↔ `Organization` eşlemesini yansıtır.
- **AD/LDAP:** read-only federasyon önerilir (kullanıcı kaynağı müşteride kalır); Flovo tarafında yalnız uygulama-içi profil/yetki tutulur.
- **Kerberos SSO** post-MVP (Sprint 6+) yol haritasında.

## İlişkili tasarım

- [`./postgresql.md`](./postgresql.md) — JWT `organizationId` → RLS Pattern B tenant izolasyonu.
- [`../models/organization-settings/user.md`](../models/organization-settings/user.md) — kullanıcı modeli; organizasyon bağlantıları.
- [`../models/organization-settings/organization.md`](../models/organization-settings/organization.md) — yetkiler organizasyon bazında.
- [`../research/tech-stack/tech_rating.md`](../research/tech-stack/tech_rating.md) — auth katmanı kararı (Keycloak vs GoTrue/custom/Azure AD).

## Dikkat / açık noktalar

- **AD/LDAP eşleme** her müşteride farklı olabilir; kullanıcı-provisioning ve `organizationId` atama akışı müşteri onboarding'inde netleştirilmeli.
- **Token'daki `organizationId`** RLS'in güven kökü — token doğrulama ve claim bütünlüğü kritik (imza doğrulama, kısa TTL + refresh).
- Custom Token Mapper SPI, Keycloak sürüm yükseltmelerinde **uyum testi** gerektirir (SPI API'si sürüm bağımlı).
