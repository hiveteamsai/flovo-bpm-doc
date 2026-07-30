# Senaryolar — Masraf & Kredi Kartı Ekstresi (`expenseAndCreditCard`) — TASLAK

> **Durum:** 🟡 TASLAK — süreç örneğini **uçtan uca senaryolarla** detaylandırma dosyası. Her senaryo, 4 servis
> (Masraf Formu · Masraf · Ekstre · Ekstre Satırı) arasındaki **veri akışını, alanları, iş kurallarını ve tetikleyicileri**
> adım adım izler.
> **Servis grubu:** → [`index.md`](./index.md) · servis dökümanları: [`expenseForm.md`](./expenseForm.md) · [`expense.md`](./expense.md) ·
> [`creditCardStatement.md`](./creditCardStatement.md) · [`creditCardStatementLine.md`](./creditCardStatementLine.md).

## Temel davranış (senaryolar için ortak)
- **Kullanıcı ↔ ParentUser:** Masraf'taki **Kullanıcı** adımı, masraf **bir masraf formuyla ilişkilendirilmediğinde** durduğu
  (beklediği) insan-görev adımıdır. Masraf **bir masraf formuyla ilişkilendirildiğinde** instance **ParentUser** (Üst Form
  Kullanıcı) adımına ilerler ve **masraf formunun süreç adımına göre** davranır (atananlar/görünüm üst formdan).
- **Parent Kontrol:** `expenseFormId` alanı **dolu mu?** → **dolu** ise `true` → **ParentUser**; **boş** ise `false` → **Kullanıcı** (Taslak).
- **Masraf iki yoldan oluşur:** **(1)** masraf formundan **bağımsız** (ilişkilendirilmeden), **(2)** masraf formu **`expenses`
  Form List** üzerinden.
- **İlişkilendirilmemiş masraflar Taslak statüsünde tutulur** → "var olanlardan ekle" bunları listeler.

## Senaryo İndeksi
| # | Senaryo | Durum |
|---|---|---|
| 1 | **Bağımsız masraf oluşturma** (ilişkilendirmesiz) | 🟢 yazıldı |
| 2 | **Masraf formu Form List üzerinden oluşturma** | 🟢 yazıldı |
| 3 | **Var olan (Taslak) masrafı sonradan forma ekleme** | 🟢 yazıldı |
| 4 | **Ekstre kurulumu + Masraf ↔ Ekstre Satırı eşleştirme** (kaskad) | 🟢 yazıldı |
| 5 | **Formdan masraf çıkarma** (kaskad: ekstre satırı + ekstre tutarları) | 🟢 yazıldı |

---

## Senaryo 1 — Bağımsız Masraf Oluşturma

**Amaç:** Masrafın masraf formundan **bağımsız** (ilişkilendirilmeden) oluşturulması.
**Ön koşul:** Kullanıcı masrafı doğrudan başlatır (açık bir üst masraf formu yok).

| # | Aktör / Sistem | Ne olur | Servis · Adım |
|---|---|---|---|
| 1 | Kullanıcı | 3 başlatma aksiyonundan biri: **Fotoğraf çek** / **Dosya Seç** / **Belgesiz Form Oluştur** | Masraf · Başlangıç |
| 2 | Sistem | **Form Creator** masraf instance'ı üretir | Masraf · Form Creator |
| 3 | Sistem (belgeli) | **AI processing** → **AI** (alanları doldurur) → **Bildirim**; AI hatası → Bildirim → **Form Sil** | Masraf · AI processing / AI / Bildirim |
| 4 | Sistem | **Parent Kontrol:** `expenseFormId` **boş** (üst form yok) → **false** | Masraf · Parent Kontrol |
| 5 | Sistem | Masraf **Taslak** statüsünde **Kullanıcı** adımına ilerler; ilişkilendirilmemiş bekler | Masraf · Kullanıcı |

**Son durum:** Masraf **Taslak**, **Kullanıcı** adımında, hiçbir üst forma bağlı değil.

---

## Senaryo 2 — Masraf Formu Form List Üzerinden Oluşturma

**Amaç:** Masrafın, masraf formunun `expenses` Form List'i üzerinden oluşturulması ve doğrudan ParentUser'a ilerlemesi.
**Ön koşul:** Açık bir **Masraf Formu** instance'ı; kullanıcı `expenses` listesinden **yeni** masraf ekler.

| # | Aktör / Sistem | Ne olur | Servis · Adım |
|---|---|---|---|
| 1 | Kullanıcı | `expenses` Form List'inde 3 başlatma aksiyonundan biri | Masraf Formu · `expenses` → Masraf · Başlangıç |
| 2 | Sistem | **Form Creator** masraf instance'ı üretir; oluşturulduktan **sonra** expense, expenseForm'a Form List üzerinden bağlanır → **`AssociatedInstance` kaydı atılır** | Masraf · Form Creator + AssociatedInstance |
| 3 | Sistem | Kayıt atıldığı için masraf formundaki **`whenAddedAssociate`** trigger'ı tespit edilir → expense'in **Forma Ekle alt süreç başlangıcı** tetiklenir | Masraf Formu ServiceTrigger → Masraf · Forma Ekle Başlangıcı |
| 4 | Sistem | Alt süreçte **Status Kontrol** → masraf **henüz Kullanıcı adımında değil** → **false** → alt süreç **işlem yapmadan** sonlanır | Masraf · Forma Ekle alt süreç · Status Kontrol |
| 5 | Sistem | Bu esnada ana süreç **AI** adımına ilerler → AI biter → **Bildirim** → **Parent Kontrol** | Masraf · AI / Bildirim / Parent Kontrol |
| 6 | Sistem | **Parent Kontrol:** `expenseFormId` **dolu** (Form List üzerinden bağlandığı için parentProperty ile doldu) → **true** → **ParentUser** | Masraf · Parent Kontrol → ParentUser |

**Son durum:** Masraf **ParentUser** adımında (masraf formunun süreç adımına göre davranır); expenseForm'a bağlı.
**Not:** Forma Ekle alt süreci (adım 3-4) **erken** ateşlenir ama statü `false` olduğundan **hiçbir şey yapmaz**; ilerleme ana akıştaki Parent Kontrol ile olur.

---

## Senaryo 3 — Var Olan (Taslak) Masrafı Sonradan Forma Ekleme

**Amaç:** Senaryo 1'de oluşan **bağımsız (Taslak)** masrafın, sonradan masraf formuna **"var olanlardan ekle"** ile bağlanması.
**Ön koşul:** İlişkilendirilmemiş, **Taslak** statüsünde, Masraf'ın **Kullanıcı** adımında bekleyen masraf(lar).

| # | Aktör / Sistem | Ne olur | Servis · Adım |
|---|---|---|---|
| 1 | Kullanıcı | Masraf Formu'nda **"var olanlardan ekle"** — eklenebilir statü **Taslak** seçili olduğundan, ilişkilendirilmemiş (Kullanıcı adımındaki) masraflar listelenir → seçer | Masraf Formu · `expenses` (`addFromExistingStatusIds=[Taslak]`) |
| 2 | Sistem | Seçilen expense Form List'e eklenir → **`AssociatedInstance` kaydı atılır** | AssociatedInstance |
| 3 | Sistem | Kayıt atılırken masraf formundaki **Forma Ekleme trigger'ı** (`whenAddedAssociate`) tespit edilir → seçilen expense'in **Forma Ekle alt süreci** başlar | Masraf Formu ServiceTrigger → Masraf · Forma Ekle Başlangıcı |
| 4 | Sistem | Alt süreçte **Status Kontrol** → instance **Taslak** → **true** → **trigger süreç adımı** (`triggerProcessStep`) ile Kullanıcı adımındaki **Forma Ekle (webhook)** aksiyonu tetiklenir | Masraf · Forma Ekle alt süreç · Status Kontrol(true) → Forma Ekle aksiyon tetikleme |
| 5 | Sistem | Forma Ekle aksiyonu expense'i **Kullanıcı → ParentUser** adımına ilerletir | Masraf · Kullanıcı → ParentUser |

**Son durum:** Daha önce bağımsız olan masraf artık forma bağlı, **ParentUser** adımında.
**Senaryo 2 ile fark:** Sen-2'de masraf **yeni** oluşur ve **Parent Kontrol (true)** ile ParentUser'a gider; Sen-3'te **var olan taslak** masraf, **Forma Ekle alt süreci (Status=Taslak → true → triggerProcessStep)** ile Kullanıcı'dan ParentUser'a taşınır.

---

## Senaryo 4 — Ekstre Kurulumu ve Masraf ↔ Ekstre Satırı Eşleştirme (kaskad)

**Amaç:** Bir ekstrenin + satırlarının masraf formuna kurulması, **kimlik/veri yayılımı** (İK-2 → parentProperty →
`fillDataSource`) ve bir masrafın bir ekstre satırıyla **eşleştirilmesinin** ekstre satırı + ekstre tutarlarına kaskad etkisi.
**Ön koşul:** Masraf formu açık; içinde masraf(lar) ilişkilendirilmiş (Senaryo 2/3).

**Aşama A — Ekstre kurulumu + kimlik/veri yayılımı:**

| # | Aktör / Sistem | Ne olur | Servis · Adım / Kural |
|---|---|---|---|
| A1 | Kullanıcı | Masraf formuna **ekstre** eklenir | Masraf Formu · `creditCardStatement` (Form List) |
| A2 | Sistem | **İK-1** `enabled=false` (max 1 ekstre) · **İK-2** ekstrenin `creditCardStatementId` değeri masraf formundaki textbox'a **kopyalanır** | Masraf Formu · İK-1 / İK-2 |
| A3 | Kullanıcı | Ekstre içine **ekstre satırları** eklenir, `amount` girilir | Ekstre · `creditCardStatementLines` |
| A4 | Sistem | Masraf formuyla ilişkili masrafların `creditCardStatementId`'si **parentProperty** ile masraf formundan **beslenir/dolar** | Masraf · `creditCardStatementId` (parentProperty) |
| A5 | Sistem | Masraf içinde **`matchedStatementLineDoldurma`** (`fillDataSource`): `creditCardStatementId` eşit **ve** `used==false` satırlar `matchedStatementLine` combobox'ına dolar → **seçilebilir** | Masraf · İş kuralı |

**Aşama B — Eşleştirme (kaskad):**

| # | Aktör / Sistem | Ne olur | Servis · Adım |
|---|---|---|---|
| B1 | Kullanıcı | Masraf üzerinden bir **ekstre satırı seçilir** (`matchedStatementLine`) → **`AssociatedInstance` kaydı atılır** | Masraf · `matchedStatementLine` + AssociatedInstance |
| B2 | Sistem | Masraf'ın **`whenAddedAssociate`** trigger'ı (`targetPropertyId=matchedStatementLine`) → **Ekstre Satırı'nın Masraf İlişkilendirme alt süreci** tetiklenir | Masraf ServiceTrigger → Ekstre Satırı · Masraf İlişkilendirme Başlangıcı |
| B3 | Sistem | Alt süreçte **ilk** "Ekstre Tutar Alt süreç Başlat" (`triggerProcessStep`) → ilişkili **Ekstre**'nin **Tutar Başlangıcı** alt süreci tetiklenir → ekstre verileri **expense'ten gelen parametrelerle** güncellenir | Ekstre Satırı → Ekstre · Tutar Başlangıcı |
| B4 | Sistem | **Sonra** Ekstre Satırı instance'ının verileri güncellenir (`expenseIds`, `usedAmount`, `remainingAmount`, `used`) | Ekstre Satırı · değer atama adımları |

**Son durum:** Masraf bir ekstre satırıyla **eşleşti**; ekstre satırının `used`/tutar alanları güncellendi; ekstre toplamları
(`totalAmount`/`remainingAmount`/`usedAmount`) yeniden hesaplandı. _(Fill kuralı `matchedStatementLineDoldurma` **`used == false`** filtreler →
satır **tümüyle kullanıldığında** (`used == true`, yani `remainingAmount == 0`) başka masrafın listesinden düşer; **kısmen kullanılmış**
(`used == false`) satır ise hâlâ seçilebilir.)_
**Simetri:** Bu senaryo **eşleştirme** (association ekleme); **Senaryo 5** aynı zincirin **çözülmesidir** (association kaldırma).

---

## Senaryo 5 — Formdan Masraf Çıkarma (kaskad)

**Amaç:** Form List'ten bir masrafın çıkarılması ve bunun **ekstre satırı + ekstre tutarlarına** kaskad etkisi.
**Ön koşul:** Forma bağlı (**ParentUser**'da), bir **Ekstre Satırı** ile eşleşmiş (`matchedStatementLine` dolu) masraf — **Senaryo 4'ün sonucu**.

| # | Aktör / Sistem | Ne olur | Servis · Adım |
|---|---|---|---|
| 1 | Kullanıcı | Masraf formundaki Form List'ten bir masrafı **siler** → **`AssociatedInstance` kaydı silinir** | Masraf Formu · `expenses` |
| 2 | Sistem | Masraf formu servisindeki **`whenRemoveAssociate`** trigger'ı çalışır → silinecek instance'ın **Formdan Çıkart alt süreci** tetiklenir | Masraf Formu ServiceTrigger → Masraf · Formdan Çıkart Başlangıcı |
| 3 | Sistem | Alt süreçte **trigger süreç adımı** (`triggerProcessStep`) ile ParentUser'daki **Formdan Çıkart** aksiyonu tetiklenir → expense **ParentUser → Kullanıcı** (Taslak) | Masraf · ParentUser · Formdan Çıkart |
| 4 | Sistem | **değerAtama** adımı ile expense'in **`matchedStatementLine`** alanındaki değer **silinir** (görselde "Ekstre Satırı Kaldır") | Masraf · Formdan Çıkart alt süreç · değerAtama |
| 5 | Sistem | `matchedStatementLine`'dan değer silinince expense ↔ Ekstre Satırı **`AssociatedInstance` kaldırılır** | AssociatedInstance (silme) |
| 6 | Sistem | Kaldırma esnasında Masraf'ın **`whenRemoveAssociate`** trigger'ı (`targetPropertyId=matchedStatementLine`) → **Ekstre Satırı'nın Masraf İlişki Kaldırma başlangıcı** tetiklenir | Masraf ServiceTrigger → Ekstre Satırı · Masraf İlişki Kaldırma Başlangıcı |
| 7 | Sistem | Ekstre Satırı alt sürecinde **trigger süreç adımı** ("Ekstre Tutar Alt süreç Başlat") ile ilişkili **Ekstre**'nin **Tutar Başlangıcı** alt süreci tetiklenir → ekstre verileri, **expense'ten parametre olarak gelen verilerle** güncellenir | Ekstre Satırı → Ekstre · Tutar Başlangıcı |
| 8 | Sistem | Ardından **Ekstre Satırı** instance'ının değerleri güncellenir | Ekstre Satırı · değer atama adımları |

**Son durum:** Masraf formdan çıkarıldı (**Taslak**, Kullanıcı'da); expense ↔ Ekstre Satırı ilişkisi çözüldü; **Ekstre Satırı** serbest/güncellendi; **Ekstre** tutarları yeniden hesaplandı.

---

## Açık noktalar (senaryolardan)
- **`değerAtama` ↔ "Ekstre Satırı Kaldır" adı:** expense Formdan Çıkart alt sürecindeki adımın tek adı netleştirilecek.
- **Parametre içeriği (adım 7):** expense'ten Ekstre Satırı → Ekstre'ye aktarılan `expenseId`/`amount`'ın Tutar alt sürecinde tam kullanımı.
- **İsim setleri (netleşti):** Masraf'ın kendi alt süreçleri **Forma Ekle / Formdan Çıkart Başlangıcı**; Ekstre Satırı'nınkiler **Masraf İlişkilendirme / Masraf İlişki Kaldırma Başlangıcı** — iki ayrı çift (→ [`creditCardStatementLine.md`](./creditCardStatementLine.md)).

*Oluşturma: 2026-07-29.*
