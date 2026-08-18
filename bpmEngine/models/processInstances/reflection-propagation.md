# Yansıma Yayılımı — `parentProperty` A′ (materialized) runtime mekanizması

> **Durum:** 🟢 TANIMLI (v0.27 — instance-seviyesi `ReflectionLink` tablosu **kaldırıldı**; yayılım `AssociatedInstance` + `Property` metadata ile çözülür · v0.28 — §9 ata-referansı kararı + §3 ters-arama yön nüansı).
> **Bu bir veri modeli DEĞİLDİR** — `parentProperty` `reflectionMode=materialized` (A′) alanların, üst kaynak değişince child kopyalarının **nasıl tazelendiğini** anlatan **çalışma-zamanı mekanizmasıdır**.
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
| `parentPropertyId` / `refPropertyId` | child `parentProperty` | **hangi üst alan** yansıtılıyor (eşleme — **mevcut alan**, yeni tablo gerekmez). |
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

## 4. Async akış (VARSAYILAN — `reflectionPropagation=async`)
```
1. Parent P · alan A güncellenir (v→v+1)
   └─ AYNI TX: InstanceValue.data yaz + Outbox{P, version, changedPropertyCodes:[A], hopCount:0}   ✅ atomik commit
2. reflection-propagation consumer olayı okur
   a. A.isReflectionSource? hayır → BİTTİ (bedava — çoğu alan)
   b. Metadata: A'yı materialized yansıtan child tanımları D (cache'li)
   c. AssociatedInstance ters araması → P'nin child instance'ları
   d. Her child C: idempotent  C.data[D.code] = yeni değer   (ordering: sourceVersion ≤ saklı ise atla)
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
- **Fan-out eşiği** — child sayısı eşiği aşarsa otomatik **async'e düş** (geniş Form List'te yazmayı kilitleme).
- Cross-partition/cross-service child yazımı aynı DB'de TX'e girer ama kilit maliyeti yüksek → eşik bunu da korur.

## 6. Doğruluk (correctness) garantileri
| Risk | Çözüm |
|---|---|
| Olay commit'ten önce çıkar | **Transactional outbox** (değer + olay aynı TX) — [`instance-value-outbox.md`](./instance-value-outbox.md). |
| Tekrar işleme (at-least-once) | **version idempotency** (`version ≤ last_projected_version → skip`). |
| Sıra dışı güncelleme eski değeri yazar | **per-instance ordering** (JetStream subject = instance) **veya** child kopyada `sourceVersion` kontrolü. |
| Döngü A→B→A | **hopCount + döngü tespiti** (motor **O3**). |
| Sonsuz kaskad | **derinlik limiti** (`hopCount > limit → düş`). |
| Bir child hata verir, hepsi durur | **child-bazlı retry + dead-letter** (fan-out izole). |
| Form List'ten çıkarılan child tazelenir | **doğal** — `AssociatedInstance`'ta yok → **bulunmaz**, güncellenmez (ayrı temizlik gerekmez). |

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
> generic yolu bozar. İkisi de **kullanılmaz**. _(Kalan açık: yalnız **sayısal** eşikler — O3 derinlik/döngü limiti + `sync` fan-out
> eşiği → `../../todo.md`.)_

*Oluşturma: 2026-08-04. Güncelleme: 2026-08-10 (ReflectionLink tablosu kaldırıldı → AssociatedInstance + Property metadata mekanizması) · 2026-08-17 (ata referansı = röle zinciri / `live`; ters arama yön nüansı).*
