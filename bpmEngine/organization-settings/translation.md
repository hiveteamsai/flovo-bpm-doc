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
metin göstermek gerektiğinde, ilgili **`code`** çeviri tablosundan çözülür ve **aktif dile** göre metin döndürülür.

İki tür çeviri vardır:
- **Ortak (global) çeviriler** — `organizationId = null`. **Flovo (Coden)** tarafından oluşturulur; **tüm
  organizasyonlar görüntüleyip kullanabilir**, fakat **güncelleyemez** (salt-okunur).
- **Organizasyon çevirileri** — `organizationId = <org>`. İlgili organizasyon **kendi çevirilerini** oluşturur ve
  **yalnız kendi kayıtlarını** güncelleyebilir.

---

## 1. Çeviri Veri Modeli
Her **dil için ayrı kayıt** tutulur (kolon-başına-dil değil, **kayıt-başına-dil**).

| Alan | Tip | Zorunlu | Açıklama |
|---|---|---|---|
| `id` | int | Otomatik | Çeviri kaydı ID'si |
| `code` | string | Evet | Çeviri kodu — **eşleştirme anahtarı** (serbest metin; istenirse `form.submit` gibi namespace'lenebilir) |
| `organizationId` | int / null | Hayır | Sahibi organizasyon (FK → `organization.md` `id`). **`null` = ortak (Flovo) çeviri.** |
| `languageCode` | string | Evet | **Dil kodu** — sabit dil seti (`tr` / `en` / `de`) içinden (krş. `organization.defaultLang`) |
| `definition` | string | Evet | Bu **dildeki metin** (`languageCode` dilinde) |

> Bir `code`'un her dili **ayrı satırdır**; aktif dile (`languageCode = userLang`) uyan kaydın `definition`'ı döndürülür.
> Yeni dil eklemek artık **şema (kolon) değişikliği değil**, yeni **kayıt** eklemektir.

---

## 2. Sahiplik & Yetki (kim neyi güncelleyebilir?)
| Kayıt | `organizationId` | Kim oluşturur | Kim görüntüler | Kim günceller |
|---|---|---|---|---|
| **Ortak (global)** | `null` | Flovo (Coden) | Herkes | **Yalnız Flovo** — organizasyonlar **güncelleyemez** |
| **Organizasyon** | `<org>` | O organizasyon | O organizasyon | **Yalnız o organizasyon** (kendi `organizationId`'si) |

- Bir organizasyon, **başka bir organizasyonun** veya **ortak (null)** kayıtları **güncelleyemez**.
- Organizasyon, ortak bir `code`'u beğenmezse **aynı `code` ile kendi kaydını oluşturarak ezer** (override → §3).

---

## 3. Çeviri Motoru (Çözümleme / Resolution)
Frontende **`code` + `definition` içeren** veriler (property label, seçili combobox metni, durum/aksiyon tanımı vb.)
iletilirken metin aşağıdaki gibi çözülür.

**Temel varsayım — kaynak `definition` = varsayılan dildeki metin:** Kaynak kaydın (property/durum/aksiyon)
`definition` alanı, **organizasyonun `defaultLang`** dilindeki metin kabul edilir (→ `organization.md`). Diğer diller
`Translation` kayıtlarında (`languageCode` + `definition`) tutulur. Motor bunun üzerine kurulur:

- **Adım 1 — Kullanıcı dili = organizasyonun `defaultLang`'i:** `definition` zaten kullanıcının dilindedir →
  **translation tablosuna gidilmez**, doğrudan `definition` iletilir. _(varsayılan dildeki kullanıcıda sorgu maliyeti yok)_
- **Adım 2 — Diller farklı:** kaynak `definition` kullanıcının dilinde **değildir** → **`code` ile translation
  tablosuna** bakılır. Eşleşme **`code` + `languageCode`(=userLang) + `organizationId` birlikte** yapılır:
  1. **`organizationId` && `code` && `languageCode`** eşleşen kayıt varsa → **ilk hedef** (organizasyon override'ı).
  2. Yoksa → **`organizationId = null` && `code` && `languageCode`** (ortak/Flovo) kaydına düşülür.
- **Adım 3 — Fallback:** Eşleşme **yoksa** *veya* bulunan kaydın **`definition`'ı boşsa** → translation kullanılmaz,
  kaynak **`definition`** iletilir.

```
resolveText(code, sourceDefinition, organizationId, userLang, orgDefaultLang):
  # 1) Kullanıcı dili = organizasyonun varsayılan dili → kaynak definition zaten o dilde
  if (userLang == orgDefaultLang):
      return sourceDefinition

  # 2) Diller farklı → translation tablosu; dil = userLang (önce organizasyon, sonra ortak)
  t = find(x => x.code == code AND x.languageCode == userLang AND x.organizationId == organizationId)
  if (t == null):
      t = find(x => x.code == code AND x.languageCode == userLang AND x.organizationId == null)

  # 3) Kayıt yok VEYA metin boş → kaynak definition'a düş
  if (t == null OR isEmpty(t.definition)):
      return sourceDefinition

  return t.definition   # languageCode = userLang dilindeki metin
```

**Sonuç:** Varsayılan dildeki kullanıcı **hiç tabloya gitmez** (performans); farklı dildeki kullanıcı önce
**organizasyon** çevirisini, yoksa **ortak** çeviriyi görür; ikisi de yoksa/boşsa güvenle **`definition`**'a düşülür.

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
- [x] **Dil seti** — `languageCode` **sabit set** (`tr`/`en`/`de`) içinden (krş. `organization.defaultLang`). Model **kayıt-başına-dil** olduğu için yeni dil **kolon değil kayıt** ekler (şema değişmez).
- [x] **Boş/eşleşmeyen davranışı** — istenen dildeki değer boşsa veya eşleşme yoksa **`definition`**'a düşülür (§3).
- [x] **`code` serbest metin** — kod **serbest**tir; kullanıcı isterse **namespace** (örn. `form.submit`) ile alanlar arası ayrım yapabilir (zorunlu değil).
- [ ] Ortak çeviri sonradan güncellenince, onu **ezmiş** organizasyon kayıtları etkilenmemeli — teyit.

---

## 6. Notlar / Ham Düşünceler
> _(Buraya ham düşünceler; sonra yukarı işlenir.)_

---

*Oluşturma: 2026-07-01.*
