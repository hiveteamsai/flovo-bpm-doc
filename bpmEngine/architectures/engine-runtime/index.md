# Engine Runtime — Çalışma-Zamanı Mimarisi (İndeks)

> **Amaç:** Motorun **çalışma-zamanı** tasarımı — orkestratör/worker/scheduler, `workflow_events` (Partial Event Sourcing), suspend/resume, hata & retry,
> zamanlayıcı & uyandırma, saklama/KVKK. Prensip → [`../engine-core/flovo-bpm-engine.md`](../engine-core/flovo-bpm-engine.md); runtime modelleri →
> [`../../models/processInstances/index.md`](../../models/processInstances/index.md) (`WorkflowEvent` · `WorkflowProjection` · `WorkflowTimer`); tek-sayfa anlatım/şema →
> [`../../research/engine-runtime/index.md`](../../research/engine-runtime/index.md).
> **Durum:** `engine-runtime.md` çekirdek karar (v0.40); **errors · scheduler · retention** 📝 v0.44 TASLAK — **kullanıcı incelemesi bekliyor**; kararlar/sorular `engine-runtime-plan.md`'de (R1–R17 · Q1–Q22).

| Dosya | İçerik | Durum |
|---|---|---|
| [`engine-runtime.md`](./engine-runtime.md) | **Runtime mimarisi:** event-driven state machine · orkestratör ↔ worker ↔ scheduler · `workflow_events` + projeksiyon · iki-TX otomatik adım · idempotency & optimistic concurrency · suspend/resume · `executionState`/`waitReason` · açık noktalar (§11) | 🟢 v0.40 (📝 v0.44 ekleri) |
| [`engine-runtime-errors.md`](./engine-runtime-errors.md) | **Hata & dayanıklılık:** hata sınıfları · retry politikası · `onFail` + `parameters.error` · dead-letter · admin kurtarma (retry/skip/cancel) · guard'lar | 📝 v0.44 TASLAK |
| [`engine-runtime-scheduler.md`](./engine-runtime-scheduler.md) | **Zamanlayıcı & uyandırma:** `WorkflowTimer` · timeout · cron/ServiceTrigger · lider seçimi · preemption | 📝 v0.44 TASLAK |
| [`engine-runtime-retention.md`](./engine-runtime-retention.md) | **Saklama · pruning · KVKK:** `workflow_events` partition/pruning · kişisel veri yolları · saklama politikası | 📝 v0.44 TASLAK |
| [`engine-runtime-plan.md`](./engine-runtime-plan.md) | **Kararlar (R1–R18) · açık sorular (Q1–Q23) · geliştirme planı** — inceleme çalışma dosyası; kesinleşince `../../todo.md`'ye taşınır | 🟡 çalışma dosyası |

*Oluşturma: 2026-09-10 (v0.48).*
