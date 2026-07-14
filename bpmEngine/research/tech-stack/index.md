# Tech-Stack & Mimari Araştırması — İndeks

> **Amaç:** Yeni Flovo iBPM v2 motorunun oturduğu **teknoloji yığını ve mimari paradigma** kararlarını besleyen araştırma
> dokümanları. Üç konu-bazlı karşılaştırma analizi (**veritabanı · dil · mimari**) + bunları Flovo kararlarıyla birleştiren
> **konsolide yönetim raporu**.
>
> **Durum:** 🔵 **REFERANS — kararlar büyük ölçüde verildi/uygulandı** (kaynak: implementation ekibi; F-Infra + Sprint 2, 2026-06).
> Bu klasör *tasarım kararı üretmez*, verilmiş yığın kararlarını **kaydeder/referanslar**.
>
> **⚠️ Not (bu depo bir kod deposu değildir):** Bu HTML'ler dış implementation sürecinden gelen **karar/araştırma çıktılarıdır**;
> burada yalnızca **referans** olarak durur. Kod ayrı repoda geliştirilir (bkz. `../../../CLAUDE.md`).

## Dosyalar
| Dosya | İçerik (özet) |
|---|---|
| [`2026-06-30-tech-stack-mimari-konsolide-rapor.html`](./2026-06-30-tech-stack-mimari-konsolide-rapor.html) | **Konsolide yönetim raporu** (sunum, 15 slide). 3 insan-ekibi analizini (mimari/db/dil) + Flovo stratejik kararlarını + **12 ADR** + 10-katmanlı **tech-stack matrix** + Sprint 2 progress'i birleştirir. |
| [`db-analiz.html`](./db-analiz.html) | **Veritabanı karşılaştırması** — Postgres · MongoDB · MySQL · CockroachDB · SurrealDB · SQL Server. BPM DB gereksinimleri, uyum matrisi, skor (**Postgres 55/60 → #1**), Supabase (OSS bileşenler), maliyet. |
| [`dil-analiz.html`](./dil-analiz.html) | **Programlama dili karşılaştırması** — performans/RAM, Linux/Windows, **gRPC** desteği, **ORM**, "backend JS = FE uyumu" argümanının çürütülmesi, nihai sıralama. |
| [`mimari-analiz.html`](./mimari-analiz.html) | **Mimari yaklaşım analizi** — Modüler Monolit · Microservices · SOA/SCS · Event-Driven+Event Sourcing · Hexagonal · Serverless · Cell-based; karşılaştırma + yatay ölçekleme. |
| [`tech_rating.md`](./tech_rating.md) | **Teknoloji değerlendirme & karar** — 4 araştırmanın sonucu 10 katmanda **katman-katman puanlama + karar** (reddedilen alternatifler + gerekçe + güven) + konsolide karar tablosu + property-value-storage bağımlılık kesişimi. |

## Konsolide karar (özet)

Üç analiz + Flovo stratejik kararı (BO, 2026-06-29) şu yığında birleşti:

| Katman | Karar |
|---|---|
| **Backend dil** | **Go** (full rewrite) — chi router + pgx/v5 + sqlc |
| **Frontend** | **TypeScript + Next.js 14** + React 18 |
| **Veritabanı** | **PostgreSQL 16** (self-host, yalın) + PgBouncer 1.23 · RLS multi-tenancy · pgvector (post-MVP AI) |
| **Auth** | **Keycloak 25** (AD/LDAP + Custom Token Mapper SPI) — Supabase GoTrue yerine |
| **Storage** | **MinIO** (embed, S3-uyumlu, bucket-per-tenant) |
| **Realtime / mesajlaşma** | **NATS 2.10 + JetStream** — Azure Service Bus / Supabase Realtime yerine |
| **Container** | **Compose (dev) + K8s (prod, OpenShift + BYO)** — sadece Helm |
| **API contract** | **Hybrid:** Protobuf kaynak + grpc-gateway REST + OpenAPI codegen (iç gRPC, dış REST) |
| **Mimari** | **Hexagonal + Bounded context + Partial Event Sourcing (Workflow)** · MVP Core BPM monolith → **SOA-ready** |
| **Konumlandırma** | **On-prem + Private Cloud ready** (Türkiye Enterprise / KVKK) — Azure-first öneriler **reddedildi** |

> **Stratejik gerilim:** İnsan-ekibi analizleri **Azure-first** (Container Apps, Azure PostgreSQL, Service Bus) önerdi; Flovo
> **on-prem + vendor-agnostic** kararı verdi (~%30 ek ops eforu karşılığında müşterinin kendi cloud/on-prem'inde çalışma esnekliği).

## Property value depolama araştırmasıyla ilişki

Bu yığın kararları, komşu [`../property-value-storage/`](../property-value-storage/index.md) araştırmasının **varsaydığı stack'i
doğrular:** Postgres/JSONB · **NATS JetStream** · Go projektör · MinIO. Yani `form_attr_questions.md`'deki **S2/D9 "senkron altyapısı
(NATS) henüz commit edilmedi"** açık notu, bu kararlarla **kapanmış** görünür (NATS JetStream F-Infra'da canlı) — depolama tasarımı
karara bağlanırken bu teyit kullanılabilir.
