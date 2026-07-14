# Teknoloji Değerlendirme & Karar (Tech Rating)

> **Amaç:** Bu klasördeki araştırmaların ([`db-analiz.html`](./db-analiz.html) · [`dil-analiz.html`](./dil-analiz.html) ·
> [`mimari-analiz.html`](./mimari-analiz.html) · [`2026-06-30-tech-stack-mimari-konsolide-rapor.html`](./2026-06-30-tech-stack-mimari-konsolide-rapor.html))
> sonuçlarını **katman-katman** değerlendirip her katmanda **en uygun teknolojiye karar vermek** ve gerekçesini kaydetmek.
>
> **Bağlam / dürüstlük notu:** Bu kararların çoğu implementation ekibi tarafından **zaten verildi ve canlı** (F-Infra + Sprint 2,
> 2026-06). Bu doküman *sıfırdan yeniden seçmez*; araştırmayı **BPM-tasarım bağlamında değerlendirip teyit eder**, reddedilen
> alternatifleri gerekçesiyle kaydeder ve **tasarımın bağlı olduğu** noktaları ([`../property-value-storage/`](../property-value-storage/index.md))
> işaretler.

## Değerlendirme ölçeği

**Karar durumu:** ✅ Canlı (implementation'da uygulandı) · 🟢 Onaylandı (bu değerlendirme teyit ediyor) · 🟡 Koşullu / benchmark bekliyor
**Alternatif uygunluğu (katman içi):** ✅ uygun · ⚠️ kısmen · ❌ elendi
**Güven:** ⭐⭐⭐ yüksek · ⭐⭐ orta

---

## 1. Veritabanı → **PostgreSQL 16** ✅ ⭐⭐⭐

BPM'in DB'den beklediği kritik özellikler: **ACID** (workflow adım + form kaydı + bildirim = tek atomik işlem), **JSONB** (dinamik
form — her müşteri farklı şema), **RLS** (DB-seviyesi multi-tenancy), **append-only event store**, pgvector (AI), tsvector (arama).

| Aday | Skor (db-analiz /60) | Uygunluk | Neden |
|---|---|---|---|
| **PostgreSQL** | **55 🥇** | ✅ | JSONB+GIN · RLS · pgvector · 35+ yıl olgunluk · extension ekosistemi |
| MongoDB | 41 | ❌ | Cross-doc tx yavaş/karmaşık (BPM için sorun) · SSPL · RLS yok |
| CockroachDB | 33 | ❌ | Ölçek overkill · pgvector çalışmaz · BSL lisans |
| MySQL/MariaDB | 35 | ❌ | JSON index zayıf · RLS yok · vector yok |
| SQL Server | 30 | ❌ | Pahalı (lisans) · JSON PG'nin gerisinde · kapalı kaynak |
| SurrealDB | 26 | ❌ | 3 yaş, prod-ready değil · managed yok · tooling ilkel |

**Karar:** **PostgreSQL 16** (self-host, yalın) + **PgBouncer 1.23** (transaction mode) + **RLS Pattern B v2**.
**Kesişim:** property-value-storage'ın **JSONB source-of-truth + GIN + `form_attr` projeksiyonu** tam Postgres üstüne kurulu →
DB seçimi depolama tasarımının **ön koşulu** ve onunla **%100 uyumlu.** *(Not: `Supabase` bir DB değil, Postgres+servis paketi;
yalnız OSS bileşenleri değerlendirildi — auth/realtime için Keycloak/NATS tercih edildi, aşağıda.)*

## 2. Backend dil → **Go** ✅ ⭐⭐⭐ (AI için Python, post-MVP)

Kriterler: düşük RAM, 3-4x hız, **concurrency** (çok sayıda aktif workflow), **gRPC** first-class, ORM (sqlc/pgx).

| Aday | Uygunluk | Neden |
|---|---|---|
| **Go** | ✅ | En düşük RAM, yüksek concurrency, gRPC+Protobuf yerel, `chi`+`pgx/v5`+`sqlc` |
| C#/.NET (mevcut) | ⚠️ | Olgun ama rewrite hedefi + RAM/ops maliyeti |
| Node/TS | ❌ | "Backend JS = FE uyumu" argümanı **çürütüldü** (paylaşılan kod az; tip güvenliği OpenAPI/proto codegen ile dil-bağımsız; ağır perf bedeli) |
| Java | ⚠️ | Olgun ama RAM ağır |
| Python | ⚠️→✅(AI) | Genel BE için yavaş; **AI Service** için ideal (asyncpg + SQLAlchemy 2.0) |
| Rust | ⚠️ | Perf zirvesi ama geliştirme hızı/ekosistem maliyeti |

**Karar:** **Go full rewrite** (chi + pgx/v5 + sqlc). **Python AI Service** post-MVP (Sprint 5+). **Kesişim:** property-value-storage'ın
**generic projektör** (D9) Go'da yazılır — Go'nun concurrency'si projeksiyon throughput'u (P5) için avantaj.

## 3. Frontend → **TypeScript + Next.js 14 + React 18** ✅ ⭐⭐⭐

BPM Studio design system (teal palette #00796b, Manrope/Inter). Sprint 1'den canlı; Form Designer, Dashboard, Notification live.
**Karar:** TS + Next.js 14. Alternatif tartışması yok (endüstri standardı + design system hazır).

## 4. API Contract → **Hybrid: Protobuf kaynak + grpc-gateway REST + OpenAPI** ✅ ⭐⭐⭐

| Katman | Protokol | Gerekçe |
|---|---|---|
| İç (servisler arası) | **gRPC + Protobuf** | SOA-split-ready, 7-10x az bandwidth, compile-time tip |
| Dış (FE/3rd party/mobile) | **HTTP/JSON + OpenAPI** | REST ergonomisi, Swagger, kolay debug |
| FE client | **OpenAPI codegen TS** | Contract drift sıfır |
| Kaynak-hakikat | **Protobuf `.proto`** | Tek kaynak, tüm istemciler türetilir |

**Karar:** Hybrid (ADR-012). **Kesişim:** dış API property-value-storage §9 (custom-code `/schema`, search) ile uyumlu; `Property.code`
immutable kuralı (S12) dış API kararlılığı için burada da geçerli.

## 5. Auth → **Keycloak 25** ✅ ⭐⭐⭐

| Aday | Uygunluk | Neden |
|---|---|---|
| **Keycloak** | ✅ | **AD/LDAP** entegrasyonu (Türkiye Enterprise zorunlu) · SSO/SAML · mature · self-host · Custom Token Mapper SPI |
| Supabase GoTrue | ❌ | Daha az mature; AD/LDAP zayıf |
| Custom auth | ❌ | 2-3 hafta + güvenlik riski |
| Azure AD / Auth0 | ❌ | Vendor lock-in (on-prem hedefine aykırı) |

**Karar:** Keycloak 25 + AD/LDAP + SPI (F-Infra canlı).

## 6. Dosya Depolama → **MinIO** ✅ ⭐⭐⭐

Kriter: **on-prem**, S3-uyumlu, bucket-per-tenant, KMS, self-host. **Reddedilen:** Azure Blob (vendor), Supabase Storage (cross-cloud).
**Karar:** MinIO (embed). **Kesişim:** property-value-storage **binary/dosya (D8)** = MinIO'da; JSONB'de yalnız URL → "yavaş belge"
sorununu çözer ve JSONB'yi küçük tutar (S9).

## 7. Realtime / Mesajlaşma → **NATS 2.10 + JetStream** ✅ ⭐⭐⭐ *(depolama omurgası)*

| Aday | Uygunluk | Neden |
|---|---|---|
| **NATS + JetStream** | ✅ | Kalıcı stream (replay), durable consumer, idempotent (Nats-Msg-Id), CNCF/açık, hafif, on-prem |
| Azure Service Bus | ❌ | Vendor lock-in |
| Kafka | ⚠️ | Güçlü ama ops ağır (bu ölçekte fazla) |
| Supabase Realtime | ❌ | Elixir ölçek tuning + cross-cloud latency |
| Redis pub/sub | ⚠️ | Kalıcılık zayıf (kuyruk için değil; **cache** olarak ayrıca kullanılıyor) |

**Karar:** NATS JetStream (F-Infra canlı; FLOVO_EVENTS stream, `flovo.{aggregate}.{verb}.{version}`).
**🔗 Kritik kesişim:** property-value-storage'ın **Outbox → kuyruk → idempotent projektör** omurgası (D9) tam NATS JetStream üstüne
oturur → **`form_attr_questions.md`'deki S2/D9 "senkron altyapısı (NATS) henüz commit edilmedi" açık notu KAPANIR.** Depolama
tasarımı karara bağlanırken NATS teyit edilmiş sayılır.

## 8. Container / Orkestrasyon → **Compose (dev) + K8s (OpenShift + BYO), Helm** ✅ ⭐⭐⭐

Kriter: on-prem + Private Cloud, vendor-agnostic, **stateful BPM** (serverless'a aykırı). **Reddedilen:** Azure Container Apps
(vendor + serverless), Azure Functions. **Karar:** Compose dev + K8s prod, tek Helm umbrella chart.

## 9. Mimari Paradigma → **Hexagonal + Bounded Context + Partial Event Sourcing; MVP monolith → SOA-ready** ✅ ⭐⭐⭐

| Yaklaşım (mimari-analiz) | Uygunluk | Not |
|---|---|---|
| Modüler Monolit (MVP çekirdek) | ✅ | Premature split overhead'den kaçınır; saga/distributed tx pahalı |
| **Hexagonal (Ports & Adapters)** | ✅ | `domain/` saf + `adapter/{http,grpc,db,nats}` → future split ~5x ucuz |
| **Partial Event Sourcing (Workflow)** | ✅ | `workflow_events` append-only + projection + replay + optimistic lock |
| Bounded context isolation | ✅ | Table prefix + Go package separation |
| Full Microservices | ❌ | MVP'de erken; distributed tx maliyeti |
| Serverless-first | ❌ | Stateful BPM'e aykırı |
| Cell-based | ⚠️ | Post-MVP ölçekte değerlendirilir |

**Karar:** MVP **Core BPM monolith** + Hexagonal + Partial Event Sourcing + Bounded context → Sprint 6+ SOA split (AI/Workers ayrı).
**Kesişim:** Partial Event Sourcing (`workflow_events`) ile property-value-storage'ın **CQRS projection + outbox** deseni **aynı
aileden** — mimari tutarlı, ikisi de "append-only kaynak + türetilmiş projeksiyon + replay" ilkesini paylaşır.

## 10. Konumlandırma → **On-prem + Private Cloud ready** ✅ ⭐⭐⭐ *(stratejik)*

**Gerilim:** İnsan-ekibi analizleri **Azure-first** (Container Apps, Azure PostgreSQL, Service Bus) önerdi; BO (2026-06-29)
**on-prem + vendor-agnostic** kararı verdi. **Maliyet:** ~%30 ek ops eforu (Helm+K8s+monitoring kendi yığınımızda). **Kazanç:**
Türkiye Enterprise pilot (KVKK + müşteri kendi data-center'ı), satış kanalı açık, vendor lock-in yok. **Karar:** on-prem + Private
Cloud ready (BO direktifi).

## Ek katmanlar

| Katman | Karar | Durum | Not |
|---|---|---|---|
| Connection pool | **PgBouncer 1.23** (transaction mode) | ✅ | 10K+ bağlantı |
| Cache | **Redis** | ✅ | Notification BE'de (S2.8); ephemeral/cache — kuyruk için NATS |
| Full-text search | **Postgres tsvector** + gerekirse **Meilisearch** / uç ölçek **Elasticsearch** (yalnız okuma projeksiyonu) | 🟢 | property-value-storage S6 "uç ölçek full-text → ES read-side" ile uyumlu |
| Vector / AI | **pgvector** (aynı DB) | 🟡 post-MVP | Ayrı vector DB gereksiz |
| Migration | ADR-003 apply CI workflow | ✅ | |

---

## Konsolide karar tablosu (final)

| Katman | Karar | Durum | Güven |
|---|---|---|---|
| Veritabanı | PostgreSQL 16 (self-host) + PgBouncer + RLS | ✅ | ⭐⭐⭐ |
| Backend dil | Go (+ Python AI post-MVP) | ✅ | ⭐⭐⭐ |
| Frontend | TypeScript + Next.js 14 + React 18 | ✅ | ⭐⭐⭐ |
| API contract | Hybrid (Protobuf + grpc-gateway REST + OpenAPI) | ✅ | ⭐⭐⭐ |
| Auth | Keycloak 25 (AD/LDAP + SPI) | ✅ | ⭐⭐⭐ |
| Dosya storage | MinIO (embed, S3-uyumlu) | ✅ | ⭐⭐⭐ |
| Realtime/mesajlaşma | NATS 2.10 + JetStream | ✅ | ⭐⭐⭐ |
| Container | Compose + K8s (OpenShift/BYO) + Helm | ✅ | ⭐⭐⭐ |
| Mimari | Hexagonal + Bounded Context + Partial ES; monolith→SOA-ready | ✅ | ⭐⭐⭐ |
| Konumlandırma | On-prem + Private Cloud ready | ✅ | ⭐⭐⭐ |
| Cache · Search · Vector | Redis · tsvector(+Meili/ES) · pgvector | ✅/🟡 | ⭐⭐ |

## Property-value-storage tasarımının bağlı olduğu teknoloji kararları

| Depolama ihtiyacı (S#/D#) | Bağlı olduğu karar | Durum |
|---|---|---|
| JSONB source-of-truth + `form_attr` projeksiyon (S1-S13) | **PostgreSQL** | ✅ karşılanıyor |
| Outbox → kuyruk → idempotent projektör (D9) | **NATS JetStream** | ✅ **S2/D9 açık notu kapandı** |
| Generic projektör (D9) | **Go** | ✅ |
| Binary/dosya URL-in-JSONB (D8) | **MinIO** | ✅ |
| Incremental rollup / materialized (D6) | Postgres (MV / rollup tablo) | ✅ substrat hazır |
| Translation-aware sorgu (D7) | Postgres join / read-model | ✅ substrat hazır |
| Append-only mantığı (event sourcing ailesi) | Partial Event Sourcing mimarisi | ✅ tutarlı |

## Açık / doğrulanacak noktalar

1. **Bunlar STACK kararı; DESIGN değil.** property-value-storage'ın D-listesi (rollup D6, translation katmanı D7, status kolonu D3,
   reflection mekanizması D4) **stack üstünde kurulacak tasarım bileşenleri** — stack onları destekliyor ama ayrıca tasarlanmalı.
2. **Benchmark kapısı (property-value-storage):** stack seçildi; ama 5M/200M ölçekli **p95 spike planı** (P1–P9) kendi donanımımızda
   doğrulanmadan depolama tasarımı "onaylandı" sayılmaz.
3. **Redis rolü netleştirilmeli:** cache/ephemeral (bildirim) için; kuyruk/kalıcılık **NATS**'ta — çakışma yok ama sınır belgelenmeli.

## Nihai hüküm

Araştırmalar **güçlü ve iç tutarlı**; kararlar BPM gereksinimleriyle (**ACID + dinamik JSONB + RLS + on-prem**) ve komşu
property-value-storage tasarımıyla **%100 hizalı.** Bu değerlendirme, verilen 10 katman kararını **teyit eder** ve tek gerçek
"bedel"in bilinçli olduğunu doğrular: **on-prem tercihinin ~%30 ek ops eforu** (karşılığında Türkiye Enterprise pazarı + vendor
bağımsızlık). **Tek cümle:** *Go · PostgreSQL · Keycloak · MinIO · NATS JetStream · K8s/Helm · Hexagonal + Partial Event Sourcing,
on-prem ready — kabul edilir ve property-value-storage tasarımının ön koşullarını karşılar.*

---

*İlgili: [`index.md`](./index.md) (araştırma özeti) · [`../property-value-storage/`](../property-value-storage/index.md) (depolama tasarımı — bu stack'e bağlı).*
