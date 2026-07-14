# form_attr — Senaryo Uygunluk Karnesi (Rating)

> **Amaç:** [`form-value-scenarios.md`](./form-value-scenarios.md)'deki **her senaryoyu**, `form_attr` (ve çekirdek
> `form_value`/`form_list_item`) projeksiyon mimarisine karşı **ölçekli** olarak puanlamak. Kanıt tabanı: bu klasördeki
> [`form_attr_questions.md`](./form_attr_questions.md) (S1–S13) + [`form-deger-saklama-sunum.html`](./form-deger-saklama-sunum.html).
>
> **⚠️ Durum:** 🟡 **DEĞERLENDİRME** — karar girdisi; henüz tasarıma işlenmedi.

## Ölçek varsayımları

| Girdi | Değer | Türetilen |
|---|---|---|
| Instance sayısı | **5M+** | `form_value` 5M satır |
| Instance başına property | **150+** | JSONB ~15–40 KB/satır → `form_value` **~75–150 GB** (TOAST'lı), GIN ~15–30 GB |
| `form_attr`'da tutulan property | **40+** | `form_attr` = 5M × 40 = **~200M satır** |
| Liste (list-of-model) kullanımı | ~%40 form, ~5 kalem × ~4 alt-alan | `form_list_item` **~40–80M satır** |
| Bulk rebuild | ~20 dk / 1M (throttle'lı) | 5M ≈ **~100 dk** |

## Rating ölçeği

| Simge | Anlam |
|---|---|
| 🟢 | **Sorunsuz** — çekirdek 5M'de doğrudan karşılar; ek iş yok |
| 🟡 | **Koşullu** — çalışır ama **benchmark / tuning / yan-çözüm** gerektirir |
| 🔴 | **Ek geliştirme zorunlu** — çekirdek tek başına yetmez; yanına bir bileşen şart |
| ⚫ | **form_attr kapsamı dışı** — başka mekanizma (status kolonu · JSONB · join) çözer; form_attr devrede değil |

**`form_attr` rolü:** *on-path* (sorgu bu tablodan gelir) · *off-path* (form_value/başka yer) · *yazma* (projeksiyon güncellenir).

---

## Bölüm-bölüm değerlendirme

### §1 Form doldurma & anlık UX (1–6) — 🟢
- **form_attr rolü:** *off-path.* Form açma/doldurma = `form_value` **tek satır** okuma (PK); yazma = JSONB update.
- **Gerekçe:** Detay-görünüm hiçbir zaman form_attr'a bakmaz (S1). Combobox ham **kod** JSONB'de; gösterim render'da translation ile
  çözülür. Özel şekiller (`groupByTax` listesi, Barcode, Map, Image Area — item 6) JSONB'de yaşar.
- **5M notu:** PK okuma satır sayısından **bağımsız** (O(1)); 5M etkilemez.
- **Risk/geliştirme:** yok. *(Combobox gösterimi = translation, downstream D7 — burada değil.)*

### §2 İş kuralları — frontend realtime (7–9) — 🟢
- **form_attr rolü:** *off-path.* Kurallar yüklü formun **bellekteki** değerleri üzerinde çalışır.
- **Gerekçe:** `expenseType==1 → alan göster`, `fromCalculation taxAmount`, `fillDataSource` — hepsi tek-form, DB projeksiyonu yok.
- **5M notu:** ölçekten bağımsız. **Risk/geliştirme:** yok.

### §3 Motor / akış kararları (10–14) — 🟢 / ⚫(status)
- **form_attr rolü:** *off-path.* Motor tek instance'ın değerlerini `form_value`'dan, akış durumunu process-state'ten okur.
- **Gerekçe:** changeList, `amount>5000` karşılaştırma, `expenseType` switch, `approver` ile değişken kullanıcı, skip — tek-instance okuma.
- **5M notu:** tek-instance; ölçekten bağımsız.
- **Risk/geliştirme:** **status = ayrı indeksli kolon (D3)** — form_attr değil; motor günceller (S3/S4).

### §4 Değer yazma — motor (15–18) — 🟡
- **form_attr rolü:** *yazma.* `form_value` update → outbox → ~40 attr satırı **delete+reinsert** + GIN bakımı.
- **Gerekçe:** item 15 (değer atama, liste alt-kalemine yazım → `form_list_item` reproject), 16 (custom ID), 17 (AI init), 18
  (HTTP→changeList). Her yazım = JSONB **tüm satır** yeniden yazımı (MVCC) + projeksiyon.
- **5M notu:** çok-adımlı akışlarda toplam yazma throughput'u + **projection lag** (<500ms hedefi) benchmark'lanmalı; projektör yatay ölçeklenir.
- **Risk/geliştirme:** **P5** (projection lag), **P7** (GIN); **D1** (projectionLevel → kaç attr reproject), **D9** (outbox omurgası).

### §5 Yansıma — Parent · User · Flow (⭐) — 🔴
- **form_attr rolü:** *karışık* (S3/S4 2×2 kuralı).
- **Gerekçe & alt-kırılım:**
  - **UserInfo** (departman/ünvan) → **A-snapshot** (yazımda JSONB'ye dondurulur) → form_attr'a **normal alan gibi** düşer 🟢.
  - **FlowInfo** `createdDate`/`creator` → **native kolon** (`created_at`/`creator_user_id`) ⚫ (form_attr off-path, sorun yok).
  - **FlowInfo** `currentStatus` → **ayrı indeksli status kolonu** ⚫ (D3).
  - **ParentProperty** → **A-snapshot** (form_attr'a girer 🟢) / **B** referans+join (⚫ off-path) / **A′** materialized+propagation (🔴).
- **5M notu:** **A′ fan-out** (parent değişimi → N child reproject) kitlesel yük (**P8**). `reflection_link` + propagation consumer
  araştırmada **YOK**.
- **Risk/geliştirme:** **P8**; **D4** (reflection mekanizması — zorunlu), **D12** (snapshot yazımı), **D3**.

### §6 Çok dillilik & dil eşleşmesi (⭐) — 🔴
- **form_attr rolü:** *on-path ama yetersiz* (S6/S8).
- **Gerekçe:** form_attr **kodu** tutar, ismi değil; isim **dile bağlı**. **Gösterim** için render'da çöz (ucuz). **Sıralama/filtre/
  gruplama isme göre** → translation join; 6a defaultLang→`definition`, 6b diğer→`translation`, 6c sorgu dile bağlı.
- **5M notu:** 200M satır + translation join, dile bağlı sıra → btree'siz sort **ağır (P3)**.
- **Risk/geliştirme:** **P3**; **D7** (translation-aware sorgu katmanı — zorunlu) + ops. defaultLang display cache / (kod→isim) per-dil lookup.

### §7 Kalıcılık & geçmiş (19–23)
| Item | Konu | Rating | Not |
|---|---|---|---|
| 19 | `savePropertyToDb` (türetilmiş `taxAmount`) | 🟢 | Raporlanıyorsa projectionLevel=AGGREGATE → normal attr |
| 20 | `saveChangeLog` (değer geçmişi) | 🔴 | **Ayrı append-only audit/changelog tablosu (D5)**; 5M×düzenleme → partition+retention. form_attr değil |
| 21 | `backingField` (gizli) | 🟢 | projectionLevel=NONE → yalnız JSONB |
| 22 | Dosya/binary (`receipt`) | 🔴 | **MinIO (D8)**, URL-in-JSONB; "yavaş belge" çözümü |
| 23 | Instance state (3 gün bekleme, persistent) | 🟢 | `form_value` kalıcı; bekleme durumu status kolonunda |

### §8 Raporlama & sorgu (⭐) — **ağır bölge**
| Alt | Senaryo | Rating | Gerekçe (5M) |
|---|---|---|---|
| §8.1 | Normal rapor (form başına 1 satır, çok-kolon) | 🟡→🔴 | **EAV pivot**: 200M satırdan form başına ~40 attr topla+pivotla. Filtre **seçici**yse OK; **zayıf filtre** (status=yaygın) tüm kümeyi tarar → **P1** |
| §8.2 | Kalem-bazlı rapor (line-item) | 🟡 | `form_list_item` pivot + cross-form; on milyon satır (S7, **P4**) |
| §8.3 | List-of-model filtre/sıralama | 🟢 | Sayısal alt-alan `ix_li_num` ile index destekli; gösterimde pivot |
| §8.4 | Dile göre farklı sorgu | 🔴 | translation join, dile bağlı sıra (**P3**, **D7**) |
| §8.5 | Gruplama & toplama (cross-form aggregation) | 🔴 | On milyon `form_list_item`'da **canlı SUM/GROUP** → p95 aşımı → **incremental rollup (D6)** zorunlu (**P2**) |

### §9 Dış / API (24–28) — 🟢
| Item | Senaryo | Rating | Not |
|---|---|---|---|
| 24 | `GET /instances/{id}` | 🟢 | Tek PK okuma (form_value) |
| 25 | `PATCH /instances/{id}` | 🟡 | Yazma yolu (§4 → P5) |
| 26 | `GET /services/{id}/schema` | 🟢 | Metadata; code-keyed (S11/S12) |
| 27 | Webhook (`parameters`) | 🟢 | Value taşıma |
| 28 | `POST /instances/search` (barcode=X) | 🟢 | **GIN eşittir** (form_value) → rebuild bile gerekmez (S5); GIN 5M için tasarlanmış |

### §10 İlişkisel / alt-servis (29–32)
| Item | Senaryo | Rating | Not |
|---|---|---|---|
| 29 | Form List value aktarımı | 🟢 | Uygulama seviyesi yazma |
| 30 | Parent Property yansıması | 🔴 | → §5 (D4); A′ ise **P8** |
| 31 | Süreç adımı tetikleme value taşıma | 🟢 | — |
| 32 | Alt-servis listelenen value + **tik/seçim** (profil bazlı) | 🟡→🔴 | Filtreli liste + profil-kolon pivot'u form_attr'dan; **tik/seçim durumu** ayrı per-user-per-view tablo (**D14**) |

### §11 Değer tipleri / şekil
| Tip | Rating | Not |
|---|---|---|
| Skalar (metin/sayı/bool), Tarih | 🟢 | form_attr tipli kolonlar (num/text/date/bool) |
| List-of-model (Group By Tax, Key-Value, Form List) | 🟢 | `form_list_item` (pivot) |
| JSON/yapısal (Image Area nokta seti) | 🟡 | NONE→JSONB; sorgu jsonpath/GIN ile **sınırlı** |
| String-kodlanmış (Barcode) | 🟢 | text kolon / GIN |
| Referans: File | 🔴 | MinIO (D8) |
| Referans: user/org id | 🟢 | id kolon |
| Referans: yansıma (Parent/User/Flow) | 🔴 | → §5 (D4) |
| Koordinat (Map) | 🟡 | JSONB yapısal; geo-filtre gerekirse **PostGIS (D13)** |

---

## 🔴 Performans riskleri (detaylı)

| # | Risk | Tetikleyen | Neden 5M'de kritik | Azaltma / çözüm | S# |
|---|---|---|---|---|---|
| **P1** | Geniş çok-kolonlu rapor **pivot**'u | §8.1 | 200M satırdan form başına ~40 attr toplayıp tek satıra pivotlamak; **zayıf filtre** aday kümeyi daraltmaz → geniş tarama | Filtre-seçicilik disiplini · covering index · en ağır dashboard'lar için **denormalize rapor projeksiyonu (D11)** | S7/S13 |
| **P2** | Cross-form **canlı aggregation** | §8.5 | On milyon `form_list_item`'da canlı SUM/GROUP → p95 (<50ms) aşılır | **Incremental rollup tabloları (D6)** — olay başına delta UPSERT | S13 |
| **P3** | Kodlu alan **isim-sıralama/gruplama** | §6c/§8.4 | 200M satır + translation join; joined-name üzerinde btree yok → sort adımı; dile göre farklı sıra | **Translation katmanı (D7)** · defaultLang (kod→isim) cache | S6/S8 |
| **P4** | **Line-item pivot** | §8.2/8.3 | `form_list_item` EAV pivot + cross-form; on milyon satır | Sayısal sort `ix_li_num` (index'li) · pivot bounded · ağırsa rollup | S7 |
| **P5** | Yazma **projection lag** | §4/§25 | 5M yazma + form başına ~40 satır reproject + GIN bakımı → lag birikimi | Projektör **yatay ölçekle** · batch · projectionLevel ile attr azalt (D1) · lag alarmı | S2 |
| **P6** | **Bulk rebuild** süresi | S5/S12 | 200M satır rebuild ~100 dk; sırasında **kısmi sonuç** | Throttle + **"projection ready" sinyali (D10)** · partition-partition | S5 |
| **P7** | **GIN bakımı** | §4/§28 | 150-anahtar × 5M → pending list büyür, index ~15–30 GB, autovacuum yükü | `gin_pending_list_limit` · agresif autovacuum · GIN tek (form_value'da) | S9 |
| **P8** | Yansıma **A′ fan-out** | §5/§10-30 | Bir parent alan değişimi → N child reproject (kitlesel) | A′'yı **yalnız gerekli alana** sınırla · derinlik limiti + döngü tespiti · asenkron | S3/S4 |
| **P9** | **Partition sıcak-nokta** | tüm sorgular | HASH(service_id); dominant tenant/servis bir partition'ı ısıtır | Alt-HASH(organization_id) · büyük tenant'a LIST partition · en büyük partition metriği | S9/Bölüm16 |

---

## 🔧 Ek geliştirme gereksinimleri (detaylı)

| # | Geliştirme | Ne / neden | Zorunluluk | S# |
|---|---|---|---|---|
| **D1** | `Property.projectionLevel` (NONE/SEARCH/SORT/AGGREGATE) | Hangi alanın hangi düzeyde yansıyacağı; satır patlamasını + write-amp'ı kontrol eder | **Zorunlu** | S5 |
| **D2** | `Property.code` **immutable** + auto-generate + veri-öncesi draft | Rename problem sınıfını sıfırlar; JSONB/form_attr/dış-API kırılmasını önler | **Zorunlu** | S12 |
| **D3** | **Status** ayrı indeksli kolon (motor günceller, JSONB'de değil) | Volatile akış durumu; form_attr/JSONB'ye konursa bayat + write-amp | **Zorunlu** | S3/S4/S10 |
| **D4** | **Reflection mekanizması** — A/B/A′ kararı + (A′) `reflection_link` + propagation consumer | Parent→child yansıma yayılımı; **araştırmada YOK** | **Zorunlu** | S3/S4 |
| **D5** | **Audit/changelog tablosu** (append-only + partition + retention) | Değer geçmişi (kim/ne zaman); KVKK; form_attr değil | **Zorunlu** | §7-20 |
| **D6** | **Incremental rollup tabloları** | Ağır cross-form aggregation'ı canlı sorgudan çıkarır (P2) | **Zorunlu (P2)** | §8.5/Bölüm10 |
| **D7** | **Translation-aware sorgu katmanı** (kod→isim per-dil) + ops. defaultLang cache | İsim-sıralama/filtre/gruplama dile göre (P3) | **Zorunlu (P3)** | S6/S8 |
| **D8** | **MinIO** entegrasyonu (binary, URL-in-JSONB) | Dosya/görsel; JSONB'yi küçük tutar; "yavaş belge" | **Zorunlu** | §7-22 |
| **D9** | **Outbox relay + kuyruk + generic projektör** + stack kararı (NATS?) | Senkron omurgası; tüm projeksiyonu besler | **Zorunlu** | S2 (açık) |
| **D10** | **Bulk rebuild job + "projection ready" sinyali** | Şema evrimi/rename/metadata sonrası backfill + kısmi-sonuç koruması | **Zorunlu** | S5 |
| **D11** | Geniş dashboard için **denormalize rapor projeksiyonu** | En ağır §8.1 raporlarında pivot maliyetini aşmak | Koşullu (P1 ağırsa) | S13 |
| **D12** | Reflection **snapshot yazımı** (UserInfo/createDate write-time capture) | A-snapshot değerlerini yazımda JSONB'ye/native kolona sabitle | **Zorunlu** | S4 |
| **D13** | **PostGIS** (Map/geo sorgu) | Koordinat alanında geo-filtre gerekiyorsa | Koşullu | §11 |
| **D14** | Alt-servis **tik/seçim durumu** tablosu (per-user-per-view) | §10-32 seçim (tik) durumu; profil bazlı | Koşullu | §10-32 |

---

## Geliştirme → senaryo önkoşul haritası

| Bu geliştirme olmadan… | …şu senaryolar hedefi tutmaz |
|---|---|
| **D3 (status kolonu)** | §3 akış, §8 status-filtreli raporlar, §5 FlowInfo |
| **D4 (reflection)** | §5, §10-30 ParentProperty (canlı/rapor) |
| **D6 (rollup)** | §8.5 cross-form aggregation |
| **D7 (translation katmanı)** | §6c, §8.4, kodlu alan isim-sıralama |
| **D9 (outbox omurgası)** | §4/§25 tüm yazma→projeksiyon zinciri |
| **D8 (MinIO)** | §7-22 dosya/binary |

---

## Özet skor

| Rating | Kapsadığı yer (yaklaşık) |
|---|---|
| 🟢 Sorunsuz | §1 · §2 · §3 · §7(19/21/23) · §8.3 · §9(çoğu) · §10(29/31) · §11(skaler/liste/id/barcode) — **runtime yükünün çoğunluğu** |
| 🟡 Koşullu (benchmark/tuning) | §4 · §8.1 · §8.2 · §9-25 · §10-32 · §11(yapısal/Map) |
| 🔴 Ek geliştirme zorunlu | §5 · §6 · §7(20/22) · §8.4 · §8.5 · §10-30 · §11(file/yansıma) |
| ⚫ form_attr dışı | status (D3) · createdDate/creator (native kolon) · file (MinIO) |

**Genel hüküm:** `form_attr` = **skaler filtre/sıralama/detay-dışı sorgu için güçlü çekirdek**; senaryoların çoğunu 5M'de
sorunsuz karşılar. **Tam raporlama yüzeyi için tek başına yetmez** — yanına **zorunlu** olarak: **rollup (D6) + translation
katmanı (D7) + status kolonu (D3) + reflection mekanizması (D4)** + omurga (D9) + audit (D5) + MinIO (D8) eklenmeli.

**En kritik üçlü (bunlar olmadan ağır raporlar çalışmaz):** **D6 · D7 · D3.**

## Nihai öneri (faz sırası)

1. **Faz 0 — Çekirdek + zorunlu kurallar:** `form_value`(JSONB) + `form_attr` + `form_list_item` + **D1** (projectionLevel) +
   **D2** (code immutable) + **D3** (status kolonu) + **D9** (outbox omurgası) + **D8** (MinIO).
2. **Faz 1 — Raporlama yüzeyi:** **D7** (translation katmanı) + **D6** (rollup, ağır aggregation) + **D10** (rebuild+ready).
3. **Faz 2 — Yansıma & geçmiş:** **D4** (reflection A/B/A′ + A′ propagation) + **D12** (snapshot yazımı) + **D5** (audit/changelog).
4. **Faz 3 — Koşullu:** **D11** (denormalize rapor projeksiyonu) · **D13** (PostGIS) · **D14** (tik/seçim tablosu) — benchmark tetiklerse.
5. **Kapı:** Her fazdan önce ilgili **benchmark kalemleri** (P1–P9) kendi donanımımızda p95 ile doğrulanmadan "onaylandı" sayılmaz.

---

*İlgili: [`form_attr_questions.md`](./form_attr_questions.md) (S1–S13 kanıt) · [`form-value-scenarios.md`](./form-value-scenarios.md) (senaryolar) · [`index.md`](./index.md) (mimari).*
