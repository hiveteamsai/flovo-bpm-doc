# Enum — HttpMethod

> **Kullanan model:** [`process-step.md`](../service-settings/process-step.md) — **HTTP Request** adımı ayarı, alan `method`, tip **HttpMethod**
> **Amaç:** HTTP Request adımının dış endpoint'e hangi **HTTP metodu** ile istek atacağını belirler.
> **Davranış:** → [`../../service-settings/process-step.md`](../../service-settings/process-step.md) §3.2.

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `get` | GET | Kaynak okuma/sorgulama. |
| `post` | POST | Oluşturma / veri gönderme. |
| `put` | PUT | Güncelleme (kaynağı değiştirme). |
| `delete` | DELETE | Silme. |

## Notlar
- **Kaynak/karar:** current Flovo'da `method` **string** olarak tutuluyordu; tipli enum'a çevrildi →
  [`../../research/current-flovo-bpm-engine/step-type-settings-and-enums.md`](../../research/current-flovo-bpm-engine/step-type-settings-and-enums.md) §7.
- İleride gerekirse `patch` genişletme adayıdır (şimdilik kapsam dışı).

*Oluşturma: 2026-07-16.*
