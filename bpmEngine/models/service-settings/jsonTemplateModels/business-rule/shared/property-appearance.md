# DTO — PropertyAppearance

> **Tür:** **DTO** — **DB tablosu değildir.** `setViewForProperties` aksiyon konfigürasyonunun içinde,
> `BusinessRule.configuration` **JSONB** gövdesinde iç-içe yaşar.
> **Amaç:** Bir alanın **görünüm durumu** — koşul **sağlanınca** / **sağlanmayınca** uygulanacak üç bayrak.
> **Davranış/kullanım:** → [`set-view-for-properties.md`](../actions/set-view-for-properties.md) · [`../../../../../service-settings/business-rule.md`](../../../../../service-settings/business-rule.md) §3

## Alanlar
| Alan | Tip | Ne için |
|---|---|---|
| `visible` | bool | Alan **görünür** mü. |
| `enabled` | bool | Alan **düzenlenebilir** mi. |
| `required` | bool | Alan **zorunlu** mu. |

## Notlar
- Verilmeyen bayrak **`false`** kabul edilir.
- **Salt-okunur modda** `enabled` her durumda **`false`**'a zorlanır (görünürlük/zorunluluk kuraldan gelir; düzenlenebilirlik açılmaz) — davranış [`set-view-for-properties.md`](../actions/set-view-for-properties.md).
- Alanların form-düzeyi **varsayılan** görünürlük/erişim/zorunluluğu **görüntüleme profilinde** tutulur (→ [`../../../view-profile-property.md`](../../../view-profile-property.md)); bu DTO, koşula bağlı **anlık (runtime) override**'dır.

*Oluşturma: 2026-08-26.*
