# NATS + JetStream — Mesajlaşma & Event Omurgası (Flovo iBPM v2)

> **Rol:** Servisler arası **olay taşıma**, **realtime bildirim** ve — en kritik — **CQRS projeksiyon senkronizasyonunun (Outbox → projektör) kalıcı omurgası**.
> **Karar:** NATS **2.10** + JetStream · ✅ canlı (F-Infra SI.5) · tam gerekçe/karşılaştırma → [`../research/tech-stack/tech_rating.md`](../research/tech-stack/tech_rating.md)

## Ne için kullanıyoruz?

NATS, Flovo'da **üç işi** üstlenir:

1. **Domain event bus** — bir aggregate (workflow, form, auth, notify) durum değiştirdiğinde olayını yayınlar; ilgilenen tüketiciler dinler (audit, saga, projeksiyon).
2. **Realtime push** — FE bildirim merkezi (bell + badge + canlı akış) ve süreç durumu değişimleri WebSocket üzerinden kullanıcıya iletilir.
3. **Projeksiyon senkronizasyonu (asıl kritik iş)** — form/property değerleri değiştiğinde `instance_attr` / `instance_list_item` okuma-modellerini güncelleyen **idempotent projektörü** besler.

Çekirdek NATS (pub/sub) *anlık* mesajlaşmayı; **JetStream** ise *kalıcı, sıralı, yeniden-okunabilir* akışı sağlar — olayların asla kaybolmaması ve tüketici çökse bile kaldığı yerden devam etmesi buna dayanır.

## Sürüm & bileşenler

| Bileşen | Değer |
|---|---|
| NATS Server | 2.10 |
| Kalıcılık | JetStream (file storage) |
| Realtime taşıma | WebSocket (port 9222) |
| İstemci | Go (`nats.go`) — publisher (outbox relay) + durable consumer (projektör) |
| Multi-tenancy | Tenant-bazlı NATS account (izolasyon; F-Infra'da 2 tenant account doğrulandı) |

## Projemizde kullanım

**Stream:** `FLOVO_EVENTS` — kalıcı, sıralı, replay edilebilir tek stream tüm domain olaylarını tutar.

**Subject deseni:** `flovo.{aggregate}.{verb}.{version}` — örn. `flovo.form.updated.v1`, `flovo.workflow.step_completed.v1`. 9 subject'lik bir katalog; sürüm eki (`.v1`) şema evrimini bozmadan taşımayı sağlar.

**Projeksiyon akışı (property value depolamasının kalbi):**

```
instance_value UPDATE + instance_value_outbox  (tek Postgres transaction — olay kaybolamaz)
        │  outbox relay (poll / logical decoding)
        ▼
   NATS JetStream  (FLOVO_EVENTS, kalıcı, sıralı)
        │  durable consumer (kaldığı yerden devam)
        ▼
   Go generic projektör (idempotent)  →  instance_attr / instance_list_item / rollup güncellenir
```

Bu, [`../research/property-value-storage/`](../research/property-value-storage/index.md) tasarımındaki **D9 (Outbox + kuyruk + projektör omurgası)** ihtiyacının fiili karşılığıdır. **Not:** [`../research/property-value-storage/form_attr_questions.md`](../research/property-value-storage/form_attr_questions.md) içindeki **S2/D9 "senkron altyapısı (NATS) henüz commit edilmedi"** açık notu bu kararla **KAPANDI** — omurga NATS JetStream olarak sabitlendi.

## Konfigürasyon / desen notları

- **Durable consumer:** Projektör çökse/yeniden başlasa da JetStream tüketiciyi son işlenen olaydan devam ettirir → **veri kaybı yok, yalnız lag birikir** (izlenir, alarmı kurulur; hedef projection lag p95 < 500 ms).
- **Idempotency:** Her olay bir `Nats-Msg-Id` envelope taşır **ve** projektör `version` karşılaştırması yapar (`olay.version <= last_projected_version → atla`). Böylece **at-least-once teslim + tekrar + sırasız olay** veriyi bozamaz — projektör *delta değil tam yansıtma* yapar.
- **Yazma yolundan ayrık:** Kayıt = 2 küçük Postgres yazması (satır + outbox); projeksiyon **arka planda** NATS üzerinden ilerler (trigger değil — kaydı yavaşlatmaz, hata kaydı geri almaz).
- **NATS erişilemezse:** Kayıtlar etkilenmez (outbox Postgres'te birikir); NATS dönünce relay boşaltır.
- **Cache ile sınır:** Kalıcı kuyruk/olay = **NATS**; ephemeral cache (bildirim sayacı vb.) = **Redis**. İkisi karışmaz.

## İlişkili tasarım

- [`../research/property-value-storage/index.md`](../research/property-value-storage/index.md) — CQRS + Outbox depolama mimarisi (bu omurgayı kullanır).
- [`../research/property-value-storage/form_attr_questions.md`](../research/property-value-storage/form_attr_questions.md) — S2 (sync yolu) · D9 (omurga) · S2/D9 kapanışı.
- [`../research/tech-stack/tech_rating.md`](../research/tech-stack/tech_rating.md) — katman 7 (Realtime/mesajlaşma) kararı ve reddedilen alternatifler (Azure Service Bus, Kafka, Supabase Realtime, Redis).

**Mimari aile:** Partial Event Sourcing'in `workflow_events` (append-only kaynak) deseni ile projeksiyon Outbox'ı **aynı ilkeyi** paylaşır: *kalıcı kaynak + türetilmiş projeksiyon + replay*.

## Dikkat / açık noktalar

- **Projection lag** eventual consistency getirir (rapor/liste birkaç yüz ms bayat olabilir; instance_value anında tutarlıdır). BPM için kabul edilebilir; **benchmark kalemidir** (yazma yükü altında lag + tüketici throughput → property-value-storage P5).
- **Yatay ölçek:** projektör durumsuz olduğundan JetStream consumer'ları **yatay ölçeklenir** (lag büyürse tüketici ekle / batch büyüt).
- **WAL/replikasyon:** Outbox relay yöntemi (poll vs logical decoding) benchmark'ta kesinleşir.
