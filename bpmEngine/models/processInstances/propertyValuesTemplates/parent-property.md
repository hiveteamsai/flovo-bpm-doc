# Değer Şablonu — `parentProperty` (Parent Property)

> **Durum:** 🟡 TASLAK — ilk çıkarım; düzenlenecek.
> **Kapsam:** `parentProperty` (üst/referans alandan türetilen salt-okunur yansıma) değerinin **`InstanceValue.data` içindeki şekli** + fihrist yansıması. Davranış **`reflectionMode`'a bağlıdır**.
> **Alan davranışı:** → [`../../../service-settings/properties.md`](../../../service-settings/properties.md) §3.15 · **model:** [`../../service-settings/property.md`](../../service-settings/property.md) · **yansıma modu:** [`../../enums/reflection-mode.md`](../../enums/reflection-mode.md) · **yayılım:** [`../reflection-link.md`](../reflection-link.md).

## 1. JSONB değer şekli — `data["<code>"]`
Şekil, **referans alınan üst alanın tipiyle aynıdır** (skaler / `LabeledValue` / liste). Depolanıp depolanmaması **`reflectionMode`**'a bağlıdır:

| `reflectionMode` | `data`'da tutulur mu? | Nasıl |
|---|---|---|
| `snapshot` (A, **vars.**) | **Evet** | Yazımda üst alandan **kopyalanır + dondurulur** (referans alanın şekliyle). |
| `live` (B) | **Hayır** | `data`'ya **yazılmaz**; okurken üst instance'tan **join/referans** ile getirilir. |
| `materialized` (A′) | **Evet** | `data`'ya kopyalanır **ve** üst değiştikçe [`ReflectionLink`](../reflection-link.md) ile **tazelenir**. |

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
- Varsayılan `snapshot`; `materialized` (A′) **bilinçli** seçilir ve **derinlik/döngü/asenkron** sınırlıdır (→ [`../reflection-link.md`](../reflection-link.md), motor **O3**).

*Oluşturma: 2026-08-06.*
