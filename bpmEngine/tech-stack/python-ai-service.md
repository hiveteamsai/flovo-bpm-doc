# Python — AI Service (Flovo iBPM v2)

> **Rol:** Yapay zekâ iş yüklerini (semantic search / RAG, NLP, belge çıkarımı, süreç madenciliği) çalıştıran, çekirdek BPM'den ayrı servis.
> **Karar:** Python 3.12+ · 🟡 **POST-MVP** (Sprint 5+) · tam gerekçe/karşılaştırma → [`../research/tech-stack/tech_rating.md`](../research/tech-stack/tech_rating.md)

## Ne için kullanıyoruz?

Çekirdek BPM motoru **Go**'dur; yapay zekâ tarafı ise **ayrı bir Python servisidir**. Python, AI/ML ekosisteminin (embedding, NLP, LLM istemcileri, veri işleme) fiili standardı olduğu için yalnız bu alanda tercih edilir. **MVP kapsamı dışındadır** — SOA split ile birlikte post-MVP devreye alınır.

## Sürüm & bileşenler

| Bileşen | Seçim | Görev |
|---|---|---|
| Dil | **Python 3.12+** | AI servis çalışma zamanı |
| DB erişimi | **asyncpg** + **SQLAlchemy 2.0** (async) | Aynı PostgreSQL'e asenkron erişim |
| Vektör arama | **pgvector** (Postgres extension) | Embedding / semantic search — ayrı vektör DB yok |
| Servis | ayrı deploy (K8s), gRPC/REST ile çekirdeğe bağlanır | SOA split |

## Projemizde kullanım

- **Semantic search / RAG:** form içerikleri ve süreç açıklamaları üzerinde embedding araması; **aynı Postgres** içindeki `pgvector` ile — ayrı bir vektör veritabanı kurulmaz (bkz. `postgresql.md`).
- **Belge / fatura çıkarımı:** [`../research/property-value-storage/form-value-scenarios.md`](../research/property-value-storage/form-value-scenarios.md) **§4 item 17 (Flovo AI)** — yüklenen fatura görselinden `amount`/`vendor`/`date` gibi alanların çıkarılıp Instance Creator init ile form alanlarına yazılması.
- **NLP / süreç madenciliği (process mining):** akış loglarından örüntü/öneri üretimi.

## Konfigürasyon / desen notları

- **Aynı DB, ayrı servis:** Python servisi çekirdek BPM'in Postgres'ine (pgvector) bağlanır ama **kendi bounded context'inde** çalışır; yazma yolu çekirdekten geçer (kaynak-hakikat tutarlılığı).
- **Ayrı deploy:** SOA split (post-MVP) ile Core BPM + AI + Workers ayrı K8s dağıtımı olur.
- **Sınır:** AI servisi form değerlerini **doğrudan** projeksiyona yazmaz; çıkarım sonuçları normal yazma yolundan (form_value → outbox → projektör) akar.

## İlişkili tasarım

- [`../research/tech-stack/tech_rating.md`](../research/tech-stack/tech_rating.md) — dil kararı (AI için Python, çekirdek için Go).
- [`postgresql.md`](./postgresql.md) — pgvector aynı Postgres'te.
- [`../research/property-value-storage/form-value-scenarios.md`](../research/property-value-storage/form-value-scenarios.md) — §4 fatura AI senaryosu.

## Dikkat / açık noktalar

- **MVP DIŞI:** Sprint 5+ kapsamı; MVP demo'da yer almaz — scope creep önleme kararı.
- **pgvector post-MVP:** vektör indeksleme AI Service ile birlikte devreye alınır (o ana kadar Postgres'te yalnız extension hazır).
- **Kaynak-hakikat kuralı:** AI çıkarımları da form_value üzerinden yazılır; projeksiyon/AI ayrımı korunur.
