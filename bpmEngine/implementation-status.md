# Uygulama Durumu (Implementation Status) — Bölüm-1 (Tasarım-Zamanı)

> **Durum tarihi:** 2026-08-31 · **Kaynak:** uygulama reposu `hiveteamsai/flovo-ibpm-v2` (pilot, canlı doğrulandı).
> **Amaç:** Bu doküman, **tasarım** (bu repo) ile **fiilen inşa edilip dağıtılan** arasındaki farkı **tek yerde** tutar.
> Tech-stack dokümanlarındaki teknoloji-bazlı "canlı" işaretleri buradaki gerçeğe göre okunmalıdır.

Bu depo Flovo iBPM v2'nin **tasarım/analiz SSOT**'udur; aşağıdaki "inşa edildi/dağıtıldı" ifadeleri uygulama
reposundan (`flovo-ibpm-v2`) türetilmiştir. Pilot kapsamı **Bölüm-1 = tasarım-zamanı** (süreç/servis tanımlama);
**runtime Motor** (`engine-runtime.md`) tasarlandı ancak **henüz inşa edilmedi.**

## ✅ İnşa edildi (Bölüm-1 = tasarım-zamanı)
- **Settings-API çatısı** (design-time CRUD) — `settings-api.md` yüzeyi + `SettingsValidator` registry.
- **Service CRUD + minimal Solutions** (create/list). **Sadeleştirme: Process ≡ Service (1:1)** — pilot varsayımı.
- **Property CRUD** (18 propertyType) + tipe-özel `settings` şema doğrulama + **Property Designer**.
- **ViewProfile CRUD + Property-Matrix + View-Profile Designer**.
- **Draft/Publish/Versiyonlama:** `service_version` tablosu · `current_version` · `has_unpublished_changes` ·
  `last_published_at` · code-lock (published'da kod değişmez).
- **Süreç Arşivleme:** `services.archived_at` / `archived_by` + **ArchivedChecker** (read-only, cross-domain guard;
  property/view-profile/service/publish yazma-yolları arşivli-parent'ta `FailedPrecondition`) + Archive/Unarchive RPC +
  `archive_filter` (active/archived/all). Soft + geri-alınabilir.
- **Design-IA yerleşimi:** Süreçler → süreç-kartı → **"Form Tasarımcı"** sekmeli
  [Alanlar | Görüntüleme Profilleri | Yayınla]. Standalone tasarımcı menüleri kaldırıldı.

## 🟢 Dağıtıldı — pilot (canlı doğrulandı)
- **BE:** Go (chi + grpc-gateway + gRPC + pgx/v5) — **Azure Container Apps**
  (uygulama `ca-flovo-ibpm-be`, kaynak-grubu `rg-flovo-pg-pilot`, imaj `flovoibpmacr.azurecr.io/flovo-api`).
- **FE:** Next.js / TypeScript — **Vercel** (`flovo-ibpm-fe-pilot`); BFF route-handler'lar bearer'ı
  **sunucu-tarafında** enjekte eder (secret istemciye çıkmaz).
- **DB:** **Azure PostgreSQL** (yönetilen, plain PG) — GUC-native RLS **"Pattern-B v2"**
  (`active_tenant_id()`, **branch-siz** → human + agent parity by-construction).
- **Kimlik:** **Keycloak** OIDC (`Authorization: Bearer`; token → tenant GUC → RLS).

## 🟡 Henüz dağıtılmadı (yalnız tasarım hedefi)
- **NATS JetStream · MinIO · Redis · Kubernetes/Helm (OpenShift) · PgBouncer** — pilotta **kurulmadı**.
- **Runtime "Motor"** (`engine-runtime.md` event-driven state machine + `workflow_events` event-sourcing) —
  **tasarlandı, inşa edilmedi.**
- **AI / Python servisi** — post-MVP.

## ⚠️ Tasarım ↔ pilot gerilimi (bilinen, bilinçli)
Tasarım **on-prem / K8s** (uzun-yaşayan stateful Motor için) hedefler; **pilot Azure-hosted**
(Container Apps + Vercel + Azure-PG). Bu, hız için alınan **bilinçli bir pilot-dağıtım kararıdır** ve üretim
hedefiyle çelişmez — pilot kapsamı **design-time**'dır (Motor runtime henüz yok, dolayısıyla stateful-K8s ihtiyacı
henüz doğmadı). `tech-stack/kubernetes-helm.md`'deki "serverless reddedildi" notu bu ayrımla okunmalıdır: reddedilen
şey **üretim runtime'ının** serverless olması; **pilot design-time**'ın Container Apps'te koşması ayrı bir karardır.

> **Sonraki:** Motor runtime fazı başladığında (NATS/MinIO/Redis + stateful worker), üretim dağıtımı bu dokümanda
> "🟢 Dağıtıldı"ya taşınır ve K8s/Helm hedefi yeniden değerlendirilir.
