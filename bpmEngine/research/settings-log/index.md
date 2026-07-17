# Ayar Değişiklik Logu (Settings Log) — İndeks

> **Amaç:** Ayar sayfalarında yapılan **ekleme / güncelleme / silme** ve **toplu güncelleme** işlemlerinin
> **sayfa bazında** görüntülenebilen bir **denetim izi** olarak tutulması — depolama yöntemi, tablo modelleri ve
> log erişimi.
>
> **Durum:** 🟡 **Karar bekliyor** — [`../../todo.md`](../../todo.md) **Tier 1** "Denetim izi (audit) / loglama"
> maddesinin **ayar logu** kısmının girdisi. Henüz tasarıma (`models/` · `organization-settings/`) dahil **değildir**.

## Dökümanlar
| Döküman | İçerik |
|---|---|
| [`settings-log-design.md`](./settings-log-design.md) | **Tasarım** — kayıtların nasıl tutulacağı (tek generic tablo · JSONB delta · sayfa/aggregate bazlı · uygulama katmanı · append-only) · modeller (`SettingsLog` · `SettingsLogBatch` · `SettingsLogBatchPage` · `changes` şeması) · enum'lar (`SettingsPage` · `SettingsLogAction` · `SettingsLogSource` · `SettingsLogBatchStatus`) · log erişimi (sayfa bazlı görünüm · yetki · RLS izolasyonu · indeksler). |

## Kapsam notu
Bu klasör **yalnız ayar değişikliklerini** kapsar. `todo.md`'nin log maddesindeki diğer iki sınıf — **form/workflow
değeri geçmişi** (→ [`../property-value-storage/index.md`](../property-value-storage/index.md)) ve **sistem logları**
(observability) — ayrı doğadadır ve buraya dahil değildir.

## Onaylanınca nereye işlenecek
| Hedef | İçerik |
|---|---|
| `models/organization-settings/settings-log.md` | `SettingsLog` · `SettingsLogBatch` · `SettingsLogBatchPage` modelleri + `changes` şeması. |
| `models/enums/` (+ `index.md`) | `SettingsPage` · `SettingsLogAction` · `SettingsLogSource` · `SettingsLogBatchStatus`; ayrıca `http-method.md`'ye **`patch`** eklenmesi. |
| `organization-settings/settings-log.md` (+ `index.md`) | Davranış — sayfa bazlı görünüm · aktör/impersonation kuralı · snapshot kuralı · yazma yolu · yetki. |
| `flovo-customer-api.md` | **Ön koşul** — ayar yazma / toplu senkron ucu (bugün yok). |
| `todo.md` | Log maddesinin bölünmesi; ayar sınıfının kapanması; KVKK/saklama açık kalır. |

*Oluşturma: 2026-07-17.*
