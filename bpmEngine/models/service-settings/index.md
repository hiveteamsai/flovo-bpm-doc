# Servise Bağlı Modeller — İndeks

> **Amaç:** Bir **Solution/Service** altındaki tasarım modelleri — form alanları, görüntüleme profilleri, süreç adımları
> ve iş kuralları ailesi. Veri modeli/şema odaklı; davranış/kullanım → `../../service-settings/`.

## Dökümanlar
| Döküman | Özet |
|---|---|
| [`solution.md`](./solution.md) | Bir organizasyona ait, **servisleri gruplayan** tanım (organizasyonda birden çok olabilir). |
| [`service.md`](./service.md) | Bir **iş sürecinin/formun** tamamı (motorun temel birimi); **`formType`**: form/parameter/eventForm. |
| [`property.md`](./property.md) | Metadata-driven formdaki tek bir **giriş/görüntüleme elemanı**; `controlTypeId` ile render edilir. |
| [`property-item.md`](./property-item.md) | Seçim alanlarının (`combobox`/`radiobuttonList`) **statik seçeneği**. |
| [`view-profile.md`](./view-profile.md) | Aynı formun **farklı adım/kullanıcılara** nasıl görüneceğini belirleyen **görüntüleme profili**. |
| [`view-profile-property.md`](./view-profile-property.md) | Profildeki **tek bir alanın** görünür/düzenlenebilir/zorunlu + sıra yapılandırması. |
| [`view-profile-property-setting.md`](./view-profile-property-setting.md) | Alanın **tipe-özel** görünüm/davranış ayarının **profil-bazlı override**'ı (key/value). |
| [`process-step.md`](./process-step.md) | İş akışındaki bir **düğüm/kutu** (süreç adımı). |
| [`process-step-action.md`](./process-step-action.md) | Bir **aksiyonun bir adıma bağlanması** (binding); `Action` alanları buraya kopyalanır. |
| [`business-rule.md`](./business-rule.md) | Form üzerinde **koşul → aksiyon** tabanlı dinamik davranış (frontend realtime). 🟡 en son şekillenecek. |
| [`business-rule-condition.md`](./business-rule-condition.md) | İki değerin bir **operatörle** karşılaştırılması; iç içe (recursive) gruplanabilir (`and`/`or`). |

*Oluşturma: 2026-07-13.*
