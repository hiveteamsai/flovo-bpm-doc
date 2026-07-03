# Flovo BPM — Yeni Proje Tasarım Dokümanları (İndeks)

> Yeni Flovo BPM motorunun tasarım dokümanları. Ayarlar, uygulamadaki gibi **iki gruba** ayrıldı:
> **genel ayarlar** (tüm servislerde kullanılan) ve **servis ayarları** (bir servise bağlı).

---

## 📁 Yapı

### `genel-ayarlar/` — Genel Ayarlar (tüm servislerde kullanılır)
Bu özellikler servisten bağımsızdır; bir kez tanımlanır, tüm servislerde kullanılır.
| Doküman | İçerik |
|---|---|
| [`action.md`](./genel-ayarlar/action.md) | **Aksiyon şablonu** (model: `ActionDto`) — yeniden kullanılabilir aksiyon tanımı; adıma eklenince kopyalanır. |
| [`style.md`](./genel-ayarlar/style.md) | **Style** — renk/görünüm varlığı (bg + font); **aksiyon/durum'da** kullanılır (form alanları kullanmaz). |
| [`status.md`](./genel-ayarlar/status.md) | **Durum (status)** — kaydın aşaması (etiket). |
| [`translation.md`](./genel-ayarlar/translation.md) | **Çeviri (translation)** — `code`-bazlı çok dilli metinler; ortak (Flovo) + organizasyon çevirileri, override çözümlemesi. |
| [`organization.md`](./genel-ayarlar/organization.md) | **Organizasyon (tenant)** — Flovo'yu kullanan kurum; kullanıcı/servis/çevirilerin üst kapsayıcısı. |

### `servis-ayarlari/` — Servis Ayarları (bir servise bağlı)
Her servisin (formun) kendine ait ayarları.
| Doküman | İçerik |
|---|---|
| [`process-step.md`](./servis-ayarlari/process-step.md) | **Süreç adımları** — adım tipleri katalogu (19 adım) + ortak yapı. |
| [`process-step-action.md`](./servis-ayarlari/process-step-action.md) | **Süreç adımı aksiyonu** — aksiyonun adıma bağlanması (binding), veri aktarımı (`parameters`/`changeList`/`action`), actionType kataloğu. |
| [`properties.md`](./servis-ayarlari/properties.md) | **Form alanları (property)** — alan tipleri (19) + ortak çekirdek. |
| [`work-rule.md`](./servis-ayarlari/work-rule.md) | **İş kuralları** — frontend realtime form davranışı (koşul→aksiyon). |
| [`view-profile.md`](./servis-ayarlari/view-profile.md) | **Görüntüleme profilleri** — formun adım-bazlı görünümü (görünür/düzenlenebilir/zorunlu). |

### Kök (motor & referans)
| Doküman | İçerik |
|---|---|
| [`flovo-bpm-engine.md`](./flovo-bpm-engine.md) | **Motor çalışma prensibi** — mimari + yürütme algoritması (adımları nasıl çalıştırır). |
| [`flovo-customer-api.md`](./flovo-customer-api.md) | **Flovo Customer API** — custom code için sağlanacak API (endpoint listesi + teorik iş). |
| [`todo.md`](./todo.md) | **Açık sorular / TODO** — tüm dokümanlardaki açık kararlar, **önceliklendirilmiş** tek liste (Tier 0–3). |
| [`models/`](./models/models.md) | **Veri modelleri (şema referansı)** — model dizini + ilişki haritası ([`models.md`](./models/models.md)) ve her model için alan-düzeyi ayrıntı dosyası. |
| [`sampleProcess/`](./sampleProcess/sampleProcess.md) | **Örnek süreçler** — uçtan uca, görselli self-servis süreç örnekleri. |
| [`research/compare/`](./research/compare/) | **Karşılaştırmalar** — hedef uygulama ↔ diğer platformlar farkları + başarılı/başarısız değerlendirmesi. |
| `research/n8n/` | n8n referans/ilham analizleri. |
| `research/current-flovo-bpm-engine/` | Mevcut (eski) Flovo BPM dökümanı (yalnız referans). |

**`research/compare/` içeriği**
| Doküman | İçerik |
|---|---|
| [`new-vs-current.md`](./research/compare/new-vs-current.md) | **Yeni vs mevcut Flovo** — eski uygulamayla farklar (ne eklendi/çıkarıldı/yeniden adlandırıldı) + başarılı/başarısız. |
| [`new-vs-n8n.md`](./research/compare/new-vs-n8n.md) | **Yeni Flovo vs n8n** — motor/adım/veri/AI kıyası + başarılı/başarısız değerlendirmesi. |

---

## İki katman (hatırlatma)
- **Form-mantığı (frontend realtime):** property · görüntüleme profili · iş kuralı.
- **Akış-mantığı (motor):** süreç adımı · aksiyon · durum.
- Detay → [`flovo-bpm-engine.md`](./flovo-bpm-engine.md) §1.

---

> **Not:** Yeni-uygulama dökümanları **kendi başına** yeni uygulamayı anlatır; eski uygulamayla **farklar yalnız**
> `research/compare/new-vs-current.md`'de tutulur.

*Oluşturma: 2026-06-30.*
