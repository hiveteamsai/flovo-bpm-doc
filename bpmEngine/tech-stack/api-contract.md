# API Contract — Hybrid (Protobuf · gRPC · REST · OpenAPI) (Flovo iBPM v2)

> **Rol:** Servisler-arası ve dış istemcilerle konuşmanın **tek kaynaktan türetilen, tip-güvenli sözleşmesi**; iç trafik gRPC, dış trafik REST/JSON.
> **Karar:** Protobuf kaynak + gRPC (iç) + grpc-gateway REST + OpenAPI v2 codegen (dış) · ✅ canlı (ADR-012, Sprint 2 S2.4) · tam gerekçe/karşılaştırma → [`../research/tech-stack/tech_rating.md`](../research/tech-stack/tech_rating.md)

## Ne için kullanıyoruz?

Flovo'da **üç istemci sınıfı** var: (1) iç Go modülleri (workflow, form, auth, notify — ileride ayrı servisler), (2) Next.js frontend, (3) müşterinin **custom code** entegrasyonları + mobil. Tek bir protokol hepsine uymaz; bu yüzden **hybrid**: içeride performanslı/tip-katı **gRPC**, dışarıda ergonomik **REST/JSON** — ikisi de **aynı Protobuf tanımından** türetilir, böylece sözleşme asla birbirinden kaymaz.

## Sürüm & bileşenler

| Katman | Protokol / araç | Kullanan |
|---|---|---|
| **Kaynak-hakikat** | **Protobuf** `proto/flovo/<svc>/v1/*.proto` | Tüm katmanlar |
| **İç (servisler arası)** | **gRPC + Protobuf** | Go BE modülleri arası |
| **Dış (public)** | **grpc-gateway** → HTTP/JSON | FE · 3rd-party · mobil |
| **API spec** | **OpenAPI v2** (protoc-gen-openapiv2) | Swagger UI + FE codegen |
| **FE istemcisi** | **OpenAPI codegen TS** → `@flovo/api-client` | Next.js |
| **Streaming** | **NATS subjects** | Realtime bildirim / proses durumu |

## Projemizde kullanım

- **İç çağrılar gRPC:** `workflow`, `form`, `auth`, `notify` modülleri birbirini gRPC ile çağırır — binary serialization ~**7-10x az bandwidth**, compile-time tip kontrolü ve **SOA-split-ready** (ileride ağ üzerinden ayrılırken kod değişmez).
- **Dış API REST:** aynı proto'lardan grpc-gateway ile üretilen REST yüzeyi. Kritik uçlar:
  - `GET /services/{id}/schema` — müşteri custom code'unun **alan adı/tipini** öğrenmesi (value yorumlama; form-value §9-26).
  - `POST /instances/search` — **alan value'suna göre arama** (`barcode=X`; form-value §9-28).
  - `GET /instances/{id}` · `PATCH /instances/{id}` — okuma / value güncelleme.
- **FE tip güvenliği:** `@flovo/api-client` OpenAPI'den üretilir → FE ve BE arasında **contract drift sıfır**; şema değişince FE tipleri derlemede kırılır (erken uyarı).

## Konfigürasyon / desen notları

- **buf pipeline:** `buf.yaml` → **lint STANDARD** + **breaking WIRE_JSON** (main'e karşı geriye-uyum kontrolü); `buf.gen.yaml` → **5 plugin pinned** (go, go-grpc, grpc-gateway, openapiv2, protobuf-es TS). **CI proto job**: lint + breaking → ci-gate aggregate.
- **Geriye uyum disziplini:** dış REST sözleşmesi müşteri entegrasyonlarını bağlar → **kırıcı değişiklik yasak**; WIRE_JSON breaking-check bunu CI'da zorlar. Bu, [`../research/property-value-storage/form_attr_questions.md`](../research/property-value-storage/form_attr_questions.md) **S12**'deki **`Property.code` immutable** kararıyla aynı hizada: alan kodu dış API kimliğidir, rename edilmez (yeniden adlandırma yalnız görünen `translation`'da).
- **Streaming ayrı:** request/response değil, olay yayını NATS subject'lerinden (`flovo.{aggregate}.{verb}.{version}`) akar — bkz. NATS dokümanı.

## İlişkili tasarım

- [`./typescript-nextjs.md`](./typescript-nextjs.md) — `@flovo/api-client` tüketicisi (FE).
- [`../research/property-value-storage/form-value-scenarios.md`](../research/property-value-storage/form-value-scenarios.md) — §9 dış/API senaryoları (schema, search, PATCH, webhook).
- [`../research/property-value-storage/form_attr_questions.md`](../research/property-value-storage/form_attr_questions.md) — S12 `Property.code` immutable → API kararlılığı.
- [`../research/tech-stack/tech_rating.md`](../research/tech-stack/tech_rating.md) — hybrid contract kararının gerekçesi.

## Dikkat / açık noktalar

- **Webhook / `parameters` value taşıma** (form-value §9-27) sözleşmesi ayrıca tanımlanmalı.
- **Versiyonlama:** `v1` proto namespace ile başlandı; ileride `v2` yayınlandığında geçiş/deprecation politikası netleştirilmeli.
- **Custom code API'si** ([`../flovo-customer-api.md`](../flovo-customer-api.md)) bu sözleşmenin dış yüzüdür — endpoint kapsamı orada detaylanır.
