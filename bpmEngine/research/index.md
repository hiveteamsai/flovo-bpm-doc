# Research (BPM Referansları & Karşılaştırmalar) — İndeks

> **Amaç:** Yeni BPM motoru tasarımını beslemek için **referans analizleri** (mevcut/eski Flovo BPM + n8n), bunlarla
> yeni tasarımı **kıyaslayan** karşılaştırma dokümanları ve **teknik mimari araştırmaları** barındırır.
> Doğrudan .md yoktur; içerik alt klasörlerdedir.

## Alt klasörler
| Klasör | İçerik (özet) | İndeks |
|---|---|---|
| **compare/** | Yeni tasarımın **eski Flovo** ve **n8n** ile farkları/kıyasları (isim değişiklikleri + fark analizleri + başarılı/eksik değerlendirmesi). | [`compare/index.md`](./compare/index.md) |
| **current-flovo-bpm-engine/** | **Mevcut (eski) Flovo BPM** sisteminin analizi — motor, adımlar, aksiyonlar, alanlar, kurallar + eski organizasyon-ayar DTO'ları. | [`current-flovo-bpm-engine/index.md`](./current-flovo-bpm-engine/index.md) |
| **n8n/** | Referans motor **n8n**'in yürütme içyapısı ve süreç adımı (node) yetenek envanteri. | [`n8n/index.md`](./n8n/index.md) |
| **property-value-storage/** | Form/property **değeri saklama mimarisi** araştırması (CQRS Projection · Outbox · Postgres/JSONB). 🟢 **Model katmanı işlendi (2026-08-04)** — `models/processInstances/` altına InstanceValue/InstanceAttr/InstanceListItem + değer modelleri alındı; artık **kaynak/mimari referans** (açık kalan operasyonel kararlar → `todo.md`). | [`property-value-storage/index.md`](./property-value-storage/index.md) |
| **settings-log/** | **Ayar değişiklik logu** tasarımı — sayfa bazlı denetim izi (tek generic tablo · JSONB delta · `SettingsLog`/`SettingsLogBatch`/`SettingsLogBatchPage` · log erişimi/yetki). 🟡 **Karar bekliyor** — `todo.md` "Denetim izi (audit) / loglama" (Tier 1) maddesinin **ayar logu** kısmının girdisi; henüz tasarıma dahil değil. | [`settings-log/index.md`](./settings-log/index.md) |
| **tech-stack/** | **Teknoloji yığını & mimari** araştırması — veritabanı · dil · mimari karşılaştırmaları + konsolide karar (Go · Postgres · Keycloak · MinIO · NATS · K8s · Hexagonal, on-prem ready). 🔵 **Referans** (kararlar verildi). | [`tech-stack/index.md`](./tech-stack/index.md) |
