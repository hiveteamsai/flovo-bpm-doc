# Architectures — Mimari Tasarım Dokümanları (İndeks)

> **Amaç:** Yeni Flovo BPM'in **mimari / işleyiş** dokümanları — motor çalışma prensibi, çalışma-zamanı mimarisi, kimlik & erişim, API yüzeyleri.
> Ayar davranışları → [`../organization-settings/`](../organization-settings/) · [`../service-settings/`](../service-settings/); şema → [`../models/index.md`](../models/index.md);
> örnekler → [`../sampleProcess/index.md`](../sampleProcess/index.md); araştırma → [`../research/index.md`](../research/index.md); teknoloji → [`../tech-stack/index.md`](../tech-stack/index.md).
> **Açık kararlar yalnız** [`../todo.md`](../todo.md) (MVP) · [`../todo-phase2.md`](../todo-phase2.md) (MVP-sonrası); tasarım ↔ inşa durumu → [`../implementation-status.md`](../implementation-status.md).

## Klasörler
| Klasör | İçerik | İndeks |
|---|---|---|
| `engine-core/` | Motor **çalışma prensibi** — kavramlar, bileşenler, veri modeli/akışı (koleksiyon-tabanlı), yürütme algoritması, tetikleme, bekle/devam, hata, kalıcılık, güvenlik, AI | [`engine-core/index.md`](./engine-core/index.md) |
| `engine-runtime/` | **Çalışma-zamanı mimarisi** — orkestrasyon ↔ yürütme (event-driven state machine, `workflow_events`), hata & dayanıklılık, zamanlayıcı & uyandırma, saklama/KVKK, runtime kararları & planı | [`engine-runtime/index.md`](./engine-runtime/index.md) |
| `login-auth/` | **Kimlik & erişim** — şifresiz OTP login akışı, çoklu-organizasyon, provisioning; token / refresh / oturum mekanizması | [`login-auth/index.md`](./login-auth/index.md) |
| `api/` | **API yüzeyleri** — Settings API (tasarım-zamanı ayar CRUD'u) · Customer API (dış custom code; ⏭️ MVP-sonrası) | [`api/index.md`](./api/index.md) |

## Okuma sırası (öneri)
1. [`engine-core/flovo-bpm-engine.md`](./engine-core/flovo-bpm-engine.md) → 2. [`engine-runtime/engine-runtime.md`](./engine-runtime/engine-runtime.md) (+ errors · scheduler · retention) →
3. [`login-auth/flovo-identity-access.md`](./login-auth/flovo-identity-access.md) → [`login-auth/flovo-auth-mechanism.md`](./login-auth/flovo-auth-mechanism.md) → 4. [`api/settings-api.md`](./api/settings-api.md).

*Oluşturma: 2026-09-10 (v0.48) — `bpmEngine/` kökündeki tasarım dokümanları konu klasörlerine taşındı.*
