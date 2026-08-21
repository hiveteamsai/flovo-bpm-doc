# Flovo — Çeviriler (Translations) Tasarımı

> **Durum:** 🟢 DETAYLANIYOR
> **Amaç:** Uygulamadaki metinlerin **çok dilli** karşılıklarını **`code` üzerinden** yönetmek; hem **Flovo'nun
> sağladığı ortak çeviriler**, hem de her **organizasyonun kendi çevirileri** tek modelde tutulur.
>
> **İlişki:** Çeviriler tüm servislerde ortaktır (genel ayar). Alan etiketleri, durum/aksiyon tanımları, bildirim
> metinleri vb. `code` ile bu tablodan çözülür.

---

## 0. Çeviri (Translation) Nedir?
Bir **çeviri (translation)**, bir **`code`**'a bağlı metnin dillere göre karşılıklarını tutan kayıttır. Uygulamada bir
metin göstermek gerektiğinde, kaynak kaydın **`translationCode`**'u çeviri tablosundan çözülür ve **aktif dile** göre
metin döndürülür.

> **Bağlanma noktası:** Çevrilebilir modeller, çeviriye **iş kodlarıyla (`code`) değil**, ayrı ve **nullable** bir
> **`translationCode`** alanıyla bağlanır (`Model.translationCode → Translation.code`). **`null` = çeviri es geçilir**,
> doğrudan `definition` kullanılır. Gerekçe ve alanı taşıyan modellerin listesi → **§3.1**.

İki tür çeviri vardır:
- **Ortak (global) çeviriler** — `organizationId = null`. **Flovo** tarafından oluşturulur; **tüm
  organizasyonlar görüntüleyip kullanabilir**, fakat **güncelleyemez** (salt-okunur).
- **Organizasyon çevirileri** — `organizationId = <org>`. İlgili organizasyon **kendi çevirilerini** oluşturur ve
  **yalnız kendi kayıtlarını** güncelleyebilir.

---

## 1. Çeviri Veri Modeli
Her **dil için ayrı kayıt** tutulur (kolon-başına-dil değil, **kayıt-başına-dil**).

| Alan | Tip | Zorunlu | Açıklama |
|---|---|---|---|
| `id` | int | Otomatik | Çeviri kaydı ID'si |
| `code` | string | Evet | Çeviri kodu — **eşleştirme anahtarı**; kaynak kayıtların **`translationCode`**'u buraya eşleşir (serbest metin; istenirse `form.submit` / `department.01` gibi namespace'lenebilir) |
| `organizationId` | int / null | Hayır | Sahibi organizasyon (FK → `organization.md` `id`). **`null` = ortak (Flovo) çeviri.** |
| `languageCode` | string | Evet | **Dil kodu** — sabit dil seti (`tr` / `en` / `de`) içinden (krş. `organization.defaultLang`) |
| `definition` | string | Evet | Bu **dildeki metin** (`languageCode` dilinde) |

> Bir `code`'un her dili **ayrı satırdır**; aktif dile (`languageCode = userLang`) uyan kaydın `definition`'ı döndürülür.
> Yeni dil eklemek artık **şema (kolon) değişikliği değil**, yeni **kayıt** eklemektir.

---

## 2. Sahiplik & Yetki (kim neyi güncelleyebilir?)
| Kayıt | `organizationId` | Kim oluşturur | Kim görüntüler | Kim günceller |
|---|---|---|---|---|
| **Ortak (global)** | `null` | Flovo | Herkes | **Yalnız Flovo** — organizasyonlar **güncelleyemez** |
| **Organizasyon** | `<org>` | O organizasyon | O organizasyon | **Yalnız o organizasyon** (kendi `organizationId`'si) |

- Bir organizasyon, **başka bir organizasyonun** veya **ortak (null)** kayıtları **güncelleyemez**.
- Organizasyon, ortak bir `code`'u beğenmezse **aynı `code` ile kendi kaydını oluşturarak ezer** (override → §3).

---

## 3. Çeviri Motoru (Çözümleme / Resolution)
Frontende **`translationCode` + `definition` içeren** veriler (property label, seçili combobox metni, durum/aksiyon
tanımı, departman/şirket adı vb.) iletilirken metin aşağıdaki gibi çözülür.

**Eşleşme anahtarı = `translationCode` (iş kodu DEĞİL):** Kaynak kayıt, çeviriye **kendi `code`'uyla değil**, ayrı
**`translationCode`** alanıyla bağlanır (→ §3.1). Eşleşme `Translation.code` ile yapılır: **`Model.translationCode →
Translation.code`**.

**Temel varsayım — kaynak `definition` = varsayılan dildeki metin:** Kaynak kaydın `definition` alanı,
**organizasyonun `defaultLang`** dilindeki metin kabul edilir (→ `organization.md`). Diğer diller `Translation`
kayıtlarında (`languageCode` + `definition`) tutulur. Motor bunun üzerine kurulur:

- **Adım 0 — `translationCode` `null`:** kayıt çeviriye **hiç bağlanmamıştır** → **translation işlemleri es geçilir**,
  doğrudan `definition` iletilir. _(Çeviri **opt-in**'dir; anahtar verilmeyen kayıt hiç sorgulanmaz.)_
- **Adım 1 — Kullanıcı dili = organizasyonun `defaultLang`'i:** `definition` zaten kullanıcının dilindedir →
  **translation tablosuna gidilmez**, doğrudan `definition` iletilir. _(varsayılan dildeki kullanıcıda sorgu maliyeti yok)_
- **Adım 2 — Diller farklı:** kaynak `definition` kullanıcının dilinde **değildir** → **`translationCode` ile translation
  tablosuna** bakılır. Eşleşme **`code`(=translationCode) + `languageCode`(=userLang) + `organizationId` birlikte** yapılır:
  1. **`organizationId` && `code` && `languageCode`** eşleşen kayıt varsa → **ilk hedef** (organizasyon override'ı).
  2. Yoksa → **`organizationId = null` && `code` && `languageCode`** (ortak/Flovo) kaydına düşülür.
- **Adım 3 — Fallback:** Eşleşme **yoksa** *veya* bulunan kaydın **`definition`'ı boşsa** → translation kullanılmaz,
  kaynak **`definition`** iletilir.

```
resolveText(translationCode, sourceDefinition, organizationId, userLang, orgDefaultLang):
  # 0) Çeviri anahtarı yok → çeviri es geçilir, doğrudan kaynak metin
  if (translationCode == null):
      return sourceDefinition

  # 1) Kullanıcı dili = organizasyonun varsayılan dili → kaynak definition zaten o dilde
  if (userLang == orgDefaultLang):
      return sourceDefinition

  # 2) Diller farklı → translation tablosu; dil = userLang (önce organizasyon, sonra ortak)
  t = find(x => x.code == translationCode AND x.languageCode == userLang AND x.organizationId == organizationId)
  if (t == null):
      t = find(x => x.code == translationCode AND x.languageCode == userLang AND x.organizationId == null)

  # 3) Kayıt yok VEYA metin boş → kaynak definition'a düş
  if (t == null OR isEmpty(t.definition)):
      return sourceDefinition

  return t.definition   # languageCode = userLang dilindeki metin
```

**Sonuç:** Anahtarı olmayan (`translationCode = null`) kayıt **hiç sorgulanmaz**; varsayılan dildeki kullanıcı da **hiç
tabloya gitmez** (performans); farklı dildeki kullanıcı önce **organizasyon** çevirisini, yoksa **ortak** çeviriyi görür;
ikisi de yoksa/boşsa güvenle **`definition`**'a düşülür.

### 3.1 Neden ayrı `translationCode`? (iş kodu ≠ çeviri anahtarı)
Çeviri ad-uzayı **organizasyon geneli** tektir (`(organizationId, code, languageCode)`); içinde **hangi varlığa ait
olduğunu** söyleyen bir ayrım **yoktur**. Modellerin `code`'u ise yalnız **kendi içinde** benzersizdir
(`(organizationId, code)`). Dolayısıyla iş kodu doğrudan eşleşme anahtarı yapılsaydı **farklı varlıkların aynı kodu
çakışırdı**:

> Departman `code = "01"` ile Şirket `code = "01"` aynı organizasyonda **meşru şekilde** birlikte bulunur — ikisi de
> **aynı** translation satırına düşerdi (departman adı şirket adının çevirisini gösterirdi).

Bu yüzden çeviri eşleşmesi **ayrı `translationCode` alanı** üzerinden yapılır; `code` yalnız **iş/tanımlayıcı** rolünü
taşır. İki alanın ayrılması, aynı ad-uzayında **kasıtlı paylaşımı** da mümkün kılar: iki farklı kayıt **aynı**
`translationCode`'u vererek **aynı** çeviriyi bilinçli olarak paylaşabilir.

**Alanı taşıyan modeller — 23** (`translationCode` `string?`):
- **Organizasyon ayarları (15):** Company · Department · Profession · CostCenter · WorkerLevel · WorkingSchedule · UserGroup ·
  CreditCard · Position (+ alt model `Staff`) · AdditionalQualification (+ alt model `QualificationItem`) · VacationDay · Status · Action.
- **Servis ayarları (8):** Service · Solution · Property · PropertyItem · ProcessStep · ProcessStepAction · BusinessRule · ViewProfile.
- **Taşımayanlar:** `Style` · `User` · `Organization` (çevrilecek `definition` metni yok) ve `Translation` (anahtarın kendisi).

> **VacationDay notu:** Bu modelde `code` **hiç yoktu** — yani çeviri anahtarı olmadığı için `definition` **hiç
> çevrilemiyordu**. `translationCode` eklenmesiyle bu boşluk da kapandı.

> **Snapshot kopyaları:** `ProcessStepAction` (Action'dan) ve `...QualificationValue.comboboxTranslationCode`
> (QualificationItem'dan) kopyalanırken **`translationCode` de birlikte kopyalanır** — kopya metin de aktif dile çözülebilsin.

---

## 4. Benzersizlik & Kısıtlar
- **Bir organizasyonda bir `code`'un bir dili tek kayıttır** → `(organizationId, code, languageCode)` **benzersiz**.
- Ortak tarafta da aynı: `organizationId = null` + `code` + `languageCode` benzersiz.
- Bir organizasyon, bir **ortak (null) `code` + `languageCode`** için **kendi kaydını** oluşturarak o dili **ezebilir**
  (override).

**Örnek** (`code = "form.submit"`):
| id | code | organizationId | languageCode | definition | Kimin gördüğü |
|---|---|---|---|---|---|
| 1 | `form.submit` | `null` | `tr` | Gönder | Kaydı olmayan **tüm** organizasyonlar (ortak) |
| 2 | `form.submit` | `null` | `en` | Submit | Ortak |
| 3 | `form.submit` | `42` | `tr` | İlet | **Yalnız `organizationId=42`** (ortak `tr`'yi ezer) |
| 4 | `form.submit` | `42` | `en` | Send | **Yalnız `organizationId=42`** (ortak `en`'i ezer) |

`organizationId=42` → "İlet/Send"; diğer tüm organizasyonlar → "Gönder/Submit".

---

## 5. Açık Kararlar / Sorular
> **Açık sorular tek yerde:** Bu dokümanın açık kararları/soruları, tutarsızlığı önlemek için **yalnız** merkezi
> [`todo.md`](../todo.md) dosyasında toplanır (önceliklendirilmiş tüm-doküman listesi). İlgili maddeler orada `(translation §..)`
> atfıyla bulunur; verilen kararlar bu dokümanın **gövdesinde** anlatılır.

> **Çözülenler (yerel karar log'u):**
- [x] **Dil seti** — `languageCode` **sabit set** (`tr`/`en`/`de`) içinden (krş. `organization.defaultLang`). Model **kayıt-başına-dil** olduğu için yeni dil **kolon değil kayıt** ekler (şema değişmez).
- [x] **Boş/eşleşmeyen davranışı** — istenen dildeki değer boşsa veya eşleşme yoksa **`definition`**'a düşülür (§3).
- [x] **`code` serbest metin** — kod **serbest**tir; kullanıcı isterse **namespace** (örn. `form.submit`) ile alanlar arası ayrım yapabilir (zorunlu değil).
- [x] **Eşleşme anahtarı = ayrı `translationCode`** — çeviri, modellerin **iş kodu (`code`)** üzerinden yapılmaz; her çevrilebilir modelde **ayrı, nullable `translationCode`** alanı vardır (§3.1). Böylece **model-içi benzersiz** iş kodlarının (Departman "01" ↔ Şirket "01") **organizasyon-geneli** çeviri ad-uzayında çakışması engellenir.
- [x] **`translationCode = null` davranışı** — çeviri **es geçilir**, doğrudan `definition` kullanılır (§3 Adım 0). Çeviri **opt-in**'dir; anahtarı olmayan kayıt hiç sorgulanmaz.
- [x] **`translationCode` ad-uzayı kuralı (v0.18)** — anahtar **otomatik üretilmez** (`<varlık>.<code>` gibi bir şema yok); alan **opsiyoneldir**. Girilmezse Translation tablosuna gidilmez, `definition` kullanılır. Serbest metin; namespace kullanımı kullanıcının tercihidir (zorunlu değil).

---

## 6. Notlar / Ham Düşünceler
> _(Buraya ham düşünceler; sonra yukarı işlenir.)_

---

*Oluşturma: 2026-07-01.*
