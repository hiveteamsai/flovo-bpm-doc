# Enum — ProcessStepType

> **Kullanan model:** [`process-step.md`](../service-settings/process-step.md) — alan `stepType`, tip **ProcessStepType**
> **Amaç:** Bir süreç adımının **tipini** belirler; tipe-özel ayarların (**process-step §2**) hangi şekilde yorumlanacağını
> söyleyen **ayrımlayıcı** (discriminator). Motor ve tasarımcı, `settings`'i bu değere göre okur.
> **Adım kataloğu (davranış):** → [`../../service-settings/process-step.md`](../../service-settings/process-step.md) §3 (22 adım).

## Değerler
| Değer | Anlam (adım) | Ne için |
|---|---|---|
| `processStart` | Süreç Başlangıcı | Ana sürecin giriş düğümü (servis başına 1 zorunlu). |
| `httpRequest` | HTTP Request | Dış endpoint'e HTTP isteği (otomatik). |
| `flovoAi` | Flovo AI | Flovo AI çalıştırıp parametre üretme (otomatik). |
| `valueAssignment` | Değer Atama | Property'ye / alt-servise sabit ya da hesaplanan değer atama. |
| `triggerProcessStep` | Süreç Adımı Tetikleme | Alt-servislerin süreç adımlarını tetikleme. |
| `notification` | Bildirim | Mail / Push / Toast bildirim gönderme. |
| `timer` | Timer | Süreçten bağımsız zamanlayıcı; süre dolunca ilerler. |
| `timerStart` | Timer Start | Seçili timer'ın süresini başlatır. |
| `timerEnd` | Timer End | Başlatılmış timer'ı sonlandırır. |
| `instanceDeleter` | Instance Deleter | Formu siler (ör. `deleted` durumuna çeker). |
| `customIdCreator` | Custom ID Creator | Özel formatlı benzersiz ID üretir. |
| `instanceCreator` | Instance Creator | Yeni form/instance üretir (init değerlerle). |
| `comparison` | Karşılaştırma | Koşula göre `true`/`false` iki dallı yönlendirme. |
| `switch` | Switch | Alan değerine göre dallanma (default zorunlu). |
| `user` | Kullanıcı | Tek kullanıcı onayı (human task). |
| `userGroup` | Kullanıcı Grubu | Grup onayı (human task). |
| `parentInstanceUser` | Üst Form Kullanıcı | Atananları/görüntülemeyi **üst formdan (parent instance)** devralan human task (alt-servis). |
| `processEnd` | Süreç Bitişi | Sürecin son adımı. |
| `processing` | Processing | Forma döner ama beklemez; `default` ile otomatik ilerler. |
| `formRedirect` | Form Yönlendirme | Create öncesi var olan başka bir formu açma. |
| `subProcessStart` | Alt Süreç Başlangıcı | Bağımsız alt sürecin giriş düğümü (servis başına N). |
| `subProcessEnd` | Alt Süreç Bitişi | Bağımsız alt sürecin **son adımı** (Süreç Bitişi'nin alt-süreç karşılığı; kol burada sonlanır). |

## Notlar
- Değerler `service-settings/process-step.md §3`'teki **22 adım** kataloğuyla birebir eşleşir; katalog genişletilebilir
  (yeni adım tipi → yeni değer). _(Tier 0 "Genişletilebilirlik" → [`../../todo.md`](../../todo.md).)_
- `switch` ve `default` gibi değerler yalnız enum **kodu**dur; görünen ad "Anlam" sütunundadır.

*Oluşturma: 2026-07-16.*
