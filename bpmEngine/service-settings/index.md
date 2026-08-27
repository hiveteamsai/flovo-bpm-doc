# Servis Ayarları (Davranış) — İndeks

> **Amaç:** Bir **servise (forma) bağlı ayarların davranış/kullanım** dokümanları. Her servis kendi süreç adımlarını,
> aksiyonlarını, alanlarını, iş kurallarını ve görüntüleme profillerini barındırır. **Şema/model karşılığı** ayrı
> tutulur → [`../models/service-settings/index.md`](../models/service-settings/index.md).

## Dökümanlar
| Döküman | Özet |
|---|---|
| [`process-step.md`](./process-step.md) | **Süreç adımları** — adım tipleri katalogu (22 adım) + ortak yapı; "hangi adım tipleri var?". |
| [`process-step-action.md`](./process-step-action.md) | **Süreç adımı aksiyonları** — aksiyonun adıma bağlanması (binding), veri aktarımı (`parameters`/`changeList`/`action`), actionType kataloğu. |
| [`properties.md`](./properties.md) | **Form alanları (property)** — formda yer alabilecek alan tipleri (18) ve her birinin detay ayarları + ortak çekirdek. |
| [`business-rule.md`](./business-rule.md) | **İş kuralları** — form üzerinde gerçek zamanlı (frontend) koşul→aksiyon tabanlı davranışlar (model + davranış). |
| [`business-rule-engine.md`](./business-rule-engine.md) | **İş kuralı motoru — işleyiş & fonksiyon spesifikasyonu** (çağrı grafiği + her fonksiyonun görev/tetiklenme/üretim/çağrı ilişkisi). |
| [`business-rule-endpoints.md`](./business-rule-endpoints.md) | **İş kuralı motoru — backend endpoint'leri** (kural taşıma · serviceInstances · organizasyon/kullanıcı verisi · httpRequest · ifade-destek uçları · kural yönetimi). |
| [`view-profile.md`](./view-profile.md) | **Görüntüleme profilleri** — formun süreç adımına göre nasıl görüntüleneceği (görünür/düzenlenebilir/zorunlu). |

*Oluşturma: 2026-07-13.*
