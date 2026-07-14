# form_attr — Projeye Uygunluk Değerlendirmesi (Soru-Cevap)

> **Amaç:** [`form-deger-saklama-sunum.html`](./form-deger-saklama-sunum.html) araştırmasındaki **`form_attr`** projeksiyon
> tablosunun **Flovo BPM'e ne kadar uygun** olduğunu netleştirmek. Kullanıcının sorduğu sorular buraya **soru olarak** yazılır,
> cevapları kaydedilir; en sonda **toplu değerlendirme** yapılır.
>
> **⚠️ Durum:** 🟡 **AÇIK — değerlendirme sürüyor.** Sonuç bölümü, sorular bitince kapatılacak.
> Karara bağlanınca özet, `todo.md` "Property value depolama modeli" açık sorusuna ve ilgili tasarım dokümanlarına işlenecek.

---

## 0. `form_attr` nedir? (bağlam — araştırmadan)

`form_attr`, form değerlerinin **kaynağı değil**; JSONB kaynağından (`form_value`) türetilen, **arama/filtre/sıralama/rapor** için
optimize edilmiş bir **projeksiyon** tablosudur. Yapısal olarak **tipli bir EAV**'dir (her sorgulanabilir alan → 1 satır):

```sql
CREATE TABLE form_attr (
  form_id bigint, organization_id int, service_id int,
  property_code text,          -- HANGİ alan
  num_value numeric, text_value text,
  date_value timestamptz, bool_value boolean,
  PRIMARY KEY (form_id, service_id, property_code)
) PARTITION BY HASH (service_id);
```

Kritik özellikleri:
- **Sadece `projection seviyesi` ≥ SEARCH olan alanlar** yansıtılır (NONE olanlar JSONB'de kalır) → satır patlaması kontrol altında.
- **Tipli kolonlar** (num/text/date/bool) → `9 < 10` doğru sıralanır (klasik EAV'nin `"10" < "9"` hatası yok).
- **Sabit index seti** — alan adı (`property_code`) index'e kolon olarak girdiği için tek index tüm alanlara hizmet eder.
- **Yeniden üretilebilir** — silinse `form_value`'dan bit-bit aynı üretilir; içinde başka yerde olmayan tek bilgi yoktur.

---

## Soru-Cevap Kaydı

> Her yeni soru aşağıya **S1, S2, …** olarak eklenir. Format:
> **Soru** → **Cevap** → **Uygunluğa etkisi** (👍 lehine / 👎 aleyhine / ⚖️ nötr-koşullu).

### S1 — Bir instance detaylı açılırken property value'ları nereden çekilir?

**Soru:** Bir instance (form) **detaylı açılırken** property'lerin value'ları nereden çekilecek — `form_attr`'dan mı?

**Cevap:** **`form_attr`'dan değil — `form_value.data` (JSONB) tek satırından.** Formu göstermek = tek satır okumak
(`WHERE form_id=… AND service_id=…`); pivot/join yok. `form_attr` bir **projeksiyondur**, yalnız *çok kayıt arasında*
arama/filtre/sıralama/rapor içindir; tek bir formu göstermenin kaynağı **asla** değildir (araştırma: "Formu göstermek → *Buradan
asla — JSONB'den tek satır*").

Detay-açılışta ham (raw) değer JSONB'den gelir; gösterim için ek çözümlemeler olur ama **hiçbiri `form_attr`'dan gelmez**:

| Alan tipi | Detay açılışında value nereden gelir |
|---|---|
| Normal alan (tutar, tarih, metin) | Doğrudan `form_value.data` |
| Combobox / referans (kod tutulur) | Ham **kod** JSONB'den; görünen ad çeviri/`PropertyItem`'dan çözülür (gösterimde) |
| Yansıma — snapshot (Parent Property, User Info) | Zaten JSONB'ye **kopyalanmış**; JSONB'den okunur |
| Yansıma — canlı (Flow Info, güncel yönetici) | Okuma anında **kaynaktan join** (org/flow şeması) |
| List-of-model (`groupByTax` vb.) | İç içe dizi **JSONB'de**; `form_list_item` değil (o da çok-kayıt rapor projeksiyonu) |
| Dosya/görsel | JSONB'de sadece **URL**; dosya **MinIO**'dan render'da |

**Uygunluğa etkisi:** 👍 (bir koşullu notla) — Detay-açılış `form_attr`'a **hiç bağımlı değildir**: (a) **projection lag**
detay görünümünü etkilemez, kullanıcı kaydettiği formu anında/tam görür (JSONB anında tutarlı); (b) `form_attr`'ın eksik/bayat
olması **bir formu açmayı bozamaz** — riski yalnız liste/rapor tarafında kalır. ⚠️ Diğer yüzü: `form_attr` hiçbir zaman detay-okuma
yolunda olmadığından **tüm varlık gerekçesi çok-kayıt sorgu/rapor performansına** dayanır (raporlama ihtiyacı ağırsa haklı çıkar).

---

### S2 — Bir alan (value) güncellendiğinde value'lar DB'de nasıl güncel tutulur?

**Soru:** Bir alan güncellendiğinde value'lar (özellikle `form_attr`) DB'de nasıl güncel tutulacak?

**Cevap:** İki katman ayrı güncellenir: **`form_value` (kaynak) anında**, **`form_attr` (projeksiyon) asenkron** (birkaç yüz ms).

1. **Yazma — tek transaction (atomik):** `UPDATE form_value SET data=…, version=version+1` **+** `INSERT INTO outbox_event(...)`
   aynı transaction'da → yarım durum imkânsız; `form_value` anında güncel (kullanıcı kendi değişikliğini anında görür).
2. **Outbox relay** olayı alır → **NATS JetStream** (kalıcı kuyruk).
3. **Idempotent generic projektör** tüketir: metadata'yı okur → bu formun `form_attr`/`form_list_item` satırlarını **siler** →
   JSONB'deki güncel değerlerden `seviye ≥ SEARCH` olanları **tipine göre yeniden yazar** → `version` karşılaştırmasıyla idempotent.
4. Varsa **rollup** delta UPSERT.

**İki kritik karar:** (a) **delta değil, tam yansıtma** (sil+yeniden yaz) → idempotency tek `version` karşılaştırması,
duplicate/retry/restart/sırasız olay veriyi bozamaz; (b) **trigger değil Outbox** → kayıt yavaşlamaz, projeksiyon hatası kaydı geri almaz.

**"Tek alan değişti" ucuz mu?** Hayır, tam ucuz değil: `form_value`'da MVCC **tüm JSONB satırını** yeniden yazar; `form_attr`'da
formun **tamamı** yeniden yansıtılır (yalnız değişen alan değil). BPM insan-güdümlü olduğu için maliyet duvar değil ama sayılır
(JSONB küçük tutulur → dosya MinIO'da, `fillfactor=85`, agresif autovacuum).

**Alan TANIMI değişirse (metadata):** rename/type/seviye değişimi → yeni `metadata_version` + etkilenen servise **bulk rebuild**
(`form_value`'dan yeniden üret; ~1M form ≈ 20 dk). Eski formlar kendi `metadata_version`'ıyla yorumlanır → yanlış okunmaz.

**Uygunluğa etkisi:** 👍 + 👎/⚖️ — **👍** Güncel tutma **otomatik ve merkezi** (tek generic projektör, alan adı koda gömülü değil →
yeni alan/servis için kod yok), idempotent + rebuild edilebilir → dayanıklı. **👎/⚖️** Bedeli: (1) **eventual consistency** —
value değişince `form_attr` birkaç yüz ms bayat (rapor/liste tarafında); (2) **write amplification** ≈15-40 fiziksel iş / value
değişimi; (3) güncel tutma **outbox relay + kuyruk + projektör** altyapısına bağımlı (işletilecek hareketli parçalar).

---

### S3 — Yansıma alanlarının (FlowInfo · UserInfo · ParentProperty) value'ları nasıl sync tutulur?

**Soru:** Kullanıcının doğrudan değiştirmediği yansıma alanları — FlowInfo (motor ilerledikçe değişen statü), UserInfo,
ParentProperty (parent instance'taki hedef alan değişince) — value'ları DB'de nasıl güncel/sync tutulacak?

**Cevap:** Tek "sync" mantığı yok; **üç tipin doğru cevabı farklı** (bu, `form-value-scenarios.md §5` kararı):

- **FlowInfo (statü/adım/süre) → kopyalanmaz, CANLI.** Forma ait değil, **süreç durumudur** → `ProcessInstance`/`ProcessStepInstance`
  state'inde veya `Instance.status` kolonunda tutulur; motor adım-geçiş transaction'ında **tek yeri** günceller; rapor **canlı** okur.
  Senkronlanacak kopya yok. (JSONB'ye yazsaydık: her statü değişimi = tüm satır yeniden yazımı + yine bayatlama → araştırma:
  "kopyalansa hep bayat kalır".)
- **UserInfo → SNAPSHOT, dondurulur.** Oluşturma anında bir kez `form_value.data`'ya kopyalanır, sonraki değişikliklerle **bilerek
  senkronlanmaz** (audit doğrusu). Bilinçli canlı alt-alan (ör. "güncel yönetici") → kopyalanmaz, **okuma anında join**.
- **ParentProperty → asıl A/B/A′ kararı:**
  - **A Snapshot:** yansıma anındaki değer kopyalanır, donar. Sync yok. En ucuz; audit için doğru olabilir.
  - **B Referans + on-read:** child yalnız `parentInstanceId + propertyCode` tutar; değer **okuma anında join**. Hep güncel, sync gerekmez; filtre/sıralama zor.
  - **A′ Materialized + propagation:** kopyalar **ve** parent değişince otomatik güncellenir → **event-driven fan-out**:
    parent `form_value` update → `outbox_event` → **reflection-propagation consumer** → `reflection_link(parentInstanceId,
    parentPropertyCode, childInstanceId, childPropertyCode)` kayıt tablosundan etkilenen child'lar bulunur → her child'ın
    `form_value`'su güncellenir → child'ın kendi outbox'ı → `form_attr` yeniden yansıtılır. **Fan-out sınırlanmalı** (derinlik
    limiti + döngü tespiti + asenkron). ⚠️ Araştırma dokümanı bu propagation'ı **çözmüyor** — projeye bırakıyor (gerçek boşluk).

**Uygunluğa etkisi:** karışık — **👍** Değer bir kez `form_value.data`'ya yazıldıysa (UserInfo snapshot / A′ propagate) `form_attr`
onu **sıradan alan gibi** yansıtır, özel-durum yok. **👎** (a) **Referans-only (B) yansımalar** JSONB'de olmadığından `form_attr`
bunları **indeksleyemez** → filtre/sıralama join ister; (b) **FlowInfo/statü `form_attr`'ın işi değil** (JSONB'de değil) → statü
raporu **ayrı indeksli status kolonu/projeksiyon** ister; `form_attr` süreç-durumu raporlamasını **kapsamaz**. **⚖️** A′ propagation
S2 write-amplification'ını **katlar** (1 parent değişimi → N child re-projection). **Net:** `form_attr` = kullanıcı-girdisi +
snapshot + propagate-edilmiş değerler için yeterli; **canlı referans-only yansımalar ve flow/statü için değil** → yanında ayrı çözüm gerekir.

---

### S4 — UserInfo+değişmez FlowInfo→A, ParentProperty+status→B mantıklı mı? (§5/§8'e göre en uygun yöntem)

**Soru:** UserInfo ve değişmez FlowInfo alanları (creatorName, createDate, instanceId) için **A**; ParentProperty ve sync
gereken FlowInfo (status) için **B** uygulamak mantıklı mı? `form-value-scenarios.md`'ye göre en uygun yöntem ne?

**Cevap:** Kısa: sezgin doğru ("değişmez→A, değişken→B" isabetli eksen; FlowInfo'yu monolitik görmemek de doğru — §5 hem
`createdDate` hem `currentStatus`'ü Flow Info sayar ama değişkenlikleri zıt). Aşağıda en uygun yöntemi **sade** anlatıyorum.

**Ana fikir (tek cümle):** Bir yansıma değerini ya **kayda yazarsın (kopya)** ya da **yazmayıp okurken kaynaktan çekersin (canlı)**.
Tek gerçek bedel:
- **Kayda yazarsan** → üzerinde kolay **rapor/filtre/sıralama** (değer kayıtta hazır), **ama** kaynak değişince **bayatlayabilir**.
- **Yazmazsan (canlı)** → **her zaman güncel**, **ama** rapor/sıralama **zorlaşır** (her okumada kaynağa join).

**Üç yöntem (benzetmeyle):**
| Yöntem | Ne yapar | Benzetme |
|---|---|---|
| **A-snapshot** | Değeri bir kez kopyalar, **dondurur** | 📷 **Fotoğraf** — kaynak sonra değişse de fotoğraf aynı kalır |
| **B (canlı)** | Hiç yazmaz; okurken kaynaktan bakar | 🪟 **Pencereden bakmak** — her bakışta güncel hali |
| **A′** | Kopyalar **ve** kaynak değişince kopyayı da yeniler | 📷🔄 **Fotoğrafı sürekli tazelemek** — pahalı (kaynak değişince tüm kopyaları bulup güncelle = fan-out) |

**En uygun yöntem = sadece 2 soru:**
1. **"Bu değer forma yazıldıktan sonra değişir mi?"**
   - **Değişmez** → 📷 **A-snapshot.** Bitti (bayatlama yok, üstelik kopya olduğu için rapora da girer — en kolay kazanç).
   - **Değişir** → Soru 2.
2. **"Bu alan üzerinde rapor/filtre/sıralama yapacak mıyım?"**
   - **Hayır, sadece göstereceğim** → 🪟 **B (canlı).** Hep güncel, saklamıyorsun, rapor derdi yok.
   - **Evet** → zor durum: alan **statü** ise → **motor-güncellemeli status kolonu** (kolon olduğu için yine raporlanabilir = "iyi
     huylu B"); alan **parent değeri** ise → 📷🔄 **A′** (yalnız burada bu masrafa değer).

**Alan-alan (senin örneklerinle):**
| Alan | Değişir? | Rapor? | Yöntem | Neden |
|---|---|---|---|---|
| `createDate` | Hayır | Evet | 📷 snapshot → aslında **hazır kolon** (`created_at`) | Oluşturma tarihi hiç değişmez; zaten kolon, kopyalamaya gerek yok |
| `instanceId` | Hayır | Evet | zaten **id kolonu** (`form_id`) | Kaydın kimliği, değişmez |
| `creatorName`/departman (UserInfo) | "O anki" hali istenir | Evet | 📷 **snapshot (dondur)** | "Fatura kesildiğinde departman neyse o" — audit doğrusu (kişi sonra terfi etse de eski masrafta eski unvan) |
| `currentStatus` (FlowInfo) | **Evet, sürekli** | Evet (çok) | 🪟 **B** = motor-güncellemeli **status kolonu** | Akış boyunca değişir; kolonda tutunca hem canlı hem raporlanabilir |
| **ParentProperty** | Duruma göre | Duruma göre | ↓ | Semantiğe bağlı |

**ParentProperty — topluca B değil, ne istediğine göre:**
- *"Alt-form oluşturulduğu **andaki** değer dursun"* (audit) → 📷 **A-snapshot** (ucuz, rapora girer; §5 notu da böyle diyor).
- *"Parent'ın **güncel** değerini hep göster"* (senin projectCode örneğin) → 🪟 **B**.
- *"Hem güncel olsun **hem de** çok-form üzerinden grupla-topla (§8.5)"* → 📷🔄 **A′** (yalnız bu ağır durumda).

**Tek cümlelik kural:** **Değişmez → fotoğrafla (snapshot; mümkünse var olan kolonu kullan) · değişen ama sadece gösterilen →
pencereden bak (B) · değişen VE ağır raporlanan → ancak o zaman tazele (A′).**

**Uygunluğa etkisi:** **Fotoğrafladıkların** (snapshot + A′) `form_attr`'a girer, kolay raporlanır; **canlılar** (status, güncel
parent) `form_attr`'a girmez → ayrı **kolon** (status) veya **join** (parent) çözer. Yani en uygun yöntem, `form_attr`'ı gereksiz
şişirmeden her alanı en ucuz doğru yere koymak. **👍** Rapora giren yansımaların çoğu değişmez (createDate/creator/UserInfo-anı) →
snapshot → native kolon ya da `form_attr` → raporlama yüzeyi temiz kapsanır. **👎** Tek gerçek boşluk: *değişken + ağır-rapor*
parent alanı (§8.5) → A′ şart (tasarlanacak tek pahalı parça). **⚖️** status raporu `form_attr` değil ayrı status kolonu → S3'ü pekiştirir.

---

### S5 — Daha önce sorgulanmadığı için `form_attr`'da olmayan bir alan, yeni custom code'da gerekince ne yapılır?

**Soru:** Var olan bir sürece yeni custom code geliştirilirken, daha önce `WHERE`'de kullanmadığımız (o yüzden `form_attr`'a
yazmadığımız) bir alana artık ihtiyaç doğarsa nasıl aksiyon alınır?

**Cevap:** Bu, mimarinin **en güçlü** olduğu senaryolardan biri. Önce **sorgu tipine** bak — bazen hiç aksiyon gerekmez:

| Yeni sorgu ne istiyor? | Aksiyon |
|---|---|
| **"alan = X" / içerir** (eşittir/containment) | **Hiçbir şey** — `form_value` üzerindeki **GIN her alanı** kapsar; custom code doğrudan sorgular |
| **Aralık (`>`/`<`), ORDER BY, prefix, ILIKE, toplam** | `form_attr`'a **terfi** gerekir → 3 adım |

**Terfi 3 adım (DDL/migration YOK):**
1. **Metadata değiştir (veri, şema değil):** alanın **projection seviyesi** `NONE → SEARCH/SORT/AGGREGATE`. Alan zaten JSONB'de
   vardı; projektöre "bundan sonra bunu da yansıt" demek. `ALTER TABLE` yok.
2. **Bulk rebuild:** servisin `form_value`'sundan geçmiş kayıtları aynı generic projektörle **backfill** (partition-partition,
   10k batch, throttle'lı, ~1M ≈ 20 dk). Yeni yazımlar zaten otomatik yansır → backfill yalnız eski kayıtlar.
3. **"Projection ready" sinyalini bekle:** rebuild bitene dek `form_attr` verisi kısmi → sorguyu otoritatif sayma (o ana dek
   GIN/JSONB'den oku).

**Yeni index GEREKMEZ:** `form_attr` index seti sabit+generic (`service_id, property_code, num_value`…); `property_code` index'te
kolon olduğu için tek index tüm alanlara hizmet eder → yeni sorgulanabilir alan = **yeni satır, yeni index değil**. (İstisna:
fuzzy/full-text → `pg_trgm` zaten kurulu/tek seferlik.) Alan liste-içi ise hedef `form_list_item` (aynı mantık); yansıma ise S3/S4.

**Uygunluğa etkisi:** güçlü **👍** — (a) **Geçmiş veri kaybolmamış** (alan `form_attr`'da olmasa da JSONB kaynakta hep vardı) →
backfill mümkün; klasik kolon/tablo tasarımında bu = canlı `ALTER TABLE` + migration + downtime, burada = **metadata flip + arka
plan rebuild**; (b) **karar geri alınabilir** (NONE'a çevir, satırları sil); (c) bazen **hiç rebuild gerekmez** (eşittir→GIN);
(d) **sabit index** → yeni alan yeni index istemez. **⚖️/👎** Bedel: rebuild süresi + I/O; alan artık her yazımda `form_attr`'a
+1 satır (kalıcı write-amplification artışı → yalnız gerçekten sorgulanan alanı işaretle); rebuild sırasında kısmi sonuç → "hazır"
sinyali gerekir. **Tasarım çıkarımı:** `Property` modeline **`projectionLevel`** (NONE/SEARCH/SORT/AGGREGATE) alanı eklenmeli
(`property.md`) — sorgulanabilirlik kararını taşıyan yer.

---

### S6 — `form_attr`'da tutulan combobox'ı raporda İSME göre sıralarken sorun olur mu?

**Soru:** `form_attr`'da tutulan bir combobox'ı raporda **isme göre** sıralamak istediğimizde sorun yaşar mıyız?

**Cevap:** **Evet, gerçek bir sınırlama** — çünkü `form_attr` combobox için **kodu** tutar, **ismi değil**; üstelik isim **dile bağlı**
(§6c/§8.4). Somut: `0=Yemek·1=Konaklama·2=Ulaşım`, form_attr'da değer `"0/1/2"` (kod). Üç farklı sıra:
- **Koda göre** (form_attr'da olan): Yemek→Konaklama→Ulaşım
- **İsme göre tr:** Konaklama→Ulaşım→Yemek · **İsme göre en:** Accommodation→Meal→Transport

→ `ORDER BY form_attr.text_value` **kodu sıralar = yanlış sıra.**

**Bu bir hata değil, bilinçli:** kod saklamak rename-safe + dilden bağımsız (§14: "A101→A-101 Market olsa da veri bozulmaz").
İsim bir **gösterim/sorgu-anı** meselesidir.

**Çözüm — ismi sorgu anında çöz:** kodu `property_item`/`translation`'a **join** et (`item_code + languageCode + organizationId`),
`ORDER BY isim`. Neden ucuz+doğru: (a) **combobox düşük kardinalite** (3-50 öğe) → çeviri tablosu minik → join küçük; (b) her zaman
**güncel** (rename → sıra otomatik değişir, bayatlama/rebuild yok); (c) **dile doğru** (tr→`definition`, en→`translation` join — §6a/§6b/§6c).

**Neden ismi form_attr'a YAZMIYORUZ:** (1) dil patlaması (isim dile bağlı → dil-başına satır); (2) rename'de bayatlama geri gelir
(kod-saklamanın kaçındığı dert). İstisna: yalnız `defaultLang` ismini snapshot'layıp hızlı sıralama = bilinçli sınırlı taviz.

**Uygunluğa etkisi:** **👎/⚖️** `form_attr` **tek başına** combobox'ı isme göre sıralayamaz → **translation join şart**; kodlu
alanların isim-sıralı/gruplu raporlarında form_attr *gerekli ama yeterli değil*. Ölümcül değil (düşük-kardinalite join, üstelik
dile-duyarlı + rename-safe = doğru davranış; tasarım §6c/§8.4'te öngörülmüş). **⚖️ Performans:** büyük sonuç kümesini join'lenmiş
isme göre sıralamak saf btree taramasından ağır → ağır isim-sıralı raporlarda **dil-başına (kod→isim) küçük indeksli tablo** veya
defaultLang-ismi projeksiyonu → **benchmark kalemi.**

---

### S7 — `form_list_item`'daki (groupByTax) kalem-bazlı raporda tax alanına göre sıralama ne olur?

**Soru:** `groupByTax` gibi `form_list_item`'da tutulan bir alanın **kalem-bazlı** raporunda **tax alanına göre** sıralama
istenirse ne olur?

**Cevap:** **"tax" sayısal oran (`vergiOranı`=18/8) ise sorun yok — index destekli, `form_list_item`'ın birinci sınıf işi.** İki nüans var.

Saklama EAV: her alt-alan ayrı satır (`form_id, list_code, item_index, attr_code, num/text/date/bool`), index `ix_li_num
(service_id, list_code, attr_code, num_value)`.

**Sayısal tax sort → sorunsuz:**
```sql
SELECT form_id, item_index, num_value FROM form_list_item
WHERE service_id=42 AND list_code='groupByTax' AND attr_code='vergiOranı'
ORDER BY num_value DESC;      -- ix_li_num'dan sıralı; form_id filtresi yoksa cross-form (§8.3/§8.5)
```

**Nüans 1 — EAV pivot:** kalem-bazlı rapor kalemi **tek satırda** ister (giderTürü|vergiOranı|tutar) ama bunlar ayrı satır →
`(form_id, item_index)`'e göre **pivot** gerekir. Sıralama anahtarı (vergiOranı) index'ten sıralı geldiği için ucuz; pivot sınırlı
(kalemde birkaç alt-alan); form-düzeyi alanlar `form_id` PK join'i. Ağır cross-form kalem raporu = **benchmark kalemi**.

**Nüans 2 — kodlu alt-alan → S6 tekrar:** sıralanan alan sayısal değil **kodlu/çevirili** alt-alansa (ör. `giderTürü`) →
`text_value` **kodu** tutar, isim dile bağlı → isme göre sıralama **translation join** ister (S6 ile aynı). Sayısal oranda bu yok.

**Nüans 3:** eşit değerlerde tiebreaker `ORDER BY num_value, form_id, item_index` (kararlı pagination).

**Uygunluğa etkisi:** **👍** Liste alt-alanına **sayısal/skaler sıralama-filtre** `form_list_item`'ın birinci sınıf işi (`ix_li_num`,
cross-form dahil). **⚖️** EAV → kalemi tek satıra toplamak için **pivot** (sınırlı; ağır raporda benchmark). **👎** (S6 mirası)
alt-alan kodlu/çevirili ise isim-sıralama yine **translation join** ister.

---

### S8 — `form_attr`/`form_list_item`'a `display` + `translationCode` ek kolonları koymanın avantaj/dezavantajı?

**Soru:** `form_attr` ve `form_list_item`'a `display` (çözülmüş isim) ve `translationCode` (çeviri anahtarı) gibi iki ek kolon
koymanın ne gibi avantaj/dezavantajları olur?

**Cevap:** İki kolonun **risk profili çok farklı** — ayrı değerlendirilmeli.

**`translationCode` (kararlı çeviri anahtarı) — düşük riskli, mantıklı ✅**
- **Avantaj:** dil-doğru join'i **tek hop**a indirir (`translationCode + languageCode`); **rename ile değişmez** → snapshot güvenli,
  kod-saklamanın rename-safe ilkesini **bozmaz**; projektör metadata'dan üretir.
- **Dezavantaj:** küçük depolama; sakladığın değer zaten **stabil semantik kod** ise **redundant**.
- **Verdict:** ekle **veya** değerin stabil kod olmasını garantile.

**`display` (çözülmüş isim) — cazip ama tehlikeli denormalizasyon ⚠️**
- **Avantaj:** join'siz isim-sıralama/filtre (S6/S7'yi çözer); export/PDF'te ismi hazır okur.
- **Dezavantaj:** (1) **dile özgü** → tek kolon tek dile hizmet eder; çoklu dil = satır patlaması, farklı dilde yine join;
  (2) **bayatlama + yeni invalidation kanalı (asıl mesele):** `display`'in kaynağı `translation` tablosu, `form_value` **değil**;
  ama projeksiyonlar `form_value` outbox'ıyla yeniden üretiliyor → çeviri/rename düzenlemesi outbox'ı **tetiklemez** → `display`
  **sessizce bayatlar**. Güncel tutmak için **çeviri-değişti → etkilenen satırları rebuild** eden yeni bir fan-out gerekir (S3/S4
  A′'nın aynısı; bir rename binlerce geçmiş satırı dokunabilir); (3) depolama/write-amp artışı (özellikle yüksek-hacimli
  `form_list_item`); (4) rename-safe ilkesini kısmen bozar.
- **Verdict:** **varsayılan ekleme.** Ancak benchmark isim-sıralamayı gerçek darboğaz gösterirse **yalnız `defaultLang` display**'i,
  açıkça bir **cache** olarak (çeviri-değişti-rebuild job'ıyla); farklı diller yine join.

**Uygunluğa etkisi:** **👍** `translationCode` (veya değeri stabil kod tutmak) S6/S7 join'ini ucuzlatır — düşük riskli ergonomi.
**⚖️/👎** `display` S6'nın **join maliyetini** **bayatlama + çeviri-rebuild** maliyetiyle **takas eder** (bedava değil, yatay
kaydırma); combobox düşük-kardinalite olduğundan S6 join'i zaten ucuzdu → `display` çoğu zaman daha pahalı. **Kural:** kaynağı
`form_value` akışının dışında olan bir değeri projeksiyonda materialize etme — sessiz bayatlama riski (bu, S3/S4 snapshot/A′ ile
aynı ilke).

---

### S9 — Instance'ta 150+ property → büyük JSONB karakter sayısı sorun olur mu?

**Soru:** Bir instance'ta 150+ property olduğunu ve bu yüzden ortalama JSONB boyutunun büyük olduğunu varsayarsak sorun olur mu?

**Cevap:** Belirleyici olan alan **sayısı** değil, toplam **bayt boyutu** ve **güncelleme sıklığı**. 150 alan tek başına sorun değil.

**Sayı→bayt:** 150 küçük-değerli alan (~50 B) ≈ **~7.5 KB**; ~10'u uzun metin (1-2 KB) ise ~**25-30 KB** (yönetilebilir, update
maliyeti hissedilir); ortalama **100+ KB** ise büyük gömülü içerik vardır (asıl bakılacak yer). Yani hangi alan şişiriyor, o önemli.

**Postgres eşikleri:** ~2 KB → **TOAST** (satır-dışı, sıkıştırılmış, **okuma şeffaf** — tasarlanmış davranış). **Sert limit YOK:**
JSONB tek değer → tablonun **1600-kolon limiti uygulanmaz**; ~255 MB'a kadar. *(Artı: 150 alan "kolon-başına-alan"da DDL/limit
cehennemiyken JSONB'de sıradan.)*

**Asıl maliyet = YAZMA (okuma değil):** MVCC her update'te **tüm JSONB satırını** yeniden yazar (S2) → büyük satır = daha çok
bayt + WAL + bloat + autovacuum; GIN'li kolon HOT-update yapamaz → 150 anahtar = daha büyük GIN + pending list. Maliyet **alan
sayısıyla değil, `satır boyutu × update sıklığı` ile** ölçeklenir. **Okuma neredeyse etkilenmez** (detay = tek satır; TOAST
decompress küçük CPU).

**Projeksiyon şişmez:** 150 alan ≠ 150 `form_attr` satırı → yalnız sorgulanabilir alt-küme (~%10-20) yansır (S5) → rapor/arama
tarafı etkilenmez.

**Gerçek sorun + çözüm:** büyük **metin/binary** → **MinIO'ya taşı** (JSONB'de url); çok **sık güncelleme** (büyük satır × yüksek
frekans) → write-amp duvarı, **benchmark**'ta ölç (BPM insan-güdümlü → nadir); büyük **yapısal/nadir sorgulanan** alan (Image Area,
Map) → projeksiyon **NONE**, JSONB'de kalır; partition **HASH(service_id)** → vacuum/backup küçük parçalarla. Ayarlar:
`fillfactor=85`, agresif autovacuum, TOAST sıkıştırma (~%40).

**Uygunluğa etkisi:** **👍** `form_attr` bu şişmeden **etkilenmez** (yalnız alt-küme yansır); detay-okuma etkilenmez; 150 alan
JSONB'nin kolon-başına-alana karşı **kazandığı** yer (limit/DDL yok). **⚖️** Yük `form_value` (JSONB) **yazma** tarafında (WAL/bloat/
vacuum/GIN) → **benchmark kalemi** (Bölüm 17). **👎 potansiyel:** JSONB gerçekten şişkin (büyük içerik) **VE** sık güncelleniyorsa →
duvar; ama bu **içerik problemi** (MinIO'ya taşınır), 150 **alan** problemi değil.

---

### S10 — JSONB'yi instance tablosunda kolon olarak mı, yoksa 1-1 ayrı tabloda mı tutmalı?

**Soru:** JSONB verisini instance tablosunda yeni bir sütunda mı tutmak daha mantıklı, yoksa sırf JSONB'yi tutan, instance ile
1-1 ilişkili ayrı bir tabloda mı?

**Cevap:** İkisi de geçerli; belirleyici **churn oranı** (instance'ın küçük kolonları — özellikle `status` — JSONB'ye göre ne kadar
sık değişiyor). **Kritik nüans:** **TOAST zaten fiziksel ayrımı büyük ölçüde yapıyor** — büyük JSONB (>~2KB) satır-dışı saklanır,
`status` update'i **TOAST'lanmış JSONB'yi yeniden yazmaz** (yeni tuple aynı TOAST parçalarına işaret eder). Yani "tek tablo = her
status update'inde JSONB yeniden yazılır" **yanlış**; research'ün `form_value` tasarımı da tek tablodur.

**Tek tabloda kalan sorunlar:** (1) ana-tuple churn'ü → GIN'i taşıyan tabloda **bloat**; (2) **GIN churny tabloda**; (3) autovacuum
sık-churn (status) + seyrek-churn (JSONB) arasında **uzlaşmak** zorunda.

**Split (Option B: `instance` küçük/sık-churn + `instance_data(instance_id, data)` büyük/seyrek-churn) kazandırır:** churn izolasyonu
(status yalnız minik tabloyu bloat'lar), **bağımsız vacuum/fillfactor**, **GIN sakin tabloda**, dar hot-tablo cache yoğunluğu.
**Kaybettirir:** full-read'de PK-join, 2-satır insert, FK/cascade tutarlılık.

**Öneri (pragmatik):** (1) **Tek tabloyla başla (A)** — TOAST + basitlik yeterli, detay-okumada join yok; (2) **her hâlükârda `status`
gibi sık-değişen küçük alanları JSONB'ye değil ayrı KOLON tut** (research: "güncellenen meta JSONB'de değil ayrı" — A/B'den bağımsız
zorunlu kural); (3) benchmark **status-churn bloat/vacuum**'unu darboğaz gösterirse **Option B'ye geç** (geri-alınabilir, düşük-riskli
refactor). Yani A/B **doğruluk değil, benchmark-güdümlü optimizasyon** kararı; kırmızı çizgi: churny alan **asla JSONB içinde değil**.

**Uygunluğa etkisi:** **⚖️** `form_attr`'ı **etkilemez** (o zaten ayrı projeksiyon) — tamamen `form_value` fiziksel yerleşimi. **👍**
Doğru default net (tek tablo + status ayrı kolon; split cepte-hazır optimizasyon), ikisi de mimariyle uyumlu, karar geri alınabilir.
**Benchmark kalemi:** "status churn'ü altında ana-tablo bloat/vacuum süresi" → B'ye geçiş eşiği.

---

### S11 — `form_attr`'da `property_id` yerine neden `property_code` tutuluyor?

**Soru:** `form_attr` tablosunda `property_id` (numeric FK) tutmak yerine neden `property_code` (metin kod) tutuluyor?

**Cevap:** Çünkü **kaynak (JSONB) zaten code-keyed** → projeksiyonu da code ile anahtarlamak kaynakla tutarlı + join'siz sorgulanabilir kılar.

- **JSONB code-keyed:** `data = {"amount":1800, "barcode":"…"}` (anahtarlar kod). Projektör `for (code,value) in data` döner (Bölüm 11) →
  kod zaten elde, `form_attr`'a yazmak **bedava**; `property_id` yazmak her alan için metadata'dan `code→id` çevirmeyi gerektirirdi.
- **Aynı dilde sorgu:** JSONB kodla (`data @> '{"amount":…}'`), form_attr kodla (`property_code='amount'`) → tutarlı; API/custom-code
  alanları **koda göre** tanır (`/schema` kodları döner) → `WHERE property_code='amount'` **metadata join'siz**.
- **FK'sız/atılabilir:** projeksiyon rebuild edilebilir; `id→Property` FK'sı atılabilir tabloya integrity + partition/rebuild yükü
  getirir. Kod, mutable tanım tablosuna bağımlılık kurmadan alanı tanımlar.
- **Self-describing + metadata-versiyonları arası anlamsal sabitlik:** satıra bakınca alanı bilirsin (join yok); `code` bir servis
  içinde alanın anlamsal kimliği (surrogate id versiyonlar arası yeniden atanabilir).

**`property_id`'nin tek avantajı = depolama** (`int` 4B < `text`); ama sınırlı (yalnız sorgulanabilir alt-küme yansır, kodlar
kısa) ve karşılığında **her sorguda bir metadata join'inden** kurtulursun → projeksiyon için doğru takas. Aşırı ölçekte kod-intern
sözlüğü düşünülebilir ama join'i geri getirir (yalnız benchmark depolamayı darboğaz gösterirse).

**Rename nüansı:** kod saklamak rename'de rebuild ister (S5) ama JSONB de code-keyed olduğundan rename zaten kaynakta rebuild
gerektirir → `id` bu problemi tam çözmez, erteler.

**Uygunluğa etkisi:** **👍/nötr** tutarlılık/ergonomi kazancı (kaynakla aynı anahtar, join'siz, FK'sız). **⚖️** depolama fazlası —
aşırı ölçekte benchmark kalemi. **Tasarım çıkarımı:** `form_value.data` **code-keyed** olmalı; `Property.code` bir servis içinde
**benzersiz + stabil** (rename = ayrı, yönetilen olay).

---

### S12 — `property_code` sonradan değişirse sorun olur mu? Düzeltme maliyeti? Code update'i engellemek çözüm mü?

**Soru:** `property_code` sonradan değişirse sorun yaşanır mı, düzeltme maliyeti ne olur, code update'ini engellemek çözüm olur mu?

**Cevap:** **Evet sorun çıkar** — ama asıl maliyet storage değil **referanslar**; ve **code'u dondurmak en doğru çözüm.**

**İki katman kırılır:** (1) **Storage (sınırlı):** JSONB eski-kod-anahtarlı (`{"amount":…}`), form_attr eski kodla → yeni sorgu eskileri
bulamaz. `metadata_version` **okumayı** kurtarır ama **sorgu-kimliğini** değil (`v14.amount==v15.expenseAmount` bilgisi = rename'i
aşan stabil kimlik gerekir; code onu sağlamaz). (2) **Referanslar (asıl acı):** iş-kuralları, view-profile, hesaplamalar,
yansıma-eşleşmeleri ve **en kötüsü dış custom-code/API** kodu kimlik olarak kullanır → rename = **müşteri için kırıcı API değişikliği**
(kontrol sende değil).

**Düzeltme maliyeti:** **Yol A (rename'e izin + migrate):** kitlesel JSONB rewrite (whole-row × tüm formlar) + form_attr rebuild +
tüm referans güncelle + dış API tüketici bildirimi → **yüksek + riskli + dış kırılma.** **Yol B (kimlik/etiket ayrımı):** aşağıda.

**Q3 → Evet, code'u immutable yapmak DOĞRU çözüm:** kullanıcının değiştirmek istediği şey **code değil, görünen isim (display
label)** — o zaten ayrı katman: `definition`/`translation` (S6), mutable, **depolamaya dokunmaz**. Ayrım:
- **`code`** (`amount`) = teknik kimlik (JSONB anahtarı, form_attr, iş-kuralı, dış API) → **dondurulur** (DB kolon adı / API field gibi).
- **`definition`/`translation`** (`"Tutar"`) = insan-okur isim → **serbest** (çeviri düzenlemesi).

Kodu dondurmak **tüm rename problem sınıfını sıfır sürekli maliyetle** kaldırır (JSONB rewrite/rebuild/kırılan referans yok) ve
S11'i tamamlar (JSONB/form_attr code-keyed **ve** code immutable → kod hem okunabilir kimlik hem stabil anahtar).

**Nüanslar:** (1) typo için **"draft" penceresi** — kod yalnız **veri yokken** (ilk instance öncesi) değişebilir, sonra kilitlenir;
(2) kodu **auto-generate** et (kullanıcı yalnız etiketi düzenler) → sorunu by-pass; (3) zorunlu rename = **explicit nadir şema
migrasyonu** (admin arkası; kitlesel rewrite/alias + rebuild + API versiyonlama), sıradan Designer tıkı değil.

**Maliyet karşılaştırması:** mutable code → her rename = kitlesel rewrite + rebuild + dış API kırılması (pahalı/riskli); frozen code
→ rename maliyeti **~0** (label'ı değiştirirsin = trivial çeviri düzenlemesi).

**Uygunluğa etkisi:** **⚖️→👍** rename sorunu **gerçek ama tamamen tasarımla önlenebilir** → `form_attr`'a karşı zayıflık değil,
bir **Property-model kuralı**; kuralla S11 code-keying tamamen güvenli. **Tasarım çıkarımı (`property.md`):** `Property.code`
**immutable** (veya yalnız veri-öncesi draft'ta değişebilir), tercihen **auto-generated**; kullanıcı-görünür isim = `definition`/
`translation` (serbest).

---

### S13 — Tüm senaryoların ölçekli (5M+ instance · 150+ prop · 40+ form_attr) değerlendirmesi + risk/geliştirme listesi

**Soru:** `form-value-scenarios.md` bu klasöre taşındı. 5M+ instance · instance başına 150+ property · form_attr'da 40+ property
varsayımıyla **tüm senaryolar** `form_attr` ile sorunsuz çalışır mı? Performans riski / ek geliştirme gereken konuları listele.

**Ölçek:** 5M instance × 40 = **~200M form_attr satırı**; 150+ prop → form_value ~150GB (TOAST'lı); ~50M+ form_list_item.

**Genel hüküm:** Runtime yükünün **çoğunluğu** (tek-form okuma/yazma/detay [§1-§3], basit filtre/arama [§9-28], skaler rapor)
5M'de **sorunsuz**. Riskler sınırlı kümede: **ağır çok-kolon/aggregate rapor, kodlu-alan isim-sıralama, yansıma yayılımı, yazma
throughput'u.** Showstopper yok ama bazıları 5M'de **zorunlu**.

**🔴 Performans riskleri (öncelik):**
- **P1** Geniş çok-kolonlu rapor **pivot**'u (§8.1) — 200M satırdan form başına ~40 attr topla+pivotla; **zayıf filtre** tüm kümeyi tarar. *(en yüksek)*
- **P2** Cross-form **canlı aggregation** (§8.5) — on milyon form_list_item'da SUM/GROUP → p95 aşımı.
- **P3** Kodlu alan **isim-sıralama/gruplama** (§6c/§8.4) — translation join + dile bağlı sıra, btree'siz (S6/S8).
- **P4** **Line-item pivot** (§8.2/8.3) — form_list_item EAV pivot + cross-form (S7).
- **P5** Yazma **projection lag** (§4/§25) — 5M yazma + form başına ~40 satır reproject (S2).
- **P6** **Bulk rebuild** süresi (S5/S12) — 200M satır ~100dk + kısmi sonuç.
- **P7** **GIN bakımı** (150-anahtar × 5M) — pending list, index boyutu, autovacuum.
- **P8** Yansıma **A′ fan-out** (§5/§10-30) — parent değişimi çok child'a yayılırsa kitlesel reproject.
- **P9** **Partition sıcak-nokta** — HASH(service_id), dominant tenant.

**🔧 Ek geliştirme (çekirdek 3 tablo dışında):**
- **D1** `Property.projectionLevel` (S5) · **D2** `Property.code` immutable+auto-generate (S12) · **D3** **Status ayrı indeksli kolon**
  (S3/S4/S10) — *zorunlu.*
- **D4** **Reflection mekanizması** (A/B/A′ + A′ için `reflection_link`+propagation consumer) — *zorunlu, araştırmada YOK* (S3/S4).
- **D5** **Audit/changelog tablosu** (§7-20) · **D6** **Incremental rollup** (§8.5, P2 için) · **D7** **Translation-aware sorgu
  katmanı** (§6c/§8.4, P3 için) — *zorunlu.*
- **D8** **MinIO** (§7-22) · **D9** **Outbox+kuyruk+projektör** omurgası + NATS stack kararı (S2) · **D10** **Bulk rebuild job +
  "projection ready" sinyali** (S5) · **D12** Reflection **snapshot yazımı** (S4) — *zorunlu.*
- **D11** Geniş dashboard için **denormalize rapor projeksiyonu** (P1) · **D13** **PostGIS** (Map/geo, §11) · **D14** alt-servis
  **tik/seçim durumu** tablosu (§10-32) — *koşullu.*

**En kritik üçlü:** **rollup (D6) + translation katmanı (D7) + status kolonu (D3)** — bunlar olmadan ağır raporlar hedefi tutmaz.

**Uygunluğa etkisi:** **⚖️** `form_attr` senaryoların çoğunu 5M'de sorunsuz karşılar (👍) ama **tam raporlama yüzeyi için tek başına
yetmez**: rollup + translation-katmanı + status-kolonu + reflection-mekanizması onun **yanına zorunlu** eklenmeli. Bu, S1-S12'nin
tekil bulgularını ölçekte doğruluyor: form_attr = **skaler filtre/sıralama/detay-dışı sorgu için güçlü çekirdek**, çevresi tamamlanacak.

---

## Toplu Değerlendirme (SONUÇ — 🟡 sorular bitince doldurulacak)

- **Lehine (👍):** [S1] Detay-açılış `form_attr`'a bağımlı değil → projection lag detay görünümünü etkilemez; form_attr'ın
  bayat/eksik olması bir formu açmayı bozamaz (JSONB anında tutarlı). · [S2] Güncel tutma **otomatik + merkezi** (tek generic
  projektör, alan adı koda gömülü değil); idempotent + rebuild edilebilir → dayanıklı. · [S3] `form_value.data`'ya **yazılmış**
  her değer (kullanıcı-girdisi / snapshot / propagate) `form_attr`'a **tek tip** yansır — yansıma özel-durum kodu gerektirmez.
  · [S5] **Şema evrimi zarif:** yeni sorgu ihtiyacı = **metadata flip + arka plan rebuild** (DDL/migration/downtime yok); geçmiş
  veri JSONB'de durduğundan backfill mümkün, karar geri alınabilir, sabit index → yeni alan yeni index istemez, eşittir sorgusu
  GIN ile rebuild bile istemez. · [S8] **`translationCode` ek kolonu** (veya değeri stabil semantik kod tutmak) düşük riskli:
  dil-doğru join'i tek hopa indirir, **rename ile bayatlamaz** → S6/S7 ergonomisini ucuzlatır. · [S9] **150+ property /
  büyük JSONB** `form_attr`'ı ve **detay-okumayı etkilemez** (yalnız sorgulanabilir alt-küme yansır; tek-satır okuma); JSONB'de
  **sert kolon limiti yok** → 150 alan kolon-başına-alana karşı JSONB'nin kazandığı yer. · [S11] `form_attr` **`property_code`**
  tutar (id değil) → kaynak JSONB code-keyed olduğundan kaynakla **tutarlı** + API/custom-code'la aynı dil + **join'siz/FK'sız**
  self-describing; bedeli yalnız sınırlı depolama fazlası (benchmark). Tasarım çıkarımı: `form_value.data` code-keyed, `Property.code` benzersiz+stabil.
  · [S12] **Code'u dondurmak** rename problem sınıfını **sıfır maliyetle** kaldırır (kullanıcı zaten *label*'ı=translation değiştirir,
  o serbest+depolamasız) → S11 code-keying tamamen güvenli; `Property.code` immutable (veri-öncesi draft + auto-generate).
- **Aleyhine / riskli (👎):** [S2] **Eventual consistency** — value değişince form_attr birkaç yüz ms bayat (rapor/liste). ·
  **Write amplification** ≈15-40 fiziksel iş / value değişimi. · Güncel tutma **outbox relay + kuyruk + projektör** altyapısına
  bağımlı (işletilecek hareketli parçalar). · [S3] `form_attr` **canlı referans-only (B) yansımaları** ve **FlowInfo/statü**
  durumunu **kapsamaz** → bunlar için yanında ayrı çözüm (join / ayrı status kolonu-projeksiyonu) gerekir. · [S3] ParentProperty
  A′ (materialized+propagation) seçilirse **fan-out** write-amplification'ı katlar. · [S6] `form_attr` **tek başına** combobox'ı
  **isme göre sıralayamaz** (kodu tutar, isim değil + isim dile bağlı) → **translation join şart**; kodlu alanların isim-sıralı/gruplu
  raporlarında form_attr gerekli-ama-yetersiz. Ağır isim-sıralı raporda dil-başına (kod→isim) tablo/benchmark gerekebilir.
  · [S7] `form_list_item` **sayısal/skaler** alt-alan sıralama-filtresini (vergiOranı, tutar) **index destekli** (`ix_li_num`) +
  cross-form karşılar (👍); ama EAV şekli kalemi tek satıra toplamak için **pivot** ister (⚖️ benchmark) ve **kodlu** alt-alan
  isim-sıralamasında yine translation join gerekir (👎, S6 mirası). · [S8] **`display` ek kolonu** join maliyetini **bayatlama +
  çeviri-değişti-rebuild fan-out**'uyla takas eder (kaynağı `form_value` akışı dışında → sessiz bayatlama); dile özgü (çoklu dil =
  satır patlaması). Yalnız benchmark kanıtlarsa **defaultLang-cache** olarak eklenebilir.
- **Koşullu / karara bağlı (⚖️):** [S9] Büyük JSONB'nin **yazma** maliyeti (`satır boyutu × update sıklığı` → WAL/bloat/vacuum/GIN)
  benchmark'ta ölçülmeli; **büyük içerik + sık güncelleme** birleşimi tek gerçek risk → çözüm MinIO + tuning + partition, alan azaltmak değil.
  · [S10] **JSONB yerleşimi (tek tablo ↔ 1-1 ayrı tablo)** benchmark-güdümlü optimizasyon (doğruluk değil): default **tek tablo**
  (TOAST zaten büyük veriyi satır-dışına alır + basit); status-churn bloat'ı ölçülürse **1-1 split**'e geç. **Zorunlu kural (A/B'den
  bağımsız):** `status` gibi sık-değişen alanlar **ayrı kolon**, asla JSONB içinde değil. `form_attr`'ı etkilemez.
  · [S13] **5M/200M ölçekte tam senaryo taraması:** form_attr çoğunluğu sorunsuz karşılar ama **tam raporlama yüzeyi için tek
  başına yetmez** → **9 performans riski** (P1 geniş-rapor pivot · P2 cross-form aggregation · P3 kodlu-alan isim-sıra · P4 line-item
  pivot · P5 projection lag · P6 rebuild süresi · P7 GIN bakımı · P8 A′ fan-out · P9 partition sıcak-nokta) + **~14 ek geliştirme**
  (zorunlu: projectionLevel · code-immutable · **status kolonu** · **reflection mekanizması** · audit tablosu · **rollup** ·
  **translation katmanı** · MinIO · outbox omurgası · rebuild+ready-sinyali · snapshot-yazımı). **En kritik üçlü: rollup + translation-katmanı + status-kolonu.**
- **Koşullu / karara bağlı (⚖️):** [S1] `form_attr` hiçbir zaman detay-okuma yolunda değil → tüm varlık gerekçesi çok-kayıt
  sorgu/rapor performansına dayanır; raporlama ihtiyacı hafifse maliyeti sorgulanmalı. · [S2] Senkron altyapısı (NATS/relay)
  proje stack'ine henüz commit edilmedi — "güncel tutma" bu karara bağlı. · [S3] **§5 ürün/hukuk kararı:** her yansıma tipi için
  A/B/A′ (snapshot ↔ referans ↔ materialized+propagation) seçimi `form_attr`'ın o alanı kapsayıp kapsamayacağını belirler.
  Araştırma parent→child **propagation'ı (reflection_link + consumer) çözmüyor** — boşluk, proje tasarlamalı.
- **[S4] Karar kuralı netleşti (2×2 — değişkenlik × rapor ihtiyacı):** "**değişmez → A-snapshot** (mümkünse native kolon:
  createDate=created_at, instanceId=form_id, creatorUserId=kolon) · **değişken+gösterim → B** (status = motor-güncellemeli
  indeksli status kolonu, join cezasız) · **değişken+ağır rapor → A′**." → `form_attr` yalnız **materialized** hücreleri taşır;
  B hücreleri **native kolon / join** ile çözülür. **Tek pahalı boşluk:** değişken+ağır-rapor **parent** alanı (§8.5) → A′.
  ParentProperty **topluca B değil**, semantiğe göre (audit→A-snapshot / güncel→B / güncel+ağır rapor→A′).
- **[S5] Sorgulanabilirlik geri-alınabilir bir metadata kararı:** alan `NONE→SEARCH/SORT/AGGREGATE` + bulk rebuild → geçmiş+yeni
  veri `form_attr`'da. Bedel: rebuild süresi/I-O + o alanın kalıcı write-amplification artışı (yalnız gerçekten sorgulananı işaretle)
  + rebuild sırasında "hazır" sinyali gerekir. **Tasarım çıkarımı:** `Property` modeline **`projectionLevel`** alanı eklenmeli.

**Nihai karar:** _(henüz verilmedi)_
