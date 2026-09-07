# Enum — ReflectionMode

> **Kullanan model:** [`property.md`](../service-settings/property.md) — alan `reflectionMode` (salt-okunur/türetilen tipler: `parentProperty` · `userInfo` · `flowInfo`), tip **ReflectionMode**
> **Amaç:** Bir **salt-okunur/türetilen alanın** kaynaktaki değeri **nasıl takip edeceğini** belirler — **kopyalama-anındaki**
> dondurulmuş kopya mı (`snapshot`), **güncel** canlı okuma mı (`live`), yoksa yayılımla tazelenen `materialized` kopya mı.
> **Kopyalama anı** kaynak tipe göre değişir: `parentProperty` → **ilişki kurulduğu an** (`AssociatedInstance` kaydı; bağ kalkınca
> **temizlenir**) · `userInfo`/`flowInfo` → instance **oluşturma anı** (KARAR v0.45, aşağıda).
> Kaynak tipe göre değişir: `parentProperty` → üst/referans alan · `userInfo` → kullanıcı (User) bilgisi · `flowInfo` → akışın
> kendi `Instance` kolonları (durum/tarih/oluşturan).
> **Ayrıntılı davranış:** → [`property.md`](../service-settings/property.md) `parentProperty` + [`../processInstances/reflection-propagation.md`](../processInstances/reflection-propagation.md).
> **İlgili enum:** `materialized` iken tazelemenin **ne zaman** yapılacağı → [`reflection-propagation.md`](./reflection-propagation.md) (`async`/`sync`).

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `snapshot` | **A — Kopyala + dondur:** değer **kopyalama anında** (`parentProperty` → ilişki kurulunca · `userInfo`/`flowInfo` → oluşturma anında) `InstanceValue.data`'ya kopyalanır, sonra **değişmez** (fotoğraf); `parentProperty`'de bağ kalkınca **`null`**. | Forma yazıldıktan sonra **değişmeyecek**/o-anki değer (ör. o anki departman/unvan); audit-dostu, ucuz. `parentProperty`/`userInfo` **varsayılanı**. |
| `live` | **B — Canlı:** değer **yazılmaz**; okurken kaynaktan **join/referans** ile **güncel** getirilir (pencereden bak). | Sürekli değişen ama yalnız **gösterilecek** değer (ör. akış durumu); rapor/filtre gerekmiyorsa. `flowInfo` **varsayılanı**. |
| `materialized` | **A′ — Materialized + yayılım (yalnız `parentProperty`):** kopya **ilişki kurulunca** `data`'ya yazılır (bağ kalkınca **`null`**) **ve** üst değiştikçe **`AssociatedInstance` üzerinden yayılımla tazelenir** (varsayılan **async**; `reflectionPropagation=sync` ile yazma anında da yapılabilir). | Hem **güncel** kalması hem de **ağır rapor/filtre** yapılması gereken değer. Pahalı (fan-out) — derinlik/döngü sınırlı. |

## Notlar
- **Tipe-göre varsayılan:** `parentProperty`/`userInfo` → `snapshot` · `flowInfo` → `live`. `materialized` (A′) **yalnız `parentProperty`**'de ve **bilinçli** seçilir (Designer'da); `userInfo`/`flowInfo` yalnız `snapshot`↔`live` arasında seçer (kaynakları — User / kendi `Instance` kolonları — `AssociatedInstance` yayılım yolunda olmadığından materialized geçerli değildir).
- **Kopyalama anı ↔ ilişki (KARAR v0.45):** `parentProperty`'de `snapshot`/`materialized` kopyası **instance oluşturma anında değil,
  ilişki kurulduğu anda** (`AssociatedInstance` insert) alınır — child çoğu zaman bağdan **önce** var olur (Form List ile yeni oluşturma
  dahil; "var olandan ekle"; ilişkili Combobox seçimi). Bağ **kaldırılınca** kopya **`null`**'a çekilir; Combobox'ta seçim değişimi =
  temizle + yeni üstten kopyala. `live`'da saklanan değer yok → işlem yok. Mekanizma → [`../processInstances/reflection-propagation.md`](../processInstances/reflection-propagation.md) §3a.
- **Faz kapsamı (KARAR v0.45):** `snapshot`/`live` Motor **Faz 1 çekirdeği**; `materialized` yayılımı **F1.A.4** (outbox · projector · NATS) ile
  açılır, öncesinde Designer `materialized`'ı **reddeder** (→ [`../processInstances/reflection-propagation.md`](../processInstances/reflection-propagation.md) §10 · `bpm-engine-build-plan.md` F1.A.4).
- `materialized` yayılımı **`AssociatedInstance` + `Property` metadata** ile çözülür (ayrı "link" tablosu **yok**); reflection-propagation
  consumer child'ları bulup tazeler. **Derinlik limiti · döngü tespiti · async** zorunludur (`sync` opt-in, guardrail'li) →
  [`../processInstances/reflection-propagation.md`](../processInstances/reflection-propagation.md), `../../todo.md` **O3**.
- Kaynak mimari: → [`../../research/property-value-storage/form-deger-saklama-v2.html`](../../research/property-value-storage/form-deger-saklama-v2.html) (§14 yansıma alanları).

*Oluşturma: 2026-08-04. Güncelleme: 2026-09-07 (kopyalama anı = ilişki anı · faz kapsamı, KARAR v0.45).*
