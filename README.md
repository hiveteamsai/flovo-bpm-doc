# Flovo BPM — Tasarım & Analiz Dokümanları

Bu depo bir **kod deposu değildir.** Flovo'nun **yeni BPM motorunun** tasarım/analiz dökümanlarını (**Markdown**) içerir.
Gerçek kod ayrı bir repoda geliştirilecektir. Çalışma dili **Türkçe**dir; tanımlayıcılar (alan/kod/enum adları) İngilizcedir.

## Flovo nedir?

Flovo, **Coden** tarafından geliştirilen **bulut tabanlı, yapay zekâ destekli kurumsal iş süreçleri yönetim (BPM)
platformudur.** Çekirdeği **masraf yönetimi** olup **görev, İK, envanter ve denetim** modülleriyle genişler.

## İçerik

- **[`bpmEngine/`](bpmEngine/index.md)** — asıl çalışma: yeni BPM motoru tasarımı.
  - `flovo-bpm-engine.md` · `flovo-customer-api.md` — motor çalışma prensibi · Customer API
  - `organization-settings/` · `service-settings/` — ayar (davranış) dokümanları
  - `models/` — veri modelleri (şema referansı) + `enums/`
  - `models/processInstances/propertyValuesTemplates/` — tip-bazlı değer saklama şablonları (18 tip)
  - `sampleProcess/` — uçtan uca örnek süreçler
  - `research/` — BPM referansları + karşılaştırmalar (`compare/`)
  - `todo.md` — açık kararlar/sorular (önceliklendirilmiş, Tier 0–3)
- **`commitNotes/`** — sürüm-bazlı değişiklik notları (`v0-X.md`)
- **`archive/`** — önceki pazar/ürün araştırması + sunum arşivi

## Nereden başlamalı?

Motor tasarımına giriş için **[`bpmEngine/index.md`](bpmEngine/index.md)**; açık kararlar için
**[`bpmEngine/todo.md`](bpmEngine/todo.md)**.

> Ayrıntılı çalışma kuralları ve klasör yapısı: **[`CLAUDE.md`](CLAUDE.md)**.
