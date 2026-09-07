# Yansıma Yayılımı — `parentProperty` A′ (materialized) runtime mekanizması

> **Durum:** 🟢 TANIMLI (v0.27 — instance-seviyesi `ReflectionLink` tablosu **kaldırıldı**; yayılım `AssociatedInstance` + `Property` metadata ile çözülür · v0.28 — §9 ata-referansı kararı + §3 ters-arama yön nüansı · **v0.45 — §3a ilk dolum/temizleme:** kopya **ilişki kurulunca** alınır, bağ kalkınca **`null`**).
> **Bu bir veri modeli DEĞİLDİR** — `parentProperty` alanlarının **ilk dolum/temizleme** kuralını (§3a — `snapshot` + `materialized`) ve `reflectionMode=materialized` (A′) alanların üst kaynak değişince child kopyalarının **nasıl tazelendiğini** (§4–§5) anlatan **çalışma-zamanı mekanizmasıdır**.
> **İlgili:** [`../enums/reflection-mode.md`](../enums/reflection-mode.md) (snapshot/live/materialized — **ne**) · [`../enums/reflection-propagation.md`](../enums/reflection-propagation.md) (async/sync — **ne zaman**) · [`propertyValuesTemplates/parent-property.md`](./propertyValuesTemplates/parent-property.md) (değer şekli) · [`associated-instance.md`](./associated-instance.md) (ilişki) · [`instance-value-outbox.md`](./instance-value-outbox.md) (olay) · [`instance-value.md`](./instance-value.md) (kaynak).

## 1. Neden ayrı bir "link" tablosu yok
A′ yansıma tek soruyu çözer: **"Üst alan değişince hangi child kopyalar tazelenecek?"** Bunun için gereken iki bilgi **zaten sistemde vardır**:

1. **Tanım eşlemesi** (hangi child alan hangi üst alanı yansıtır): `Property`'de — child'ın `parentProperty` alanı `parentPropertyId`/`refPropertyId` ile üst alanı zaten işaret eder (**design-time**, instance-bağımsız).
2. **Instance ilişkisi** (hangi child instance hangi parent'a bağlı): [`AssociatedInstance`](./associated-instance.md)'te — Form List üyeliği zaten burada tutulur.

Bu yüzden **instance-seviyesi `ReflectionLink` tablosu kaldırıldı:** `(parentInstance → childInstance)` kenarları `AssociatedInstance`'ı **kopyalıyordu** (redundant + senkron tutma/staleness külfeti). İlişkinin **tek doğ. kaynağı `AssociatedInstance`**'tır; child eklenince/çıkınca ayrı bir edge bakımı gerekmez.

## 2. Konfigürasyon (`Property`)
| Ayar | Nerede | Rol |
|---|---|---|
| `reflectionMode` | child `parentProperty` | `materialized` (A′) → yayılım açık (`snapshot`/`live`'da yayılım yok). |
| `reflectionPropagation` | child `parentProperty` | `async` (vars.) / `sync` — kopya **ne zaman** tazelensin → [`../enums/reflection-propagation.md`](../enums/reflection-propagation.md). |
| `parentPropertyId` / `refPropertyId` | child `parentProperty` | `parentPropertyId` = **bağlayan alan** (Form List **veya** tek-seçimli ilişkili Combobox) → üst servis buradan türetilir · `refPropertyId` = üst servisteki **yansıtılan alan** (eşleme — **mevcut alan**, yeni tablo gerekmez; KARAR v0.45). |
| `isReflectionSource` | **üst (kaynak) alan** | "Bu alan değişince yansıma tetikler mi?" — servis yayınında hesaplanan **hızlı-çıkış** bayrağı (çoğu alan `false`). |

> Eşleme runtime'da **`code` ile** eşlenir (değer katmanı **code-keyed**): değişen üst alanın `code`'u ↔ child tanımının referans aldığı alanın `code`'u.

## 3. Child'ları bulma (`AssociatedInstance` ters araması)
Parent instance **P** güncellenince, P'yi üst kabul eden child'lar bulunur. **Ters aramanın yönü, bağlayan alanın tipine göre
değişir** — çünkü `AssociatedInstance`'ta "üst" tarafın hangi kolonda durduğu Form List ↔ Combobox'ta farklıdır
(bkz. [`associated-instance.md`](./associated-instance.md) alan semantiği):

| Bağlayan alan | Üst (P) hangi kolon | Sorgu | Child'lar |
|---|---|---|---|
| **Form List** (üst form listeyi **içerir**) | `associatedInstanceId` | `WHERE associatedInstanceId = P AND associatedPropertyId = <Form List>` | `instanceId` |
| **Combobox** (child, P'yi **seçer**) | `instanceId` | `WHERE instanceId = P AND associatedPropertyId = <Combobox>` | `associatedInstanceId` |

Eşleme (`parentPropertyId`/`refPropertyId`) **hangi bağlayan alanı** işaret ettiğinden alanın tipi bellidir → runtime **doğru kolonu**
seçer. Her iki yön de indekslidir (`associatedInstanceId` / `instanceId`) → **tarama yok**. (Bu ters arama, **Üst Form Kullanıcı**
adımının aramasının yön olarak tersidir — bkz. [`associated-instance.md`](./associated-instance.md).)

## 3a. İlk dolum ve temizleme — ilişki yazım yolu (KARAR v0.45)
`snapshot` ve `materialized` kopyaları **instance oluşturma anında değil, ilişki kurulduğu anda** alınır; bağ kalkınca **temizlenir**.
Gerekçe: child instance çoğu zaman bağdan **önce** var olur — Form List'ten yeni oluşturmada bile önce instance üretilir, sonra
`AssociatedInstance` kaydı atılır; "var olandan ekle" ve ilişkili Combobox seçiminde ise child günler önce oluşmuş olabilir. Oluşturma-anı
kopyası bu durumlarda **boş kalırdı**.

**Tetikleyici:** `AssociatedInstance` **insert** / **delete** — ilişkiyi kuran **her** yol (Form List'e ekleme/çıkarma, "var olandan ekle",
`isAssociatedCombobox` seçimi/değişimi/temizlenmesi). Tespit, ServiceTrigger ile **aynı çekirdek DB güncelleme katmanında** yapılır
(→ [`associated-instance.md`](./associated-instance.md) "Yazım-yolu tüketicisi"); ilişki kuran her yer ayrıca kod yazmaz.
**Kapsam:** yalnız `data`'da kopya taşıyan modlar (`snapshot` · `materialized`). `live` saklanan değer taşımadığından **işlem yok**.

| Adım | Insert (bağ kuruldu) | Delete (bağ kaldırıldı) |
|---|---|---|
| 1. Tanım | `parentPropertyId == associatedPropertyId` olan child `parentProperty` tanımları **D** (metadata cache) | aynı |
| 2. Taraflar | Bağlayan alanın tipine göre (§3 tablosu): **Form List** → child **C** = `instanceId`, üst **P** = `associatedInstanceId` · **Combobox** → C = `associatedInstanceId`, P = `instanceId` | aynı |
| 3. Yazım | bu bağlayan alandaki **ilk bağ** ise her D için `C.data[D.code] = P.data[refProperty.code]` (üst boşsa **`null`**); ikinci bağda **dokunma** | silinen bağ **birincil** ise: kalan en erken bağ varsa **ondan yeniden kopyala**, yoksa `null`; birincil değilse **dokunma** |
| 4. Yol | **Ortak yazma kapısı** (aynı TX: `InstanceValue.data` merge + outbox) → generic projector (`projectToAttr`) | aynı |

- **Seçim değişimi** (Combobox'ta başka üst seçildi) = delete + insert → önce temizle, sonra yeni üstten kopyala.
- **Fan-out yok:** insert/delete tek child ↔ tek üst çiftidir; `isReflectionSource` kontrolü bu yolda gerekmez.
- **Röle zinciri (§9):** C'ye yazılan kopya kendisi bir kaynaksa (`isReflectionSource=true`) yazım outbox'a düştüğü için §4 kaskadı
  **doğal olarak** devam eder (`hopCount` + O3 sınırları geçerli).
- **Sonuç:** `snapshot` = **ilişki-anı** fotoğrafı (sonra değişmez, bağ kalkınca `null`) · `materialized` = ilişki-anı kopya **+** sonraki üst
  değişimleri §4/§5 ile izler · `live` = hiçbir şey yazılmaz.
- **Birden fazla üst instance (KARAR v0.45):** aynı bağlayan alan üzerinden child'ın birden çok üst bağı varsa **birincil üst = en erken bağ**
  (en küçük `AssociatedInstance.id`) — §3.22 "ilk tespit edilen" ile **aynı deterministik kural**. Insert yalnız ilk bağda kopyalar; delete'te birincil
  düşerse kalan en erken bağdan yeniden kopyalanır (§4 yayılımı da yalnız birincil üstten gelir). Normalde oluşmaz — süreç tasarımı önler (örnek:
  `addFromExistingStatusIds=[Taslak]` + bağlanan masrafın ParentUser'a geçmesi ikinci eklemeyi keser).
- **Designer kısıtı (KARAR v0.45):** `parentPropertyId` yalnız **Form List** ya da **tek-seçimli** ilişkili Combobox (`isAssociatedCombobox=true`,
  `isMultiSelect=false`) olabilir; çok-seçimli Combobox **reddedilir** (hangi üstün yansıtılacağı belirsiz olurdu). `refPropertyId` bu bağlayan alandan
  türetilen **üst servise** ait olmalıdır (`SettingsValidator`).

## 4. Async akış (VARSAYILAN — `reflectionPropagation=async`)
```
1. Parent P · alan A güncellenir (v→v+1)
   └─ AYNI TX: InstanceValue.data yaz + Outbox{P, version, changedPropertyCodes:[A], hopCount:0}   ✅ atomik commit
2. reflection-propagation consumer olayı okur
   a. A.isReflectionSource? hayır → BİTTİ (bedava — çoğu alan)
   b. Metadata: A'yı materialized yansıtan child tanımları D (cache'li)
   c. AssociatedInstance ters araması → P'nin child instance'ları
   d. Her child C (P, C'nin o bağlayan alandaki BİRİNCİL üstü ise — §3a): idempotent  C.data[D.code] = yeni değer   (ordering: sourceVersion ≤ saklı ise atla)
      └─ C'nin KENDİ outbox'ı {C, hopCount+1}
3. Generic projector C'nin outbox'ından InstanceAttr/InstanceListItem'i yeniden yansıtır (mevcut yol)
4. C de bir kaynaksa (isReflectionSource) → 2 tekrar — hopCount limiti + döngü tespiti ile sınırlı
```
Parent commit anı ile child tazeleme arası: **eventual consistency** (A′'in kabul ettiği bedel).

## 5. Sync akış (opt-in — `reflectionPropagation=sync`)
```
1. Parent P · alan A güncellenirken AYNI TX içinde:
   - sync child tanımları için AssociatedInstance'tan instance'lar bulunur
   - onların InstanceValue.data + outbox'ı aynı TX'te yazılır  → anında tutarlı
   - async child tanımları yalnız outbox alır (§4 yolu)
```
**Zorunlu guardrail'ler** (yoksa sync bir performans/bug tuzağıdır):
- **Yalnız 1-hop sync** — daha derin kaskad yine async'e devreder (child'ın outbox'ı taşır); tek TX belirsiz derinlikte ağaç kilitleyemez.
- **Fan-out eşiği (KARAR v0.31: 20 child)** — sync yazılacak child sayısı **20'yi aşarsa** otomatik **async'e düş** (geniş Form List'te yazmayı kilitleme).
- Cross-partition/cross-service child yazımı aynı DB'de TX'e girer ama kilit maliyeti yüksek → eşik bunu da korur.

## 6. Doğruluk (correctness) garantileri
| Risk | Çözüm |
|---|---|
| Olay commit'ten önce çıkar | **Transactional outbox** (değer + olay aynı TX) — [`instance-value-outbox.md`](./instance-value-outbox.md). |
| Tekrar işleme (at-least-once) | **version idempotency** (`version ≤ last_projected_version → skip`). |
| Sıra dışı güncelleme eski değeri yazar | **per-instance ordering** (JetStream subject = instance) **veya** child kopyada `sourceVersion` kontrolü. |
| Döngü A→B→A | **hopCount + döngü tespiti** (motor **O3**). |
| Sonsuz kaskad | **derinlik limiti** (KARAR v0.31: **3 hop**; `hopCount > 3 → düş`, kaskad durur). |
| Bir child hata verir, hepsi durur | **child-bazlı retry + dead-letter** (fan-out izole). |
| Form List'ten çıkarılan child eski kopyayı taşır | Bağ silinirken kopya **`null`**'a çekilir (§3a); sonrasında `AssociatedInstance`'ta yok → yayılımda **bulunmaz**. |
| Sonradan bağlanan child'ın kopyası boş kalır | **İlk dolum ilişki kurulduğu anda** (§3a) — instance oluşturma anına bağlı değil. |

## 7. Performans
- **`isReflectionSource=false` → hızlı çıkış:** kaynak olmayan alan güncellemesi **hiç ek maliyet** üretmez (alanların çoğu böyle).
- **İndeksli çözümleme:** child bulma `AssociatedInstance(associatedInstanceId)` indeksiyle — **tarama yok**.
- **Delta:** yalnız `changedPropertyCodes`'taki alanların yansıması tazelenir (tüm `data` değil).
- **Batch + coalesce:** child update'leri toplu; hızlı ardışık üst güncellemeler en son değere indirgenebilir.
- **Async worker:** concurrency cap + `organizationId`/`serviceId` partition (mevcut altyapıyla hizalı).
- **Tek tip yansıma yolu:** child'ın Attr'ı **mevcut generic projector** ile yansır (özel yol yok).

## 8. Eventual consistency (kabul)
`async`'te üst commit olduğu an child kopya **kısa süre eski** olabilir; tazeleme arka planda tamamlanır. Değer okuması hep **somut** (hızlı), güncelliği **eventual**. Anında tutarlılık gerekiyorsa `sync` (guardrail'li) seçilir.

## 9. Referans kapsamı — doğrudan üst vs ata (KARAR, v0.28)
**Her `parentProperty` kenarı daima yalnız DOĞRUDAN üst formu referans alır** (`AssociatedInstance` **tek-hop**). **Ata (grandparent+)
referansı ayrı/non-adjacent bir mekanizma değildir** — `AssociatedInstance`'ta "ata instance" diye bir satır yoktur (iki kenar ortak
bir ara-formu paylaşır); ata ancak zincir yürünerek bulunur. Bu yüzden ata değeri iki mevcut yolla modellenir:

1. **Röle zinciri (materialized — sorgulanabilir/indekslenebilir ata değeri, önerilen varsayılan):** **ara form**, ata alanını **kendi
   `parentProperty`'si** olarak (gizli olabilir) yeniden yayınlar; yaprak, **ara formun bu alanını** yansıtır. Böylece her kenar tek-hop
   kalır ve değer **hop başına** aşağı iner. Yayılım **§4 kaskadının kendisidir**: ara alan `isReflectionSource=true` olduğundan üst
   değişince önce ara form (hop 1), sonra yaprak (hop 2) tazelenir; derinlik/döngü **`hopCount` + O3** ile sınırlı.

   ```
   Proje.budget değişti  →  reverse(Combobox): masraf formu.projeBudget (hop1)  →  reverse(FormList): masraf.projeBudget (hop2)
   ```
   **Bedel:** ara form o alanı (görünmese de) **taşımak zorundadır**; ve her hop **eventual-consistency** penceresi ekler (async).

2. **`live` okuma-anı zincir join (yalnız gösterim — depolama/yayılım yok):** yaprağın `parentProperty`'si `reflectionMode=live` ise
   ata değeri **okuma anında** `AssociatedInstance` zinciri yürünerek çözülür. Sıfır depolama + sıfır yayılım, ama **okuma pahalı**
   ve **indekslenemez/aggregate edilemez**. Ata alanı yalnız görüntüleniyor + sorgu/toplam gerekmiyorsa tercih edilir.

> **Reddedilen seçenek:** non-adjacent kenarlar için ayrı **edge-cache** tablosu — kaldırılan `ReflectionLink`'i geri getirir
> (redundant + staleness). Recursive reverse-join (path expression) ise fan-out patlaması + ordering/döngü karmaşası getirir; tek
> generic yolu bozar. İkisi de **kullanılmaz**. _(Sayısal eşikler — **ÇÖZÜLDÜ v0.31:** A′ derinlik/döngü limiti = **3 hop**
> (O3; `hopCount > 3 → düş`) · `sync` fan-out eşiği = **20 child** (üstü otomatik async'e düşer).)_

## 10. Faz kapsamı (KARAR v0.45)
| Katman | `snapshot` · `live` | `materialized` |
|---|---|---|
| **Tasarım-zamanı (pilot Bölüm-1)** | ayar saklanır + doğrulanır | ayar saklanır; **`SettingsValidator` F1.A.4 öncesi reddeder** (seçilemez) |
| **Motor Faz 1 çekirdek** (build-plan Grup A) | §3a ilk dolum/temizleme + `live` okuma-anı join | — |
| **F1.A.4** (outbox · projector · NATS) ile | — | §3a + §4/§5 yayılım açılır; Designer kısıtı kalkar |

`materialized` hedeflenen alan (örn. Masraf.`creditCardStatementId`) F1.A.4 öncesi **`live`** olarak tanımlanır, sonra `materialized`'a çevrilir
(mevcut instance'lar ilk üst değişiminde/yeniden bağlanmada dolar; toplu ilk dolum için tek seferlik backfill görevi F1.A.4 kapsamında).

*Oluşturma: 2026-08-04. Güncelleme: 2026-08-10 (ReflectionLink tablosu kaldırıldı → AssociatedInstance + Property metadata mekanizması) · 2026-08-17 (ata referansı = röle zinciri / `live`; ters arama yön nüansı) · 2026-09-07 (§3a ilk dolum/temizleme = ilişki yazım yolu · birincil üst kuralı · Designer kısıtı · FK semantiği · §10 faz kapsamı, KARAR v0.45).*
