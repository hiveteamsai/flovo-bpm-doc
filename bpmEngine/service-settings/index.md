# Servis Ayarları (Davranış) — İndeks

> **Amaç:** Bir **servise (forma) bağlı ayarların davranış/kullanım** dokümanları. Her servis kendi süreç adımlarını,
> aksiyonlarını, alanlarını, iş kurallarını ve görüntüleme profillerini barındırır. **Şema/model karşılığı** ayrı
> tutulur → [`../models/service-settings/index.md`](../models/service-settings/index.md).

## Dökümanlar
| Döküman | Özet |
|---|---|
| [`process-step.md`](./process-step.md) | **Süreç adımları** — adım tipleri katalogu (20 adım) + ortak yapı; "hangi adım tipleri var?". |
| [`process-step-action.md`](./process-step-action.md) | **Süreç adımı aksiyonları** — aksiyonun adıma bağlanması (binding), veri aktarımı (`parameters`/`changeList`/`action`), actionType kataloğu. |
| [`properties.md`](./properties.md) | **Form alanları (property)** — formda yer alabilecek alan tipleri (19) ve her birinin detay ayarları + ortak çekirdek. |
| [`business-rule.md`](./business-rule.md) | **İş kuralları** — form üzerinde gerçek zamanlı (frontend) koşul→aksiyon tabanlı davranışlar. |
| [`view-profile.md`](./view-profile.md) | **Görüntüleme profilleri** — formun süreç adımına göre nasıl görüntüleneceği (görünür/düzenlenebilir/zorunlu). |

*Oluşturma: 2026-07-13.*
