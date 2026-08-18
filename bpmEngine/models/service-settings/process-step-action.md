# Model — ProcessStepAction (adım-aksiyon binding)

> **Durum:** 🟡 TASLAK (ilk çıkarım — gözden geçirilecek)
> **Amaç:** Bir **aksiyonun bir adıma bağlanması**. Şablon (`Action`/ActionDto) alanları buraya **kopyalanır**;
> ayrıca adım-özel yönlendirme/yetki alanları tutulur.
> **Davranış/kullanım + veri aktarımı:** → `../../service-settings/process-step-action.md`

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Binding kaydı ID'si. |
| `processStepId` | int | FK → ProcessStep.id | Bağlı olduğu adım. |
| `targetProcessStepId` | int | FK → ProcessStep.id | Aksiyon çalışınca **ilerlenecek hedef adım**. |
| `changeStatusId` | int | FK → Status.id | Aksiyon sonrası atanacak **durum**. |
| `mergeParameter` | bool | — | **Parametre birleştirme.** `true` ise aksiyon, hedefe taşıdığı `parameters`'a **bu adıma gelen parametreleri** de ekler (önce gelen `in`, sonra aksiyonun ürettiği `out`; **aynı anahtarda `out` ezer**). `false` (vars.) → yalnız aksiyonun kendi ürettiği parametreler taşınır. Davranış → `../../service-settings/process-step-action.md` §2.1. |
| `authorizationLevel` | — | — | **Yetki seviyesi** (aksiyonu kim yürütebilir). |
| `actionDisplayAuthorizedUserGroupId` | int | FK → UserGroup | Aksiyonu **görebilecek** kullanıcı grubu. |
| `environmentRestriction` | string | — | Ortam kısıtı. |

> Yukarıdakiler **binding-özel** (adıma bağlı) alanlardır. Aşağıdaki tablo, şablondan kopyalanan Action alanlarıdır (**bu sayfada tanımlı**).

### Şablondan kopyalanan alanlar (Action/ActionDto → bu sayfada tanımlı)
Adıma aksiyon eklenirken şablonun (`Action`) **`organizationId` dışındaki tüm alanları bir kez kopyalanır**
(→ [`../organization-settings/action.md`](../organization-settings/action.md)). Tanımları:

| Alan | Tip | Açıklama / amaç |
|---|---|---|
| `code` | string | Aksiyon kodu **ve yönlendirme tanımlayıcısı** (`default`/`onFail`/`true`/`false`/switch değeri…). Adım bu koda göre aksiyon seçer; **çeviri için kullanılmaz** → `translationCode`. |
| `definition` | string | Aksiyon adı/etiketi — **varsayılan dildeki** metin. |
| `translationCode` | string? | **Çeviri eşleşme anahtarı** (→ [`../organization-settings/translation.md`](../organization-settings/translation.md) `code`). `null` = doğrudan `definition`. |
| `icon` | string | İkon. |
| `styleId` | int (FK → Style) | Renk/görünüm (bg + font). |
| `actionType` | ActionType | Aksiyonun **türü** (`manual`/`eventForm`/`takePhoto`/`selectFile`/`scanBarcode`/`webhook`/`autoAction`) → [`../enums/action-type.md`](../enums/action-type.md). |
| `validation` | bool | Aksiyon öncesi **form validasyonu** gerekli mi. |
| `stayOnPage` | bool | Aksiyon sonrası **sayfada kal**. |
| `showInHistory` | bool | Aksiyon, kullanıcının geçmiş görüntülemesinde **görünsün** mü. |
| `showHistory` | bool | Aksiyon **tamamlanınca** kullanıcıya **akış tarihçesini otomatik göster**. |
| `actionDisplayType` | ActionDisplayType | Görünürlük (`invisible`/`everywhere`/`onlyFormDetail`/`onlyFastApprove`) → [`../enums/action-display-type.md`](../enums/action-display-type.md). |

Kopya **çeviri anahtarını da taşır** — binding etiketi aktif dile çözülür; `translationCode` `null` ise `definition` kullanılır.
**Canlı bağ/FK yoktur** (`actionId` tutulmaz): kopyadan sonra ProcessStepAction ile Action **bağımsızdır** — Action
değişince bu binding güncellenmez, binding değişince Action etkilenmez. _(`Action` = havuz şablonu; farkı yalnız `organizationId` +
şablon kimliği.)_

## İki ayrı katman (önemli)
- **Aksiyon kodu (`code`)** = adımın **hangi aksiyonu** tetikleyeceğini seçer (`default`/`onFail`/`true`/`false`/switch/HTTP `response.action`).
- **`targetProcessStepId`** = tetiklenen aksiyonun **hangi adıma** ilerleyeceğini belirler.

## İlişkiler
- **N – 1** → `ProcessStep` (`processStepId`, `targetProcessStepId`), `Status` (`changeStatusId`).
- **Action:** yalnız **kopya kaynağı** (oluşturmada alanlar kopyalanır); **FK/canlı bağ tutulmaz** (bkz. yukarıda).

## Notlar / açık noktalar
- `changeList` öğe yapısı, `action` nesnesi şekli, `action` zinciri döngü koruması → `../../todo.md`.

*Oluşturma: 2026-07-02.*
