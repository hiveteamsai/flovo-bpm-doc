# Enum — ReflectionMode

> **Kullanan model:** [`property.md`](../service-settings/property.md) — alan `reflectionMode` (yalnız `parentProperty` tipi), tip **ReflectionMode**
> **Amaç:** Bir **yansıma alanının** (`parentProperty`) üst kaynaktaki değeri **nasıl takip edeceğini** belirler —
> dondurulmuş kopya mı, canlı okuma mı, yoksa yayılımla tazelenen materialized kopya mı.
> **Ayrıntılı davranış:** → [`property.md`](../service-settings/property.md) `parentProperty` + [`../processInstances/reflection-link.md`](../processInstances/reflection-link.md).

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `snapshot` | **A — Kopyala + dondur:** değer yazım anında `InstanceValue.data`'ya kopyalanır, sonra **değişmez** (fotoğraf). | Forma yazıldıktan sonra **değişmeyecek** değer (ör. o anki departman/unvan); audit-dostu, ucuz. **Varsayılan.** |
| `live` | **B — Canlı:** değer **yazılmaz**; okurken kaynaktan **join/referans** ile getirilir (pencereden bak). | Değişen ama yalnız **gösterilecek** değer; rapor/filtre gerekmiyorsa. |
| `materialized` | **A′ — Materialized + yayılım:** kopya `data`'ya yazılır **ve** üst değiştikçe `ReflectionLink` üzerinden **arka planda tazelenir**. | Hem **güncel** kalması hem de **ağır rapor/filtre** yapılması gereken değer. Pahalı (fan-out) — derinlik/döngü sınırlı. |

## Notlar
- **Varsayılan `snapshot`'tır**; `materialized` (A′) **bilinçli** seçilir (Designer'da), aksi hâlde kullanılmaz.
- `materialized` yayılımı `ReflectionLink` + reflection-propagation consumer ile çalışır; **derinlik limiti · döngü tespiti ·
  asenkron** zorunludur (→ [`../processInstances/reflection-link.md`](../processInstances/reflection-link.md), `../../todo.md` **O3**).
- Kaynak mimari: → [`../../research/property-value-storage/form-deger-saklama-v2.html`](../../research/property-value-storage/form-deger-saklama-v2.html) (§14 yansıma alanları).

*Oluşturma: 2026-08-04.*
