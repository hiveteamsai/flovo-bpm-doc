# Property Value — Depolama Mimarisi (Araştırma) — İndeks

> **Amaç:** Form/property **değerlerinin veritabanında nasıl saklanacağı** açık sorusunu besleyen mimari araştırma.
> Bu klasör, `todo.md`'deki **"Property value depolama modeli"** (Tier 1) açık sorusunun **girdisidir**.
>
> **⚠️ Durum:** 🟡 **DEĞERLENDİRME BEKLİYOR** — bu bir araştırma/öneri dokümanıdır; **henüz tasarıma dahil edilmemiştir.**
> İçerik değerlendirilip karara bağlandıktan sonra ilgili tasarım dokümanlarına ([`form-value-scenarios.md`](./form-value-scenarios.md),
> `../../models/service-settings/property.md`, `../../models/` PropertyValue modeli) işlenecektir.

## Dosyalar
| Dosya | İçerik (özet) |
|---|---|
| [`form-deger-saklama-sunum.html`](./form-deger-saklama-sunum.html) | Form/property değeri saklama için **eksiksiz mimari önerisi** — sunum/analiz (HTML). Aşağıda özetlenmiştir. |
| [`form-value-scenarios.md`](./form-value-scenarios.md) | **Form value kullanım senaryoları** (§1–§13) — form değerlerinin nerede/nasıl okunup yazıldığı; depolama & `form_attr` uygunluk değerlendirmesinin **girdi/gereksinim** dokümanı. |
| [`form_attr_questions.md`](./form_attr_questions.md) | 🟡 **AÇIK** — `form_attr` projeksiyon tablosunun projeye **uygunluğunu** değerlendiren soru-cevap çalışma dosyası (S1–S13); sorular biriktirilir, sonda toplu karar verilir. |
| [`form_attr_scenerios_rating.md`](./form_attr_scenerios_rating.md) | 🟡 **DEĞERLENDİRME** — her senaryonun (`form-value-scenarios.md` §1–§11) `form_attr`'a karşı **ölçekli** (5M+ · 150+ · 40+) **puanlaması** (🟢/🟡/🔴/⚫) + 9 performans riski + 14 ek geliştirme + faz sırası. |

## `form-deger-saklama-sunum.html` — ne öneriyor?

**Problem:** Binlerce müşteri (account) · her formda **değişken sayıda alan** (20–100+) · müşteri alanları Form Designer'dan
istediği an değiştiriyor · yine de **hızlı rapor, arama, sıralama, toplam** gerekiyor · sistem bozulunca **toparlanabilmeli**,
**izlenebilmeli** ve **kanıtlanabilmeli** (audit/KVKK).

**Önerilen çekirdek mimari — CQRS + Outbox + Postgres:**
- **Kaynak-hakikat (source of truth):** form değerleri **JSONB** olarak tek yerde tutulur (esnek şema; alan sayısı/tipi değişse de yazma bozulmaz).
- **Read-model / Projection:** raporlama-arama-sıralama-toplam için JSONB'den türetilen **projeksiyon (okuma modeli)** tabloları.
- **Outbox pattern:** yazma → outbox → projeksiyon güncelleme; **idempotency** (aynı olay iki kez gelirse etki yok); **trigger yerine** outbox tercihi.
- **Projeksiyon seviyesi kuralı:** büyümeyi kontrol eden zorunlu kural — kalem-bazlı rapor (kaleme 1 satır), cross-form toplam,
  gerçekten yapısal JSON (harita koordinatı, görsel alan nokta seti), **versiyonlu metadata** (alan değişince ne olur?).

**Cevaplanan itirazlar:** JSONB update = satırın yeniden yazılması · write amplification (1 kayıt = kaç fiziksel yazma) · WAL üretimi ·
"JSONB'de rapor/arama/sıralama yavaş" iddiası · "account başına tablo" neden ölçekte çöker (7 sebep).

**Operasyonel kapsam:** GIN index stratejisi (naif "her hot alana index" ✗ vs önerilen ✓) · partition stratejisi (dürüst değerlendirme) ·
arıza senaryoları (bulk rebuild ile projeksiyonu sıfırdan üretme, projection lag izleme, canlı guardrail) · depolama hesabı (1M form) ·
NATS JetStream · kapıda **JSON Schema** doğrulama.

**Bilinmesi şart 4 Postgres iç mekanizması:** TOAST · HOT update · Autovacuum (MVCC/bloat) · GIN pending list.

**Kapsam çerçevesi:** kabul kriterleri (hedefler) · 2–3 günlük ölçüm (spike) planı · çok dilli sıralama · dosya/fatura görseli ·
değişiklik geçmişi (audit/KVKK) · "kazandıklarımız / bilinçli reddettiklerimiz" · 30 saniyelik kapanış diyagramı.

## İlgili tasarım dokümanları (değerlendirme sonrası işlenecek)
- [`form-value-scenarios.md`](./form-value-scenarios.md) — form değeri senaryoları (bu klasörde).
- [`../../models/service-settings/property.md`](../../models/service-settings/property.md) — Property (alan) modeli.
- `../../todo.md` — **"Property value depolama modeli"** açık sorusu (Tier 1).
