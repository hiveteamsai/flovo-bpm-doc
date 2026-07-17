# Ayar Değişiklik Logu (Settings Logs) — Tasarım

> **Durum:** 🟡 **PLAN — karara bağlanacak.** Henüz `models/`'e işlenmedi; onaylanınca model + enum + davranış
> dokümanlarına dağıtılacak (→ [`index.md`](./index.md)).
> **Amaç:** Ayar sayfalarında yapılan **ekleme / güncelleme / silme** ve **toplu güncelleme** işlemlerinin,
> **sayfa bazında** görüntülenebilen bir **denetim izi** olarak tutulması.
> **Kapsam:** Yalnız **ayar değişiklikleri** — organizasyon ayarları + servis ayarları.
> **Beslediği açık madde:** [`../../todo.md`](../../todo.md) **Tier 1** — "Denetim izi (audit) / loglama" → **ayar
> değişiklik logları**. Açık sorular **yalnız `todo.md`**'de tutulur; §5 bu dokümanın **kendi girdi listesi**dir.

---

## 1. Kayıtlar nasıl tutulur?

**Tek generic tablo (`SettingsLog`) + JSONB delta**, uygulama katmanında yazılır.

| İlke | Kural |
|---|---|
| **Log birimi = sayfa (aggregate root)**, tablo değil | Bir "Kaydet" → **bir log kaydı**. Alt varlıklar (Staff, QualificationItem, üyeler, takvim günleri…) ana kaydın `changes`'ı içinde gömülü gelir — kendi satırlarını açmaz. |
| **Niyet yazılır, fiziksel işlem değil** | Silme fizikselde `deleted=true` (bir UPDATE); log bunu **`delete`** olarak yazar. `active=false` ise gerçek bir **`update`**'tir. Bu ayrımı yalnız uygulama katmanı bilebilir — bu yüzden log DB trigger'ı ile değil, **uygulama katmanında** yazılır. |
| **Aynı transaction** | Log satırı, ayar değişikliğiyle **aynı transaction'da** (aynı PostgreSQL) yazılır → "değişiklik var ama log yok" durumu imkânsız. NATS/outbox yalnız **downstream** tüketiciler (arşiv/SIEM) içindir; denetim kaydı async teslimata bağlanmaz. |
| **Append-only** | UPDATE/DELETE **yok**. Log bir projeksiyon değil, **hukuki kayıttır**. |
| **Değişmeyen kayıt log üretmez** | Yazma katmanı eski↔yeni karşılaştırması yapar; no-op **hiçbir şey yazmaz**. (Toplu senkronda hacmi bu kural sınırlar.) |
| **Görünen metin snapshot'lanır** | FK'lerin ve kaydın adı **yazma anında** kopyalanır (`entityDefinition`, `oldDisplay`/`newDisplay`). Sonradan join edilse **bugünkü** adı verirdi; kayıt silinmişse hiçbir şey. Log "o an ne yazıyordu"yu gösterir. |

---

## 2. Modeller

### 2.1 `SettingsLog` — değişiklik kaydı

| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | bigint | PK | Log kaydı ID'si. |
| `organizationId` | int | FK → `organization.md` | Sahibi organizasyon. **RLS anahtarı** (→ §4.3). |
| `serviceId` | int? | FK → `service.md` | **Servis ayarı** sayfalarında dolu; organizasyon ayarlarında **null**. |
| `page` | SettingsPage | — | Değişikliğin yapıldığı **ayar sayfası** (→ §3.1). Sayfa bazlı görünümün filtresi. |
| `entityId` | int | mantıksal ref | Değişen **aggregate root** kaydın id'si. `page`'e göre farklı tabloya işaret ettiği için **FK değildir** — uygulama katmanı doğrular. |
| `entityDefinition` | string | — | Kaydın **adı — snapshot**. Kayıt silinse/yeniden adlandırılsa da log okunabilir. |
| `action` | SettingsLogAction | — | Bu kayda **ne oldu** (→ §3.2). |
| `changedByUserId` | int? | FK → `user.md` | Değişikliği **fiilen yapan** kullanıcı. |
| `changedByApiKeyId` | int? | FK → ApiKey | Değişikliği yapan **API anahtarı** (kullanıcı yerine API). |
| `onBehalfOfUserId` | int? | FK → `user.md` | **Yerine geçilen** kullanıcı (impersonation). |
| `batchId` | bigint? | FK → `SettingsLogBatch` | **`null` = tekil değişiklik.** Dolu ise bir toplu işlemin parçası (→ §2.2). |
| `changedAt` | datetime | — | Değişiklik zamanı (UTC). |
| `changes` | jsonb | — | **Alan-alan delta** (→ §2.3). |

**Kısıtlar**
- `changedByUserId` ve `changedByApiKeyId` **ikisi birden null olamaz** — her değişikliğin bir aktörü vardır.
- **Append-only:** tabloya UPDATE/DELETE uygulanmaz.

> **`onBehalfOfUserId` neden ayrı alan:** `impersonationUserGroupId` canlı bir yetkidir (→ `permissions.md`) — bir kullanıcının
> **yerine geçip onun adına** işlem yapılabilir. Log yalnız yerine geçilen kişiyi yazsaydı, **yapmadığı işlem ona atfedilir**
> ve denetim izi yanıltıcı olurdu. Bu yüzden **fiilen yapan** (`changedByUserId`) ile **adına yapılan** (`onBehalfOfUserId`)
> ayrı tutulur.

### 2.2 `SettingsLogBatch` — istek (toplu işlem) başlığı

**Bir istek = bir `SettingsLogBatch` kaydı.** İsteğin kendisine ait bilgiler (endpoint, metot, header, body) burada tutulur;
kayıt-kayıt değişiklikler `SettingsLog`'a (`batchId` ile) bağlanır.

> **Her Customer API isteği batch üretir** — tek kayıt değiştirse bile. İstek bilgisi burada durduğu için tekil API
> çağrıları da başlıksız kalamaz. Arayüzden yapılan **tekil** değişiklikler batch üretmez (`SettingsLog.batchId = null`).

| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | bigint | PK | İstek/toplu işlem ID'si. |
| `organizationId` | int | FK → `organization.md` | Sahibi organizasyon (RLS). |
| `source` | SettingsLogSource | — | İsteğin kaynağı (→ §3.3). |
| `changedByApiKeyId` | int? | FK → ApiKey | Aktör — §2.1 ile aynı kural (ikisi birden null olamaz). |
| `changedByUserId` | int? | FK → `user.md` | Aktör. |
| **— İstek bilgileri —** | | | |
| `endpoint` | string | — | İstek atılan **yol** (ör. `/settings/users/bulk`). |
| `httpMethod` | HttpMethod | — | İstek metodu → [`../../models/enums/http-method.md`](../../models/enums/http-method.md). ⚠️ Enum'a **`patch`** eklenmeli (→ §5). |
| `requestHeaders` | jsonb | — | İstek başlıkları — **maskelenmiş** (↓ güvenlik kuralı). |
| `requestBody` | jsonb? | — | İstek gövdesi. **Eşiği aşarsa `null`**, gövde MinIO'ya taşınır (↓). |
| `requestBodyUrl` | string? | — | Gövde büyükse **MinIO nesne URL'i**; küçükse `null`. |
| `responseStatusCode` | int? | — | Dönen HTTP durum kodu. |
| `ipAddress` | string? | — | İsteğin geldiği IP. |
| **— Sonuç —** | | | |
| `startedAt` | datetime | — | Başlangıç. |
| `finishedAt` | datetime? | — | Bitiş. |
| `status` | SettingsLogBatchStatus | — | Sonuç (→ §3.4). |
| `errorMessage` | string? | — | `partial` / `failed` ise. |

> 🔒 **Güvenlik — header'lar ham saklanmaz.** `Authorization`, `X-Api-Key`, `Cookie` ve benzeri kimlik taşıyan
> başlıkların **değeri maskelenir** (`"Authorization": "***"`). Ayar logunu **o sayfaya erişebilen herkes** okuyabilir
> (→ §4.2); ham token saklamak, kimlik bilgisini bu geniş kitleye açmak olurdu.

> 📦 **Gövde boyutu.** Küçük gövde `requestBody`'de (jsonb) satır içinde durur. **Eşiği aşan** gövde (ör. 5.000 kayıtlık
> senkron payload'ı) **MinIO'ya** yazılır ve satırda yalnız `requestBodyUrl` kalır — projenin yerleşik kuralı:
> *"binary asla JSONB'ye konmaz; JSONB yalnız referans/URL tutar"* (→ `tech-stack/minio.md`). Böylece log tablosu küçük kalır.

**İlişkiler:** **1 – N** → `SettingsLog` (`batchId`) · **1 – N** → `SettingsLogBatchPage` (`batchId`).

### 2.3 `SettingsLogBatchPage` — istek ↔ sayfa kırılımı

**Tek bir istek birden fazla sayfayı değiştirebilir.** Örnek: kullanıcı eklenirken, olmayan **departmanlar** da
oluşturulur → aynı istek hem `users` hem `departments` sayfasını etkiler.

Bu yüzden `SettingsLogBatch` üzerinde **`page` alanı yoktur**; hangi sayfaların ne kadar etkilendiği burada tutulur.
Sayfa bazlı görünüm, bir isteği **dokunduğu her sayfanın** logunda ve **o sayfaya ait sayaçlarla** gösterir.

| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | bigint | PK | Kayıt ID'si. |
| `batchId` | bigint | FK → `SettingsLogBatch` | Bağlı istek. |
| `page` | SettingsPage | — | Etkilenen ayar sayfası. |
| `addedCount` · `updatedCount` · `deletedCount` · `failedCount` | int | — | **O sayfaya ait** sayaçlar. |

**Benzersizlik:** `(batchId, page)` — bir istek için bir sayfa tek satır.

> **Neden sayaçlar burada?** Kullanıcı senkronu 500 kullanıcı güncelleyip 3 departman eklediyse, **Departmanlar**
> sayfasının logunda "500 güncellendi" yazmak yanlış olurdu. Her sayfa **kendi** özetini görür; isteğin toplamı bu
> satırların toplamıdır (ayrıca saklanmaz).

> **Neden başlık + detay?** Tek bir toplu çağrı **aynı anda ekler + günceller + siler**. Bunu tek bir `action` değeri
> yapsaydık *hangi kayda ne olduğu* kaybolurdu; kayıt başına satır yazıp başlık koymasaydık tek bir gece senkronu
> sayfa görünümünü **5.000 satırla** boğardı. Başlık **özeti**, detaylar **denetimi** taşır.

### 2.4 `changes` (jsonb)

```json
{
  "fields": [
    { "property": "definition", "old": "Muhasebe", "new": "Mali İşler" },
    { "property": "managerUserId", "old": 12, "new": 15,
      "oldDisplay": "Ali Yılmaz", "newDisplay": "Ayşe Demir" },
    { "property": "active", "old": true, "new": false }
  ],
  "subChanges": [
    { "subModel": "Staff", "subId": 7, "subDefinition": "Kadro 01", "action": "add",
      "fields": [ { "property": "userId", "new": 42, "newDisplay": "Mehmet Kaya" } ] },
    { "subModel": "Staff", "subId": 3, "subDefinition": "Kadro 02", "action": "delete", "fields": [] }
  ]
}
```

| Kural | |
|---|---|
| `add` | `fields` yalnız **dolu** alanları taşır (`old` yok). |
| `update` | Yalnız **değişen** alanlar. |
| `delete` | `fields` **boş**; neyin silindiğini `entityDefinition` söyler. |
| FK alanları | `oldDisplay`/`newDisplay` ile **görünen metin** snapshot'lanır. |
| Alt varlıklar | `subChanges` içinde, kendi `action`'ıyla. |

---

## 3. Enum'lar

### 3.1 `SettingsPage`
Değişikliğin yapıldığı ayar sayfası. **Sayfa = aggregate root**; alt varlıklar kendi değeri değildir.

**Organizasyon ayarları:** `organization` · `permissions` · `companies` · `departments` · `professions` · `positions` ·
`users` · `userGroups` · `workerLevels` · `costCenters` · `creditCards` · `additionalQualifications` · `actions` ·
`statuses` · `styles` · `translations` · `workingSchedules` · `vacationDays` · `processTransfer` · `schedulerJobs`

**Servis ayarları:** `solutions` · `services` · `properties` · `viewProfiles` · `processSteps` · `businessRules`

> **`permissions` neden ayrı:** `adminUserIds` + 4 yetki grubu alanı teknik olarak `Organization` kaydının parçasıdır,
> ama "**kim admin oldu**" denetimdeki en kritik satırdır — `logoUrl` değişikliğiyle aynı akışta kaybolmamalıdır.

### 3.2 `SettingsLogAction`
| Değer | Anlam |
|---|---|
| `add` | Yeni kayıt oluşturuldu. |
| `update` | Mevcut kayıt güncellendi (**`active=false`** dahil). |
| `delete` | Kayıt silindi (fizikselde `deleted=true`). |
| `execute` | CRUD olmayan **işlem** çalıştırıldı (ör. Süreç Transferi). |
| `toggle` | Salt-okunur bir kaydın durumu değiştirildi / tetiklendi (ör. Zamanlanmış Görev aç/kapa/çalıştır). |

### 3.3 `SettingsLogSource`
| Değer | Anlam |
|---|---|
| `customerApi` | Customer API ile toplu güncelleme. |
| `ui` | Arayüzden toplu işlem (çoklu seçim). |

### 3.4 `SettingsLogBatchStatus`
| Değer | Anlam |
|---|---|
| `success` | Tüm kayıtlar işlendi. |
| `partial` | Bir kısmı başarısız (`failedCount` > 0). |
| `failed` | İşlem bütünüyle başarısız. |

---

## 4. Log erişimi

### 4.1 Sayfa bazlı görünüm
- **Filtre:** `page` + `changedAt DESC` — birincil erişim yolu.
- **Varsayılan liste — iki kaynak:**
  1. **Tekil değişiklikler** — `SettingsLog` (`page = X` ve `batchId IS NULL`).
  2. **İstek başlıkları** — o sayfaya dokunan istekler: `SettingsLogBatchPage` (`page = X`) → `SettingsLogBatch`,
     **o sayfanın sayaçlarıyla** ("Customer API — 3 departman eklendi").
- **Toplu detaylar listeye karışmaz;** yalnız başlık açılınca çekilir (`batchId` + `page`) — aksi hâlde tek bir senkron,
  insan değişikliklerini listeden siler.
- **Çok sayfalı istek:** aynı istek, dokunduğu **her sayfanın** listesinde görünür; her sayfada **kendi** sayaçlarıyla.
- **İstek detayı:** başlık açılınca endpoint · metot · header (maskeli) · gövde · durum kodu görünür.
- **Kayıt geçmişi:** `page` + `entityId` → o kaydın tüm değişiklikleri.
- **Aktör görünümü:** `changedByUserId` → "bu kullanıcı ne yaptı".

### 4.2 Yetki — mevcut modelden gelir
Log görme yetkisi = **o sayfaya erişim yetkisi**. Yeni bir yetki alanı **gerekmez** (→ `permissions.md`):

| Yetki alanı | Görebildiği log |
|---|---|
| `organizationSettingsUserGroupId` | Organizasyon ayarı sayfalarının logu |
| `serviceSettingsUserGroupId` | Servis ayarı sayfalarının logu |
| `adminUserIds` | Hepsi |

### 4.3 İzolasyon
**RLS** (`organizationId`) — organizasyon **yalnız kendi loglarını** görür; izolasyon DB seviyesinde garanti edilir.

### 4.4 İndeksler
| Tablo | İndeks | Karşıladığı erişim |
|---|---|---|
| `SettingsLog` | `(organizationId, page, changedAt DESC)` | Sayfa bazlı liste (tekil değişiklikler) |
| `SettingsLog` | `(organizationId, page, entityId, changedAt DESC)` | Kayıt geçmişi |
| `SettingsLog` | `(batchId, page)` | İstek detaylarını açma (sayfaya göre) |
| `SettingsLog` | `(organizationId, changedByUserId, changedAt DESC)` | Aktör görünümü |
| `SettingsLogBatchPage` | `(page, batchId)` | Bir sayfaya dokunan **istekleri** listeleme |
| `SettingsLogBatch` | `(organizationId, startedAt DESC)` | İstek listesi / zaman sıralı |

---

## 5. Açık kalanlar

| # | Konu |
|---|---|
| **1** | ⚠️ **Ön koşul — Customer API'de ayar yazma ucu yok.** Bugün yalnız `GET /users/{userId}` · `GET /me` var; tüm yazma uçları instance tarafında. **Toplu güncelleme yeteneği önce tasarlanmalı** (`flovo-customer-api.md`), sonra loglanabilir. Toplu güncellemenin doğal yüzeyi `synchronizationStatus` taşıyan 7 model: Company · Department · Profession · Position · User · CostCenter · CreditCard. |
| **2** | **Saklama süresi / KVKK.** Log kişisel veri içerir (ad, e-posta, kim-ne-yaptı) **ve artık istek gövdesi de** (`requestBody`/`requestBodyUrl`) — ham payload. "Denetim kaydı silinmez" ilkesi ile **silme hakkı** çelişir. Teknik hazırlık var (parametrik süre + soğuk arşiv → MinIO); **karar hukukidir**. |
| **3** | **`HttpMethod` enum'una `patch` eklenmeli.** Enum bugün `get`/`post`/`put`/`delete` taşıyor ve notunda *"ileride gerekirse `patch` … şimdilik kapsam dışı"* diyor — ama `flovo-customer-api.md` **zaten `PATCH /instances/{instanceId}`** kullanıyor. Enum'un "kullanan model" satırına `SettingsLogBatch` de eklenecek. |
| **4** | **Gövde eşiği** — `requestBody` satır içinde mi, MinIO'da mı? Sınır kaç KB olmalı? |

*Oluşturma: 2026-07-17.*
