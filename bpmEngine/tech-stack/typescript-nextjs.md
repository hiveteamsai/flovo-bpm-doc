# TypeScript + Next.js — Frontend Katmanı (Flovo iBPM v2)

> **Rol:** Kullanıcının form tasarladığı, süreç yürüttüğü ve raporları gördüğü **web arayüzünün** tamamı; tarayıcıda tip-güvenli, bileşen tabanlı SPA/SSR uygulaması.
> **Karar:** TypeScript 5 + Next.js 14 (App Router) + React 18 · ✅ canlı (Sprint 1+2) · tam gerekçe/karşılaştırma → [`../research/tech-stack/tech_rating.md`](../research/tech-stack/tech_rating.md)

## Ne için kullanıyoruz?

Flovo'nun **tüm kullanıcı arayüzü** bu katmanda çalışır: self-servis **Form Designer**, süreç izleme **Dashboard**, görev **Gelen Kutusu**, **Flow Designer**, organizasyon ayarları ve gerçek-zamanlı **bildirim merkezi**. Arka uçla (Go) yalnızca **tip-güvenli sözleşme** üzerinden konuşur (bkz. [`./api-contract.md`](./api-contract.md)); iş mantığı FE'de tutulmaz — FE **sunum + etkileşim** katmanıdır.

## Sürüm & bileşenler

| Bileşen | Seçim |
|---|---|
| Dil | **TypeScript 5** (strict) |
| Framework | **Next.js 14** (App Router, RSC + client components) |
| UI kütüphanesi | **React 18** |
| Tipli API istemcisi | **`@flovo/api-client`** — OpenAPI codegen (bkz. api-contract) |
| Gerçek-zaman | **NATS üzerinden WebSocket** (bildirim/proses durumu) |
| İkon / font | **Heroicons** · **Manrope** (başlık) + **Inter** (gövde) |

## Projemizde kullanım

- **Form Designer** — self-servis form tasarım aracı: **16 kontrol tipi** + sol palet + orta canvas + sağ **PropertiesPanel** (alan özellikleri) + **Publish** akışı. Kullanıcı burada tanımladığı formu **çalışma zamanında** doldurur; bu, [`../research/property-value-storage/form-value-scenarios.md`](../research/property-value-storage/form-value-scenarios.md) **§1 (form doldurma & anlık UX)** senaryolarının FE tarafıdır. Değerler backend'e gönderilir; combobox gibi kodlu alanlarda **ham kod** taşınır, **gösterim** çeviriyle çözülür (§6).
- **Dashboard** — KPI kartları + SLA bar grafik + aktivite akışı + proses durumu (KPI/rapor verisi backend projeksiyonlarından gelir).
- **Gelen Kutusu (Tasks Inbox)** — kullanıcının onayı/aksiyonu bekleyen görevler (3-pane).
- **Flow Designer** — süreç akışını görsel kurma (SVG canvas + node detay görünümü — planlı).
- **Bildirim merkezi** — zil + rozet + canlı akış; olaylar **NATS JetStream**'den WebSocket ile gelir (anlık güncelleme).

## Konfigürasyon / desen notları

- **BPM Studio design system:** kurumsal B2B kimlik — **teal-forward palet (`#00796b`)**, Manrope/Inter, 100+ tasarım token. Ortak primitive bileşenler: `StatusPill`, `ProgressBar`, `KpiCard`, `ActivityFeed` — tüm ekranlar bunları paylaşır (görsel tutarlılık + tek yerden bakım).
- **Tip güvenliği dil-bağımsız sağlanır:** FE ile Go BE aynı dilde değil; sözleşme birliği **OpenAPI/Protobuf codegen** ile kurulur (`@flovo/api-client`) → **contract drift sıfır** (bkz. [`./api-contract.md`](./api-contract.md)). "Backend de JS olsun ki uyumlu olsun" argümanı bu yüzden geçersiz (kod paylaşımı değil, sözleşme paylaşımı).
- **App Router:** sayfa/segment bazlı yükleme; ağır ekranlar (Form Designer, Flow Designer) client-component, liste/rapor ekranları SSR/RSC ile ilk-yük hızlı.

## İlişkili tasarım

- [`./api-contract.md`](./api-contract.md) — FE'nin backend ile konuştuğu sözleşme + `@flovo/api-client` codegen.
- [`../research/property-value-storage/form-value-scenarios.md`](../research/property-value-storage/form-value-scenarios.md) — form doldurma/gösterim senaryoları (§1, §6) FE tarafı.
- [`../research/tech-stack/tech_rating.md`](../research/tech-stack/tech_rating.md) — dil/framework kararının gerekçesi.

## Dikkat / açık noktalar

- **İş kuralı realtime (form-value §2):** koşullu göster/gizle, `fromCalculation`, `fillDataSource` gibi kurallar FE'de bellekte çalışır — kural motorunun FE yürütme sınırları netleştirilmeli.
- **Gerçek-zaman ölçek:** çok sayıda eşzamanlı WebSocket bağlantısında bildirim akışı performansı benchmark edilmeli (NATS tarafı ölçeklenir).
- **Flow Designer** henüz planlı; SVG canvas + node-detail-view kapsamı ayrı tasarlanacak.
