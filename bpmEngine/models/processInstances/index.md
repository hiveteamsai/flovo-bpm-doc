# Çalışma-Zamanı (Runtime) Modelleri — İndeks

> **Amaç:** Ayarlardan (`Service`/`ProcessStep`/`Property`…) motor tarafından üretilen **çalışma-zamanı** kayıtları —
> süreç çalıştırma, doldurulmuş form ve onay/bekleme verisi. 🟢 TANIMLI (yalnız `Instance` property value depolaması açık → `../../todo.md`).

## Dökümanlar
| Döküman | Özet |
|---|---|
| [`process-instance.md`](./process-instance.md) | Bir servis sürecinin **çalıştırma örneği** (runtime); tasarımdaki `Service`/`ProcessStep`'in canlı karşılığı. |
| [`process-step-instance.md`](./process-step-instance.md) | **Tek bir süreç adımının çalıştırılması** — hangi adım, hangi aksiyon, kim/ne tarafından, ne zaman. |
| [`instance.md`](./instance.md) | Bir iş akışında oluşturulan **doldurulmuş form** (runtime veri kaydı); mevcut `statusId`. |
| [`instance-awaiting-user.md`](./instance-awaiting-user.md) | Form üzerinde **atanan / aksiyon alabilecek** kullanıcı veya grup (aksiyon/onay kuyruğu). |
| [`user-group-approved-user.md`](./user-group-approved-user.md) | Bir **grup onayında** onaylayan üye + onay zamanı. |
| [`associated-instance.md`](./associated-instance.md) | Bir formu **başka bir formla ilişkilendirme** (property boyutuyla). |

*Oluşturma: 2026-07-13.*
