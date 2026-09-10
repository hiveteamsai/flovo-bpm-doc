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
  (**tasarım gereği application filtresine güvenilmez, izolasyonu DB zorlar**). Multi-tenancy'nin **kritik** bileşeni. **"v2" = GUC-native:** backend her
  istekte **tenant GUC**'unu set eder, RLS politikası bunu **`active_tenant_id()`** fonksiyonuyla okur; **branch-siz** (tenant için
  ayrı şema/bağlantı-dalı yok) → **insan kullanıcı ile AI-agent aynı tenant/RLS yolunu kullanır** ("agent parity" by-construction).
  Pilotta Azure-PG üzerinde tasarım/kod katmanları hazır → [`../implementation-status.md`](../implementation-status.md).
  - ⚠️ **Pilot durumu (2026-09-09 ölçümü · #410):** bu zorlama pilotta HENÜZ ETKİN DEĞİL. Ürün
    `flovo_admin` ile bağlanıyor; bu rol public şemadaki 69 tablonun tamamının sahibi ve
    `rolbypassrls = TRUE` → RLS politikaları onun için uygulanmıyor (`FORCE ROW LEVEL SECURITY`
    hiçbir tabloda açık değil: 0/69). Ölçüm: kiracı bağlamı verilmeden `property` sorgusu 238
    satırın tamamını döndürüyor; kiracı-B token'ıyla kiracı-A'nın kaydı token → interceptor →
    handler → app → repo → SQL zincirinin tamamından okunabiliyor. Bugün yalıtımı fiilen sağlayan
    katman yoktur — uygulama katmanı da tasarım gereği kiracı yüklemi taşımaz. Kapatma planı ve
    kabul ölçütleri → #410.
    - **Ölçümün adresi** (origin/main `e6136a75` · 2026-09-10): mevcut "Pilotta doğrulandı"
      beyanının dayanağı `tests/migrations/property_rls.spec.ts:59 ⊕ :73` (`set role app_user`) —
      ve desen tek dosyaya ait değil: `tests/**` altında 46 dosya · 84 geçiş, `apps/api-go/**`
      altında 8 dosya · 16 geçiş. ⚠️ O 16'nın **2'si yorum satırıdır** ve #410'un kendi rung'unda
      kusuru TARİF eder (`tenant_isolation_owner_principal_integration_test.go`), yani fiilî
      kullanım **14**. #410'un çıkış noktası Go tarafıdır: testler migration sahibiyle açılıp
      `app_user` rolüne geçiyor, üretim ise `flovo_admin` ile bağlanıyor → süit, ürünün fiilen
      koştuğu özneyi hiçbir yerde ölçmüyor.
- **Partition — `HASH(service_id)`:** `instance_value`/`instance_attr`/`instance_list_item` partition'lı; her sorgu `service_id` (mümkünse
  `organizationId`) filtresi taşır → partition pruning. Dominant tenant sıcak-nokta olursa alt-`HASH(organizationId)` (S9, P9).
- **Partition — `RANGE(occurredAt)` aylık (📝 v0.44, öneri):** `workflow_events` **zamanla yaşlanan** append-only tablo → saklama = partition **detach/drop**
  (satır `DELETE` yok, vacuum yükü yok); sıcak → soğuk tablo (`ATTACH`) → MinIO JSONL.gz arşiv → drop. Değer tablolarının HASH stratejisinden bilinçli farklı
  (→ [`../engine-runtime-retention.md`](../engine-runtime-retention.md) §3 · plan Q2). Yeni partition 2 ay önceden housekeeping ile açılır.
- **Claim deseni — `FOR UPDATE SKIP LOCKED` (📝 v0.44):** `workflow_timer` dolan satırlarını N scheduler kopyası **çakışmadan** paylaşır → **lider seçimi gerekmez**;
  `pg_try_advisory_lock` yalnız singleton housekeeping (relay sweep · stuck detector · pruning) için (→ [`../engine-runtime-scheduler.md`](../engine-runtime-scheduler.md) §1/§7).
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
