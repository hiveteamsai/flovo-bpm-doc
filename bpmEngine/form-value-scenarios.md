# Flovo — Form Value Kullanım Senaryoları (depolama kararı için)

> **Durum:** 🟡 TOPLANIYOR — senaryolar **somut örneklerle** detaylandırılıyor.
> **Amaç:** **Form value'larının nasıl tutulacağına** (depolama modeli) karar vermeden önce, bu değerlerin **nerede ve
> nasıl** okunup yazıldığını **eksiksiz ve örnekli** toplamak. Depolama kararı **en sonda** bu senaryolara göre verilecek.
>
> **İlgili:** `service-settings/properties.md` · `service-settings/process-step-action.md` §2 (`changeList`) ·
> `organization-settings/translation.md` (dil çözümleme) · `flovo-bpm-engine.md` · `flovo-customer-api.md` · `todo.md`.

---

## 0. Tanım & koşu örneği

Bir **form value** = belirli bir **form instance**'ındaki (doldurulmuş kayıt) bir **property**'nin **değeridir**.
Ayrımlar: **ham değer (raw)** ↔ **gösterim (display)** (çeviriye bağlı) · **instance value** ↔ **tanım** · **kalıcı** ↔ **türetilmiş/yansıma**.

**Koşu örneği — Masraf Formu (Service):**
- `expenseNo` (metin), `expenseType` (combobox: `0`=Yemek · `1`=Konaklama · `2`=Ulaşım), `amount` (numeric),
  `currency`, `receipt` (file), `status` (durum),
- **`groupByTax`** (Group By Tax alanı — **liste/list-of-model**): her **kalem** = `{ giderTürü, vergiOranı, tutar }`.
- Organizasyon `defaultLang = tr`. Kullanıcı bazen `en`/`de`.

> Notasyon: **[R]** oku · **[W]** yaz · **[FE]** frontend · **[M]** motor · **[D]** depolama · **[API]** dış · **[RPT]** rapor.

---

## 1. Form doldurma & anlık UX (frontend)
1. **[W][FE]** Kullanıcı yeni masraf açar: `amount=1500`, `expenseType=2`, `groupByTax`'a 2 kalem ekler. → value'lar oluşur/güncellenir.
2. **[W][FE→M]** `amount` `1500→1800` değişince `saveAndRefreshOnAfterChange` → kaydet isteği + toplam yeniden hesaplanmış form döner.
3. **[R][FE]** Onaylayan profilinde `amount` **salt-okunur**, talep edende düzenlenebilir (aynı value, farklı görünüm).
4. **[R][FE]** Validasyon: `amount` **zorunlu** ve sayısal; `receipt` zorunlu ise boş dosya hata verir.
5. **[R/W][FE]** `expenseType`: **value=`2` saklanır**, ekranda display "Ulaşım" (tr) gösterilir (bkz. §6).
6. **[R/W][FE]** Özel alan value şekilleri: `groupByTax` = `[{giderTürü,vergiOranı:18,tutar:1000},{…:8,tutar:500}]` · Barcode=`"8690…"` · Map=`{lat,lng}` · Image Area Selector = JSON nokta seçimi.

## 2. İş kuralları (frontend realtime — `business-rule.md`)
7. **[R][FE]** Koşul: `expenseType == 1 (Konaklama)` → `nightsCount` alanını **göster + zorunlu** yap.
8. **[W][FE]** `assignValueToProperty` (`fromCalculation`): `taxAmount = amount * (vergiOranı/100)` hesapla ve yaz.
9. **[R/W][FE]** `fillDataSource`: `city` seçilince `district` combobox veri kaynağını doldur (değere bağlı).

## 3. Motor / akış kararları (backend — `flovo-bpm-engine.md`)
10. **[W][M]** `changeList`: onaylayan "Onayla" aksiyonuyla `note="uygun"` gönderir → adım **işini yapmadan ÖNCE** forma yazılır.
11. **[R][M]** Karşılaştırma: `amount > 5000` → `true` (üst-yönetici onayı) / değilse `false`.
12. **[R][M]** Switch: `expenseType` değerine göre farklı onay dalı.
13. **[R][M]** Değişken kullanıcı ataması: `approver` alanındaki **user id** değerine göre adımı ata.
14. **[R][M]** Atlama: `skipIfPreApproved` — bir alanın değeri "önceden onaylı" ise adımı atla.

## 4. Değer yazma (motor)
15. **[W][M]** Değer Atama: `status`'a "Onaylandı" yaz **veya** `groupByTax` **alt-kalemlerine** KDV oranı yaz (`targetInstancesPropertyId`).
16. **[W][M]** Custom ID Creator: `MSR-2026-0001` üret → `expenseNo` alanına yaz.
17. **[W][M]** Flovo AI (fatura): `receipt` file'ından `amount`/`vendor`/`date` çıkar → **Instance Creator init** ile alanlara yaz.
18. **[R/W][M]** HTTP Request: body'de `{amount,currency}` gönder; response `{approvedAmount}` → `changeList` ile `approvedAmount` güncelle.

## 5. Yansıma (reflection) alanları — **Parent Property · User Info · Flow Info** ⭐ (DEĞERLENDİRME)
Bu alanların **kendine ait, kullanıcı tarafından değişen bir value'su yoktur**; başka bir yerdeki değerin **yansımasıdır**:
- **Parent Property** — ana/üst formun bir alanının değeri. _Örn:_ alt-servis "Masraf Kalemi" formunda, ana "Masraf Talebi"nin `projectCode`'unu yansıtan alan.
- **User Info** — kullanıcı metadata. _Örn:_ `creatorDepartment` = formu oluşturan kullanıcının **departmanı**.
- **Flow Info** — akış metadata. _Örn:_ `createdDate`, `currentStatus`, `creatorUser`.

**⭐ Karar verilecek — bu yansıma değerleri value tablosunda tutulsun mu?**

| Seçenek | Nasıl | Artı | Eksi / Soru |
|---|---|---|---|
| **A — Kopya tut (materialized) + senkron** | Yansıma değeri **kayda yazılır** | Rapor/filtre/sıralama/arama **kolay** (değer kayıtta hazır) | Kaynak değişince (departman değişti, ana form `projectCode` güncellendi) **buradaki kopya güncellensin mi?** → **snapshot mı, canlı mı?** |
| **B — Saklama, on-read getir** | Değer **hiç yazılmaz**; okunurken kaynaktan (parent form / user / flow) **join/lookup** ile getirilir | Her zaman **güncel**, tutarsızlık yok, depolama yok | Okuma/rapor/**sorgu maliyeti** (join); raporda **filtre/sıralama zor** (hesaplanan kolon) |

**Snapshot ↔ canlı ikilemi (Seçenek A için):**
- **Snapshot:** yansıma anındaki değer **sabit** kalır. _Örn:_ "**Onay anında** departman = Satınalma"yı korumak (audit/denetim için doğru davranış olabilir).
- **Canlı:** kaynak değişince kopya **güncellenir** (senkron maliyeti + tutarsızlık riski). _Örn:_ kullanıcı departman değiştirince eski masraflarda da yeni departman görünür.

> **Açık:** Yansıma alanları için A/B ve (A ise) snapshot/canlı kararı → §12 / `todo.md`. Not: farklı yansıma tipleri **farklı** karar isteyebilir (Flow Info doğası gereği canlı/anlık; Parent Property audit için snapshot).

## 6. Çok dillilik & **dil eşleşmesi** (`translation.md`) ⭐
`expenseType` value=`2`, `code="expenseType.transport"`, `definition(tr)="Ulaşım"`, `translation(en)="Transport"`, `translation(de)="Transport"`.
> **Ham value (`2`) her zaman aynıdır; değişen yalnız gösterim/sorgu metnidir.**

- **6a — Kullanıcı dili = organizasyon `defaultLang` (tr):** [R][FE/M]
  Display **doğrudan `definition`** ("Ulaşım"); **translation tablosuna gidilmez** (performans). Sorgu/gösterim `definition` üzerinden.
- **6b — Kullanıcı dili ≠ `defaultLang` (en):** [R][FE/M]
  Display **`translation`** tablosundan: `code` + `languageCode=en` + `organizationId` → "Transport". Yoksa/boşsa **`definition` fallback**.
- **6c — Sorguya etkisi (kritik):** Gösterime bağlı **filtre/sıralama/gruplama** yapılırken sorgu **dile göre değişir**:
  - dil eşleşiyor → **`definition`** üzerinden,
  - eşleşmiyor → **`translation` join** (`code`+`languageCode`) üzerinden.
  _Örn:_ "gider türünü **alfabetik sırala" → tr'de `definition`'a göre, en'de `translation`'a göre **farklı sıra**.

## 7. Kalıcılık & geçmiş (`flovo-bpm-engine.md` §8)
19. **[D]** `savePropertyToDb`: `taxAmount` **hesaplanan/türetilmiş** — DB'ye yazılsın mı (rapor gerekiyorsa evet)?
20. **[D]** `saveChangeLog`: `amount` **değişiklik geçmişi** (kim `1500→1800` yaptı, ne zaman).
21. **[D]** `backingField`: gizli/arka-plan value.
22. **[D]** **Dosya/binary**: `receipt` faturası — url + binary depolama (mevcut "yavaş belge yükleme" şikâyeti).
23. **[D]** **Instance state**: onay bekleyen masraf **3 gün** beklerken **tüm value'lar kalıcı** (uyu-uyan).

## 8. Raporlama & sorgu ⭐ (`view-profile.md` §3 — ayrı özellik)

### 8.1 Normal rapor — **form başına 1 satır**
Her form = **1 satır**; kolonlar = seçili alan value'ları. [R][RPT]
_Örn (Masraf raporu):_
| expenseNo | expenseType | amount | status |
|---|---|---|---|
| MSR-0001 | Ulaşım | 1500 | Onaylandı |
- Filtre: `amount > 1000`, `status = Onaylandı` · Sıralama: `createdDate desc`.

### 8.2 **Kalem bazlı rapor** (line-item — list-of-model açılımı) ⭐
**Tanım:** Bir **liste-içeren alan** (list-of-model: **Group By Tax**, Key-Value List, Form List) seçilerek oluşturulan rapor.
O alanın value **listesindeki HER kayıt için ayrı satır** üretilir; form-düzeyi alanlar her satırda **tekrarlanır**.
**Örnek:** 1 masraf formunun `groupByTax`'ında **2 kalem** varsa (%18→1000, %8→500), kalem-bazlı raporda o form **2 satır** üretir:
| expenseNo | expenseType | vergiOranı | tutar |
|---|---|---|---|
| MSR-0001 | Ulaşım | %18 | 1000 |
| MSR-0001 | Ulaşım | %8 | 500 |
> Normal raporda **1 satır** olan form, kalem-bazlıda **alt-kayıt sayısı kadar** satır olur. [R][RPT]

### 8.3 List-of-model value'larını getirme + **filtre/sıralama**
Kalem-düzeyi alanlara göre filtre/sıralama: sadece `vergiOranı = %18` kalemleri; `tutar desc` sırala.
→ Value içindeki listeyi **açıp (unnest)** sorgulamayı gerektirir; depolama modeli buna izin vermeli. [R][RPT]

### 8.4 **Dile göre farklı sorgu** (translation birleşimi) ⭐
Kalem/alan gösterimi çeviriye bağlıysa (örn. `giderTürü` combobox display), filtre/sıralama **dile göre**:
- dil = `defaultLang` → **`definition`** üzerinden sorgu,
- dil ≠ `defaultLang` → **`translation` join** (`code`+`languageCode`) üzerinden sorgu.
→ Aynı rapor, `tr` ve `en` kullanıcıda **farklı sıralama/gruplama** üretir; depolama+sorgu bunu desteklemeli (value ⋈ translation, `languageCode` filtreli). [R][RPT]

### 8.5 **Gruplama & toplama** (cross-form aggregation) ⭐
Liste-içeren alandaki kalemleri bir boyuta göre **grupla + topla**, **birden çok form** üzerinden.
**Örnek:** Bir kullanıcının **tüm masraf formlarındaki** `groupByTax` kalemlerini **vergi oranına göre grupla, tutarları topla**:
| vergiOranı | toplamTutar (tüm formlar) |
|---|---|
| %18 | 42.000 |
| %8 | 12.500 |
→ Tüm instance'ların list-of-model value'larını **açıp gruplayıp topla** (ağır sorgu). Gruplama boyutu çeviriye bağlıysa §8.4 kuralı da geçerli. [R][RPT]

## 9. Dış / API / entegrasyon (`flovo-customer-api.md`)
24. **[R][API]** `GET /instances/{id}` — tüm alan value + meta okuma (PDF üretimi).
25. **[W][API]** `PATCH /instances/{id}` — value güncelleme (`changeList` benzeri).
26. **[R][API]** `GET /services/{id}/schema` — custom code'un alan adı/tipini bilmesi (value yorumlama).
27. **[R/W][API]** Webhook — `parameters` ile value taşıma.
28. **[R][API]** `POST /instances/search` — **alan value'suna göre arama** (`barcode = X`).

## 10. İlişkisel / alt-servis
29. **[R/W][M]** Form List — ana ↔ alt-servis value **aktarımı** (`parameterTransfer`/`propertyTransferParameters`).
30. **[R][M/FE]** Parent Property yansıması (bkz. §5).
31. **[R/W][M]** Süreç Adımı Tetikleme — alt-servis adımı tetiklerken value taşıma.
32. **[R][RPT]** Alt-servis kayıtlarının **listelenen alan value'ları** + seçim (tik) durumu (profil bazlı → `view-profile-property-setting`).

---

## 11. Değer tipleri / şekil (depolama için kritik girdi)
- **Skalar:** metin · sayı (ondalık/negatif) · bool.
- **Tarih/saat.**
- **Liste (list-of-model):** multi-select combobox · Key-Value List · **Group By Tax** (kalem: türü+oran+tutar) · Form List.
- **JSON/yapısal:** Image Area Selector (nokta seçimleri).
- **String-kodlanmış:** Barcode.
- **Referans:** File (url/binary) · user/organization id · **yansıma** (Parent/User/Flow — §5).
- **Koordinat:** Map.

---

## 12. Değerlendirme / açık depolama soruları (SONRA)
> **Açık sorular tek yerde:** Bu bölümdeki depolama soruları, tutarsızlığı önlemek için merkezi
> [`todo.md`](todo.md)'de **"Property value depolaması"** (Tier 1) maddesinin **7 alt-sorusu** olarak toplanmıştır:
> **(1)** EAV ↔ kolon ↔ JSON ↔ hibrit; **(2)** yansıma alanları (§5) A (kopya+senkron) ↔ B (on-read), snapshot ↔ canlı;
> **(3)** çeviri-bağımlı sorgu/indeksleme (§6c/§8.4); **(4)** list-of-model unnest / cross-form (§8.2–8.5); **(5)** binary
> ayrımı (§7); **(6)** value geçmişi/sürüm (§7); **(7)** instance state serileştirme (§7). Karar, buradaki senaryolar
> (§1–§11) ışığında verilecek.

---

## 13. Eklenecekler / eksikler (KULLANICI DOLDURACAK)
> _(Eksik gördüğün senaryoları buraya yaz; sonra ilgili kategoriye işlenecek.)_
- _(henüz eklenmedi)_

---

*Oluşturma: 2026-07-03.*
