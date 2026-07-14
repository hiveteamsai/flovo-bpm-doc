# Redis — Cache & Ephemeral Katman (Flovo iBPM v2)

> **Rol:** Geçici (ephemeral) hızlı erişim katmanı — cache, oturum/rate-limit, anlık bildirim tamponu; **kalıcı veri veya kuyruk değil**.
> **Karar:** Redis · ✅ canlı (Sprint 2 S2.8 notification BE) · tam gerekçe → [`../research/tech-stack/tech_rating.md`](../research/tech-stack/tech_rating.md)

## Ne için kullanıyoruz?

Redis, **kaybı tolere edilebilir, hızlı, geçici** veriler için kullanılır. BPM'de tipik kullanım:

- **Cache** — sık okunan ama nadir değişen veri (metadata/servis tanımı, çeviri sözlüğü, projeksiyon-hazır sinyalleri).
- **Bildirim (notification) tamponu** — kullanıcıya anlık bildirim akışı için hafif ara katman (Sprint 2 S2.8).
- **Oturum / rate-limit / kilit** — kısa ömürlü sayaç ve dağıtık kilitler.

## Sürüm & bileşenler

| Bileşen | Karar | Not |
|---|---|---|
| Redis | ✅ canlı | Notification BE'de kullanımda (S2.8) |
| Kalıcılık | Ephemeral öncelikli | Kalıcı iş kuyruğu **değil** |

## Projemizde kullanım

- **Bildirim BE:** üretilen bildirimlerin kullanıcıya iletilene kadar hızlı tamponlanması; gerçek gerçek-zamanlı push NATS/WS ile.
- **Cache:** metadata/servis-tanımı ve çeviri (`translation`) çözümlemesi gibi tekrar eden okumaların hızlandırılması —
  özellikle [`property-value-storage`](../research/property-value-storage/index.md)'daki dile-bağlı gösterim (S6) join yükünü
  azaltmak için opsiyonel `(code→isim)` per-dil cache adayı.
- **Rate-limit / kilit:** Customer API çağrılarında ve tekil iş tetiklemelerinde kısa ömürlü koruma.

## Konfigürasyon / desen notları

- **NET SINIR — Redis ≠ kuyruk/outbox.** Kalıcı, sıralı, replay-edilebilir olay akışı (**Outbox → projeksiyon** omurgası) **NATS
  JetStream**'dedir (bkz. [`nats-jetstream.md`](./nats-jetstream.md), D9). Redis yalnız **cache + ephemeral** rolündedir. İki
  teknolojinin **rolleri ayrık**, çakışma yoktur.
- Cache'lenen değer **kaynak-hakikat değildir**; kaybı halinde Postgres'ten/NATS'ten yeniden üretilir → cache invalidation basit tutulur.
- Bildirim akışında **at-most-once** kabul edilebilir; kayıp kritik değildir (kritik olan kalıcılık NATS/Postgres'te).

## İlişkili tasarım

- [`nats-jetstream.md`](./nats-jetstream.md) — kalıcı olay/kuyruk (Redis'in **yapmadığı** iş).
- [`postgresql.md`](./postgresql.md) — kaynak-hakikat (cache'in beslendiği yer).
- [`../research/tech-stack/tech_rating.md`](../research/tech-stack/tech_rating.md) — "Redis rolü netleştirilmeli" açık notu (bu doküman onu belgeler).

## Dikkat / açık noktalar

- **Rol sınırı belgelenmeli (açık not — tech_rating):** ekip içinde "kuyruk için Redis mi NATS mi?" karışıklığını önlemek için
  kural nettir: **kalıcılık gereken her şey NATS/Postgres, yalnız ephemeral Redis.**
- Bildirim ölçeğinde (çok kullanıcı) Redis bellek kullanımı izlenmeli; kalıcı bildirim geçmişi gerekiyorsa o Postgres'e yazılır.
