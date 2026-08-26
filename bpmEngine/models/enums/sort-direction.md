# Enum — SortDirection

> **Kullanan model:** [`../service-settings/dto/business-rule/data-source/assign-value-from-dataset.md`](../service-settings/dto/business-rule/data-source/assign-value-from-dataset.md) — alan `sortType`
> **Amaç:** Bir veri seti / liste sonucunun **sıralama yönünü** belirler.

## Değerler
| Değer | Anlam |
|---|---|
| `none` | Sıralama yok (kaynağın doğal sırası korunur). |
| `asc` | Artan (A→Z, küçükten büyüğe). |
| `desc` | Azalan (Z→A, büyükten küçüğe). |

## Notlar
- Sıralama yalnız **sıralama kolonu** verildiğinde uygulanır (`none` değilse ve `sortPropertyId` doluysa).

*Oluşturma: 2026-08-26.*
