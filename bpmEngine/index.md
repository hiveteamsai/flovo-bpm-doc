# Flovo BPM — Yeni Proje Tasarım Dokümanları (İndeks)

> **Amaç:** Yeni Flovo BPM motorunun tüm tasarım/analiz dokümanlarının kök indeksi. Kökteki motor & referans dokümanları
> + alt klasörlere (ayarlar, modeller, örnekler, araştırma) giriş noktası.
>
> **İki katman (hatırlatma):** **Form-mantığı (frontend realtime)** = property · görüntüleme profili · iş kuralı;
> **Akış-mantığı (motor)** = süreç adımı · aksiyon · durum. Ayarlar, uygulamadaki gibi **genel ayarlar** (tüm servislerde)
> ve **servis ayarları** (bir servise bağlı) olarak ikiye ayrılır. Detay → [`flovo-bpm-engine.md`](./flovo-bpm-engine.md) §1.

## Dökümanlar
| Döküman | Özet |
|---|---|
| [`flovo-bpm-engine.md`](./flovo-bpm-engine.md) | **Motor çalışma prensibi** — BPM motorunun nasıl çalışacağı (mimari + yürütme algoritması); adımları nasıl çalıştırır. |
| [`flovo-customer-api.md`](./flovo-customer-api.md) | **Flovo Customer API** — müşterilerin **custom code** geliştirmesi için sağlanacak API servisi (endpoint + teorik iş). |
| [`todo.md`](./todo.md) | **Açık sorular / TODO** — tüm dokümanlardaki açık kararlar, önceliklendirilmiş tek liste (Tier 0–3). |

## Alt klasörler
| Klasör | İçerik (özet) | İndeks |
|---|---|---|
| **organization-settings/** | Tüm servislerde ortak **genel ayarların davranış/kullanım** dokümanları (action · style · status · translation · organization · permissions). | [`organization-settings/index.md`](./organization-settings/index.md) |
| **service-settings/** | Bir **servise bağlı ayarların davranış/kullanım** dokümanları (süreç adımı · adım aksiyonu · property · iş kuralı · görüntüleme profili). | [`service-settings/index.md`](./service-settings/index.md) |
| **models/** | **Veri modelleri (şema referansı)** — organizasyon ayarları, runtime, servis ayarları ve enum tanımları + ilişki haritası. | [`models/index.md`](./models/index.md) |
| **research/** | **BPM referansları + karşılaştırmalar + teknik araştırmalar** — yeni ↔ eski/n8n kıyasları, mevcut (eski) Flovo BPM analizi, n8n referansları ve **property value depolama mimarisi** (form value senaryoları + `form_attr` uygunluk değerlendirmesi). | [`research/index.md`](./research/index.md) |
| **sampleProcess/** | Uçtan uca, görselli **örnek süreçler** (self-servis). | [`sampleProcess/index.md`](./sampleProcess/index.md) |

---

> **Not:** Yeni-uygulama dökümanları **kendi başına** yeni uygulamayı anlatır; eski uygulamayla **farklar yalnız**
> `research/compare/new-vs-current.md`'de tutulur.

*Oluşturma: 2026-06-30. Güncelleme: index.md yapısına geçiş.*
