# Kubernetes + Helm (+ Docker Compose) — Konteyner & Orkestrasyon (Flovo iBPM v2)

> **Rol:** Uygulamayı **geliştirmede Compose**, **üretimde Kubernetes** ile paketleyip çalıştırmak; tek Helm chart ile **on-prem + Private Cloud** dağıtımı sağlamak.
> **Karar:** Docker Compose (dev) + Kubernetes (prod, OpenShift + BYO) + Helm · ✅ canlı (F-Infra SI.1/SI.6) · tam gerekçe/karşılaştırma → [`../research/tech-stack/tech_rating.md`](../research/tech-stack/tech_rating.md)

## Ne için kullanıyoruz?

Flovo iBPM v2 **stateful bir BPM motorudur** (uzun-yaşayan süreçler, bekleyen instance'lar, kalıcı durum). Bu yüzden:

- **Geliştirme:** tek komutla ayağa kalkan **Docker Compose** yığını (Postgres · Keycloak · MinIO · NATS · BE · FE) — hızlı yerel döngü.
- **Üretim:** **Kubernetes** — hem **OpenShift** hem **müşterinin kendi (BYO) K8s** kümesi hedeflenir. Dağıtım tek **Helm umbrella chart** ile yapılır.

Amaç, ürünü **müşterinin kendi veri merkezinde / private cloud'unda** çalıştırabilmek (Türkiye Enterprise + KVKK) — belirli bir bulut sağlayıcısına bağlanmadan.

## Sürüm & bileşenler

| Bileşen | Değer |
|---|---|
| Dev orkestrasyon | Docker Compose (7-servis yığın) |
| Prod orkestrasyon | Kubernetes — OpenShift + BYO K8s |
| Paketleme | Helm **umbrella chart** (subchart'lar: BE, FE, Postgres, Keycloak, MinIO, NATS) |
| Hedef platform | Vendor-agnostic (on-prem, private cloud, gerekirse managed K8s) |

## Projemizde kullanım

- **Compose → K8s eşdeğerliği:** Dev'deki Compose servisleri, prod'da Helm subchart'larına birebir karşılık gelir; ortam farkı **values** dosyalarıyla yönetilir.
- **Helm subchart values customization:** Her müşteri kurulumunda kaynak limitleri, replica sayısı, tenant ayarları ve dış bağımlılıklar (kendi Postgres'i mi, embed mi) **values** ile özelleştirilir — chart tek, kurulum profili değişken.
- **Stateful bileşenler:** Postgres, MinIO, NATS JetStream (file storage) kalıcı volume ister; K8s StatefulSet/PVC ile yönetilir.

## Konfigürasyon / desen notları

- **Neden serverless değil?** BPM **stateful** ve uzun-yaşayan bir yüktür; serverless (Azure Functions/Container Apps) kısa-ömürlü, durumsuz iş için tasarlıdır → BPM'e **aykırı**. Bu yüzden Container Apps + Service Bus önerileri **reddedildi** (bkz. tech_rating katman 8, 10).
- **On-prem birinci sınıf:** vendor-agnostic olduğundan managed servislere (Azure PostgreSQL, Blob, Service Bus) bağımlılık yok — hepsinin self-host karşılığı yığında (Postgres, MinIO, NATS, Keycloak).
- **Yatay ölçekleme (horizontal scaling):** Uygulama servisleri **durumsuz** tutulur; **durum Postgres'te**, **kuyruk/olay NATS'ta** (bkz. [`nats-jetstream.md`](./nats-jetstream.md)). Böylece BE ve özellikle **CQRS projektör** replica'ları yatay ölçeklenir — form/property projeksiyon throughput'unu (property-value-storage **P5 projection lag**) artırmak için tüketici eklenir. Süreç durumu paylaşımlı DB/kuyrukta olduğundan replica'lar çakışmaz.
- **Sprint 3 hardening (planlı):** SCC (OpenShift security context) · NetworkPolicy · cert-manager (TLS) · ServiceMonitor (Prometheus) · Helm subchart values profilleri → prod-grade OpenShift + BYO.

## İlişkili tasarım

- [`../research/tech-stack/mimari-analiz.html`](../research/tech-stack/mimari-analiz.html) — §5 yatay ölçekleme + tek-container ölçek analizi.
- [`../research/tech-stack/tech_rating.md`](../research/tech-stack/tech_rating.md) — katman 8 (container) + katman 10 (on-prem konumlandırma) kararı.
- [`nats-jetstream.md`](./nats-jetstream.md) · [`postgresql.md`](./postgresql.md) — durum ve kuyruk katmanları (durumsuz servislerin dayandığı yer).

## Dikkat / açık noktalar

- **Ops maliyeti:** On-prem/vendor-agnostic tercih, managed servise kıyasla **~%30 ek ops eforu** (Helm + K8s + monitoring kendi yığınımızda) getirir — bilinçli stratejik bedel (karşılığında Türkiye Enterprise pazarı + esneklik).
- **Stateful ölçek sınırı:** Postgres/NATS gibi stateful bileşenlerin ölçeği uygulama replica'sından farklı yönetilir (read-replica, JetStream cluster) — kapasite planı benchmark'a bağlı.
- **BYO K8s çeşitliliği:** Müşteri kümesi sürüm/CNI/storage-class farkları values profilleriyle soğurulur; her hedef için smoke-test gerekir.
