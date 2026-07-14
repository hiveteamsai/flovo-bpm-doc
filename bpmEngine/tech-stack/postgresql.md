# PostgreSQL — Birincil Veritabanı & Depolama Substratı (Flovo iBPM v2)

> **Rol:** Tüm kalıcı verinin (form değerleri, süreç durumu, organizasyon ayarları, event log) tek gerçek kaynağı ve raporlama/arama substratı.
> **Karar:** PostgreSQL **16** (self-host, yalın) + PgBouncer 1.23 · ✅ canlı (F-Infra SI.1) · tam gerekçe/karşılaştırma → [`../research/tech-stack/tech_rating.md`](../research/tech-stack/tech_rating.md) (skor 55/60, #1)

## Ne için kullanıyoruz?

Flovo iBPM v2'nin **tek birincil veritabanı**. BPM'in DB'den beklediği dört kritik yeteneği tek üründe verdiği için seçildi:

- **ACID transaction** — bir workflow adımını ilerletmek + form değerini yazmak + outbox olayı bırakmak **tek atomik işlem** olmalı.
- **JSONB** — form alanları **dinamik** (her müşteri/servis farklı şema); esnek, DDL'siz, indekslenebilir depolama.
- **RLS (Row Level Security)** — **organizasyon (tenant) izolasyonu** DB seviyesinde garanti edilir.
- **Genişletilebilirlik** — pgvector (AI), tsvector (arama), partition, extension ekosistemi.

## Sürüm & bileşenler

| Bileşen | Sürüm/karar | Not |
|---|---|---|
| PostgreSQL | **16** | Self-host (on-prem + Private Cloud ready; managed vendor yok) |
| Connection pool | **PgBouncer 1.23** | `transaction` mode → 10K+ istemci bağlantısı |
| Extension: pgvector | 🟡 **post-MVP** | AI embedding / semantic search (aynı DB, ayrı vector DB gereksiz) |
| Full-text | **tsvector** (yerleşik) | Basit arama; uç ölçekte read-side Elasticsearch (opsiyonel) |
| Migration | ADR-003 apply CI | Şema değişiklikleri CI ile uygulanır |

## Projemizde kullanım

PostgreSQL, [`property-value-storage`](../research/property-value-storage/index.md) tasarımının **doğrudan substratıdır** — CQRS
(tek kaynak + türetilmiş projeksiyon) deseninin tüm katmanları Postgres nesneleridir:

| Katman | Postgres nesnesi | Rol |
|---|---|---|
| **Kaynak-hakikat** | `form_value` (**JSONB** `data` kolonu) | Formun tüm alanları tek satırda; DDL'siz esnek şema (S1/S9) |
| **Skaler projeksiyon** | `form_attr` (tipli EAV: num/text/date/bool) | Arama/filtre/sıralama/rapor için türetilmiş okuma modeli (S1-S13) |
| **Liste projeksiyonu** | `form_list_item` | List-of-model (groupByTax vb.) kalem-bazlı sorgu (S7) |
| **Süreç durumu** | `workflow_events` (append-only) + `workflow_projection` | **Partial Event Sourcing**; replay + audit + saga temeli |
| **Statü** | `Instance.status` **ayrı indeksli kolon** | Volatile akış durumu — JSONB'ye **konmaz** (S3/S4/S10, D3) |
| **Organizasyon ayarları** | `models/organization-settings/*` tabloları | Kiracıya bağlı yapısal veri (Position, User, Translation…) |

**Eşittir/içerir aramaları** `form_value.data` üzerindeki tek **GIN index** (`jsonb_path_ops`) ile herhangi bir alanda karşılanır
(S5: yeni eşittir sorgusu rebuild bile gerektirmez). **Aralık/sıralama/metin** ise `form_attr`'ın sabit btree seti + `pg_trgm`
GIN'i ile çözülür.

## Konfigürasyon / desen notları

- **RLS Pattern B v2:** her tenant-tabloda `organizationId` + RLS politikası; sorgu-zamanı tenant context ile satır izolasyonu
  (application filtresine güvenilmez, DB garanti eder). Multi-tenancy'nin **kritik** bileşeni.
- **Partition — `HASH(service_id)`:** `form_value`/`form_attr`/`form_list_item` partition'lı; her sorgu `service_id` (mümkünse
  `organizationId`) filtresi taşır → partition pruning. Dominant tenant sıcak-nokta olursa alt-`HASH(organizationId)` (S9, P9).
- **Yazma maliyeti tuning (S9/S10):** JSONB update = MVCC ile **tüm satır** yeniden yazımı → JSONB küçük tutulur (dosyalar MinIO'da,
  yalnız URL JSONB'de); `fillfactor=85` + **agresif autovacuum** (`autovacuum_vacuum_scale_factor≈0.02`); GIN pending list için
  `gin_pending_list_limit`. Büyük değerler **TOAST** ile satır-dışı (okuma şeffaf).
- **Statü ayrı kolon (D3):** sık değişen `status` JSONB'de değil, indeksli kolonda — MVCC yeniden-yazımını ve bayatlamayı önler.
- **JSONB code-keyed (S11/S12):** `data` anahtarları `Property.code` (numeric id değil) → kaynakla tutarlı, join'siz; `code`
  **immutable** kuralı bu yüzden zorunlu.
- **projectionLevel (D1):** hangi alanın `form_attr`'a yansıyacağı `Property.projectionLevel` (NONE/SEARCH/SORT/AGGREGATE) ile
  kontrol edilir → satır patlaması + write-amp kontrolü.

## İlişkili tasarım

- [`../research/property-value-storage/index.md`](../research/property-value-storage/index.md) — depolama mimarisi (bu DB'nin üstünde).
- [`../research/property-value-storage/form_attr_scenerios_rating.md`](../research/property-value-storage/form_attr_scenerios_rating.md) — 5M/200M ölçekli senaryo puanlaması + D1/D3/D6/D7 gereksinimleri (hepsi Postgres'te).
- [`../research/tech-stack/tech_rating.md`](../research/tech-stack/tech_rating.md) — DB karar/karşılaştırma.
- [`../models/`](../models/index.md) — tüm veri modelleri (şema referansı).
- [`nats-jetstream.md`](./nats-jetstream.md) — outbox → projeksiyon senkron omurgası (Postgres outbox tablosu → NATS).

## Dikkat / açık noktalar

- **Benchmark kapısı (P1–P9):** 5M instance / ~200M `form_attr` satırı ölçeğinde p95 (yazma, projection lag, rapor, rebuild ~100dk,
  autovacuum, WAL) kendi donanımımızda spike ile doğrulanmadan depolama tasarımı "onaylandı" sayılmaz.
- **Ağır raporlama:** çok-kolon rapor pivotu (P1) ve cross-form aggregation (P2) için Postgres **materialized view / incremental
  rollup tabloları** (D6) gerekir — DB destekliyor, tasarım ayrıca yapılacak.
- **pgvector post-MVP:** AI/RAG Sprint 5+; MVP'de kurulmaz.
- **HA:** self-host olduğundan replica/backup/PITR bizim sorumluluğumuz (managed vendor yok) — ~%30 ek ops eforunun parçası.
