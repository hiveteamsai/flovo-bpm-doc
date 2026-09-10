# Flovo BPM — Yeni Proje Tasarım Dokümanları (İndeks)

> **Klasör yapısı (v0.48):** Kökte yalnız **`index.md` · `todo.md` (MVP) · `todo-phase2.md` (MVP-sonrası) · `implementation-status.md`** durur. Mimari tasarım
> dokümanları **[`architectures/`](./architectures/index.md)** altında konu klasörlerinde (her klasörün kendi `index.md`'si var): **`engine-core/`** (motor çalışma prensibi) · **`engine-runtime/`** (runtime mimarisi · hata/dayanıklılık ·
> zamanlayıcı · saklama/KVKK · runtime planı) · **`login-auth/`** (login akışı · auth/token mekanizması) · **`api/`** (Settings API · Customer API). Ayar davranışları
> `organization-settings/` · `service-settings/`, şema `models/`, örnekler `sampleProcess/`, referans/araştırma `research/`, teknoloji `tech-stack/`.

> **Amaç:** Yeni Flovo BPM motorunun tüm tasarım/analiz dokümanlarının kök indeksi. Kökteki motor & referans dokümanları
> + alt klasörlere (ayarlar, modeller, örnekler, araştırma) giriş noktası.
>
> **İki katman (hatırlatma):** **Form-mantığı (frontend realtime)** = property · görüntüleme profili · iş kuralı;
> **Akış-mantığı (motor)** = süreç adımı · aksiyon · durum. Ayarlar, uygulamadaki gibi **genel ayarlar** (tüm servislerde)
> ve **servis ayarları** (bir servise bağlı) olarak ikiye ayrılır. Detay → [`flovo-bpm-engine.md`](./architectures/engine-core/flovo-bpm-engine.md) §1.

## Dökümanlar
| Döküman | Özet |
|---|---|
| [`flovo-bpm-engine.md`](./architectures/engine-core/flovo-bpm-engine.md) | **Motor çalışma prensibi** — BPM motorunun nasıl çalışacağı (mimari + yürütme algoritması); adımları nasıl çalıştırır. |
| [`engine-runtime.md`](./architectures/engine-runtime/engine-runtime.md) | **Motor runtime mimarisi (ana spec)** — senkron yürütme döngüsünün event-driven (Go worker + NATS + Postgres event-sourcing) **state machine**'e çevrimi: orkestrasyon↔yürütme · durum · kalıcılık · idempotency/409 sözleşmesi · uyandırma. (flovo-bpm-engine §2.2/§8/§4.5 doldurma.) |
| [`engine-runtime-errors.md`](./architectures/engine-runtime/engine-runtime-errors.md) | 📝 **Hata & dayanıklılık** — hata sınıfları · retry (BPM timer) · in-doubt · `onFail` çözümleme · dead-letter/`failed` · admin kurtarma (retry/skip/cancel) · döngü/derinlik guard'ları · compensation (post-MVP). (v0.44, onay bekliyor.) |
| [`engine-runtime-scheduler.md`](./architectures/engine-runtime/engine-runtime-scheduler.md) | 📝 **Zamanlayıcı & uyandırma** — `WorkflowTimer` claim modeli (`SKIP LOCKED`, lider yok) · Timer/timeout/retry/cron yaşam döngüsü · preemption kuralı · TZ/DST/kaçırılan tetik · housekeeping. (v0.44, onay bekliyor.) |
| [`engine-runtime-retention.md`](./architectures/engine-runtime/engine-runtime-retention.md) | 📝 **Runtime verisi saklama · pruning · KVKK** — `workflow_events` sıcak/soğuk/arşiv katmanları (RANGE partition → MinIO) · pseudonymization (tombstone) · kısa-ömürlü tablolar. (v0.44, onay bekliyor.) |
| [`engine-runtime-plan.md`](./architectures/engine-runtime/engine-runtime-plan.md) | 🟡 **Motor runtime — kararlar (R1–R17) · açık sorular (Q1–Q22) · geliştirme planı** — bu konunun inceleme çalışma dosyası; kesinleşince `todo.md`'ye taşınır. |
| [`flovo-customer-api.md`](./architectures/api/flovo-customer-api.md) | ⏭️ **MVP-sonrası (v0.47).** **Flovo Customer API** — müşterilerin **custom code** geliştirmesi için sağlanacak API servisi (runtime veri: instance oku/yaz, webhook). |
| [`flovo-identity-access.md`](./architectures/login-auth/flovo-identity-access.md) | 🟡 **Kimlik & Erişim — login akışı** (v0.48): şifresiz **OTP** (e-posta/telefon) · kimlik ↔ `User` ↔ organizasyon · **çoklu-organizasyon seçimi/değiştirme** · provisioning (kayıt yok) · auth uçları · kenar durumlar. Kararlar → `todo.md` Tier 2 "Login / Auth". |
| [`flovo-auth-mechanism.md`](./architectures/login-auth/flovo-auth-mechanism.md) | 🟡 **Auth mekanizması** (v0.48): erişim token'ı **1 saat** · refresh **30 gün** (rotasyon) · org-kapsamlı claim şeması · yenileme/org değiştirme/logout/idle · backend doğrulama + RLS · OTP politikası · hata sözleşmesi · saklama (BFF) · Keycloak ayar özeti. |
| [`settings-api.md`](./architectures/api/settings-api.md) | **Flovo Settings API** — **tasarım-zamanı ayar CRUD'u** (service/property/step/view-profile/business-rule + org ayarları); `settings` doğrulama = tipe-özel JSON Schema. |
| [`implementation-status.md`](./implementation-status.md) | **Uygulama Durumu** — tasarım ↔ fiilen **inşa-edilen/dağıtılan** farkı: Bölüm-1 (design-time) **BUILT** + pilot **DEPLOYED** (Azure Container Apps + Vercel + Azure-PG + Keycloak); NATS/MinIO/Redis/K8s + Motor runtime = **tasarım hedefi**. |
| [`todo.md`](./todo.md) | **Açık sorular / TODO** — tüm dokümanlardaki açık kararlar, önceliklendirilmiş tek liste (Tier 0–3) — **MVP kapsamı**. |
| [`todo-phase2.md`](./todo-phase2.md) | ⏭️ **Faz 2 (MVP-sonrası) açık konular** — yetkilendirme detayı · vekalet `UserDelegate` · loglama · toplu senkron · `SchedulerJob` · Form List red akışı · Flovo AI · `triggerProcessStep`/`formRedirect` · Timer üçlüsü · ServiceTrigger · tik olayları · servis template · Customer API. |

## Alt klasörler
| Klasör | İçerik (özet) | İndeks |
|---|---|---|
| **organization-settings/** | Tüm servislerde ortak **genel ayarların davranış/kullanım** dokümanları (action · style · status · translation · organization · permissions). | [`organization-settings/index.md`](./organization-settings/index.md) |
| **service-settings/** | Bir **servise bağlı ayarların davranış/kullanım** dokümanları (süreç adımı · adım aksiyonu · property · iş kuralı · görüntüleme profili). | [`service-settings/index.md`](./service-settings/index.md) |
| **models/** | **Veri modelleri (şema referansı)** — organizasyon ayarları, runtime, servis ayarları ve enum tanımları + ilişki haritası. | [`models/index.md`](./models/index.md) |
| **tech-stack/** | **Kullanılacak teknolojiler (tasarım/kullanım)** — her teknoloji için projeye-özel kullanım dokümanı (PostgreSQL · Go · NATS · Next.js · Keycloak · MinIO · K8s · Redis · API contract · Python AI). *Karşılaştırma/karar: `research/tech-stack/`.* | [`tech-stack/index.md`](./tech-stack/index.md) |
| **research/** | **BPM referansları + karşılaştırmalar + teknik araştırmalar** — yeni ↔ eski/n8n kıyasları, mevcut (eski) Flovo BPM analizi, n8n referansları, **property value depolama mimarisi**, **ayar değişiklik logu (settings-log)** tasarımı, **teknoloji yığını karşılaştırma/kararları** (tech-stack) ve **motor runtime anlatımı** (engine-runtime — v0.44 taslak setinin özet+detay HTML'i). | [`research/index.md`](./research/index.md) |
| **sampleProcess/** | Uçtan uca, görselli **örnek süreçler** (self-servis). | [`sampleProcess/index.md`](./sampleProcess/index.md) |

---

> **Not:** Yeni-uygulama dökümanları **kendi başına** yeni uygulamayı anlatır; eski uygulamayla **farklar yalnız**
> `research/compare/new-vs-current.md`'de tutulur.

*Oluşturma: 2026-06-30. Güncelleme: index.md yapısına geçiş.*
