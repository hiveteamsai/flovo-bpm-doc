# `form-deger-saklama-v2.html` — Mimari Analizi (güçlü/zayıf yanlar + eksikler)

> **Durum:** 🟡 DEĞERLENDİRME — `form-deger-saklama-v2.html` (güncel ana öneri) mimarisinin proje açısından incelemesi.
> **Amaç:** v2'deki Property value depolama mimarisinin **güçlü/zayıf yanlarını** ve **eksiklerini** listelemek; `models/`'e
> resmi işleme (Tier 1 "Property value depolama modeli") öncesi karar girdisi olmak.
> **Kaynak:** [`form-deger-saklama-v2.html`](./form-deger-saklama-v2.html) · **İndeks:** [`index.md`](./index.md) ·
> **Açık soru:** [`../../todo.md`](../../todo.md) Tier 1.

---

## 1. Mimari (özet)

CQRS: **tapu** = `InstanceValue.data` (JSONB, code-keyed, Instance ile 1–1) → **fihrist** = `InstanceAttr` (tipli skaler) +
`InstanceListItem` (liste-of-model kalemleri), **yeniden-üretilebilir projeksiyon**. Yazım aynı TX'te **Outbox** → NATS
JetStream → **generic projektör** (tam-yansıtma, delta değil + `version` idempotency). Status/creator/createdDate = `Instance`
kolonları (JSONB'de değil); dosya = MinIO URL; etiketli seçim = `LabeledValue {value, display, translationCode}`.

**v1'den (`form-deger-saklama-sunum.html`) başlıca farklar:** Flovo model dili (`InstanceValue`/`InstanceAttr`/`InstanceListItem`) ·
**`projectToAttr` (bool)** (çok-seviyeli `projectionLevel` yerine) · ayrı **çeviri/LabeledValue** bölümü · **`metadataVersion` yok**.

**Yardımcı tablolar:** `InstanceValueOutbox` · `ReflectionLink` (parentProperty A′) · `InstanceValueChange` (append-only audit) ·
(mevcut) ilişki tablosu. **Property'ye eklenenler:** `projectToAttr` (bool) · `hasTranslation` (bool).

---

## 2. ✅ Güçlü yanlar (proje için)

| # | Güç | Neden proje için doğru |
|---|---|---|
| 1 | **Metadata-driven forma tam uyum** | Alan ekle/sil = metadata; `ALTER TABLE`/migration yok — "her müşteri farklı, canlıda değişen form" gerçeğine birebir. |
| 2 | **CQRS ayrımı savunulabilir** | Detay ekranı JSONB'den (anında doğru, lag'siz); rapor tipli fihristten — human-driven BPM için doğru takas. |
| 3 | **Dayanıklılık modeli net** | Tek gerçek kaynak + yeniden-üretilebilir projeksiyon; fihrist bozulsa **rebuild**, yalnız InstanceValue kaybı felaket → yedek/PITR odağı. |
| 4 | **Outbox (trigger değil) + idempotency** | Tam-yansıtma + `version` karşılaştırması; duplicate/retry/sırasız olaya dayanıklı — **tech-stack NATS JetStream kararıyla hizalı**. |
| 5 | **`projectToAttr` (bool) sadeleşmesi** | Karar yükü düşük; tipli kolonlar (num/text/date/bool) sayesinde tek "true" hem eşitlik hem aralık/sıra/isim'i karşılıyor; fihrist büyümesini disipline ediyor (~%10–20 alan). |
| 6 | **code-immutable + code-keyed + generic projektör** | API/iş kuralı/custom code aynı dili; yeni servis/alan **projektör kodunu değiştirmiyor** — ölçeklenebilirliğin kalbi. |
| 7 | **LabeledValue (value/display/translationCode)** | kod≠isim'i temiz çözüyor; dinamik/BR listelerinde bile isim araması çalışıyor; mevcut `translationCode` çeviri modeliyle uyumlu. |
| 8 | **Status/creator/date ayrımı** | Sık-churn alanlar Instance kolonunda → JSONB yeniden yazımını önlüyor; mevcut `instance.md` tasarımıyla tutarlı. |
| 9 | **Dosya MinIO'da (JSONB'de URL)** | "Yavaş belge yükleme" şikâyetini adresliyor; tech-stack MinIO kararıyla uyumlu. |
| 10 | **Dürüst risk/benchmark bölümü** | Write-amp, projection lag, partition hot-spot, A′ fan-out açıkça listeli + "kendi donanımında p95 doğrulanmadan onaylı değil" kapısı. |
| 11 | **Yansıma taksonomisi (snapshot/live/materialized)** | UserInfo/FlowInfo/ParentProperty'yi tek kurala zorlamıyor; audit-dostu snapshot varsayılanı mantıklı. |
| 12 | **Fazlı benimseme (0–3)** | MVP çekirdeği net; ağır/koşullu özellikler (rollup, A′, PostGIS, tik tablosu) sonraya. |

---

## 3. ⚠️ Zayıf yanlar / riskler

| # | Zayıflık | Detay |
|---|---|---|
| 1 | **Write amplification (MVCC)** | Her küçük değişiklik tüm JSONB satırını yeniden yazıyor (~15–40 fiziksel iş/kayıt). `saveAndRefreshOnAfterChange` + büyük form (15–40 KB) yükü birikir; net **byte üst-sınırı / "kaç KB'den sonra böl"** eşiği yok. |
| 2 | **Rapor tarafı eventual consistency** | Liste/inbox lag'e tabi; **operasyonel liste ("onay bekleyenler") vs analitik rapor** için lag toleransı ayrımı yapılmamış — kullanıcı kendi eyleminden sonra listeye dönünce bayat görebilir. |
| 3 | **Rebuild ölçekte pahalı** | `projectToAttr` false→true = bulk rebuild (1M ~20dk, 5M ~100dk); süre boyunca "kısmi sonuç riski"; **"ready sinyali" Faz 1'e ertelenmiş** → MVP'de bir alanı aranabilir yapmak yavaş/riskli. |
| 4 | **A′ (materialized reflection) fan-out** | Parent değişince tüm child'lara propagation; derinlik/döngü limitleri "zorunlu" deniyor ama **somut sınır/algoritma yok** (Faz 2) — ölçekte tehlikeli. |
| 5 | **Operasyonel karmaşıklık** | Attr + ListItem + Rollup + ReflectionLink + Outbox + Change = **6 yardımcı tablo**; her biri partition/retention/vacuum/index bakımı ister — MVP için DevOps olgunluk varsayımı büyük. |
| 6 | **Cross-form ağır toplam** | Canlı GROUP BY ölçekte yetmiyor; incremental **rollup "zorunlu" ama tasarımı yok**. |
| 7 | **Çok-dilli rapor** | `display` snapshot dili sabit (defaultLang); EN kullanıcı EN isimle arama/sıralama translationCode+join gerektiriyor, tam çözülmemiş (doc'ta **P3 riski**). `defaultLang` sonradan değişirse display'ler eski dilde kalır. |
| 8 | **`metadataVersion` kaldırıldı** | Basitlik kazandırıyor ama "eski kayıt hangi şemayla yazıldı" izlenebilirliğini ve şema-evrim uyumsuzluk yönetimini kaldırıyor; JSON Schema ↔ canlı Property senkronu garanti belirsiz. |
| 9 | **code-keyed, FK yok** | Referans bütünlüğü DB'de garanti değil; Property silme koruması/orphan temizliği **uygulama katmanına** kalıyor; typo bir code'u sessizce orphan yapabilir. |
| 10 | **İsim güncelliği (tutarsızlık)** | v2 **eski adlar** kullanıyor: `controlTypeId` (→ `propertyType`, v0.15) · `RelatedInstance`/`relatedInstanceId`/`relatedPropertyId` (→ `Associated*`, v0.17) · `Instance.delete` (→ `deleted`, v0.18) — models/'e işlenmeden düzeltilmeli. |

---

## 4. 📌 Eksikler (benimsemeden önce netleşmeli)

1. **Resmi karar + `models/`'e işleme yok** — doc kendisi diyor (SSS 20: "🟡, ürün onayı sonrası models/ + todo [x]").
   `InstanceValue`/`InstanceAttr`/`InstanceListItem` model dosyaları henüz yok (`models/processInstances/` altına); `property.md`'ye
   `projectToAttr`/`hasTranslation` işlenmemiş.
2. **Benchmark/spike sonucu yok** — 5M/200M Attr satırı, ~200ms lag varsayımları **doğrulanmamış** (doc "benchmark kapısı" koyuyor ama ölçüm yok).
3. **Rollup tasarımı yok** — cross-form incremental aggregation "zorunlu" deniyor, şema/güncelleme mekanizması tanımsız.
4. **"Projection ready" sinyali** — rebuild sırasında bir alanın otoritatif olduğunu belirleme mekanizması yok.
5. **A′ propagation sınırları** — derinlik limiti/döngü tespiti somut değeri/algoritması yok.
6. **Çok-dilli rapor sıralama/arama** — collation + "kullanıcının dilinde ara" tam çözüm yok.
7. **Retention/KVKK politikaları** — `InstanceValueChange` + hard-purge + orphan cleanup için somut saklama/silme politikası yok
   ([`../settings-log/`](../settings-log/index.md) KVKK açık sorusuyla paralel).
8. **Property silme koruması / orphan yönetimi** — code-keyed referans bütünlüğü için operasyonel job tanımı.
9. **Klasör içi terminoloji hizası** — [`form-value-scenarios.md`](./form-value-scenarios.md) / [`form_attr_questions.md`](./form_attr_questions.md) /
   [`form_attr_scenerios_rating.md`](./form_attr_scenerios_rating.md) hâlâ `form_value`/`form_attr` adlarını kullanıyor; v2
   `InstanceValue`/`InstanceAttr`'a geçti — birleştirilmeli.
10. **`property.md` çekirdek ↔ v2 alanları** — `savePropertyToDb`/`saveChangeLog` mevcut modelde var; `projectToAttr`/`hasTranslation`/
    `reflectionMode` eklenmeli ve tipe-özel alanlarla çelişki taranmalı.

---

## 5. Genel değerlendirme

Mimari **olgun ve projeye çok uygun** — doğru problem-çözüm eşleşmesi, dürüst risk analizi, mevcut tech-stack kararlarıyla
(PostgreSQL/JSONB · NATS JetStream · MinIO) hizalı. Ana boşluklar **tasarım değil, doğrulama ve operasyon detayı**: benchmark,
rollup / ready-signal / A′-sınır tasarımları, çok-dilli rapor, ve `models/`'e resmi işleme (isim uyumlamasıyla). Bunlar netleşince
[`../../todo.md`](../../todo.md) Tier 1 "Property value depolama modeli" maddesi kapanabilir.

**Önerilen sıradaki adım:** v2'yi `models/`'e işle (güncel isimlerle: `InstanceValue`/`InstanceAttr`/`InstanceListItem` model
dosyaları + `property.md`'ye `projectToAttr`/`hasTranslation`) ve Tier 1 maddesini karara bağla.

*Oluşturma: 2026-07-27.*
