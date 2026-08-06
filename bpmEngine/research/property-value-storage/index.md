# Property Value — Depolama Mimarisi (Araştırma) — İndeks

> **Amaç:** Form/property **değerlerinin veritabanında nasıl saklanacağı** sorusunu besleyen mimari araştırma.
> Bu klasör, `todo.md`'deki "Property value depolama modeli" sorusunun **girdisi olmuştur**; **model katmanı 2026-08-04'te işlendi**
> (→ `models/processInstances/`) ve klasör artık **kaynak/mimari referans** olarak durur (yalnız operasyonel kararlar `todo.md`'de açık).
>
> **Durum:** 🟢 **MODEL KATMANI İŞLENDİ (2026-08-04)** — v2 önerisi (`form-deger-saklama-v2.html`) **model dokümanlarına**
> alındı: `models/processInstances/` altına **InstanceValue · InstanceAttr · InstanceListItem · InstanceValueOutbox ·
> InstanceValueChange · ReflectionLink · LabeledValue** oluşturuldu; `Property`'ye `projectToAttr`/`hasTranslation`/`reflectionMode`
> + `code` immutable eklendi; `Instance` 1–1 `InstanceValue`'ya bağlandı; **ReflectionMode** enum'u eklendi.
> **Bu klasör** artık **kaynak/mimari referans** olarak durur (araştırma; alt-senaryo/rating dosyaları besleyici).
> **Açık kalan** operasyonel kararlar (rollup, yansıma yayılım sınırları, retention/KVKK, davranış-dokümanı entegrasyonu) → `../../todo.md`.

## Dosyalar
| Dosya | İçerik (özet) |
|---|---|
| ⭐ [`form-deger-saklama-v2.html`](./form-deger-saklama-v2.html) | **Ana sunum (GÜNCEL öneri) — A'dan Z'ye.** Flovo model diliyle (`InstanceValue`/`InstanceAttr`/`InstanceListItem`), **`projectToAttr` (bool)**, ayrı **çeviri/LabeledValue** bölümü, **`metadataVersion` yok**. `sunum.html`'nin evrimi. Aşağıda özetlenmiştir. |
| [`form-deger-saklama-sunum.html`](./form-deger-saklama-sunum.html) | **Önceki teknik-derin sunum** (`form_value`/`form_attr` adlarıyla; çok-seviyeli `projectionLevel`; `metadataVersion`). v2 bunun sadeleştirilmiş/güncel hâlidir. |
| [`form-deger-saklama-v2-analiz.md`](./form-deger-saklama-v2-analiz.md) | **v2 mimari analizi** — güçlü/zayıf yanlar (12 güç · 10 risk) + eksikler (10 madde) + genel değerlendirme. `models/`'e işleme öncesi karar girdisi. |
| [`form-value-scenarios.md`](./form-value-scenarios.md) | **Form value kullanım senaryoları** (§1–§13) — form değerlerinin nerede/nasıl okunup yazıldığı; depolama & `form_attr` uygunluk değerlendirmesinin **girdi/gereksinim** dokümanı. |
| [`form_attr_questions.md`](./form_attr_questions.md) | 🟡 **AÇIK** — `form_attr` projeksiyon tablosunun projeye **uygunluğunu** değerlendiren soru-cevap çalışma dosyası (S1–S13); sorular biriktirilir, sonda toplu karar verilir. |
| [`form_attr_scenerios_rating.md`](./form_attr_scenerios_rating.md) | 🟡 **DEĞERLENDİRME** — her senaryonun (`form-value-scenarios.md` §1–§11) `form_attr`'a karşı **ölçekli** (5M+ · 150+ · 40+) **puanlaması** (🟢/🟡/🔴/⚫) + 9 performans riski + 14 ek geliştirme + faz sırası. |

## `form-deger-saklama-v2.html` — ne öneriyor? (GÜNCEL, v1'den farkı)

**Çekirdek mimari (v1 ile aynı temel):** CQRS + Outbox + NATS + Postgres/JSONB + MinIO. **Kaynak-hakikat** = JSONB (tapu),
**fihrist** (Attr/ListItem) yeniden üretilebilir projeksiyon; Outbox aynı TX'te, generic projektör tam-yansıtma (delta değil) + `version` idempotency.

**Model seti (Flovo diliyle):**
- **`InstanceValue`** — Instance ile 1–1, `data` JSONB **code-keyed**, `version`; **7 kolon** (kolon eklenmez, şekil zenginleşir).
- **`InstanceAttr`** — sorgulanabilir skaler fihrist (tipli EAV); **+`display` +`translationCode`** eklendi → 10 alan.
- **`InstanceListItem`** — liste-of-model (`groupByTax`, key-value) fihristi; +`display`/`translationCode` → ~12 alan.
- **`InstanceValueOutbox`** · **`ReflectionLink`** (parentProperty A′) · **`InstanceValueChange`** (append-only audit) · (mevcut) ilişki tablosu.

**v1'den başlıca farklar:**
- **`projectToAttr` (bool)** — eski çok-seviyeli `projectionLevel` (NONE/SEARCH/SORT/AGGREGATE) **kaldırıldı**; tek soru: fihriste yazılsın mı? (~%10–20 alan `true`).
- **`metadataVersion` YOK** — projektör güncel Property tanımına göre yansıtır.
- **Ayrı çeviri/LabeledValue bölümü** — etiketli seçimler `{value, display, translationCode}`; `display` = org `defaultLang` snapshot; rapor isim araması `Attr.display` (`projectToAttr=true`). Display kaynağı: statik `PropertyItem` **veya** dinamik iş-kuralı/API (istekte `LabeledValue` zorunlu).
- **Property'ye eklenenler:** `projectToAttr` (bool) · `hasTranslation` (bool).
- **Yansıma kararı** 2 soruyla: değişmez→**snapshot (A)** · değişen+göster→**canlı (B)** · değişen+ağır rapor→**materialized (A′)** (ReflectionLink + propagation, sınırlı).
- `code` **immutable** (draft penceresi hariç) · status **Instance.statusId kolonu** (JSONB'de değil) · dosya **MinIO URL** · uygulama **fazları 0–3**.

> **⚠️ Benimseme öncesi uyumlanacaklar (isim güncelliği):** v2 sunumu bazı **eski adları** kullanıyor; `models/`'e işlenirken güncel
> proje adlarına çevrilmeli: **`controlTypeId` → `propertyType`** (v0.15) · **`RelatedInstance`/`relatedInstanceId`/`relatedPropertyId`
> → `AssociatedInstance`/`associatedInstanceId`/`associatedPropertyId`** (v0.17) · **`Instance.delete` → `deleted`** (v0.18) ·
> **`imageAreaSelector` alan tipi kaldırıldı** (v0.21) — sunum/senaryolardaki "Image Area" yapısal-JSON örneği artık geçersiz
> (yerine `mapViewer` kalır). _(Sunum araştırma dokümanı olduğundan içerik olduğu gibi bırakıldı; uyumlama models/ tarafında yapılacak.)_

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

## İlgili tasarım dokümanları (model katmanı işlendi)
- [`../../models/processInstances/index.md`](../../models/processInstances/index.md) — **değer modelleri** (InstanceValue/InstanceAttr/InstanceListItem/InstanceValueOutbox/InstanceValueChange/ReflectionLink/LabeledValue).
- [`../../models/service-settings/property.md`](../../models/service-settings/property.md) — Property (`projectToAttr`/`hasTranslation`/`reflectionMode` + `code` immutable).
- [`form-value-scenarios.md`](./form-value-scenarios.md) — form değeri senaryoları (bu klasörde).
- `../../todo.md` — Property value **operasyonel kararları** (rollup · yansıma yayılım sınırları · retention/KVKK · davranış-dokümanı entegrasyonu).
