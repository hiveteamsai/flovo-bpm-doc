# Model — ProcessStepAction (adım-aksiyon binding)

> **Durum:** 🟡 TASLAK (ilk çıkarım — gözden geçirilecek)
> **Amaç:** Bir **aksiyonun bir adıma bağlanması**. Şablon (`Action`/ActionDto) alanları buraya **kopyalanır**;
> ayrıca adım-özel yönlendirme/yetki alanları tutulur.
> **Davranış/kullanım + veri aktarımı:** → `../servis-ayarlari/process-step-action.md`

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Binding kaydı ID'si. |
| `processStepId` | int | FK → ProcessStep.id | Bağlı olduğu adım. |
| `targetProcessStepId` | int | FK → ProcessStep.id | Aksiyon çalışınca **ilerlenecek hedef adım**. |
| `changeStatusId` | int | FK → Status.id | Aksiyon sonrası atanacak **durum**. |
| `authorizationLevel` | — | — | **Yetki seviyesi** (aksiyonu kim yürütebilir). |
| `actionDisplayAuthorizedUserGroupId` | int | FK → UserGroup | Aksiyonu **görebilecek** kullanıcı grubu. |
| `showInHistory` | bool | — | Süreç geçmişinde göster. |
| `environmentRestriction` | string | — | Ortam kısıtı. |

### Şablondan kopyalanan alanlar (Action/ActionDto)
Adıma aksiyon eklenirken **bir kez kopyalanır**: `code` · `definition` · `icon` · `styleId` · `actionType` (→ `action.md`).
**Canlı bağ/FK yoktur** (`actionId` tutulmaz): kopyadan sonra ProcessStepAction ile Action **bağımsızdır** — Action
değişince bu binding güncellenmez, binding değişince Action etkilenmez.

## İki ayrı katman (önemli)
- **Aksiyon kodu (`code`)** = adımın **hangi aksiyonu** tetikleyeceğini seçer (`default`/`onFail`/`true`/`false`/switch/HTTP `response.action`).
- **`targetProcessStepId`** = tetiklenen aksiyonun **hangi adıma** ilerleyeceğini belirler.

## İlişkiler
- **N – 1** → `ProcessStep` (`processStepId`, `targetProcessStepId`), `Status` (`changeStatusId`).
- **Action:** yalnız **kopya kaynağı** (oluşturmada alanlar kopyalanır); **FK/canlı bağ tutulmaz** (bkz. yukarıda).

## Notlar / açık noktalar
- `changeList` öğe yapısı, `action` nesnesi şekli, `action` zinciri döngü koruması → `../todo.md`.

*Oluşturma: 2026-07-02.*
