# Örnek Süreç — Masraf (`expense`) — TASLAK

> **Durum:** 🟡 TASLAK — görselden ilk çıkarım (diyagram + aksiyon/trigger taslağı). Detay sonra eklenecek.
> **Servis grubu:** `expenseAndCreditCard` (4 bağlantılı servis) → [`index.md`](./index.md)
> **Görsel:** `expense.jpg`
> **Amaç:** Tek bir **masraf** kaydının yaşam döngüsü. Masraf **3 yolla** oluşturulur (fotoğraf/dosya/belgesiz);
> belgeli yolda **Flovo AI** ile taranır. **Parent Kontrol** ile masrafın bir üst forma bağlı olup olmadığına göre
> **ParentUser** (üst formun kullanıcısı) veya bağımsız **Kullanıcı** akışına ayrılır. Masraf bir **Ekstre Satırı** ile
> ilişkilendirilince/ayrılınca **ServiceTrigger** ile Ekstre Satırı alt süreçleri tetiklenir.

## Ana Süreç Diyagramı
```mermaid
flowchart LR
  start(["Başlangıç"])
  fc1["Form Creater"]
  fc2["Form Creater (belgesiz)"]
  proc["AI processing (Processing)"]
  ai["AI (Flovo AI)"]
  n1["Bildirim gönder (toast)"]
  n2["Bildirim gönder (toast)"]
  del["Form Sil (Instance Deleter)"]
  pc{"Parent Kontrol"}
  user["Kullanıcı"]
  puser["ParentUser"]
  son(["Süreç Bitişi"])

  start -->|"Fotoğraf çek (takePhoto)"| fc1
  start -->|"Dosya Seç (selectFile)"| fc1
  start -->|"Belgesiz Form Oluştur (manual)"| fc2
  fc1 -->|"default"| proc
  proc -->|"default"| ai
  ai -->|"default"| n1
  ai -->|"onFail"| n2
  n2 -->|"default"| del
  n1 -->|"default"| pc
  fc2 -->|"default"| pc
  pc -->|"true / Forma Eklendi"| puser
  pc -->|"false / Taslak"| user
  user -->|"Kaydet (manual)"| user
  user -->|"Forma Ekle (webhook)"| puser
  puser -->|"Kaydet (manual)"| puser
  puser -->|"Formdan Çıkart (webhook)"| user
  puser -->|"Tamamlandı (webhook)"| son
```

## Alt Süreçler
**Forma ekleme** (`subProcessStart` → Status Kontrol → aksiyon tetikleme):
```mermaid
flowchart LR
  s1(["Forme Ekleme Başlangıcı"])
  sc{"Status Kontrol"}
  t1["Forma Ekle aksiyon tetikleme (triggerProcessStep)"]
  e1(["Bitiş"])

  s1 -->|"default"| sc
  sc -->|"true"| t1
  t1 --> e1
  sc -->|"false"| e1
```

**Formdan çıkarma** (`subProcessStart` → aksiyon tetikleme → Ekstre Satırı Kaldır):
```mermaid
flowchart LR
  s2(["Formdan çıkart Başlangıcı"])
  t2["Formdan Çıkart aksiyon tetikleme (triggerProcessStep)"]
  rm["Ekstre Satırı Kaldır"]
  e2(["Bitiş"])

  s2 -->|"default"| t2
  t2 -->|"default"| rm
  rm -->|"default"| e2
```

## Süreç adımları (taslak)
| # | Adım | Tip | Rol |
|---|---|---|---|
| 1 | Başlangıç | Süreç Başlangıcı | 3 başlatma: `takePhoto` / `selectFile` / belgesiz `manual` |
| 2 | Form Creater | Instance Creator | Masraf instance'ı üretir (belgeli/belgesiz iki dal) |
| 3 | AI processing | Processing | Belge taranırken "yükleniyor" gösterimi |
| 4 | AI | Flovo AI | Masraf belgesini tarayıp alanları doldurur |
| 5 | Bildirim gönder | Bildirim (toast) | Sonuç/hata bildirimi |
| 6 | Form Sil | Instance Deleter | AI hatasında yarım formu siler (telafi) |
| 7 | Parent Kontrol | Karşılaştırma | **`expenseFormId` dolu mu?** → dolu: `true` → ParentUser · boş: `false` → Kullanıcı (Taslak) |
| 8 | Kullanıcı | Kullanıcı (human task) | Masraf **bir masraf formuyla ilişkilendirilmediğinde** durduğu adım (Taslak); kaydeder / forma ekler |
| 9 | ParentUser | **Üst Form Kullanıcı** (human task) | Masraf **bir masraf formuyla ilişkilendirildiğinde** ilerlediği adım; **masraf formunun süreç adımına göre** davranır (atananlar/görünüm üst formdan) |
| — | Süreç Bitişi | Süreç Bitişi | — |

## Aksiyonlar (taslak)
| Kaynak adım | Aksiyon | actionType | Hedef adım | Not |
|---|---|---|---|---|
| Başlangıç | Fotoğraf çek | `takePhoto` | Form Creater | belgeli |
| Başlangıç | Dosya Seç | `selectFile` | Form Creater | belgeli |
| Başlangıç | Belgesiz Form Oluştur | `manual` | Form Creater (belgesiz) | belgesiz |
| Form Creater | default | `autoAction` | AI processing / Parent Kontrol | belgeli → AI; belgesiz → Parent Kontrol |
| AI processing | default | `autoAction` | AI | — |
| AI | default | `autoAction` | Bildirim gönder | başarı |
| AI | onFail | `autoAction` | Bildirim gönder → Form Sil | hata telafi |
| Bildirim gönder | default | `autoAction` | Parent Kontrol | — |
| Parent Kontrol | true | (comparison) | ParentUser | durum: Forma Eklendi |
| Parent Kontrol | false | (comparison) | Kullanıcı | durum: Taslak |
| Kullanıcı | Kaydet | `manual` | Kullanıcı (self) | — |
| Kullanıcı | Forma Ekle | `webhook` | ParentUser | — |
| ParentUser | Kaydet | `manual` | ParentUser (self) | — |
| ParentUser | Formdan Çıkart | `webhook` | Kullanıcı | durum: Taslak |
| ParentUser | Tamamlandı | `webhook` | Süreç Bitişi | — |

## Önemli Alanlar (properties)
| Alan (`code`) | Tip | Açıklama |
|---|---|---|
| `amount` | Numeric | Masraf tutarı. |
| `expenseId` | **flowInfo → instanceId** | Masrafın kimliği = kendi `instanceId`'si (akış bilgisinden; salt-okunur). |
| `expenseFormId` | **parentProperty** → Masraf Formu (`expenseForm`).`expenses` | Masraf'ı `expenses` listesinde tutan **Masraf Formu**'nun `expenseFormId` değerini **kopyalar** → masrafın **hangi masraf formuna** ait olduğunu belirler. |
| `creditCardStatementId` | **parentProperty** → Masraf Formu (`expenseForm`).`expenses` | Masraf'ı `expenses` listesinde tutan **Masraf Formu**'ndan `creditCardStatementId` değerini **kopyalar** → masrafın **hangi ekstreye ait** olduğunu belirler. |
| `creditCardStateLine` | **Combobox** — `isAssociatedCombobox = true`, `associatedServiceId = creditCardStatementLine` | Masrafı bir **Ekstre Satırı** ile eşleştirir. Seçim **association** kurar → **ServiceTrigger'ı tetikler** (bkz. `targetPropertyId`). Seçenekleri iş kuralı `crediCardStatementLineDoldurma` doldurur. |

## İş Kuralları (business rules)
> Model → [`../../models/service-settings/business-rule.md`](../../models/service-settings/business-rule.md). Frontend'de çalışır (realtime).

| Kural (`code`) | Hedef | businessRuleActionType | Davranış |
|---|---|---|---|
| `crediCardStatementLineDoldurma` | `creditCardStateLine` (veri kaynağı) | `fillDataSource` | `creditCardStatementLine` (Ekstre Satırı) instance'larından **`creditCardStatementId` bu forma eşit** **ve** **`used == false (0)`** olanları `creditCardStateLine` combobox'ının **veri kaynağına** doldurur → yalnız **aynı ekstreye ait, henüz kullanılmamış** satırlar seçilebilir. |

## ServiceTrigger (otomatik tetikleyiciler)
> Masraf, **`creditCardStateLine`** alanıyla (`isAssociatedCombobox=true`) bir **Ekstre Satırı** seçilince/kaldırılınca tetiklenir;
> izlenen alan **`targetPropertyId = creditCardStateLine`**. Hedef **Ekstre Satırı** servisinin alt süreç başlangıcı çalışır.

| serviceTriggerType | targetService | targetPropertyId | targetProcessStarter (`subProcessStart`) | async | parameters |
|---|---|---|---|---|---|
| `whenAddedAssociate` | Ekstre Satırı | `creditCardStateLine` | Forma Ekle Başlangıcı | `false` | `expenseId`, `amount` |
| `whenRemoveAssociate` | Ekstre Satırı | `creditCardStateLine` | Formdan Kaldırma Başlangıcı | `true` | `expenseId`, `amount` |

## Notlar / açık noktalar
- **ParentUser** adımı = **Üst Form Kullanıcı** (§3.22) — masrafın üst formundan (Masraf Formu) atananları/görünümü devralır.
- **Forma Ekle aksiyon tetikleme** / **Formdan Çıkart aksiyon tetikleme** = `triggerProcessStep` (alt süreç içinde).
- **Ekstre Satırı Kaldır** adımının tipi/davranışı sonra netleşecek (Ekstre Satırı ilişki temizliği).
- Masraf'ın trigger'ı **Ekstre Satırı**'nı hedefler; oradaki başlangıç adları görselde **"Masraf İlişkilendirme/İlişki Kaldırma
  Başlangıcı"** — **isim uyumlaması** gerekiyor (→ [`creditCardStatementLine.md`](./creditCardStatementLine.md), açık nokta).
- `whenRemoveAssociate` **async=true** (çıkarmada beklenmez); `whenAddedAssociate` **async=false** (eklemede beklenir).
- **İlişki yönü / döngü:** ilişkiyi kuran **tek taraf** Masraf'tır — `creditCardStateLine` **`isAssociatedCombobox=true`**
  (association + trigger). Karşı taraf **Ekstre Satırı.`expenseIds`** `isAssociatedCombobox=false` (bilgi amaçlı, geri-association
  kurmaz) → **A→B→A döngüsü oluşmaz** (→ [`creditCardStatementLine.md`](./creditCardStatementLine.md)).
- **parentProperty hedefi (`creditCardStatementId` · `expenseFormId`):** `expenses` Form List'i **Masraf Formu (`expenseForm`)**
  servisinde olduğundan üst form = **Masraf Formu**'dur. _(Kullanıcı "expense" olarak belirtti; `expenses` listesi expenseForm'da olduğundan üst = expenseForm.)_
- **`flowInfo` / `parentProperty` alan tipleri (açık):** `expenseId` (flowInfo) · `expenseFormId` + `creditCardStatementId`
  (parentProperty) — **PropertyType** listesinde karşılıkları teyit edilecek → [`../../models/enums/property-type.md`](../../models/enums/property-type.md).

*Oluşturma: 2026-07-29.*
