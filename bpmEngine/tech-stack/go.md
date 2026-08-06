# Go — Backend Dili & Çalışma Zamanı (Flovo iBPM v2)

> **Rol:** Tüm çekirdek BPM motorunu (workflow yürütme, form/servis yönetimi, iş kuralları, projeksiyon üretimi) çalıştıran backend dili.
> **Karar:** Go 1.22+ · ✅ canlı (full rewrite, F-Infra) · tam gerekçe/karşılaştırma → [`../research/tech-stack/tech_rating.md`](../research/tech-stack/tech_rating.md)

## Ne için kullanıyoruz?

Flovo iBPM v2'nin **backend'inin tamamı Go** ile yazılır (eski yığından full rewrite). Go, üç nedenle çekirdek dilimizdir:

- **Yüksek eşzamanlılık (goroutine):** aynı anda binlerce aktif workflow instance'ı + arka planda çalışan projeksiyon tüketicileri düşük RAM ile taşınır.
- **Düşük gecikme + düşük bellek:** BPM motoru sürekli çalışan (stateful) bir servis; Go'nun düşük ayak izi on-prem/K8s dağıtımında maliyeti düşürür.
- **gRPC + Protobuf yerel desteği:** servisler arası iletişim ve SOA-ready ayrışma için birinci sınıf.

## Sürüm & bileşenler

| Bileşen | Seçim | Görev |
|---|---|---|
| Dil | **Go 1.22+** | Backend çalışma zamanı |
| HTTP router | **chi** | Dış REST (grpc-gateway ile birlikte) |
| DB sürücü | **pgx/v5** (+ `pgxpool`) | PostgreSQL erişimi, connection pool |
| Sorgu katmanı | **sqlc** | Tip-güvenli, derleme-zamanı SQL → Go kodu |
| RPC | **google.golang.org/grpc** + Protobuf | Servisler arası + iç API |

## Projemizde kullanım

**Hexagonal (Ports & Adapters) mimari** — kod tabanı iş mantığını altyapıdan ayırır:

```
internal/
  domain/                     # SAF iş mantığı (framework-free, test edilebilir)
    workflow/  forms/  auth/  notify/    # bounded context'ler
  adapter/                    # dış dünya bağlantıları (portların implementasyonu)
    http/  grpc/  db/  storage/  nats/
```

- **`internal/domain/`** çerçeveye bağımsızdır; Postgres, NATS, HTTP burada geçmez → future SOA split ~5x ucuzlar.
- **Bounded context isolation:** her alan (workflow/forms/auth/notify) hem Go paketi hem tablo öneki (`workflow_*`, `forms_*` …) ile ayrılır.
- **gRPC servisleri:** workflow/form/auth/notify için iç RPC; dışa `grpc-gateway` ile REST (bkz. `api-contract.md`).

**property-value-storage bağı — Go'nun kritik rolü:** Değer saklama mimarisinin senkron omurgası Go'da çalışır:

```
instance_value UPDATE + instance_value_outbox  →  NATS JetStream  →  [Go idempotent generic projektör]  →  instance_attr / instance_list_item
```

- **Generic projektör (D9):** tek Go tüketici tüm servisleri besler; alan adı koda gömülü değil, metadata'dan okunur (property-value-storage S11/D9). Goroutine havuzuyla **yatay ölçeklenir** → projection lag (P5) ve 5M/200M ölçekli reproject yükü Go'nun eşzamanlılığıyla karşılanır.
- **Idempotency:** projektör olayın `version`'ını karşılaştırır (S2); duplicate/retry/restart veriyi bozamaz.
- **Bulk rebuild job (D10):** aynı projektör kodu partition-partition backfill'de de kullanılır (tek mantık kopyası).

## Konfigürasyon / desen notları

- **`sqlc` derleme-zamanı SQL:** dinamik SQL yerine tip-güvenli üretilmiş sorgular; `instance_attr`/`instance_list_item` projeksiyon sorguları burada tanımlı.
- **`pgxpool` + PgBouncer:** uygulama havuzu + PgBouncer transaction-mode (bkz. `postgresql.md`).
- **RLS ile uyum:** her sorgu `organization_id` (tenant) bağlamı taşır; oturum değişkeni RLS Pattern B v2 için ayarlanır.
- **Partial Event Sourcing:** `workflow_events` append-only tablosu + Aggregate/Apply/Replay Go domain katmanında modellenir (optimistic locking).

## İlişkili tasarım

- [`../research/property-value-storage/index.md`](../research/property-value-storage/index.md) — Go projektörün beslediği depolama mimarisi (D9 outbox omurgası, S2 NATS teyidi).
- [`api-contract.md`](./api-contract.md) — gRPC/Protobuf iç API + grpc-gateway REST.
- [`nats-jetstream.md`](./nats-jetstream.md) — projektörün dinlediği olay omurgası.
- [`postgresql.md`](./postgresql.md) — pgx/sqlc/RLS hedefi.
- [`../research/tech-stack/tech_rating.md`](../research/tech-stack/tech_rating.md) — dil kararı + reddedilen alternatifler.

## Dikkat / açık noktalar

- **Projeksiyon throughput'u benchmark kalemi:** 5M instance yazma yükünde projektör lag'i (P5) kendi donanımımızda p95 ile doğrulanmalı; goroutine/batch ayarı buna göre.
- **AI Service Go değil:** yapay zekâ iş yükü **Python**'da (post-MVP, bkz. `python-ai-service.md`) — Go yalnız çekirdek BPM.
- **Hexagonal disiplini zorunlu:** domain katmanına altyapı sızarsa SOA-split avantajı kaybolur; kod incelemesinde denetlenir.
