# Örnek Süreç — Ekstre Satırı (`creditCardStatementLine`) — TASLAK

> **Durum:** 🟡 TASLAK — görselden ilk çıkarım (diyagram + aksiyon/trigger taslağı). Detay sonra eklenecek.
> **Servis grubu:** `expenseAndCreditCard` (4 bağlantılı servis) → [`index.md`](./index.md)
> **Görsel:** `creditCardStatementLine.jpg`
> **Amaç:** Bir **kredi kartı ekstresinin tek satırı**. Her satır bir **Masraf** ile ilişkilendirilebilir; ilişki
> kurulunca/kaldırılınca satırın **masraf formu id / kalan tutar / kullanılan tutar / kullanıldı mı** alanları güncellenir
> ve üst **Ekstre**'nin tutar alt süreci tetiklenir. Böylece ekstre satırının bir masrafla eşleşip eşleşmediği (kullanıldı mı) izlenir.

## Ana Süreç Diyagramı
```mermaid
flowchart LR
  start(["Başlangıç"])
  fc["Form Creater (Instance Creator)"]
  puser["ParentUser"]
  chk{"Kullanıldı mı Kontrol"}
  son(["Süreç Bitişi"])

  start -->|"satır oluştur (manual · invisible)"| fc
  fc -->|"default"| puser
  puser -->|"onayla (webhook)"| chk
  chk -->|"true / Tamamlandı"| son
  chk -->|"false / Masraf Girişi Yapılmadı"| son
```

## Alt Süreçler
**Masraf ilişkilendirme** (`subProcessStart`):
```mermaid
flowchart LR
  s1([Masraf İlişkilendirme Başlangıcı]) -->|default| b1[Ekstre Tutar Alt süreç Başlat · triggerProcessStep]
  b1 -->|default| id1[masraf formu id atama · valueAssignment]
  id1 -->|default| k1[kalan tutar atama]
  k1 -->|default| ku1[kullanılan tutar atama]
  ku1 -->|default| u1[Kullanıldı mı atama]
  u1 -->|default| e1([Bitiş])
```

**Masraf ilişki kaldırma** (`subProcessStart`):
```mermaid
flowchart LR
  s2([Masraf İlişki Kaldırma Başlangıcı]) -->|default| b2[Ekstre Tutar Alt süreç Başlat · triggerProcessStep]
  b2 -->|default| id2[masraf formu id Kaldırma · valueAssignment]
  id2 -->|default| k2[kalan tutar atama]
  k2 -->|default| ku2[kullanılan tutar atama]
  ku2 -->|default| u2[Kullanıldı mı atama]
  u2 -->|default| e2([Bitiş])
```

## Süreç adımları (taslak)
| # | Adım | Tip | Rol |
|---|---|---|---|
| 1 | Başlangıç | Süreç Başlangıcı | Tek aksiyon: **satır oluştur** (`manual`, **displayType=invisible**) — bağımsız başlatılamaz; yalnız Ekstre'nin `creditCardStatementLines` Form List'i üzerinden oluşur |
| 2 | Form Creater | Instance Creator | Ekstre satırı instance'ı üretir |
| 3 | ParentUser | **Üst Form Kullanıcı** (human task) | Üst Ekstre kullanıcısı; onaylar |
| 4 | Kullanıldı mı Kontrol | Karşılaştırma | Satır bir masrafla eşleşti mi? |
| — | Süreç Bitişi | Süreç Bitişi | true → Tamamlandı · false → Masraf Girişi Yapılmadı |
| — | Masraf İlişkilendirme Başlangıcı | **Alt Süreç Başlangıcı** (`subProcessStart`) | Masraf bağlanınca çalışır |
| — | Masraf İlişki Kaldırma Başlangıcı | **Alt Süreç Başlangıcı** (`subProcessStart`) | Masraf bağlantısı kalkınca çalışır |
| — | Ekstre Tutar Alt süreç Başlat | **triggerProcessStep** | Üst **Ekstre**'nin Tutar alt sürecini tetikler |
| — | masraf formu id atama / Kaldırma | Değer Atama | Satıra bağlı masraf formu id'sini set/temizle |
| — | kalan / kullanılan tutar atama | Değer Atama | Satır tutar alanlarını günceller |
| — | Kullanıldı mı atama | Değer Atama | Satırın "kullanıldı" bayrağını set eder |

## Aksiyonlar (taslak)
| Kaynak adım | Aksiyon | actionType | Hedef adım | Durum |
|---|---|---|---|---|
| Başlangıç | **satır oluştur** | `manual` · **actionDisplayType: `invisible`** | Form Creater | — |
| Form Creater | default | `autoAction` | ParentUser | — |
| ParentUser | onayla | `webhook` | Kullanıldı mı Kontrol | — |
| Kullanıldı mı Kontrol | true | (comparison) | Süreç Bitişi | Tamamlandı |
| Kullanıldı mı Kontrol | false | (comparison) | Süreç Bitişi | Masraf Girişi Yapılmadı |
| (alt süreç adımları) | default | `autoAction` | sıradaki adım | — |

## Önemli Alanlar (properties)
> **Kural:** Bu serviste **yalnız `amount` enable/düzenlenebilir**; diğer alanlar **iş kuralları + süreç adımlarıyla** doldurulur.

| Alan (`code`) | Tip | Enable | Açıklama |
|---|---|---|---|
| `amount` | Numeric | ✅ | Satır tutarı — **tek düzenlenebilir alan** (kullanıcı girer). |
| `remaningAmount` | Numeric | ❌ | `amount - usedAmount` (iş kuralı `remaningAmountAtama`). |
| `usedAmount` | Numeric | ❌ | Kullanılan tutar — süreç adımı/iş kuralıyla atanır. |
| `used` | Checkbox | ❌ | `remaningAmount == 0` (iş kuralı `usedAtama`). |
| `expenseIds` | MultiselectCombobox → **Masraf (`expense`)** | ❌ | İlişkili **masraf (`expense`) instance'larının** id'leri — **yalnız bilgi amaçlı**. **`isAssociatedCombobox = false`** → `AssociatedInstance` kaydı **oluşturmaz**; böylece **Masraf ↔ Ekstre Satırı döngüsü** (A→B→A) **önlenir**. |
| `creditCardStatementId` | **parentProperty** → Ekstre.`creditCardStatementLines` | ❌ | Üst formdan — bu satırı `creditCardStatementLines` listesinde tutan **Ekstre**'den — **`creditCardStatementId` değerini kopyalar**; satırı ait olduğu ekstreye bağlar. |

## İş Kuralları (business rules)
> Model → [`../../models/service-settings/business-rule.md`](../../models/service-settings/business-rule.md). Frontend'de çalışır (realtime).

| Kural (`code`) | Hedef alan | Kaynak | businessRuleActionType | Davranış |
|---|---|---|---|---|
| `remaningAmountAtama` | `remaningAmount` | `amount - usedAmount` | `assignValueToProperty` (`fromCalculation`) | Kalan tutar = tutar − kullanılan. |
| `usedAtama` | `used` | `remaningAmount == 0` | `assignValueToProperty` (`fromCalculation`) | Kalan tutar 0 ise **`used = true`** (satır tümüyle kullanıldı). |

## ServiceTrigger (otomatik tetikleyiciler)
- Bu servis görselinde **ayrı ServiceTrigger tablosu yok**. Ekstre Satırı'nın alt süreçleri (**Masraf İlişkilendirme /
  İlişki Kaldırma Başlangıcı**), **Masraf** servisinin ServiceTrigger'ları ile tetiklenir (→ [`expense.md`](./expense.md)).

## Notlar / açık noktalar
- **Satır bağımsız oluşturulamaz:** Başlangıç aksiyonu **satır oluştur** (`manual`), **`actionDisplayType = invisible`**
  olduğundan "aksiyon bekleyenler"de **görünmez** — satır doğrudan başlatılamaz; **yalnız Ekstre'nin `creditCardStatementLines`
  Form List'i** üzerinden (yeni instance olarak) oluşturulur.
- **İsim uyumlaması (açık):** Masraf'ın trigger tablosu hedef başlangıçları **"Forma Ekle Başlangıcı" / "Formdan Kaldırma
  Başlangıcı"** olarak anıyor; bu servisteki karşılıklar görselde **"Masraf İlişkilendirme Başlangıcı" / "Masraf İlişki
  Kaldırma Başlangıcı"**. Tek isim setine indirgenmeli.
- **Ekstre Tutar Alt süreç Başlat** = `triggerProcessStep`; üst **Ekstre** servisinin **Tutar Başlangıcı** alt sürecini
  (kalan/kullanılan tutar) tetikler (→ [`creditCardStatement.md`](./creditCardStatement.md)).
- `false → Masraf Girişi Yapılmadı` kolu görselde Süreç Bitişi'ne ulaşıyor (farklı durumla); "geri dönüş mü, bitiş mi"
  sonra netleşecek.
- **Döngü önleme (tasarım deseni):** `expenseIds` **`isAssociatedCombobox = false`** olduğundan, Ekstre Satırı masraf(lar)ın
  id'sini **bilgi olarak** tutar ama **geri association kurmaz** → Masraf'ın ServiceTrigger'ı yeniden ateşlenmez, **A→B→A döngüsü
  oluşmaz**. _(ServiceTrigger "döngü koruması" açık maddesinin tasarım-zamanı örneği → [`../../models/service-settings/service-trigger.md`](../../models/service-settings/service-trigger.md).)_
- `expenseIds` alanı, alt süreçteki **"masraf formu id atama / Kaldırma"** adımlarıyla set/temizlenir.
- **`parentProperty` / `flowInfo` alan tipleri (açık):** `creditCardStatementId` (**parentProperty** — üst formdan değer kopyalar)
  ve Ekstre'deki `creditCardStatementId` (**flowInfo**) gibi özel alan tiplerinin **PropertyType** listesinde karşılığı teyit edilecek
  → [`../../models/enums/property-type.md`](../../models/enums/property-type.md). _(Parent Property, todo'da da açık: `process-step §4`.)_
- İlişki: **Masraf → (association) → Ekstre Satırı → (içinde) → Ekstre**.

*Oluşturma: 2026-07-29.*
