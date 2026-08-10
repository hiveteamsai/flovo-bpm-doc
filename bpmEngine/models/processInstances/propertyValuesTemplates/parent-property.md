# Değer Şablonu — `parentProperty` (Parent Property)

> **Durum:** 🟡 TASLAK — ilk çıkarım; düzenlenecek.
> **Kapsam:** `parentProperty` (üst/referans alandan türetilen salt-okunur yansıma) değerinin **`InstanceValue.data` içindeki şekli** + fihrist yansıması. Davranış **`reflectionMode`'a bağlıdır**.
> **Alan davranışı:** → [`../../../service-settings/properties.md`](../../../service-settings/properties.md) §3.15 · **model:** [`../../service-settings/property.md`](../../service-settings/property.md) · **yansıma modu:** [`../../enums/reflection-mode.md`](../../enums/reflection-mode.md) (snapshot/live/materialized) · **yayılım zamanı:** [`../../enums/reflection-propagation.md`](../../enums/reflection-propagation.md) (async/sync) · **yayılım mekanizması:** [`../reflection-propagation.md`](../reflection-propagation.md).

## 1. JSONB değer şekli — `data["<code>"]`
Şekil, **referans alınan üst alanın tipiyle aynıdır** (skaler / `LabeledValue` / liste). Depolanıp depolanmaması **`reflectionMode`**'a bağlıdır:

| `reflectionMode` | `data`'da tutulur mu? | Nasıl |
|---|---|---|
| `snapshot` (A, **vars.**) | **Evet** | Yazımda üst alandan **kopyalanır + dondurulur** (referans alanın şekliyle). |
| `live` (B) | **Hayır** | `data`'ya **yazılmaz**; okurken üst instance'tan **join/referans** ile getirilir. |
| `materialized` (A′) | **Evet** | `data`'ya kopyalanır **ve** üst değiştikçe [`AssociatedInstance` üzerinden yayılımla](../reflection-propagation.md) **tazelenir** (varsayılan **async**; `reflectionPropagation=sync` opsiyonu). |

```json
{ "parentBudgetCode": { "value": "P-9", "display": "Proje 9", "translationCode": null } }
```
_(örnek: üst alan etiketli seçimse `LabeledValue`; sayısalsa `number`…)_

## 2. Projeksiyon — `projectToAttr=true`
| `reflectionMode` | Projeksiyon |
|---|---|
| `snapshot` / `materialized` | **InstanceAttr**/`InstanceListItem` — **referans alanın tipinin kuralıyla** (skaler→tipli kolon; etiketli→`textValue`+`display`+`translationCode`; liste→ListItem) |
| `live` | **Yok** — `data`'da değer olmadığından projekte edilmez; rapor gerekiyorsa üst instance join'i (veya `materialized`'e geç) |

## 3. Notlar
- Varsayılan `snapshot`; `materialized` (A′) **bilinçli** seçilir ve **derinlik/döngü/async** sınırlıdır (→ [`../reflection-propagation.md`](../reflection-propagation.md), motor **O3**).
- **Yayılım mekanizması:** ayrı bir "link" tablosu **yok** — child'lar `AssociatedInstance` ters aramasıyla, eşleme `Property.refPropertyId`/`code` ile çözülür.
- **`async` (vars.):** üst commit'i ile child tazeleme arası **eventual consistency** (kısa gecikme). Anında tutarlılık gerekiyorsa **`sync`** (1-hop + fan-out eşiği guardrail'li).

*Oluşturma: 2026-08-06.*
