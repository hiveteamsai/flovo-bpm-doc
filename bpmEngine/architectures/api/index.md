# API — Settings API · Customer API (İndeks)

> **Amaç:** Flovo'nun iki dış yüzeyi: **Settings API** (tasarım-zamanı ayar CRUD'u — Designer/organizasyon ayarları) ve **Customer API** (müşteri custom code'unun
> instance okuma/yazma + webhook tetikleme yüzeyi). Motoru ilerleten **runtime uçları** (aksiyon tetikleme · instance okuma · liste) bu klasörde değil,
> motor planındadır → [`../../../bpm-engine-build-plan.md`](../../../bpm-engine-build-plan.md) (F1.E.3 · F2.G).

| Dosya | İçerik | Durum |
|---|---|---|
| [`settings-api.md`](./settings-api.md) | **Settings API:** ortak sözleşme · kaynak hiyerarşisi · servis-ayarı kaynakları (Solution/Service/Property/ProcessStep+Action/ViewProfile/BusinessRule/ServiceTrigger) · organizasyon-ayarı kaynakları · `settings` doğrulama & referans bütünlüğü · toplu işlemler · draft/yayınlama & versiyonlama (pilotta inşa) · açık noktalar | 🟢 yüzey tasarlandı · pilotta çatı inşa edildi |
| [`flovo-customer-api.md`](./flovo-customer-api.md) | **Customer API:** genel ilkeler · uç listesi (instance oku/yaz · arama · webhook aksiyonu) · iş özeti | 🟡 TASLAK · ⏭️ **MVP-sonrası** (→ `../../todo-phase2.md` §13) |

*Oluşturma: 2026-09-10 (v0.48).*
