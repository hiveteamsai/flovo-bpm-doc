# Enum — ReflectionPropagation

> **Kullanan model:** [`property.md`](../service-settings/property.md) — alan `reflectionPropagation` (yalnız `parentProperty` + `reflectionMode=materialized`), tip **ReflectionPropagation**
> **Amaç:** Materialized (A′) bir yansıma alanının, **üst kaynak değiştiğinde** child kopyanın **ne zaman/nasıl** tazeleneceğini belirler — arka planda (async) mı, yazma anında (sync) mı.
> **Ayrıntılı davranış:** → [`../processInstances/reflection-propagation.md`](../processInstances/reflection-propagation.md).

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `async` | **Arka planda (VARSAYILAN):** üst güncelleme commit olur; child kopya **outbox → consumer** ile **eventual** tazelenir. | Güvenli varsayılan. Fan-out/kaskad maliyeti yazmayı kilitlemez; kısa **eventual consistency** penceresi kabul edilir. |
| `sync` | **Yazma anında:** üst değer güncellenirken child kopya(lar) **aynı transaction'da** tazelenir (anında tutarlı). | Küçük fan-out + **sığ (1-hop)** + anında tutarlılık gereken alanlar. **Guardrail'li:** derin kaskad yine async'e devreder, fan-out eşiği aşılırsa async'e düşer. |

## Notlar
- Yalnız `reflectionMode=materialized` (A′) için anlamlıdır; `snapshot`/`live`'da **yok sayılır** (snapshot dondurur, live saklamaz → tazelenecek şey yok).
- **Varsayılan `async`.** `sync` **bilinçli** seçilir ve motor guardrail'leriyle sınırlıdır (**1-hop + fan-out eşiği**; derinlik/döngü → `../../todo.md` **O3**).
- Adlandırma: enum **tip** PascalCase (`ReflectionPropagation`), **değerler** camelCase (`async`/`sync`), model **alan adı** `reflectionPropagation`.
- Mekanizma (async/sync akış + doğruluk/performans): → [`../processInstances/reflection-propagation.md`](../processInstances/reflection-propagation.md).

*Oluşturma: 2026-08-10.*
