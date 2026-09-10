# PostgreSQL — Birincil Veritabanı & Depolama Substratı (Flovo iBPM v2)

> **Rol:** Tüm kalıcı verinin (form değerleri, süreç durumu, organizasyon ayarları, event log) tek gerçek kaynağı ve raporlama/arama substratı.
> **Karar:** PostgreSQL **16** (yalın) — **üretim hedefi self-host** (on-prem/Private-Cloud); **pilot: Azure PostgreSQL** (yönetilen, plain PG, GUC-native RLS). ✅ canlı (pilot); **PgBouncer pilotta henüz yok.** Detay → [`../implementation-status.md`](../implementation-status.md). Tam gerekçe → [`../research/tech-stack/tech_rating.md`](../research/tech-stack/tech_rating.md) (skor 55/60, #1)

## Ne için kullanıyoruz?

Flovo iBPM v2'nin **tek birincil veritabanı**. BPM'in DB'den beklediği dört kritik yeteneği tek üründe verdiği için seçildi:

- **ACID transaction** — bir workflow adımını ilerletmek + form değerini yazmak + outbox olayı bırakmak **tek atomik işlem** olmalı.
- **JSONB** — form alanları **dinamik** (her müşteri/servis farklı şema); esnek, DDL'siz, indekslenebilir depolama.
- **RLS (Row Level Security)** — **organizasyon (tenant) izolasyonu** DB seviyesinde garanti edilir.
- **Genişletilebilirlik** — pgvector (AI), tsvector (arama), partition, extension ekosistemi.

## Sürüm & bileşenler

| Bileşen | Sürüm/karar | Not |
|---|---|---|
| PostgreSQL | **16** | Üretim hedefi: self-host (on-prem/Private-Cloud). **Pilot: Azure PostgreSQL** (yönetilen) |
| Connection pool | **PgBouncer 1.23** | `transaction` mode → 10K+ istemci bağlantısı · 🟡 **pilotta henüz yok** |
| Extension: pgvector | 🟡 **post-MVP** | AI embedding / semantic search (aynı DB, ayrı vector DB gereksiz) |
| Full-text | **tsvector** (yerleşik) | Basit arama; uç ölçekte read-side Elasticsearch (opsiyonel) |
| Migration | ADR-003 apply CI | Şema değişiklikleri CI ile uygulanır |

## Projemizde kullanım

PostgreSQL, [`property-value-storage`](../research/property-value-storage/index.md) tasarımının **doğrudan substratıdır** — CQRS
(tek kaynak + türetilmiş projeksiyon) deseninin tüm katmanları Postgres nesneleridir:

| Katman | Postgres nesnesi | Rol |
|---|---|---|
| **Kaynak-hakikat** | `instance_value` (**JSONB** `data` kolonu) | Formun tüm alanları tek satırda; DDL'siz esnek şema (S1/S9) |
| **Skaler projeksiyon** | `instance_attr` (tipli EAV: num/text/date/bool) | Arama/filtre/sıralama/rapor için türetilmiş okuma modeli (S1-S13) |
| **Liste projeksiyonu** | `instance_list_item` | List-of-model (groupByTax vb.) kalem-bazlı sorgu (S7) |
| **Süreç durumu** | [`workflow_events`](../models/processInstances/workflow-event.md) (append-only, **aylık RANGE partition**) + [`workflow_projection`](../models/processInstances/workflow-projection.md) (1–1 imleç) + [`workflow_timer`](../models/processInstances/workflow-timer.md) (uyandırma; `FOR UPDATE SKIP LOCKED` claim) | **Partial Event Sourcing**; replay + audit + idempotency (`messageId` UNIQUE) + optimistic concurrency (`(processInstanceId, version)` UNIQUE) + **outbox-in-event** (`dispatch`/`publishedAt`). 📝 v0.44 model dosyaları — onay bekliyor |
| **Statü** | `Instance.statusId` **ayrı indeksli kolon** | Volatile akış durumu — JSONB'ye **konmaz** (S3/S4/S10, D3) |
| **Organizasyon ayarları** | `models/organization-settings/*` tabloları | Kiracıya bağlı yapısal veri (Position, User, Translation…) |

> **Fiziksel ad = model adının snake_case'i:** `instance_value`=`InstanceValue` · `instance_attr`=`InstanceAttr` ·
> `instance_list_item`=`InstanceListItem` · `instance_value_outbox`=`InstanceValueOutbox` → [`../models/processInstances/index.md`](../models/processInstances/index.md).

**Eşittir/içerir aramaları** `instance_value.data` üzerindeki tek **GIN index** (`jsonb_path_ops`) ile herhangi bir alanda karşılanır
(S5: yeni eşittir sorgusu rebuild bile gerektirmez). **Aralık/sıralama/metin** ise `instance_attr`'ın sabit btree seti + `pg_trgm`
GIN'i ile çözülür.

## Konfigürasyon / desen notları

- **RLS Pattern B v2:** her tenant-tabloda `organizationId` + RLS politikası; sorgu-zamanı tenant context ile satır izolasyonu
  (application filtresine güvenilmez, DB garanti eder). Multi-tenancy'nin **kritik** bileşeni. **"v2" = GUC-native:** backend her
  istekte **tenant GUC**'unu set eder, RLS politikası bunu **`active_tenant_id()`** fonksiyonuyla okur; **branch-siz** (tenant için
  ayrı şema/bağlantı-dalı yok) → **insan kullanıcı ile AI-agent aynı tenant/RLS yolunu kullanır** ("agent parity" by-construction).
  Pilotta Azure-PG üzerinde doğrulandı → [`../implementation-status.md`](../implementation-status.md).
- **Partition — `HASH(service_id)`:** `instance_value`/`instance_attr`/`instance_list_item` partition'lı; her sorgu `service_id` (mümkünse
  `organizationId`) filtresi taşır → partition pruning. Dominant tenant sıcak-nokta olursa alt-`HASH(organizationId)` (S9, P9).
- **Partition — `RANGE(occurredAt)` aylık (📝 v0.44, öneri):** `workflow_events` **zamanla yaşlanan** append-only tablo → saklama = partition **detach/drop**
  (satır `DELETE` yok, vacuum yükü yok); sıcak → soğuk tablo (`ATTACH`) → MinIO JSONL.gz arşiv → drop. Değer tablolarının HASH stratejisinden bilinçli farklı
  (→ [`../architectures/engine-runtime/engine-runtime-retention.md`](../architectures/engine-runtime/engine-runtime-retention.md) §3 · plan Q2). Yeni partition 2 ay önceden housekeeping ile açılır.
- **Claim deseni — `FOR UPDATE SKIP LOCKED` (📝 v0.44):** `workflow_timer` dolan satırlarını N scheduler kopyası **çakışmadan** paylaşır → **lider seçimi gerekmez**;
  `pg_try_advisory_lock` yalnız singleton housekeeping (relay sweep · stuck detector · pruning) için (→ [`../architectures/engine-runtime/engine-runtime-scheduler.md`](../architectures/engine-runtime/engine-runtime-scheduler.md) §1/§7).
- **Yazma maliyeti tuning (S9/S10):** JSONB update = MVCC ile **tüm satır** yeniden yazımı → JSONB küçük tutulur (dosyalar MinIO'da,
  yalnız URL JSONB'de); `fillfactor=85` + **agresif autovacuum** (`autovacuum_vacuum_scale_factor≈0.02`); GIN pending list için
  `gin_pending_list_limit`. Büyük değerler **TOAST** ile satır-dışı (okuma şeffaf).
- **Statü ayrı kolon (D3):** sık değişen `status` JSONB'de değil, indeksli kolonda — MVCC yeniden-yazımını ve bayatlamayı önler.
- **JSONB code-keyed (S11/S12):** `data` anahtarları `Property.code` (numeric id değil) → kaynakla tutarlı, join'siz; `code`
  **immutable** kuralı bu yüzden zorunlu.
- **projectToAttr (D1):** hangi alanın skaler fihriste (`InstanceAttr`/`InstanceListItem`) yansıyacağı `Property.projectToAttr`
  (**bool**) ile kontrol edilir → satır patlaması + write-amp kontrolü (tipik alanların %10–20'si `true`; çok-seviyeli eski
  `projectionLevel` **yok**). → [`../models/service-settings/property.md`](../models/service-settings/property.md).

## İlişkili tasarım

- [`../research/property-value-storage/index.md`](../research/property-value-storage/index.md) — depolama mimarisi (bu DB'nin üstünde).
- [`../research/property-value-storage/form_attr_scenerios_rating.md`](../research/property-value-storage/form_attr_scenerios_rating.md) — 5M/200M ölçekli senaryo puanlaması + D1/D3/D6/D7 gereksinimleri (hepsi Postgres'te).
- [`../research/tech-stack/tech_rating.md`](../research/tech-stack/tech_rating.md) — DB karar/karşılaştırma.
- [`../models/`](../models/index.md) — tüm veri modelleri (şema referansı).
- [`nats-jetstream.md`](./nats-jetstream.md) — outbox → projeksiyon senkron omurgası (Postgres outbox tablosu → NATS).

## Dikkat / açık noktalar

- **Benchmark kapısı (P1–P9):** 5M instance / ~200M `instance_attr` satırı ölçeğinde p95 (yazma, projection lag, rapor, rebuild ~100dk,
  autovacuum, WAL) kendi donanımımızda spike ile doğrulanmadan depolama tasarımı "onaylandı" sayılmaz.
- **Ağır raporlama:** çok-kolon rapor pivotu (P1) ve cross-form aggregation (P2) için Postgres **materialized view / incremental
  rollup tabloları** (D6) gerekir — DB destekliyor, tasarım ayrıca yapılacak.
- **pgvector post-MVP:** AI/RAG Sprint 5+; MVP'de kurulmaz.
- **HA:** self-host olduğundan replica/backup/PITR bizim sorumluluğumuz (managed vendor yok) — ~%30 ek ops eforunun parçası.
