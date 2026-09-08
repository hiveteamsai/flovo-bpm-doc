# Flovo — İş Kuralı Motoru: İşleyiş & Fonksiyon Spesifikasyonu

> **Durum:** 🟢 İşleyiş spesifikasyonu (v0.35). **Amaç:** İş kuralı motorunun **çalışma prensibini fonksiyon düzeyinde**
> tanımlamak — hangi fonksiyonlar var, görevleri, ne zaman tetiklenir, ne üretir, birbirini nasıl çağırır (çağrı grafiği).
>
> **Üst doküman:** davranış özeti → [`business-rule.md`](./business-rule.md) · model ailesi → [`../models/service-settings/jsonTemplateModels/business-rule/index.md`](../models/service-settings/jsonTemplateModels/business-rule/index.md) · **backend uçları** → [`business-rule-endpoints.md`](./business-rule-endpoints.md).
> **Konum/dil:** Motor **tam frontend** çalışır (kurallar servise gömülü gelir, her client kendi motorunu yürütür). Aşağıdaki
> imzalar **dil-agnostik sözde-imzadır**; fonksiyon adları yeni-motor önerisidir.

---

## 0. Temel ilkeler
- **Durumsuz motor:** Motorun kendi kalıcı durumu yoktur; tüm çalışma durumu **form nesnesi (`Instance` + alan koleksiyonu)**
  üzerinde taşınır — `busyCount` (çalışan async kural sayacı), `validationList`, `dataError` (veri yükleme hata bayrağı),
  gömülü `rules`, `properties` (form alanları).
- **Alan mutasyonu 5 metotla olur** (form alanı = `Property` runtime örneği): `setValue` · `setDataSource` ·
  `setAppearance` · `setAttribute` · `clearValue`. **Her biri değeri _gerçekten_ değiştirdiyse `true` döner** — zincirleme
  (cascade) ve döngü-sonlanması bu **idempotency**'ye dayanır (§4).
- **İki giriş olayı:** (a) **form açılışı** (değişen alan yok → tam tarama), (b) **alan değişimi** (değişen alan → kapsam-filtreli tarama).

### 0.1 Runtime alan nesnesi (`Property` runtime — tasarım-zamanı metadata'dan ayrı)
Motorun üzerinde çalıştığı **çalışma-zamanı** alan nesnesi (`property.md` **tasarım-zamanı** metadata'sının runtime örneği):

| Alan | Açıklama |
|---|---|
| `propertyId` · `code` | Kimlik (`code` = form-içi benzersiz binding anahtarı). |
| `value` | O anki değer — **ortak değer modeli** (`propertyValuesTemplates`: skaler · `LabeledValue{value,display,translationCode}` · user-ref · list-of-model → [`../models/processInstances/propertyValuesTemplates/index.md`](../models/processInstances/propertyValuesTemplates/index.md)). |
| `dataSource` | Seçim öğeleri: `[DataSourceItem]` (§0.3). |
| `appearance` | `{ visible, enabled, required }` (bool). |
| `style` | Tekil görünüm nitelikleri map'i (fontSize/titleColor…). |
| `attributes` | Öznitelik map'i (`minDate`/`maxDate`/`helperText`/`sideText`/`addNewEnabled`). |
| `busy` | Async kural bu alanı çözerken `true`. |

### 0.2 "Gerçekten değişti mi?" (idempotency — cascade sonlanmasının temeli)
5 mutasyon metodu yeni değeri mevcutla **karşılaştırır**, yalnız **fark varsa** uygular + `true` döner (fark yoksa `false` → o dalda cascade başlamaz → zincir yakınsar):
- `setValue`: skaler → eşitlik; `LabeledValue` → **`value`** alanı; list → eleman-bazlı eşitlik.
- `setDataSource`: öğe listesi (value+display) eşitliği. · `setAppearance`/`setAttribute`: alan-bazlı. · `setStyle`: nitelik-bazlı. · `clearValue`: değer zaten boşsa `false`.

### 0.3 Yardımcı runtime modelleri
- **`DataSourceItem`** = `{ value, display, subText? }` — `fillDataSource` çıktısı (combobox/radiobutton/Form List öğesi).
- **`ValidationItem`** = `{ ruleId, rowId?, message, canPassValidation, showAsPopup }` — `applyValidation` çıktısı; `validationList`'te **`ruleId`(+`rowId`)** bazlı tutulur; `canPassValidation=false` girdisi varsa form gönderimi **bloklanır**.

---

## 1. Çağrı grafiği (üst → alt)

```
[DIŞ OLAY] form açılışı / yenileme ─→ prepareEngine (async ön-yükleme)
[DIŞ OLAY] alan değişimi (changeList) ─→ dispatchExecute ─┐
                                                          ▼
executeRules(changedProperty?)
├─ ruleAppliesTo                         (kapsam filtresi; changedProperty varsa)
│    └─ ruleAppliesTo (özyineli — koşul ağacı + aksiyon/ifade alanları)
├─ evaluateConditionGroup
│    └─ evaluateCondition
│         ├─ evaluateConditionGroup (özyineli — iç içe grup)
│         ├─ resolveCompareValue ─→ readPropertyValue · evaluateExpression
│         └─ compareValues
└─ dispatchAction   (businessRuleActionType → 7 aksiyon)
   ├─ applySetViewForProperties        → findTargetProperty
   ├─ applyValidation                  → evaluateExpression · evaluateConditionGroup · upsertValidation
   ├─ showMessage                      → evaluateExpression
   ├─ applyAssignValueToProperty       → findTargetProperty · resolveAssignValue*
   ├─ applyFillDataSource              → findTargetProperty · fetchServiceInstances · buildDataSourceItems ·
   │                                     matchesDataSetParameters · matchesOrganizationParameters · compareForSort · readPropertyValue
   ├─ applyAssignValueToPropertyAttribute → findTargetProperty · resolveAssignValue*
   └─ applySetStyle                    → evaluateConditionGroup

resolveAssignValue* (ortak değer çözümleme; kaynağa göre):
   ├─ (fixedValue/propertyValue) → resolveCompareValue · readPropertyValue
   ├─ (fromCalculation)          → evaluateExpression
   ├─ (fromDataSet)              → fetchServiceInstances · buildServiceInstanceQuery · matchesDataSetParameters · compareForSort
   └─ (httpRequest)              → callHttpRequest · resolveHttpParameter

fetchServiceInstances ─→ buildServiceInstanceQuery ─→ resolveCompareValue   (+ ağ: serviceInstances sorgusu)
matchesDataSetParameters / matchesOrganizationParameters ─→ resolveCompareValue · readPropertyValue · compareValues
evaluateExpression ─→ [yerleşik fonksiyon kataloğu, §7]
```

---

## 2. Giriş / Orkestrasyon

### `prepareEngine(context, instance) → void (async)`
- **Görev:** Kuralların ihtiyaç duyacağı **organizasyon/kullanıcı verilerini** (departman, masraf-merkezi, kredi kartı, çalışma-takvimi…) önceden, paralel yükler. İhtiyaç, kuralların `fillDataSource` kaynak tiplerinden **ve** ifadelerde geçen yerleşik fonksiyon adlarından çıkarılır.
- **Tetiklenme:** Form açılışı/yenileme; `executeRules`'tan **önce** (bir kez).
- **Üretir/etki:** `void`; `busyCount++/--` (yükleme boyunca form aksiyonları bekletilir); yükleme hatasında `dataError` işaretlenir.
- **Çağırır:** — (dış veri servisleri).
- 🟩 **KARAR (v0.35) — hibrit ön-yükleme:** kuralların ihtiyaç duyduğu **organizasyon/kullanıcı verisi** (fillDataSource kaynakları + ifade fonksiyon bağımlılıkları) form açılışında **paralel ön-yüklenir → cache** (yerleşik fonksiyonlar cache'ten **sync** okur); büyük/nadir **`serviceInstances`** çalışma-anı **lazy** çekilir. İhtiyaç, kuralların kaynak tiplerinden + ifade fonksiyon adlarından çıkarılır.

### `executeRules(context, instance, changedProperty?) → bool hasChange`
- **Görev:** Kural kümesini **`priority` sırasıyla** dolaşır; her kural için **ön-filtre** (§3) + **kapsam** (`ruleAppliesTo`) uygular, koşulu değerlendirir (`evaluateConditionGroup`), sonucu `dispatchAction`'a verir.
- **Tetiklenme:** (a) form açılışı → `changedProperty = null` (tam tarama), (b) alan değişimi → `changedProperty` dolu (kapsam-filtreli), (c) **cascade** (bir aksiyonun mutasyonu → yeni `executeRules`).
- **Üretir/etki:** en az bir kural formu değiştirdiyse `true`; `busyCount++/--`.
- **Çağırır:** `ruleAppliesTo`, `evaluateConditionGroup`, `dispatchAction`.
- 🟩 **KARAR (v0.35):** kurallar **`priority`** ile sıralı (eşitlikte `id`); "son yazan kazanır" belirsizliği giderildi.
- 🟦 **AÇIK:** hata görünürlüğü (kural/koşul/aksiyon hatası kullanıcıya/tasarımcıya yansısın mı) + veri-yükleme hatasında **tek kural mı atlanır, küme mi durur** → todo (hata yönetimi).

### `dispatchAction(context, instance, rule, conditionResult, ...) → bool`
- **Görev:** `rule.businessRuleActionType`'a göre 7 aksiyon işleyicisinden birini çağırır (dağıtıcı).
- **Tetiklenme:** Yalnız `executeRules`.
- **Üretir/etki:** çağrılan işleyicinin `bool`'u (eşleşme yoksa `false`).
- **Çağırır:** `applySetViewForProperties` · `applyValidation` · `showMessage` · `applyAssignValueToProperty` · `applyFillDataSource` · `applyAssignValueToPropertyAttribute` · `applySetStyle`.

---

## 3. Ön-filtreler & tetikleme kapsamı

### `ruleAppliesTo(rule, changedProperty) → bool`
- **Görev:** Değişen alan bu kuralı **ilgilendiriyor mu** — kuralın **koşul ağacında** (özyineli) **veya aksiyon/ifade alanlarında** (`propertyValue` kaynağı, `fromCalculation` `#token`'ları, veri seti/filtre alanları) geçiyor mu? Eşleşme **`propertyId`** ile (alan referansı FK); form-içi taşımada ayrıca **`code`** anahtarı kullanılabilir (aynı alanın iki kimliği — §0.1).
- **Tetiklenme:** `executeRules` (yalnız `changedProperty != null` turunda).
- **Üretir/etki:** `bool`; yan etki yok.
- **Çağırır:** kendisi (özyineli — iç içe koşul grupları).
- 🟩 **KARAR (v0.35):** kapsam **koşul + aksiyon/ifade alanlarını** kapsar → hesaplama kurallarında ifade alanlarını yapay olarak koşula ekleme zorunluluğu **kalktı**.

**Ön-filtre sırası** (`executeRules` içinde, kural çalışmadan önce):
1. `activeViewProfiles` doluysa ve aktif görüntüleme profili listede yoksa → **atla**.
2. `shouldNotWorkInReadonlyMode` → **motor okur** (KARAR v0.35): salt-okunur form'da (tamamlanmış / başkasının kaydı vb.) bu bayrak `true` ise kural **atlanır**.
3. `environmentRestriction` → geçerli değerler/eşleştirme **ortam (env) modeli** kararına bağlı (🟦 → todo, Tier 1).

### `findTargetProperty(propertyId, childPropertyId?, properties) → Property?`
- **Görev:** Hedef alanı **`propertyId`** ile bulur. **`childPropertyId`** yalnız **Form List** hedefleyen aksiyonlarda anlamlıdır (`applyValidation`/`applySetStyle` → `formListPropertyId` + `formListRowCondition`); değer/görünüm/öznitelik aksiyonları (`assignValueToProperty`/`setViewForProperties`/…) Form List **satır-alanı hedeflemez** (v0.35 — DTO'larında child alanı yoktur).
- **Tetiklenme:** `applySetViewForProperties`, `applyAssignValueToProperty`, `applyFillDataSource`, `applyAssignValueToPropertyAttribute`.
- **Üretir/etki:** `Property?`; yan etki yok. **Çağırır:** —.

---

## 4. Zincirleme (cascade) & döngü
- **Değer-atayan aksiyonlar** (`applyAssignValueToProperty` · `applyFillDataSource` · `applyAssignValueToPropertyAttribute`)
  bir alanı **gerçekten değiştirince** o alan için **yeni `executeRules` turu** başlatır (değişim, `changeList`'e
  `manualChange=false` ile girer → aynı kaydetme akışına dahil).
- **Değer-atamayan aksiyonlar** (`applySetViewForProperties` · `applySetStyle` · `showMessage` · `applyValidation`) zincir **tetiklemez**.
- **Sonlanma:** zincir, mutasyon metotları **değişiklik olmadığında `false` döndüğünde** (yakınsama) durur.
- 🟦 **AÇIK:** birbirini besleyen kurallar için **tur/derinlik limiti + döngü tespiti** → todo (döngü koruması).

---

## 5. Aksiyon İşleyicileri (7)

> Ortak: her işleyici `conditionResult` (koşul TRUE/FALSE) alır, `bool hasChange` döner. Hedef alan `findTargetProperty` ile bulunur.

### `applySetViewForProperties(instance, rule, conditionResult) → bool`
- **Görev:** Listedeki her alana koşul sonucuna göre görünüm uygular. TRUE → `providedAppearance`, FALSE → `notProvidedAppearance` (ancak `notProvidedDeactive` ise **dokunulmaz**).
- **Üretir/etki:** `hasChange`; `target.setAppearance(visible, enabled, required)`. **Salt-okunur modda `enabled` zorla `false`.** Zincir **tetiklemez**.
- **Çağırır:** `findTargetProperty`.

### `applyValidation(context, instance, rule, conditionResult) → bool`
- **Görev:** Validasyon mesajı üretir (`fixedValue`/`fromCalculation`) ve `validationList`'e **kural-bazlı** ekler; koşul FALSE → aynı kurala ait girdiyi **kaldırır** (uyarı otomatik kalkar). **Satır-bazlı** (`withFormList`): hedef Form List'in her satırında `formListRowCondition` ayrıca değerlendirilir; sonuç = ana koşul **ve** satır koşulu.
- **Üretir/etki:** `hasChange`; `validationList` mutasyonu. `canPassValidation=false` girdisi kaydı/aksiyonu **bloklar**.
- **Çağırır:** `evaluateExpression`, `evaluateConditionGroup` (satır koşulu), `upsertValidation`.

### `upsertValidation(instance, ruleId, conditionResult, item, rowId?) → bool`
- **Görev:** `validationList`'te `ruleId` (+ satır id) bazlı idempotent ekle/güncelle/kaldır.
- **Tetiklenme:** yalnız `applyValidation`. **Üretir/etki:** `bool`; liste mutasyonu. **Çağırır:** —.

### `showMessage(context, instance, rule, conditionResult) → bool`
- **Görev:** Koşul TRUE ise başlık+mesaj (`fixedValue`/`fromCalculation`; başlık boşsa "Bilgilendirme") ile dialog gösterir.
- **Üretir/etki:** **her zaman `false`** (form değişmez); dialog. Zincir tetiklemez. 🟦 "bir kez göster" açık → todo.
- **Çağırır:** `evaluateExpression`.

### `applyAssignValueToProperty(context, instance, rule, conditionResult, ...) → bool`
- **Görev:** Hedef alanın **değerine** değer atar. TRUE → `resolveAssignValue` ile değeri üret ve `setValue`. FALSE → `clearIfConditionNotTrue` ise `clearValue`.
- **Üretir/etki:** `hasChange`; `setValue`/`clearValue`; değiştiyse **cascade**. Async kaynaklarda (`fromDataSet` lazy · `httpRequest` · async ifade) alan **meşgul**, `busyCount++`, yanıtta atama.
- **Çağırır:** `findTargetProperty`, `resolveAssignValue` (ve alt zinciri).

### `applyFillDataSource(context, instance, rule, conditionResult, ...) → bool`
- **Görev:** Hedef seçim alanının veri kaynağını doldurur. Ön koşul: koşul TRUE **ve** hedef dolu. Kaynak (`fillDataSourceType`): `serviceInstances` (lazy → sorgu / statik → filtre+sıra), `organizationData` (parametre filtreli), `userData` (kullanıcı verisi), `httpRequest`.
- **Üretir/etki:** `hasChange`; `setDataSource(items, selected?)`; değiştiyse cascade. Async'te meşgul/`busyCount`. **Koşul FALSE'ta temizleme yok.**
- **Çağırır:** `findTargetProperty`, `fetchServiceInstances`, `buildDataSourceItems`, `matchesDataSetParameters`, `matchesOrganizationParameters`, `compareForSort`, `readPropertyValue`.

### `applyAssignValueToPropertyAttribute(context, instance, rule, conditionResult, ...) → bool`
- **Görev:** Alanın bir **özniteliğine** (`minDate`/`maxDate`/`helperText`/`sideText`/`addNewEnabled`) değer atar. Yalnız koşul TRUE iken.
- **Üretir/etki:** `hasChange`; `setAttribute(value, attributeType)`; cascade. **Çağırır:** `findTargetProperty`, `resolveAssignValue`.

### `applySetStyle(context, instance, rule, conditionResult) → bool`
- **Görev:** Alanın (veya Form List satırı / satır-alanı) **tekil görünüm niteliklerini** (fontSize/titleColor…) uygular; koşul FALSE + `clearIfConditionNotTrue` → temizler. Form List'te `formListRowCondition` her satırda değerlendirilir.
- **Üretir/etki:** **her zaman `false`**; `style` mutasyonu. Zincir tetiklemez. **Çağırır:** `evaluateConditionGroup` (satır koşulu).

---

## 6. Koşul Motoru & Değer Çözümleme

### `evaluateConditionGroup(conditions, connector, instance, context) → bool`
- **Görev:** Koşul kümesini birleştirir: `and` → **hepsi**, `or` → **en az biri**. **Boş/null liste → TRUE.**
- **Tetiklenme:** `executeRules`; `applyValidation`/`applySetStyle` (satır koşulu); `evaluateCondition` (özyineli iç içe grup).
- **Üretir/etki:** `bool`. **Çağırır:** `evaluateCondition`.

### `evaluateCondition(condition, instance, context) → bool`
- **Görev:** Tek koşulu değerlendirir: grup ise (`isConditionList`) alt gruba iner; yaprak ise iki tarafı çözüp karşılaştırır.
- **Tetiklenme:** `evaluateConditionGroup`.
- **Üretir/etki:** `bool`. **Çağırır:** `evaluateConditionGroup` (özyineli), `resolveCompareValue` (×2 — sol/sağ), `compareValues`.

### `resolveCompareValue(side, instance, context) → value`
- **Görev:** Koşul tarafını (`BusinessRuleConditionCompareValue`) değere çözer: `propertyValue`→alandan (`valueTypeOfList` ile liste alanı), `viewProfile`→profil kodu, `fixedValue`→sabit, `fromCalculation`→ifade.
- **Tetiklenme:** `evaluateCondition`, aksiyon değer çözümleri, veri seti sorgu kurulumu, parametre koşulları.
- **Üretir/etki:** `value` (dinamik). **Çağırır:** `readPropertyValue`, `evaluateExpression`.

### `readPropertyValue(propertyId, properties, valueTypeOfList?) → value`
- **Görev:** `propertyId` ile alanın **kontrol-tipine göre tipli değerini** döndürür (metin/sayı/tarih/liste). Liste/çok-değerli kontrollerde `valueTypeOfList` ile hangi değer.
- **Tetiklenme:** `resolveCompareValue`, sıralama, parametre koşulları, veri kaynağı doldurma.
- **Üretir/etki:** `value`. **Çağırır:** —.
- 🟦 **AÇIK (motor spesifikasyonu):** kontrol-tipi → runtime tip eşlemesi (boş tarih temsili, sayı yerelleştirmesi, çok-değerli alan) → todo (davranış spesifikasyonu).

### `compareValues(left, right, operator) → bool`
- **Görev:** Tip-duyarlı karşılaştırma çekirdeği. Önce **boş/dolu** özel durumları (liste/çok-değerli alanlar), sonra **metin/sayı/tarih** kategorisine göre `criterionType` uygulanır.
- **Tetiklenme:** `evaluateCondition`, `matchesDataSetParameters`, `matchesOrganizationParameters`.
- **Üretir/etki:** `bool` (belirsiz/hata → **güvenli-false**). **Çağırır:** —.
- 🟩 **KARAR (v0.35) — tip-semantiği:** karşılaştırma tipi **alanın `propertyType`'ından** belirlenir (`propertyValue` tarafı: `numericTextbox`→sayı, `datepicker`→tarih, aksi→metin) — deterministik. **İki taraf da `fixedValue`** ise operatöre göre (`>`/`<` → sayısal parse dene, olmazsa metin). Sayı **kanonik** format (yerelleştirme yok); boş-tarih **gerçek null**; çoklu-değer → **`containsAny`/`containsAll`** (→ [`../models/enums/criterion-type.md`](../models/enums/criterion-type.md)). Belirsiz/hata → **güvenli-false**.

---

## 7. Değer Çözümleyiciler

### `resolveAssignValue(assignValue, instance, context) → value (sync | async)`
- **Görev:** `AssignValue`'yu `valueAssignType`'a göre değere çözer: `fixedValue` (+ `translationCode`), `propertyValue` (`useDisplay`), `fromCalculation` (çok-dilli: `expression` default + `localizedExpressions`), `fromDataSet`, `httpRequest`, `search`.
- **Tetiklenme:** `applyAssignValueToProperty`, `applyAssignValueToPropertyAttribute`, validasyon/mesaj metni, veri seti/filtre değeri, HTTP parametreleri.
- **Üretir/etki:** `value` (senkron **veya** `Future`). **Çağırır:** `resolveCompareValue`, `evaluateExpression`, `fetchServiceInstances`, `buildServiceInstanceQuery`, `matchesDataSetParameters`, `compareForSort`, `readPropertyValue`, `callHttpRequest`.
- 🟩 **KARAR:** `httpRequest` ← eski Function; `fromEba` **kaldırıldı**. 🟦 `search` davranışı + `httpRequest` şeması (query/header/body/template ↔ `DynamicParameter`) → todo.

### `resolveHttpParameter(value) → value (async)`
- **Görev:** HTTP çağrısı parametresini normalize eder (Future çöz · liste→ilk eleman · tarih→ISO-8601).
- **Tetiklenme:** `callHttpRequest` (template/query/header/body parametreleri). **Üretir/etki:** `value`. **Çağırır:** —.

### `callHttpRequest(config, instance, context) → value (async)`
- **Görev:** `httpRequest` konfigiyle dış çağrı yapar, yanıttan değeri çıkarır. **Konfig** (endpoint · `HttpMethod` · parametreler) `process-step` HTTP Request modelini paylaşır; **yanıt→değer çıkarımı iş-kuralına özeldir:**
  - **Tek değer** (`assignValueToProperty`): `responseParameter` (JSON alan yolu) verilirse o alan, yoksa yanıtın kendisi; yanıt liste ise ilk öğe.
  - **Liste** (`fillDataSource`): yanıt dizisinin her öğesinden `{value, display}` — hangi alanların value/display olacağı konfigde (`valueField`/`displayField`).
  - 🟩 **KARAR (v0.35) — alan-yolu dili = basit nokta-yolu** (`data.items.0.code`); gerekirse JSONPath'e genişletilir (aşırı mühendislik yok).
- **Tetiklenme:** `resolveAssignValue` (httpRequest), `applyFillDataSource` (httpRequest). **Üretir/etki:** `value`/liste; ağ çağrısı. **Çağırır:** `resolveHttpParameter`.

---

## 8. Veri Kaynağı (serviceInstances)

### `fetchServiceInstances(query, instance, context) → response (async)`
- **Görev:** Sorgu gövdesini kurup **başka servisin instance'larını** çeker (cache opsiyonlu).
- **Tetiklenme:** `applyFillDataSource` (lazy), `resolveAssignValue` (fromDataSet lazy). **Üretir/etki:** yanıt (hata → null); ağ çağrısı. **Çağırır:** `buildServiceInstanceQuery`.

### `buildServiceInstanceQuery(config, instance, context) → query`
- **Görev:** Sorgu gövdesini üretir: parametreler (değer çözümü, tarih→ISO, `searchActive`), istenen alanlar, sıralama, durum filtresi.
- **Tetiklenme:** `fetchServiceInstances`; `applyFillDataSource` (arama modunda hazır sorgu). **Üretir/etki:** `query`. **Çağırır:** `resolveCompareValue`.

### `buildDataSourceItems(response, valueProperty, displayProperty) → items`
- **Görev:** Yanıtı seçim listesine (`{value, display}`) çevirir; sayısal biçimleme.
- **Tetiklenme:** `applyFillDataSource` (lazy sonuç). **Üretir/etki:** `items`. **Çağırır:** —.

### `matchesDataSetParameters(params, row, instance, context) → bool`
- **Görev:** Bir instance satırı, tüm veri-seti parametre koşullarını (`every`) sağlıyor mu (`changeToCompare` yön çevirme).
- **Tetiklenme:** `applyFillDataSource`, `applyAssignValueToProperty`, `applyAssignValueToPropertyAttribute`, `resolveAssignValue` (statik filtre). **Çağırır:** `resolveCompareValue`, `readPropertyValue`, `compareValues`.

### `matchesOrganizationParameters(params, record, instance, context) → bool`
- **Görev:** Bir organizasyon-veri kaydı, tüm `FillDataSourceParameter` koşullarını (`every`) sağlıyor mu.
- **Tetiklenme:** `applyFillDataSource` (organizationData). **Çağırır:** `resolveCompareValue`, `compareValues`.

### `compareForSort(a, b, sortDirection) → int`
- **Görev:** Veri seti sıralama karşılaştırıcısı: `none`/`asc`/`desc`, null-güvenli, tip-öncelikli.
- **Tetiklenme:** veri seti sıralaması (assign/fill dalları). **Çağırır:** —.

---

## 9. Expression Motoru

### `evaluateExpression(expression, properties, instance, context) → value (sync | async)`
- **Görev:** İfadeyi değerlendirir. `#propertyCode` (ve `#propertyCode__display`) token'larını alan değerleriyle bağlar; **yerleşik fonksiyon kataloğunu** context'e koyar; `DateTime` üye erişimi (`.year/.month/.day/.hour/.minute`) destekler. Bir async fonksiyon kullanılırsa sonuç `Future` olur (çağıran `is Future` kontrolü yapar → async atama deseni).
- **Tetiklenme:** `resolveCompareValue` (fromCalculation), `applyValidation`, `showMessage`, `resolveAssignValue` (fromCalculation).
- **Üretir/etki:** `value` (senkron **veya** Future); async fonksiyonlar ağ çağrısı yapabilir, `dataError` set edebilir. **Çağırır:** — (kendi içinde bağımsız).
- 🟩 **KARAR (v0.35) — ifade dili = JSONLogic + yerleşik fonksiyon kataloğu:** ifadeler **JSONLogic** ağacıdır (JSON; tasarımcı UI'dan üretir, elle yazılmaz). Seçim gerekçesi: **tam-frontend + çok-client** (Dart + JS portu olgun; CEL'in Dart portu yok) ve **veri-only → sandbox içsel** (kod yürütmez, güvenlik gereksinimini doğal karşılar). Eski yerleşik fonksiyonlar (`getExchange`/`getUser*`/`sumFormList`…) **custom operator** olarak eklenir; imzaları katalog dokümanında. **Async operatörler** (ağ çağıranlar) sarmalayıcı ile desteklenir (çoğu fonksiyon cache'ten **sync** okur — §6.2 endpoints). 🟩 çok-dilli ifade `expression` + `localizedExpressions`. 🟦 **AÇIK:** katalog **kesin kapsamı** + operatör imzaları → todo.

### Yerleşik fonksiyon kataloğu (kategoriler)
İfade dilinde çağrılabilen ~70 yerleşik fonksiyon (tek tek değil, **kategoriler**):

| Kategori | Örnekler |
|---|---|
| **Tarih/zaman/iş-günü** | `now` · `today` · `day` · `dayOfWeek` · `isWeekend` · `isHoliday` · `dateTimeAdd` · `toStringDateTime` · `getWorkDayHour` · `addWorkDay` · `findNextWorkDay` · `differenceWorkDay` |
| **String/sayı** | `intTryParse` · `doubleTryParse` · `toStringDouble` · `toUpperCase(TR)` · `toLowerCase(TR)` · `replace` · `subString` · `split` · `isMail` · `isForbiddenCharacters` · `isAlnumTR` · `count` |
| **Kullanıcı/organizasyon** (çoğu async) | `getUserMail/FullName/Id/Code` · `getManagerUserId/Code` · `getUserManagerByProfession` · `getUserWorkerLevelCode` · `getUserCompany/Department/ProfessionCode/Name` · `getDepartmentManagerCode` · `getExpenseCenterAdditional` · `checkUserInUserGroup` |
| **Kredi kartı** | `getCreditCardNumber` · `getUserCreditCardNumber/Code/Desc` · `getUserByCreditCardCode` |
| **Kontrol-toplama/validasyon** | `sumDatagrid` · `avgDatagrid` · `findPropValueFromDatagrid` · `sumFormList` · `combineFormList` · `findPropValueFromFormList` · `isServiceValidate` · `isPropertyValidate` |
| **Döviz/diğer** | `getExchange` (async) — ⏸️ **Currency askıya alındı (v0.47)** → katalog-dışı adayı (→ todo) |

- 🟦 **AÇIK:** kataloğun yeni motordaki **kesin kapsamı** (hangileri taşınır/sadeleşir; masraf-spesifik olanlar — GroupByTax vb.) + **çok-client portlanabilirlik** → todo (ifade dili).

---

## 10. Yeni motor kararları (özet)
| Konu | Karar |
|---|---|
| Çalışma yeri | **Tam frontend** (kurallar gömülü; client motoru) |
| Kural sırası | **`priority`** (küçük = önce; eşitlikte `id`) |
| Tetikleme kapsamı | **koşul + aksiyon/ifade alanları** (`ruleAppliesTo`) |
| Aksiyon konfigi | tip-başına **JSONB** (discriminated union) |
| Değer kaynağı | `httpRequest` (← Function); `fromEba` **kaldırıldı** |
| Çok-dilli ifade | `expression` (default) + `localizedExpressions` |

## 11. Açık noktalar (→ [`../todo.md`](../todo.md))
**Kalan (karar bekleyen):** hata görünürlüğü + veri-hatası davranışı · cascade **döngü/derinlik limiti** · `search` değer kaynağı ·
ifade **katalog kesin kapsamı + operatör imzaları** (dil = JSONLogic seçildi) · `httpRequest` alan-yolu **JSONPath'e genişletme** ·
`environmentRestriction` (ortam modeli) · `setStyle` `style` şeması.
**Çözüldü (v0.35):** ifade dili = JSONLogic · tip-semantiği (`propertyType`-güdümlü) + `any`/`every` (`containsAny`/`containsAll`) ·
koşul depolama = gömülü JSONB · `prepareEngine` = hibrit ön-yükleme · `shouldNotWorkInReadonlyMode` = motor uygular · httpRequest çıkarım = nokta-yolu.

---

## 12. Uçtan uca örnek (golden fixture)
Tam `BusinessRule` kayıtları — `configuration`, koşullar ve runtime tipi **birlikte**. (`configuration` = doğrudan aksiyon DTO'su; ayrımlayıcı `businessRuleActionType`.)

### Örnek 1 — `setViewForProperties` (koşullu görünüm)
*"Talep tipi = **AVANS** ise AÇIKLAMA (propertyId 73) görünür + zorunlu; değilse gizli."*
```jsonc
{
  "id": 421, "organizationId": 12, "serviceId": 30,
  "code": "avansAciklamaZorunlu", "definition": "Avans talebinde açıklama zorunlu",
  "businessRuleActionType": "setViewForProperties",
  "businessRuleRuntimeType": "always", "businessRuleConditionType": "and",
  "priority": 10, "activeViewProfiles": [], "shouldNotWorkInReadonlyMode": false,
  "businessRuleConditions": [
    { "isConditionList": false, "criterionType": "equals",
      "referenceValue": { "compareType": "propertyValue", "propertyValue": { "propertyId": 55 } },
      "valueToCompare": { "compareType": "fixedValue", "fixedValue": { "value": "AVANS" } } }
  ],
  "configuration": {
    "properties": [
      { "propertyId": 73,
        "providedAppearance":    { "visible": true,  "enabled": true,  "required": true  },
        "notProvidedAppearance": { "visible": false, "enabled": false, "required": false },
        "notProvidedDeactive": false }
    ]
  }
}
```
**Çalışma:** Form açılışında + `TALEP_TIPI`(55) her değiştiğinde tetiklenir (koşulda geçiyor). Koşul TRUE → alan 73'e `providedAppearance`; FALSE → `notProvidedAppearance`. Değer atamadığı için **cascade yok**.

### Örnek 2 — `assignValueToProperty` + `fromCalculation` (zincirleme)
*"TUTAR(80) veya KUR(81) değişince TL_TUTAR(90) = TUTAR × KUR."*
```jsonc
{
  "id": 422, "organizationId": 12, "serviceId": 30,
  "code": "tlTutarHesapla", "definition": "TL tutarını hesapla",
  "businessRuleActionType": "assignValueToProperty",
  "businessRuleRuntimeType": "always", "businessRuleConditionType": "and", "priority": 20,
  "businessRuleConditions": [
    { "isConditionList": false, "criterionType": "isNotEmpty",
      "referenceValue": { "compareType": "propertyValue", "propertyValue": { "propertyId": 80 } },
      "valueToCompare": { "compareType": "fixedValue", "fixedValue": { "value": "" } } },
    { "isConditionList": false, "criterionType": "isNotEmpty",
      "referenceValue": { "compareType": "propertyValue", "propertyValue": { "propertyId": 81 } },
      "valueToCompare": { "compareType": "fixedValue", "fixedValue": { "value": "" } } }
  ],
  "configuration": {
    "propertyId": 90,
    "value": { "valueAssignType": "fromCalculation", "fromCalculation": { "expression": "#TUTAR * #KUR" } },
    "clearIfConditionNotTrue": false
  }
}
```
**Çalışma:** `TUTAR` değişir → kural tetiklenir (koşulda **ve** ifadede geçiyor — genişletilmiş kapsam §3), koşul TRUE → `#TUTAR * #KUR` hesaplanır, alan 90'a `setValue`. Değer **gerçekten değiştiyse** (§0.2) alan 90 için **yeni tur** → 90'ı kapsamında kullanan kurallar çalışır (cascade); değişmezse zincir durur.

> **Not:** `businessRuleConditions` **gömülü JSONB** olarak taşınır (KARAR v0.35 — ayrı ilişkisel tablo değil; `configuration` ile tutarlı).

---

*Oluşturma: 2026-08-27 · Güncelleme: 2026-08-27 (runtime modeli §0.1–0.3 · httpRequest çıkarımı · golden fixture §12 · tutarsızlık düzeltmeleri).*
