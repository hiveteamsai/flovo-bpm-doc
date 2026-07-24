# Örnek Süreç — Yönlendirmeli Onay (referred) — İndeks

> **Amaç:** Webhook ile başlayan bir onay talebinin **Kontrol Grubu → (Yönlendir) Yönlendirilen Kullanıcı Atama →
> Yönlendirilen Kullanıcı → Yönetici (kullanıcının yöneticisi) → TransferUser Kontrol** döngüsünden geçip **Muhasebe**
> onayıyla kapandığı süreç. **Odak:** **`ProcessStepAction.mergeParameter`** — yönlendirme hedefi **`transferUser`**,
> onu **üretmeyen** adımlardan (Yönetici `Onayla`, TransferUser Kontrol `false`) da **taşınır** (gelen `in` korunur,
> `out` çakışmada ezer).

## Dökümanlar
| Döküman | Özet |
|---|---|
| [`referred.md`](./referred.md) | Yönlendirmeli onay: webhook başlatma → Form Creator → Kontrol Grup → (Yönlendir) **Değer Atama** → Yönlendirilen Kullanıcı (Onayla / Yönlendir / Onayla ve Yönlendir) → Yönetici → **TransferUser Kontrol** (`transferUser` boş mu? → Karşılaştırma) → Muhasebe Grup → Süreç Bitişi. Detaylı spec (amaç · diyagram · adım/ayar/aksiyon · **`transferUser` akışı + `mergeParameter`**). |

> **Görsel:** `referred.jpg` (yönlendirme zinciri + geri-gönderme/onay kolları + TransferUser Kontrol dallanması).
