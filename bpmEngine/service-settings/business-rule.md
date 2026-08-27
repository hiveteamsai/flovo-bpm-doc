# Flovo — İş Kuralları (Business Rules) Tasarımı

> **Durum:** 🟢 Model + **davranış spesifikasyonu** tanımlı (v0.35); ince mekanik motor implementasyonuyla netleşir.
> **Amaç:** Form üzerinde **gerçek zamanlı (realtime) frontend davranışlarını** koşul-aksiyon tabanlı tanımlamak
> (alan göster/gizle, validasyon, değer atama, veri kaynağı doldurma, stil).
>
> **İlişki:** Alanlar → `properties.md` · Görüntüleme profilleri → `view-profile.md` · Stil → `../organization-settings/style.md` ·
> Süreç adımları/aksiyonlar → `process-step.md` / `process-step-action.md` · Model ailesi → [`../models/service-settings/dto/business-rule/index.md`](../models/service-settings/dto/business-rule/index.md).

---

## 0. Önemli — İş Kuralı ≠ BPM Motoru (katman ayrımı)
İş kuralları **frontend'de gerçek zamanlı çalışan işlerdir**; bu yüzden **BPM motorunu (flow/orkestrasyon) doğrudan
etkilemez.** İki **ayrı katman** vardır:

| Katman | Nerede çalışır | Ne yapar | Doküman |
|---|---|---|---|
| **Form-mantığı** = **İş Kuralları** | **Frontend, realtime** (form açıkken) | Açık formda anlık UX: alan göster/gizle, anlık validasyon, anlık değer/stil | **bu dosya** |
| **Akış-mantığı** = **BPM Motoru** | **Backend / motor** (adım geçişleri) | Süreç adımları arası ilerleme, aksiyon kodu yönlendirmesi, durum değişimi | `../flovo-bpm-engine.md` |

> **Çalışma yeri (KARAR):** İş kuralları **tam frontend** çalışır — kurallar **servise gömülü** gelir (ayrı istek yok), her client
> kendi motorunu yürütür. Form açılır açılmaz kurallar ek tur beklemeden çalışabilir. İş kuralı, kullanıcı form üzerinde
> gezinirken tetiklenir ve **o anki formu** düzenler; motorun adım-geçiş kararına karışmaz.

---

## 1. İş Kuralı Nedir?
Bir **iş kuralı (business rule)**, form üzerinde **koşul → aksiyon** tabanlı dinamik bir davranıştır. Belirli koşullar
sağlandığında **frontend'de anlık** olarak tetiklenir ve formu değiştirir: validasyon, değer atama, alan görünürlüğü,
veri kaynağı doldurma, stil vb.

---

## 2. Veri Modeli (`BusinessRuleDto`)
| Alan | Tip | Açıklama |
|---|---|---|
| `id` | int | Kural ID'si |
| `organizationId` | int | Organizasyon ID'si (FK → `../organization-settings/organization.md` `id`) |
| `serviceId` | int | Servis ID'si |
| `code` | string | Kural kodu |
| `definition` | string | Kural adı/tanımı |
| `icon` | string | İkon |
| `environmentRestriction` | string | Ortam kısıtlaması |
| `businessRuleActionType` | BusinessRuleActionType | Kural aksiyon tipi (§3) |
| `configuration` | jsonb | **Aksiyon konfigürasyonu** — `businessRuleActionType`'a göre şekillenen **yapısal JSONB** (alt-şemalar → [`../models/service-settings/dto/business-rule/index.md`](../models/service-settings/dto/business-rule/index.md)) |
| `businessRuleRuntimeType` | BusinessRuleRuntimeType | Çalışma zamanı: `always` / `firstOpening` / `whenChanging` |
| `businessRuleConditionType` | BusinessRuleConditionType | Koşul birleştirme (`and`/`or`) |
| `businessRuleConditions` | jsonb | Koşul ağacı — **gömülü JSONB** (recursive; ayrı tablo değil) (§4) |
| `activeViewProfiles` | List\<int\> | Sadece bu görüntüleme profillerinde çalış (→ `view-profile.md`) |
| `shouldNotWorkInReadonlyMode` | bool | Salt-okunur modda çalışmasın |
| `priority` | int | Kural **çalışma sırası/önceliği** (küçük = önce; aynı alana yazan kurallarda belirleyici) |

---

## 3. Aksiyon Tipleri (`businessRuleActionType`)
İş kuralı tetiklendiğinde **frontend'de** ne yapacağını belirler.

| Aksiyon | Ne yapar |
|---|---|
| `setViewForProperties` | Hedef property'lerin `visible` / `enabled` / `required` durumunu ayarlar |
| `applyValidation` | Koşullu validasyon; sağlanmazsa hata mesajı |
| `showMessage` | Kullanıcıya bilgi mesajı (başlık + içerik; dinamik değer) |
| `assignValueToProperty` | Bir property'nin **değerine** değer atar (§3.1) |
| `fillDataSource` | Combobox / Radiobutton / Form List gibi seçim alanlarının veri kaynağını **çalışma-zamanında** doldurur. **Kaynak tipleri:** organizasyon verileri · kullanıcı bilgileri · başka bir servisin instance'ları · dış/API kaynağı |
| `assignValueToPropertyAttribute` | Property'nin **değerine değil, bir niteliğine** (attribute) değer atar |
| `setStyle` | Property/form'un **tekil görünüm niteliklerini** (örn. `fontSize`, `titleColor`) değiştirir. **`../organization-settings/style.md` Style varlığını seçmez** — daha spesifik, tekil nitelik değişimidir |

### 3.1 — `assignValueToProperty` değer kaynakları (`ValueAssignType`)
`fixedValue` (sabit) · `propertyValue` (başka bir property'nin değeri) · `fromCalculation` (**JSONLogic** ifade — §5) ·
`fromDataSet` (veri setinden) · `search` (arama) · `httpRequest` (HTTP Request çağrısı ile → `process-step.md` §3.2).

> **Aksiyon konfig şemaları:** Her aksiyon tipinin `configuration` (JSONB) şekli **parçalanmış** olarak
> [`../models/service-settings/dto/business-rule/`](../models/service-settings/dto/business-rule/index.md) altındadır — ör. `setViewForProperties` → `actions/set-view-for-properties.md`,
> `assignValueToProperty` → `actions/assign-value-to-property.md`. Ortak değer modeli: **`AssignValue`** (`shared/assign-value.md`).

---

## 4. Koşul Yapısı (`BusinessRuleConditionDto`)
Her koşul iki değerin bir **operatörle** karşılaştırılmasıdır; koşullar **iç içe** (recursive) gruplanabilir (`and`/`or`).

| Alan | Açıklama |
|---|---|
| `referenceValue` | Referans değer (sol taraf) — `BusinessRuleConditionCompareValue` (→ `shared/business-rule-condition-compare-value.md`) |
| `valueToCompare` | Karşılaştırılacak değer (sağ taraf) — aynı tip |
| `criterionType` | Operatör (§7.3 → `../models/enums/criterion-type.md`) |
| `isConditionList` | İç içe koşul grubu mu |
| `businessRuleConditionType` | Alt grup birleştirme (`and`/`or`) |
| `businessRuleConditions` | İç içe koşullar (recursive) |

**Karşılaştırma değeri kaynağı (`compareType`):** `propertyValue` (form alanı) · `viewProfile` (aktif görüntüleme
profili kodu) · `fixedValue` (sabit) · `fromCalculation` (expression). Her taraf, ayrımlayıcı + payload yapısındadır (§7.2).

---

## 5. Çalışma Prensibi (genel akış)
> **Fonksiyon-düzeyi işleyiş** (çağrı grafiği + her fonksiyonun görevi/tetiklenmesi/ürettiği/çağırdığı fonksiyonlar) →
> [`business-rule-engine.md`](./business-rule-engine.md). Aşağısı özet; motor spesifikasyonu o dosyadadır.

1. **Form açılır** veya **bir property değişir** (frontend olayı).
2. Servise gömülü **kural kümesi** taranır; her kural için **ön-filtreler** (§6.3) uygulanır, ardından **kural seçimi** (§6.1).
3. Seçilen kuralın **koşul ağacı** değerlendirilir (§7).
4. Koşul **TRUE/FALSE** sonucuna göre `businessRuleActionType`'ın **aksiyon davranışı** çalışır (§8).
5. Aksiyon bir alanın değerini/kaynağını **gerçekten değiştirirse**, o alan için **yeni bir tur** tetiklenir (zincirleme, §6.2).

> Tümü **istemci tarafında**, motoru beklemeden olur — anlık UX içindir. Kalıcı/akış kararları motorun işidir (§0).

---

## 6. Tetikleme & Zincirleme

### 6.1 Runtime tipi & kural seçimi (`businessRuleRuntimeType`)
Bir kuralın **ne zaman** değerlendirileceği runtime tipi + tetikleyen olayla belirlenir:

| Runtime tipi | Form açılışı | Bir alan değişince |
|---|---|---|
| `always` | ✔ çalışır | ✔ **eğer tetikleyen alan kuralın kapsamındaysa** (§6.2) |
| `firstOpening` | ✔ çalışır | ✖ asla |
| `whenChanging` | ✖ asla | ✔ eğer tetikleyen alan kuralın kapsamındaysa |

> `businessRuleRuntimeType` boş/bilinmeyen ise **`always`** kabul edilir (varsayılan).

### 6.2 Tetikleme kapsamı (KARAR — genişletildi)
Bir alan değiştiğinde, o alanı **kapsamında** kullanan kurallar seçilir. Kapsam = kuralın **koşullarında** geçen alanlar
**+ aksiyon/ifade alanlarında** (atanan değerin `propertyValue` kaynağı, `fromCalculation` ifadesindeki `#PROPKODU`
token'ları, veri seti/filtre alanları) geçen alanlar. Böylece **hesaplama kurallarında** ifade alanlarını yapay olarak
koşula ekleme zorunluluğu **yoktur** — ifadede kullanılan alan değişince kural kendiliğinden tetiklenir.

### 6.3 Ön-filtreler (kural çalışmadan önce, sırayla)
1. **`activeViewProfiles`** doluysa ve formun **aktif görüntüleme profili** listede yoksa → kural atlanır.
2. **`shouldNotWorkInReadonlyMode`** → **motor okur** (KARAR v0.35): salt-okunur form'da bu bayrak `true` ise kural **atlanır**.
3. **`environmentRestriction`** → ortam modeli ile birlikte netleşecek *(→ todo; ortam modeli)*.

### 6.4 Zincirleme (cascade) & öncelik
- **Değer-atayan aksiyonlar** (`assignValueToProperty` · `fillDataSource` · `assignValueToPropertyAttribute`) bir alanı
  **gerçekten değiştirdiğinde**, o alan için yeni bir tur başlatır → onu kapsamında kullanan kurallar tekrar çalışır.
- **Değer-atamayan aksiyonlar** (`setViewForProperties` · `setStyle` · `showMessage` · `applyValidation`) zincir **tetiklemez**.
- **Sıra:** kurallar `priority` (küçük = önce) sırasıyla çalışır; aynı alana yazan kurallarda öncelik belirleyicidir
  (eşitlikte kararlı bir ikincil ölçüt — `id` — uygulanır). *(Eski motorun "son yazan kazanır" belirsizliği `priority` ile giderildi.)*
- **Döngü koruması:** zincir, atama metodları **değeri gerçekten değiştirmediğinde** (yakınsama) durur. Bunun ötesinde bir
  **tur/derinlik limiti** + karşılıklı besleyen kural tespiti **açık** *(→ todo; hata yönetimi / döngü koruması)*.

---

## 7. Koşul Değerlendirme

### 7.1 Ağaç değerlendirme (recursive AND/OR)
- Grup (`isConditionList == true`) → alt `businessRuleConditions`, grubun `businessRuleConditionType`'ıyla:
  `and` → **hepsi** sağlanmalı; `or` → **en az biri**.
- Yaprak koşul → `referenceValue ⟨criterionType⟩ valueToCompare`.
- **Boş/null koşul listesi → TRUE** (koşulsuz kural, seçildiği her turda "sağlandı" sayılır).
- Ağaç **sınırsız derinlikte** iç içe olabilir → `(A ve B) veya (C ve D)` gibi mantıklar.

### 7.2 Karşılaştırma değeri çözümleme (`compareType`)
Her taraf (`referenceValue`/`valueToCompare`) ayrımlayıcı + payload yapısındadır:

| `compareType` | Çözülen değer |
|---|---|
| `propertyValue` | Alanın değeri (`propertyId`); liste-tipli kontrolde `valueTypeOfList` ile hangi değer okunacağı seçilir |
| `viewProfile` | Aktif görüntüleme profilinin **kodu** |
| `fixedValue` | Sabit değer |
| `fromCalculation` | İfade (expression) sonucu |

### 7.3 Operatör semantiği (`criterionType`)
Karşılaştırma, **alanın tipine** (metin / sayı / tarih) göre yürütülür. Operatörün davranışı tipe bağlıdır:

| Operatör | Metin | Sayı | Tarih |
|---|---|---|---|
| `equals` / `notEquals` | `==` / `!=` | sayısal eşitlik | aynı tarih mi |
| `isEmpty` / `isNotEmpty` | boş mu | değer yok mu | boş-tarih mi |
| `greaterThan` / `…OrEqual` / `lessThan` / `…OrEqual` | — | sayısal karşılaştırma | tarih karşılaştırma |
| `startsWith` / `endsWith` / `contains` / `notContains` | metin arama | — | — |

> **Tip-semantiği (KARAR v0.35):** karşılaştırma tipi **alanın `propertyType`'ından** belirlenir (`propertyValue` tarafı:
> `numericTextbox`→sayı, `datepicker`→tarih, aksi→metin) — deterministik. İki taraf da `fixedValue` ise operatöre göre. Sayı
> **kanonik** format, boş-tarih **gerçek null**, çoklu-değer → **`containsAny`/`containsAll`**. Tip belirsizse **güvenli-false**.

---

## 8. Aksiyon Davranışları
Koşul sonucuna göre her aksiyonun davranışı:

| Aksiyon | Koşul **TRUE** | Koşul **FALSE** | Zincir tetikler? |
|---|---|---|---|
| `setViewForProperties` | Her alana **providedAppearance** (visible/enabled/required) | **notProvidedAppearance** — ancak `notProvidedDeactive` ise alana **dokunulmaz** | Hayır |
| `applyValidation` | Validasyon girdisini ekler/günceller | Aynı kurala ait girdiyi **kaldırır** (koşul düzelince uyarı otomatik kalkar) | Hayır |
| `showMessage` | Dialog gösterir (başlık boşsa "Bilgilendirme") | Hiçbir şey | Hayır |
| `assignValueToProperty` | Değeri atar | `clearIfConditionNotTrue` ise alanı **temizler** | **Evet** |
| `fillDataSource` | Kaynağı doldurur | Hiçbir şey | **Evet** |
| `assignValueToPropertyAttribute` | Özniteliği (`minDate`/`helperText`…) atar | Hiçbir şey | **Evet** |
| `setStyle` | Stili uygular | `clearIfConditionNotTrue` ise stili **temizler** | Hayır |

**Özel davranışlar:**
- **Salt-okunur mod:** `setViewForProperties`'te `enabled` her durumda **`false`**'a zorlanır (görünürlük/zorunluluk kuraldan gelir; düzenlenebilirlik açılmaz).
- **`clearIfConditionNotTrue`** yalnız `assignValueToProperty` ve `setStyle` için anlamlıdır (diğerlerinde alan yoktur).
- **Satır-bazlı (`withFormList`):** `applyValidation` ve `setStyle`, bir **Form List** alanının **her satırında** ayrıca bir
  `formListRowCondition` değerlendirebilir; nihai sonuç ana koşul **ve** satır koşuludur.
- **`showMessage` durum tutmaz:** koşul her sağlandığında dialog yeniden açılabilir; "bir kez göster" mekanizması **açık** (→ todo).

---

## 9. Değer Çözümleme (`AssignValue` — §3.1)
Değer üreten her nokta (aksiyon değeri, validasyon/mesaj metni, koşul `fromCalculation`, filtre değeri) ortak `AssignValue`
modelini kullanır. `valueAssignType`'a göre:

| Kaynak | Çözümleme | Asenkron |
|---|---|---|
| `fixedValue` | Sabit değer (+ `translationCode` → Translation ile çok-dilli sabit metin) | Hayır |
| `propertyValue` | Başka alanın değeri (`useDisplay` ile görünen metin) | Hayır |
| `fromCalculation` | İfade sonucu; **çok-dilli**: `expression` (default) + `localizedExpressions` (dile-özel, eksik dilde default) | Olabilir |
| `fromDataSet` | Başka servisin instance'larından (lazy → sunucu sorgusu) | Lazy'de evet |
| `httpRequest` | Dış HTTP çağrısının yanıtı | Evet |
| `search` | Arama sonucu seçilen değer *(davranış açık → todo)* | — |

**Asenkron kaynaklar** (lazy dataset · httpRequest · async ifade) için: ilgili alan **meşgul** işaretlenir, form aksiyonları
istek bitene kadar bekletilir, yanıt gelince değer atanır ve (değiştiyse) zincir tetiklenir.

---

## 10. Eşzamanlılık & Hata
- **Meşgul göstergesi:** en az bir asenkron kural çözümlenirken forma "iş kuralları çalışıyor" durumu yansır; bu sırada
  form aksiyon butonları (kaydet/ilerlet) **bekletilir** (yarım hesaplanmış değerle gönderim önlenir).
- **Hata görünürlüğü (KARAR — açık):** kural/koşul/aksiyon hataları **kullanıcıya/­tasarımcıya nasıl yansıyacak** (sessiz
  yutma yerine görünür hata/log) ve organizasyon/ağ verisi yüklenemediğinde davranış (tekil kural mı atlanır, yoksa küme mi
  durur) → todo (hata yönetimi).

---

## 11. Açık Kararlar / Sorular
> **Açık sorular tek yerde:** Bu dokümanın açık kararları/soruları, tutarsızlığı önlemek için **yalnız** merkezi
> [`todo.md`](../todo.md) dosyasında toplanır. İlgili maddeler orada `(business-rule §..)` atfıyla ("İş kuralı — açık detaylar")
> bulunur; verilen kararlar bu dokümanın **gövdesinde** anlatılır.

> **Çözülenler (yerel karar log'u):**
- [x] **Çalışma yeri = tam frontend** (kurallar servise gömülü; her client kendi motorunu yürütür) — §0.
- [x] **Aksiyon konfigi = yapısal JSONB** (`configuration`, tip-başına şema) — §2 · model ailesi.
- [x] **Tetikleme kapsamı genişletildi** (koşul + aksiyon/ifade alanları) — §6.2.
- [x] **`priority` ile kural sırası** (aynı alana yazan kurallarda belirleyici) — §6.4.
- [x] **`setStyle`** `style.md` Style varlığını **seçmez**; yalnız tekil görünüm niteliklerini değiştirir — §3.
- [x] İş kuralları **servis-bazlı** tanımlanır (`serviceId`).

---

*Oluşturma: 2026-06-30 · Güncelleme: 2026-08-27 (davranış spesifikasyonu — tetikleme/koşul/aksiyon/değer/eşzamanlılık).*
