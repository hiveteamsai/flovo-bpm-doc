# Tech-Stack — Kullanılacak Teknolojiler (Tasarım/Kullanım) — İndeks

> **Amaç:** Flovo iBPM v2'de **kullanmayı hedeflediğimiz teknolojilerin** her biri için, projeye-özel **nasıl kullanılacağını**
> anlatan tasarım dokümanları. Her doküman: rol · sürüm · projemizde kullanım · konfigürasyon/desen · ilişkili tasarım · dikkat.
>
> **Bu klasör ≠ `research/tech-stack/`:** Buradaki dosyalar **kullanım/tasarım** (nasıl kullanıyoruz) anlatır; **karşılaştırma +
> hangi teknolojiyi neden seçtiğimiz** ise araştırma tarafındadır → [`../research/tech-stack/index.md`](../research/tech-stack/index.md)
> (özellikle katman-katman karar: [`../research/tech-stack/tech_rating.md`](../research/tech-stack/tech_rating.md)).

## Yığın özeti (bir bakışta)

**On-prem + Private Cloud ready** · vendor-agnostic · Türkiye Enterprise / KVKK.

```
Frontend   : TypeScript + Next.js 14 + React 18
API        : Protobuf (kaynak) → iç gRPC + dış grpc-gateway REST + OpenAPI codegen
Backend    : Go (chi + pgx/v5 + sqlc) · Hexagonal + Bounded Context + Partial Event Sourcing
Veri       : PostgreSQL 16 (JSONB source-of-truth + RLS) + PgBouncer · Redis (cache)
Mesajlaşma : NATS 2.10 + JetStream (event omurgası + realtime)
Kimlik     : Keycloak 25 (AD/LDAP + SPI)
Depolama   : MinIO (S3-uyumlu, bucket-per-tenant)
Çalıştırma : Docker Compose (dev) + Kubernetes (OpenShift + BYO, prod) + Helm
AI         : Python AI Service (🟡 post-MVP)
```

## Dokümanlar

### Çekirdek runtime
| Teknoloji | Rol | Doküman |
|---|---|---|
| **PostgreSQL** | Birincil DB & depolama substratı (JSONB source-of-truth, RLS, instance_attr projeksiyon) | [`postgresql.md`](./postgresql.md) |
| **Go** | Backend dili & çalışma zamanı (Hexagonal, generic projektör) | [`go.md`](./go.md) |
| **NATS + JetStream** | Mesajlaşma & **event/outbox omurgası** + realtime | [`nats-jetstream.md`](./nats-jetstream.md) |

### Frontend & API
| Teknoloji | Rol | Doküman |
|---|---|---|
| **TypeScript + Next.js** | Frontend (Form Designer, Dashboard, Notification, design system) | [`typescript-nextjs.md`](./typescript-nextjs.md) |
| **API Contract** | Hybrid — Protobuf kaynak + iç gRPC + dış REST/OpenAPI | [`api-contract.md`](./api-contract.md) |

### Kimlik & depolama
| Teknoloji | Rol | Doküman |
|---|---|---|
| **Keycloak** | Kimlik doğrulama & yetkilendirme (AD/LDAP + SPI → RLS) | [`keycloak.md`](./keycloak.md) |
| **MinIO** | Nesne depolama (binary/dosya, bucket-per-tenant, URL-in-JSONB) | [`minio.md`](./minio.md) |

### Altyapı & yardımcı
| Teknoloji | Rol | Doküman |
|---|---|---|
| **Kubernetes + Helm (+ Compose)** | Konteyner & orkestrasyon (on-prem, yatay ölçekleme) | [`kubernetes-helm.md`](./kubernetes-helm.md) |
| **Redis** | Cache & ephemeral (bildirim/session; kalıcı kuyruk **değil** — o NATS'ta) | [`redis.md`](./redis.md) |

### Post-MVP
| Teknoloji | Rol | Doküman |
|---|---|---|
| **Python AI Service** | 🟡 Post-MVP — RAG/semantic search (pgvector), fatura AI, process mining | [`python-ai-service.md`](./python-ai-service.md) |

## İlişkili tasarım

- **Depolama tasarımı bu yığına bağlı:** [`../research/property-value-storage/`](../research/property-value-storage/index.md)
  (JSONB source-of-truth = PostgreSQL · outbox→projektör omurgası = NATS + Go · binary = MinIO). `instance_attr` uygunluk
  değerlendirmesindeki **S2/D9 "NATS stack açık"** notu bu kararlarla **kapandı**.
- **Karar/karşılaştırma gerekçesi:** [`../research/tech-stack/tech_rating.md`](../research/tech-stack/tech_rating.md) (10 katman puanlama).
- **Mimari paradigma** (Hexagonal + Bounded Context + Partial Event Sourcing) ayrı bir "teknoloji" değil, `go.md` · `postgresql.md`
  (`workflow_events`) · `nats-jetstream.md` dokümanlarına **yayılmış** olarak yansır; tam analiz `../research/tech-stack/mimari-analiz.html`.
