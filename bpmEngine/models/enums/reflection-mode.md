# Enum — ReflectionMode

> **Kullanan model:** [`property.md`](../service-settings/property.md) — alan `reflectionMode` (salt-okunur/türetilen tipler: `parentProperty` · `userInfo` · `flowInfo`), tip **ReflectionMode**
> **Amaç:** Bir **salt-okunur/türetilen alanın** kaynaktaki değeri **nasıl takip edeceğini** belirler — **oluşturma-anındaki**
> dondurulmuş kopya mı (`snapshot`), **güncel** canlı okuma mı (`live`), yoksa yayılımla tazelenen `materialized` kopya mı.
> Kaynak tipe göre değişir: `parentProperty` → üst/referans alan · `userInfo` → kullanıcı (User) bilgisi · `flowInfo` → akışın
> kendi `Instance` kolonları (durum/tarih/oluşturan).
> **Ayrıntılı davranış:** → [`property.md`](../service-settings/property.md) `parentProperty` + [`../processInstances/reflection-propagation.md`](../processInstances/reflection-propagation.md).
> **İlgili enum:** `materialized` iken tazelemenin **ne zaman** yapılacağı → [`reflection-propagation.md`](./reflection-propagation.md) (`async`/`sync`).

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `snapshot` | **A — Kopyala + dondur:** değer **oluşturma anında** `InstanceValue.data`'ya kopyalanır, sonra **değişmez** (fotoğraf). | Forma yazıldıktan sonra **değişmeyecek**/o-anki değer (ör. o anki departman/unvan); audit-dostu, ucuz. `parentProperty`/`userInfo` **varsayılanı**. |
| `live` | **B — Canlı:** değer **yazılmaz**; okurken kaynaktan **join/referans** ile **güncel** getirilir (pencereden bak). | Sürekli değişen ama yalnız **gösterilecek** değer (ör. akış durumu); rapor/filtre gerekmiyorsa. `flowInfo` **varsayılanı**. |
| `materialized` | **A′ — Materialized + yayılım (yalnız `parentProperty`):** kopya `data`'ya yazılır **ve** üst değiştikçe **`AssociatedInstance` üzerinden yayılımla tazelenir** (varsayılan **async**; `reflectionPropagation=sync` ile yazma anında da yapılabilir). | Hem **güncel** kalması hem de **ağır rapor/filtre** yapılması gereken değer. Pahalı (fan-out) — derinlik/döngü sınırlı. |

## Notlar
- **Tipe-göre varsayılan:** `parentProperty`/`userInfo` → `snapshot` · `flowInfo` → `live`. `materialized` (A′) **yalnız `parentProperty`**'de ve **bilinçli** seçilir (Designer'da); `userInfo`/`flowInfo` yalnız `snapshot`↔`live` arasında seçer (kaynakları — User / kendi `Instance` kolonları — `AssociatedInstance` yayılım yolunda olmadığından materialized geçerli değildir).
- `materialized` yayılımı **`AssociatedInstance` + `Property` metadata** ile çözülür (ayrı "link" tablosu **yok**); reflection-propagation
  consumer child'ları bulup tazeler. **Derinlik limiti · döngü tespiti · async** zorunludur (`sync` opt-in, guardrail'li) →
  [`../processInstances/reflection-propagation.md`](../processInstances/reflection-propagation.md), `../../todo.md` **O3**.
- Kaynak mimari: → [`../../research/property-value-storage/form-deger-saklama-v2.html`](../../research/property-value-storage/form-deger-saklama-v2.html) (§14 yansıma alanları).

*Oluşturma: 2026-08-04.*
