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
| Alan | Tip | Zorunlu | Açıklama |
|---|---|---|---|
| `id` | int | Otomatik | Çeviri kaydı ID'si |
| `code` | string | Evet | Çeviri kodu — **eşleştirme anahtarı** (serbest metin; istenirse `form.submit` gibi namespace'lenebilir) |
| `organizationId` | string / null | Hayır | Sahibi organizasyon. **`null` = ortak (Flovo) çeviri.** |
| `tr` | string | — | Türkçe metin |
| `en` | string | — | İngilizce metin |
| `de` | string | — | Almanca metin |

> Aktif dile göre `tr` / `en` / `de` alanlarından biri döndürülür.

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

**Temel varsayım — `definition` = varsayılan dildeki metin:** Bir kaydın `definition` alanı, **organizasyonun
`defaultLang`** dilindeki metin kabul edilir (→ `organization.md`). Motor bunun üzerine kurulur:

- **Adım 1 — Kullanıcı dili = organizasyonun `defaultLang`'i:** `definition` zaten kullanıcının dilindedir →
  **translation tablosuna gidilmez**, doğrudan `definition` iletilir. _(varsayılan dildeki kullanıcıda sorgu maliyeti yok)_
- **Adım 2 — Diller farklı:** `definition` kullanıcının dilinde **değildir** → **`code` ile translation tablosuna**
  bakılır. Eşleşme **`code` + `organizationId` birlikte** yapılır:
  1. **`organizationId` && `code`** eşleşen kayıt varsa → **ilk hedef**, o alınır (organizasyon override'ı).
  2. Yoksa → **`organizationId = null` && `code`** (ortak/Flovo) kaydına düşülür.
- **Adım 3 — Fallback:** Translation eşleşmesi **yoksa** *veya* bulunan kaydın **istenen dildeki değeri boşsa** →
  translation kullanılmaz, **`definition`** iletilir.

```
resolveText(code, definition, organizationId, userLang, orgDefaultLang):
  # 1) Kullanıcı dili = organizasyonun varsayılan dili → definition zaten o dilde
  if (userLang == orgDefaultLang):
      return definition

  # 2) Diller farklı → translation tablosu (önce organizasyon, sonra ortak)
  t = find(x => x.code == code AND x.organizationId == organizationId)
  if (t == null):
      t = find(x => x.code == code AND x.organizationId == null)

  # 3) Kayıt yok VEYA istenen dildeki değer boş → definition'a düş
  if (t == null OR isEmpty(t[userLang])):
      return definition

  return t[userLang]   # tr | en | de
```

**Sonuç:** Varsayılan dildeki kullanıcı **hiç tabloya gitmez** (performans); farklı dildeki kullanıcı önce
**organizasyon** çevirisini, yoksa **ortak** çeviriyi görür; ikisi de yoksa/boşsa güvenle **`definition`**'a düşülür.

---

## 4. Benzersizlik & Kısıtlar
- **Bir organizasyonda aynı `code`'lu birden fazla çeviri olamaz** → `(organizationId, code)` **benzersiz**.
- Aynı şekilde **ortak tarafta da** aynı `code`'tan **tek** kayıt olur → `organizationId = null` + `code` benzersiz.
- Yani bir organizasyon, kendi içinde aynı koddan **çoğaltamaz**; ama bir **ortak (null) `code`** ile **aynı `code`'a
  sahip 1 kayıt** oluşturabilir (bu, o organizasyon için ortak kaydı **ezer**).

**Örnek** (`code = "form.submit"`):
| id | code | organizationId | tr | en | Kimin gördüğü |
|---|---|---|---|---|---|
| 1 | `form.submit` | `null` | Gönder | Submit | Kaydı olmayan **tüm** organizasyonlar (ortak) |
| 2 | `form.submit` | `org-42` | İlet | Send | **Yalnız `org-42`** (ortak kaydı ezer) |

`org-42` → "İlet/Send"; diğer tüm organizasyonlar → "Gönder/Submit".

---

## 5. Açık Kararlar / Sorular
- [x] **Dil seti sabit** — `tr`/`en`/`de` **sabit kolonlardır** (dinamik dil eklenmez); yeni dil, modele **kolon eklenerek** yapılır.
- [x] **Boş/eşleşmeyen davranışı** — istenen dildeki değer boşsa veya eşleşme yoksa **`definition`**'a düşülür (§3).
- [x] **`code` serbest metin** — kod **serbest**tir; kullanıcı isterse **namespace** (örn. `form.submit`) ile alanlar arası ayrım yapabilir (zorunlu değil).
- [ ] Ortak çeviri sonradan güncellenince, onu **ezmiş** organizasyon kayıtları etkilenmemeli — teyit.

---

## 6. Notlar / Ham Düşünceler
> _(Buraya ham düşünceler; sonra yukarı işlenir.)_

---

*Oluşturma: 2026-07-01.*
