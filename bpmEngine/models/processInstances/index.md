# Çalışma-Zamanı (Runtime) Modelleri — İndeks

> **Amaç:** Ayarlardan (`Service`/`ProcessStep`/`Property`…) motor tarafından üretilen **çalışma-zamanı** kayıtları —
> süreç çalıştırma, doldurulmuş form, onay/bekleme ve **form-değer saklama** (JSONB tapu + fihrist projeksiyonları) verisi. 🟢 TANIMLI.

## Dökümanlar

### Süreç & form çekirdeği
| Döküman | Özet |
|---|---|
| [`process-instance.md`](./process-instance.md) | Bir servis sürecinin **çalıştırma örneği** (runtime); tasarımdaki `Service`/`ProcessStep`'in canlı karşılığı. |
| [`process-step-instance.md`](./process-step-instance.md) | **Tek bir süreç adımının çalıştırılması** — hangi adım, hangi aksiyon, kim/ne tarafından, ne zaman. |
| [`instance.md`](./instance.md) | Bir iş akışında oluşturulan **doldurulmuş form** (runtime veri kaydı); mevcut `statusId`. Değerleri **taşımaz** (→ `InstanceValue`). |
| [`instance-awaiting-user.md`](./instance-awaiting-user.md) | Form üzerinde **atanan / aksiyon alabilecek** kullanıcı veya grup (aksiyon/onay kuyruğu). |
| [`associated-instance.md`](./associated-instance.md) | Bir formu **başka bir formla ilişkilendirme** (property boyutuyla). |

### Değer saklama (form değerleri — CQRS + Outbox + NATS)
| Döküman | Özet |
|---|---|
| [`instance-value.md`](./instance-value.md) | **Kaynak-hakikat (tapu)** — Instance ile 1–1; tüm alan değerleri `data` **JSONB, code-keyed** + `version`. |
| [`instance-attr.md`](./instance-attr.md) | **Skaler fihrist** — sorgulanabilir alan → 1 satır (tipli EAV projeksiyonu); `InstanceValue`'dan yeniden üretilebilir. |
| [`instance-list-item.md`](./instance-list-item.md) | **Liste kalemleri fihristi** — liste-of-model (`groupByTax`, key-value) alanları için kalem-bazlı projeksiyon. |
| [`instance-value-outbox.md`](./instance-value-outbox.md) | **Outbox olayı** — değer update'iyle aynı TX'te; relay → NATS → projektör. |
| [`instance-value-change.md`](./instance-value-change.md) | **Değer geçmişi** (append-only audit; `saveChangeLog=true` alanlar) — projeksiyon değil, kaynak kanıt. |
| [`reflection-link.md`](./reflection-link.md) | **Yansıma yayılım bağı** — `parentProperty` `reflectionMode=materialized` (A′) için parent→child tazeleme. |
| [`propertyValuesTemplates/`](./propertyValuesTemplates/index.md) | **Değer şablonları (property tipine göre)** — her `propertyType` için `data` içindeki JSONB şekli + `projectToAttr` projeksiyon eşlemesi; **core `labeled-value.md`** (etiketli değer şekli) bu klasördedir. |

*Oluşturma: 2026-07-13.*
