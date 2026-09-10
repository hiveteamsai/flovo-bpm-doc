# Login & Auth — Kimlik & Erişim (İndeks)

> **Amaç:** Kullanıcının sisteme **nasıl girdiği** (şifresiz OTP, çoklu-organizasyon) ve oturumun **nasıl sürdüğü** (1 saatlik erişim + 30 günlük refresh token).
> İşlevsel kararlar (L1–L13) **kesin**; teknik gerçekleştirme noktaları dokümanlarda **🟦 VARSAYIM** — kararlar → [`../../todo.md`](../../todo.md) Tier 2 "Login / Auth" (K2–K12).
> Teknoloji → [`../../tech-stack/keycloak.md`](../../tech-stack/keycloak.md) · yetki → [`../../organization-settings/permissions.md`](../../organization-settings/permissions.md) ·
> modeller → [`../../models/organization-settings/user.md`](../../models/organization-settings/user.md) · [`organization.md`](../../models/organization-settings/organization.md).

| Dosya | İçerik | Durum |
|---|---|---|
| [`flovo-identity-access.md`](./flovo-identity-access.md) | **Login akışı:** kavramlar (kimlik org-üstü ↔ `User` org-içi ↔ aktif organizasyon) · mimari sınır (authN Keycloak · authZ Flovo · BFF) · OTP akışı (sequence) · "kullanıcı bulunamadı" · ilk organizasyon otomatik · organizasyon değiştirme (OTP'siz, aktiflik doğrulamalı) · canlı organizasyon listesi · provisioning (kayıt yok) · auth uçları · Faz 2 bağları | 🟡 TASLAK v0.48 |
| [`flovo-auth-mechanism.md`](./flovo-auth-mechanism.md) | **Auth mekanizması:** token türleri/süreleri (erişim 1 saat · refresh 30 gün, rotasyon) · claim şeması (`userId` + `organizationId`) · yenileme · org değiştirme · logout/idle · backend doğrulama + RLS · OTP politikası · hata kodları · saklama (BFF) · Keycloak ayar özeti · güvenlik | 🟡 TASLAK v0.48 |

*Oluşturma: 2026-09-10 (v0.48).*
