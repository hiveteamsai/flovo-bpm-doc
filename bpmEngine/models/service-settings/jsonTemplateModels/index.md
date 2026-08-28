# Servis Ayarları — JSON Template Modelleri — İndeks

> **Amaç:** Bu klasör, **DB tablosu OLMAYAN** — yalnız **JSON** olarak taşınan/saklanan — model ve şema tanımlarını toplar:
> bir alanın JSONB gövdesi, adımlar arası taşınan veri paketi, ya da bir **JSONB kolonun tipe-özel şeması**.
>
> **Genel kural (proje geneli):** `models/` altında bir model **DB tablosu değilse** (JSONB gövde · adımlar arası paket ·
> bir JSONB kolonun tipe-göre değişen şeması), tanımı ilgili kırılımın **`jsonTemplateModels/`** klasörüne konur. **DB
> tabloları** eskisi gibi kendi kırılımlarında (ör. `service-settings/`) kalır.

## Dökümanlar
| Döküman | Özet |
|---|---|
| [`action-transfer.md`](./action-transfer.md) | Aksiyon tetiklendiğinde sonraki adıma taşınan **veri aktarım paketi** (`parameters` / `changeList` / `action`); `ProcessStepInstance.processStepActionParameter`'da JSON olarak saklanır. |

## Alt klasörler
| Klasör | İçerik | İndeks |
|---|---|---|
| **business-rule/** | İş kuralı **aksiyon konfig ailesi** — 3 alt grup: **`actions/`** (7 aksiyon şeması) · **`shared/`** (AssignValue · PropertyAppearance · koşul-değeri) · **`data-source/`** (dataset + fillDataSource kaynakları); `BusinessRule.configuration` JSONB alt-şemaları. | [`./business-rule/index.md`](./business-rule/index.md) |
| **property-settings/** | **Tip-başına `Property.settings` (JSONB) ayar şeması** — 18 `propertyType` için tipe-özel ayar alanları + kısıt + **JSON Schema**; backend doğrulama kapısı + frontend form-üreticisinin girdisi. | [`./property-settings/index.md`](./property-settings/index.md) |
| **process-step-settings/** | **Tip-başına `ProcessStep.settings` (JSONB) ayar şeması** — 22 `stepType` için tipe-özel ayar alanları + alt-modeller + **JSON Schema**; backend doğrulama kapısı + akış editörünün girdisi. | [`./process-step-settings/index.md`](./process-step-settings/index.md) |

*Oluşturma: 2026-08-25. Güncelleme: 2026-08-28 — `dto/` → `jsonTemplateModels/` (JSON-only model/şema ailesi); `property-settings/` eklendi.*
