# Servis Ayarları — DTO'lar — İndeks

> **Amaç:** Bu klasör, **DB tablosu OLMAYAN** (kalıcı şeması bir tabloya karşılık gelmeyen) **DTO** (Data Transfer Object)
> modellerini toplar.
>
> **Genel kural (proje geneli):** `models/` altında bir model **DB tablosu değilse** — yalnız **JSON** olarak taşınan/
> saklanan veri paketi (ör. bir alanın JSONB gövdesi, adımlar arası taşınan paket) — tanımı ilgili kırılımın **`dto/`**
> klasörüne konur. **DB tabloları** eskisi gibi kendi kırılımlarında (ör. `service-settings/`) kalır.

## Dökümanlar
| Döküman | Özet |
|---|---|
| [`action-transfer.md`](./action-transfer.md) | Aksiyon tetiklendiğinde sonraki adıma taşınan **veri aktarım paketi** (`parameters` / `changeList` / `action`); `ProcessStepInstance.processStepActionParameter`'da JSON olarak saklanır. |

## Alt klasörler
| Klasör | İçerik | İndeks |
|---|---|---|
| **business-rule/** | İş kuralı **aksiyon konfig ailesi** — 3 alt grup: **`actions/`** (7 aksiyon şeması) · **`shared/`** (AssignValue · PropertyAppearance · koşul-değeri) · **`data-source/`** (dataset + fillDataSource kaynakları); `BusinessRule.configuration` JSONB alt-şemaları. | [`./business-rule/index.md`](./business-rule/index.md) |

*Oluşturma: 2026-08-25.*
