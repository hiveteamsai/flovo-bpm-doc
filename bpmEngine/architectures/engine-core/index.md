# Engine Core — Motor Çalışma Prensibi (İndeks)

> **Amaç:** Motorun **ne olduğu ve nasıl çalıştığı** — tüm tasarım dokümanlarının üst çerçevesi. Runtime ayrıntısı → [`../engine-runtime/index.md`](../engine-runtime/index.md).

| Dosya | İçerik |
|---|---|
| [`flovo-bpm-engine.md`](./flovo-bpm-engine.md) | **Çalışma prensibi:** temel kavramlar & bileşenler (§1) · orkestrasyon vs yürütme (§2, ÇÖZÜLDÜ v0.40 → runtime) · **veri modeli & akışı — koleksiyon-tabanlı `ActionTransfer`** (§3) · yürütme algoritması: adım + aksiyonla ilerleme, `changeList` giriş kuralı, otomatik vs insan-tetiklemeli, paralel dallanma kararı (§4) · tetikleme & zamanlama (§5) · bekle/devam et, timeout, aksiyon yanıtı (§6) · hata yönetimi özeti (§7) · kalıcılık, ölçekleme, güvenlik, AI (§8–§11) · açık kararlar (§12). |

*Oluşturma: 2026-09-10 (v0.48).*
