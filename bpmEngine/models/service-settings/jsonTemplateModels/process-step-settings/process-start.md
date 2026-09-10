# Process Step Settings — `processStart` (Süreç Başlangıcı)

> **stepType:** `processStart` · **Adım:** **ana sürecin** giriş düğümü (servis başına **1 zorunlu**); altındaki başlangıç aksiyonlarının **kimlerce başlatılabileceğini** kısıtlar.
> **Davranış:** → [`../../../../service-settings/process-step.md`](../../../../service-settings/process-step.md) §3.1 · **Model (§3):** [`../../process-step.md`](../../process-step.md) §3.14 · **İndeks:** [`index.md`](./index.md).
> **Depolama:** `ProcessStep.settings` (JSONB), ayrımlayıcı `stepType`.

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `userGroupId` | int? | hayır | `null` | Süreci **manuel** başlatabilecek **kullanıcı grubu** (UserGroup id'si; `settings` içi mantıksal referans, DB FK'si değil). **`null` → herkes** başlangıç aksiyonlarını görüntüleyebilir ve süreci başlatabilir; **dolu → yalnız o gruptaki** kullanıcılar. |

> **`userGroupId` kısıtının davranışı (KARAR) — manuel ↔ webhook farkı:**
> - **Manuel (frontend) başlatma:** **görünürlük = tetikleme yetkisi.** `userGroupId` **dolu** ise başlangıç aksiyonları **yalnız o gruptaki** kullanıcıların "başlatılabilir" listesinde **görünür**; **grup dışı kullanıcı bu aksiyonları görmez** (ayrı "görür ama tetikleyemez" durumu **yoktur**). **Boş** ise herkes görür ve başlatır.
> - **Webhook / Customer API başlatma:** Kısıt **yalnız manuel** başlatıma özgüdür. Dış tetikleme bir kullanıcı değil **`ApiKey`** ile kimliklendirildiğinden `userGroupId` **uygulanmaz** — dış erişim yetkisi **ayrı katmandadır** (→ [`../../../../architectures/api/flovo-customer-api.md`](../../../../architectures/api/flovo-customer-api.md)). Başlatan → `ProcessInstance.createdByApiKeyId`.

> **Akış yönlendirme `settings`'te DEĞİL:** Süreci hangi başlangıç aksiyonunun ilerlettiği (manuel aksiyon veya webhook) ve o aksiyonun hedefi, adıma bağlı `ProcessStepAction`'lardadır (`targetProcessStepId`) → [`../../process-step-action.md`](../../process-step-action.md). Süreç Başlangıcı **1'den fazla** başlangıç aksiyonu barındırabilir (manuel ve/veya webhook).

## 2. Alt-modeller
Yok — `settings` tek opsiyonel referans alandan ibarettir.

## 3. Ortak alanlar (settings'te değil — `ProcessStep` kolonu)
`code`·`stepType`·`definition`·`order`·`showInHistory`·`skip*`·`environmentRestriction` → [`../../process-step.md`](../../process-step.md) §1.

## 4. JSON Schema
```json
{
  "$id": "process-step-settings/processStart",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "userGroupId": { "type": ["integer", "null"], "default": null }
  }
}
```
> Not: `userGroupId`'nin var-olan bir `UserGroup`'u işaret etmesi **uygulama-katmanı** doğrulamasıdır (DB FK'si değil); grup silinmeden önce "bunu kullanan Süreç Başlangıcı var mı?" denetimi de uygulama tarafındadır.

## 5. Örnek
**a) Herkes başlatabilir (kısıtsız):**
```json
{ "userGroupId": null }
```
**b) Yalnız seçili grup manuel başlatabilir:**
```json
{ "userGroupId": 5 }
```

*Oluşturma: 2026-08-28.*
