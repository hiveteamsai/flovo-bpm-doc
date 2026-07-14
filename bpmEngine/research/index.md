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
| **property-value-storage/** | Form/property **değeri saklama mimarisi** araştırması (CQRS Projection · Outbox · Postgres/JSONB). 🟡 **Değerlendirme bekliyor** — `todo.md` "Property value depolama modeli" açık sorusunun girdisi; henüz tasarıma dahil değil. | [`property-value-storage/index.md`](./property-value-storage/index.md) |
