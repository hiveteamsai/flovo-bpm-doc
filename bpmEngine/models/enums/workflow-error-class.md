# Enum — WorkflowErrorClass

> **Kullanan model:** [`../processInstances/workflow-event.md`](../processInstances/workflow-event.md) — `stepFailed.payload.errorClass` · [`../processInstances/workflow-projection.md`](../processInstances/workflow-projection.md) — `lastError.errorClass`
> **Amaç:** Bir adım hatasının **retry edilebilir olup olmadığını** ve yönlendirmesini belirleyen sınıf. Sınıflandırma kuralları
> (HTTP status → sınıf, ifade hatası → sınıf …) → [`../../engine-runtime-errors.md`](../../engine-runtime-errors.md) §1.
> **Durum:** 📝 TASLAK v0.44 — onay bekliyor.

## Değerler
| Değer | Anlam | Örnek | Motor davranışı |
|---|---|---|---|
| `transient` | **Geçici** — tekrar denenirse geçebilir | HTTP 5xx / 408 / 429 / bağlantı zaman aşımı · DB deadlock / lock timeout · NATS publish hatası | **Retry** (backoff); tükenirse `permanent` gibi |
| `permanent` | **Kalıcı iş/veri hatası** — tekrar aynı sonucu verir | HTTP 4xx (408/429 hariç) · response şema uyumsuz · ifade hatası (`null` bölme, tip) · `changeList` JSON Schema reddi · atama çözülemedi (yönetici boş) | Retry **yok** → `onFail` → yoksa `failed` |
| `design` | **Tasarım hatası** — süreç tanımı bozuk | Aksiyonun `targetProcessStepId` eksik/arşivlenmiş · seçilen aksiyon kodu adımda yok · `settings` şeması geçersiz · `onFail` hedefi kendisi | Retry **yok** → `onFail` (geçerliyse) → yoksa `failed`; **admin alarmı** (designer'a) |
| `inDoubt` | **Şüpheli yan etki** — deneme başladı, sonucu bilinmiyor (worker çöktü) | `stepStarted` var, `stepCompleted`/`stepFailed` yok; redelivery geldi | Adım tipi **idempotent** ise yeniden koş; değilse `permanent` gibi (admin karar verir) |
| `guard` | **Koruma sınırı** aşıldı | ardışık otomatik adım limiti · toplam adım limiti · alt süreç derinliği · ServiceTrigger kaskad | Retry **yok** → `failed` (onFail'e **gitmez** — döngü onFail'de de sürebilir) |

## Notlar
- `transient` dışındaki tüm sınıflar **retry sayacını tüketmez** — anında yönlendirme.
- Sınıf, hatayı üreten **adım tipi yürütücüsü** tarafından belirlenir; belirlenemeyen (bilinmeyen exception) → `transient` sayılır (**tek** ek deneme ile), sonra `permanent`.

*Oluşturma: 2026-08-31.*
