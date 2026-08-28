# Process Step Settings — Tipe-Özel Ayar Şemaları (İndeks)

> **Durum:** 🟢 DETAYLANIYOR (v0.38) — `stepType`-başına `ProcessStep.settings` (JSONB) ayar şeması.
> **Amaç:** Her `stepType` için o adımın **tipe-özel ayarlarını** tek tek tanımlar: alanlar · tip · zorunluluk · varsayılan ·
> kısıt + alt-modeller + **JSON Schema**. Backend `settings` **doğrulama kapısının** ve tasarımcı **akış editörünün** girdisidir.
> **Kaynak (§3 ham tablolar):** [`../../process-step.md`](../../process-step.md) §3 · **davranış (22 adım):**
> [`../../../../service-settings/process-step.md`](../../../../service-settings/process-step.md) §3 · **ayrımlayıcı enum:** [`../../../enums/process-step-type.md`](../../../enums/process-step-type.md).

## Property settings'ten farkları (adım özgü)
| Konu | Property (`property-settings/`) | Process Step (bu klasör) |
|---|---|---|
| Ayrımlayıcı | `propertyType` | `stepType` |
| Profil-bazlı katman | Var (`ProcessViewProfilePropertySetting`) | **Yok** — adımın profil ayarı yoktur |
| Referans id'ler | Çoğu **çekirdek kolon** (FK) | **`settings` içinde** (`propertyId`/`userGroupId`/`targetPropertyId`…) — DB FK'si değil, **uygulama-katmanı** doğrulaması + silme koruması |
| Akış yönlendirme | — | `true`/`false`/`default`/case **`settings`'te değil**, `ProcessStepAction.targetProcessStepId`'de (→ [`../../process-step-action.md`](../../process-step-action.md)) |

## Ortak (settings'e girmeyen) alanlar
Her adımın kimlik/yaşam-döngüsü alanları (`code`·`stepType`·`definition`·`order`·`icon`·`showInHistory`·`skipIfPreApproved`·
`skipIfUserProcessStarter`·`skipWithThisProcessStepActionId`·`environmentRestriction`) **`ProcessStep` kolonlarındadır**, `settings`'te değil
(→ [`../../process-step.md`](../../process-step.md) §1). Bu dosyalar yalnız **tipe-özel `settings` JSONB'sini** tanımlar.

## Ortak kurallar
- Her `settings` JSON Schema **`additionalProperties: false`**.
- `settings` içindeki **referans id'ler** DB FK'si değildir → uygulama-katmanı doğrulaması + silme koruması (→ [`../../../../todo.md`](../../../../todo.md)).
- Değer-kaynağı alanları **ValueAssignType** ailesini kullanır (`fixedValue`/`propertyValue`/`fromCalculation`).

## Tip dizini (22 stepType → 20 dosya)
| stepType | Adım | Ayar modeli / durum | Dosya |
|---|---|---|---|
| `httpRequest` | HTTP Request | `ProcessStepHttpRequestSettings` | [`http-request.md`](./http-request.md) |
| `flovoAi` | Flovo AI | `ProcessStepFlovoAiSettings` (açık: selectedAi/aiSettings/fileSourceType) | [`flovo-ai.md`](./flovo-ai.md) |
| `valueAssignment` | Değer Atama | `ProcessStepValueAssignmentSettings` | [`value-assignment.md`](./value-assignment.md) |
| `customIdCreator` | Custom ID Creator | `ProcessStepCustomIdCreatorSettings` | [`custom-id-creator.md`](./custom-id-creator.md) |
| `comparison` | Karşılaştırma | `ProcessStepComparisonSettings` (recursive koşul) | [`comparison.md`](./comparison.md) |
| `switch` | Switch | `ProcessStepSwitchSettings` (`propertyId`) | [`switch.md`](./switch.md) |
| `instanceDeleter` | Instance Deleter | `ProcessStepInstanceDeleterSettings` | [`instance-deleter.md`](./instance-deleter.md) |
| `instanceCreator` | Instance Creator | `ProcessStepInstanceCreatorSettings` | [`instance-creator.md`](./instance-creator.md) |
| `notification` | Bildirim | `ProcessStepNotificationSettings` (mesaj+alıcı alt-modelleri) | [`notification.md`](./notification.md) |
| `timer` · `timerStart` · `timerEnd` | Timer ailesi | `ProcessStepTimerSettings` (timeout bloğu olarak da kullanılır) | [`timer.md`](./timer.md) |
| `processing` | Processing | `ProcessStepProcessingSettings` (`showLoading`) | [`processing.md`](./processing.md) |
| `processStart` | Süreç Başlangıcı | `ProcessStepProcessStartSettings` (`userGroupId`) | [`process-start.md`](./process-start.md) |
| `user` | Kullanıcı | `ProcessStepUserSettings` (human-task) | [`user.md`](./user.md) |
| `userGroup` | Kullanıcı Grubu | `ProcessStepUserGroupSettings` (human-task) | [`user-group.md`](./user-group.md) |
| `parentInstanceUser` | Üst Form Kullanıcı | `ProcessStepParentInstanceUserSettings` (üstten devralır) | [`parent-instance-user.md`](./parent-instance-user.md) |
| `processEnd` | Süreç Bitişi | `ProcessStepProcessEndSettings` | [`process-end.md`](./process-end.md) |
| `subProcessStart` | Alt Süreç Başlangıcı | **ayarsız** (`settings = {}`) | [`sub-process-start.md`](./sub-process-start.md) |
| `subProcessEnd` | Alt Süreç Bitişi | **ayarsız** (`settings = {}`) | [`sub-process-end.md`](./sub-process-end.md) |
| `triggerProcessStep` | Süreç Adımı Tetikleme | **ertelendi** (modellenmedi → todo) | [`trigger-process-step.md`](./trigger-process-step.md) |
| `formRedirect` | Form Yönlendirme | **ertelendi** (modellenmedi → todo) | [`form-redirect.md`](./form-redirect.md) |

> _(Dosyalar oluşturuldukça link eklenir. `timer.md` üç `stepType`'ı birlikte kapsar; `timeout` bloğu `user`/`userGroup` içinde gömülü kullanılır.)_

*Oluşturma: 2026-08-28.*
