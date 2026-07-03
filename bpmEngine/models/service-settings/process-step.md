# Model — ProcessStep (süreç adımı)

> **Durum:** 🟡 TASLAK (ilk çıkarım — gözden geçirilecek)
> **Amaç:** İş akışındaki bir **düğüm/kutu**. Adımlar aksiyonlarla bağlanarak süreci oluşturur.
> **Davranış/kullanım + adım kataloğu (19 tip):** → `../../service-settings/process-step.md`

## 1. Ortak alanlar (her adımda)
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Adım ID'si. |
| `organizationId` | int | FK → Organization.id | Kiracı. |
| `serviceId` | int | FK → Service | Bağlı servis. |
| `code` | string | benzersiz | Adımın kodu. |
| `definition` | string | — | Adımın adı/tanımı. |
| `icon` | string | — | Adım ikonu. |
| `order` | int | — | Sıralama (sürükle-bırak). |
| `environmentRestriction` | string | — | Ortam kısıtı. |
| `hideInHistory` | bool | — | Süreç geçmişinde gizle. |
| `skipIfPreApproved` | bool | — | Önceden onaylanmışsa adımı atla. |
| `skipIfUserProcessStarter` | bool | — | Başlatan kullanıcıysa adımı atla. |
| `skipWithThisActionId` | int | — | Atlamayı tetikleyen aksiyon. **Referans tipi açık** (action `code` / `ProcessStepAction` / Action?) → `../../todo.md`. Not: Action **şablonuna canlı FK tutulmaz** (kopya modeli). |

## 2. Tipe-özel ayarlar (adım tipine göre — özet)
> Tam açıklama → `../../service-settings/process-step.md` §3. Örnek notable alanlar:

| Adım tipi | Notable ayarlar |
|---|---|
| HTTP Request | `endpoint` · `method` · `templateParameters` · `queryParameters` · `headers` · `body` · `returns` · `async` |
| Flovo AI | seçili AI + AI'a özel ayarlar · dosya kaynağı (thumbnail / file alanı) |
| Değer Atama | `valueType` (`FixedValue`/`PropertyValue`/`FromCalculation`) · `fixedValue` · `expression` · `useDisplay` · `targetPropertyId` · `propertyId` · (alt-servis) `useRelatedService`·`relatedServiceId`·`targetInstancesPropertyId` |
| Karşılaştırma | `conditions` · `conditionType` (VE/VEYA) · operatörler |
| Switch | seçili alan · değere göre eşleşen aksiyon (default zorunlu) |
| Bildirim | kanal (Mail/Push/Toast) · alıcılar · TR/EN başlık+mesaj · (Push/Toast) `parameters` |
| Timer / Timer Start / Timer End | süre stili (çalışma takvimi/normal/sabit) · `selectedTimerProcessStepId` |
| Custom ID Creator | `customId` · `targetPropertyId` · `createWithBarcode` · `targetFilePropertyId` |
| Form Creator | init değerleri (property↔`parameters` eşlemesi / thumbnail url) |
| Kullanıcı | `userType` · `stableUserId` · `processViewProfileId` · bildirim · timeout |
| Kullanıcı Grubu | `userGroupType` · `organizationUserGroupId` · `groupApproval` · profil · bildirim · timeout |
| Süreç Bitişi | `processViewProfileId` · `organizationUserGroupIds` |
| Processing | `showLoading` |

## İlişkiler
- **N – 1** → `Organization` (`organizationId`), `Service` (`serviceId`).
- **1 – N** ← `ProcessStepAction` (`processStepId`); ayrıca `ProcessStepAction.targetProcessStepId` → bu model.

## Notlar / açık noktalar
- `default action` kavramı; Timer yaşam döngüsü; Süreç Bitişi re-open; human-task ailesi; adım seti genişletilebilirliği → `../../todo.md`.
- **Not:** Tipe-özel ayarların ayrı alt-model mi yoksa gömülü mü tutulacağı gözden geçirilecek.

*Oluşturma: 2026-07-02.*
