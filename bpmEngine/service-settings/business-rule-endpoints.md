# Flovo — İş Kuralı Motoru: Backend Endpoint'leri

> **Durum:** 🟢 Endpoint spesifikasyonu (v0.35). **Amaç:** İş kuralı motorunun **çalışması için ihtiyaç duyduğu backend
> uçlarını** tanımlamak — hangi durumda hangi uç, method/path, istek/yanıt, tetikleyen motor fonksiyonu.
>
> **Üst doküman:** işleyiş → [`business-rule-engine.md`](./business-rule-engine.md) · davranış → [`business-rule.md`](./business-rule.md).
> **Yol/konum:** Motor **tam frontend** çalışır (kurallar client'ta yürür); aşağıdaki uçlar yalnız **veri/işlem** ihtiyaçları içindir.
> Path'ler **yeni-motor önerisidir** (REST konvansiyonu).

---

## 0. Ne zaman backend'e gidilir?
Motor çoğu işi client'ta yapar; backend'e yalnız şu 6 durumda çıkar:

| # | Durum | Bölüm |
|---|---|---|
| 1 | **Kural taşıma** — kurallar servis/instance detayına **gömülü** gelir | §1 |
| 2 | **Veri seti (`serviceInstances`)** — başka servisin instance'larından değer/liste | §2 |
| 3 | **Organizasyon / kullanıcı verisi** — `fillDataSource` + ön-yükleme | §3 · §4 |
| 4 | **`httpRequest`** — kullanıcı-tanımlı dış çağrı | §5 |
| 5 | **İfade-destek uçları** — `fromCalculation` yerleşik fonksiyonlarının sunucu sorguları | §6 |
| 6 | **Kural yönetimi (ayar)** — CRUD (tasarım-zamanı; motor runtime'ı değil) | §7 |

## 0.1 Ortak sözleşme
- **Kimlik:** `Authorization: Bearer <token>` (Keycloak OIDC); token'daki **`organizationId`** claim'i ile tenant izolasyonu
  (**PostgreSQL RLS** — Pattern B). Ayrı `accountId` header **yok** → [`tech-stack/keycloak.md`](../tech-stack/keycloak.md).
- **Ortak header'lar:** `Content-Type: application/json` · `Accept-Language` (çok-dilli metin/çeviri) · sürüm.
- **İçerik:** istek/yanıt JSON; hata sözleşmesi Customer/iç API ortak standardı (→ todo).

---

## 1. Kural taşıma (runtime — gömülü, AYRI uç değil)
Kurallar ayrı endpoint'ten **çekilmez**; servis/instance detay yanıtının içinde **gömülü** gelir. Böylece form açılır açılmaz
motor ek tur beklemeden çalışır.

| Uç | Method | Amaç | Yanıtta gömülü |
|---|---|---|---|
| `GET /services/{serviceCode}` (form açılışı) · `GET /instances/{id}` (mevcut kayıt) | GET | Form/servis detayı | `businessRules[]` (kural + `configuration`) + **statik** (lazy-olmayan) veri seti satırları |

> **Not:** `fillDataSource`/`fromDataSet` **lazy-olmayan** kaynak, kural içine gömülü gelen satırlarla **client-side** çözülür (ağa çıkmaz).

---

## 2. Veri seti — `serviceInstances` sorgusu
Başka bir servisin instance'larından **tek değer** (`fromDataSet`) veya **liste** (`fillDataSource serviceInstances`) çekme.

| Uç | Method | Amaç | Tetikleyen | İstek | Yanıt |
|---|---|---|---|---|---|
| `POST /instances/search` | POST | Kaynak servisin kayıtlarını filtreli sorgula | `fetchServiceInstances` (→ `fromDataSet` lazy · `fillDataSource serviceInstances` lazy · lazy+arama'da her arama tuşunda) | `{ serviceId, parameters[] (parameterPropertyId · criterion · value · changeToCompare · isSearchValue), wantedPropertyIds[], statusIds[], sort{propertyId, direction}, searchText? }` | `{ items: [{ propertyId, value }] }` (satır listesi) |

- **`searchActive`:** sunucu-tarafı arama — istekte `searchText` gelir, liste tümüyle çekilmez (büyük veri).
- **Cache:** `cacheDeactive` → istemci cache kapalı.
- 🟦 **Hizalama:** sorgu dili Customer API `POST /instances/search` ile **ortak** olmalı (→ todo · flovo-customer-api §3).

---

## 3. Organizasyon verisi (`organizationData`)
`fillDataSource organizationData` ve `prepareEngine` **ön-yükleme** için. Kaynaklar `OrganizationDataSourceType` ile birebir.

| Uç | Method | Kaynak (`OrganizationDataSourceType`) | Yanıt |
|---|---|---|---|
| `GET /organization/companies` | GET | `companies` | `[Company]` |
| `GET /organization/departments` | GET | `departments` | `[Department]` |
| `GET /organization/cost-centers` | GET | `costCenters` | `[CostCenter]` |
| `GET /organization/professions` | GET | `professions` | `[Profession]` |
| `GET /organization/credit-cards` | GET | `creditCards` | `[CreditCard]` |
| `GET /organization/worker-levels` | GET | `workerLevels` | `[WorkerLevel]` |
| `GET /organization/user-groups` | GET | `userGroups` | `[UserGroup]` |
| `GET /organization/positions` | GET | `positions` | `[Position]` |
| `GET /organization/working-schedules` | GET | `workingSchedules` | `[WorkingSchedule]` |
| `GET /organization/users` | GET | `users` (organizasyon kullanıcı listesi) | `[User]` |

- **Tetikleyen:** `prepareEngine` (gerekli depoları paralel ön-yükler) + `applyFillDataSource` (organizationData) → filtreleme `matchesOrganizationParameters` **client-side**.
- **Kapsam-dışı:** eski masraf-spesifik kaynaklar (`expense-types` / `expense-categories`) **yok** (masraf çekirdek modeli yok → todo).
- 🟩 **KARAR (v0.35) — hibrit:** kuralların ihtiyaç duyduğu org/user verisi form açılışında **toplu ön-yüklenir** (cache; ifade fonksiyonları sync okur); büyük/nadir `serviceInstances` **çalışma-anı** çekilir (→ [`business-rule-engine.md`](./business-rule-engine.md) `prepareEngine`).

---

## 4. Kullanıcı verisi (`userData`) — oturum kullanıcısı
| Uç | Method | Kaynak (`UserDataSourceType`) | Yanıt |
|---|---|---|---|
| `GET /me/credit-cards` | GET | `creditCards` (aktif kartlar) | `[CreditCard]` |
| `GET /me/companies` | GET | `companies` | `[Company]` |
| `GET /me/cost-centers` | GET | `costCenters` | `[CostCenter]` |

- **Tetikleyen:** `applyFillDataSource` (userData). Kaynak **oturum kullanıcısına** özeldir (token'dan çözülür).

---

## 5. `httpRequest` — kullanıcı-tanımlı dış çağrı
Sabit bir uç değildir; **kuralın `httpRequest` konfigindeki** `endpoint` + `method` (`HttpMethod`) + parametrelerle (query/header/body/template) çalışır.

| Uç | Method | Amaç | Tetikleyen | İstek | Yanıt |
|---|---|---|---|---|---|
| *(kural tanımından)* `endpoint` | `HttpMethod` (get/post/put/delete) | Entegrasyon/dış-API değeri veya listesi | `callHttpRequest` (→ `assignValueToProperty httpRequest` · `fillDataSource httpRequest`) | `DynamicParameter[]` → template `{name}` doldurma + query/header/body | JSON; opsiyonel `responseParameter` ile alan çıkarımı |

- 🟩 **KARAR:** eski **Eba entegrasyon ucu (`getintegrationqueryresult`) kaldırıldı** → dış kaynak yalnız `httpRequest` ile.
- 🟦 **GÜVENLİK (açık):** kullanıcı-tanımlı URL çağrısı → **allowlist/sandbox** + credential yönetimi → todo (güvenlik).

---

## 6. İfade-destek uçları (`fromCalculation` yerleşik fonksiyonları)
Bazı yerleşik fonksiyonlar sunucuya gider; çoğu ise **ön-yüklenen veriden** (client, §3 depoları + kullanıcı listesi) okunur.

**6.1 Sunucuya giden (ağ):**

| Fonksiyon | Uç | Method | İstek | Yanıt |
|---|---|---|---|---|
| `getExchange(date, from, to)` | `GET /exchange-rates/{date}` | GET | query: `from`, `to` | `rate: number` |
| `getUserAdditional` · `getUserWorkerLevelCode` | `GET /users/{userId}` | GET | path: `userId` | `User` (ek nitelik / kademe alanları) |
| `getUserManagerByProfession(userCode, professions)` | `POST /users/manager-by-profession` | POST | `{ userCode, professionCodes[] }` | `User` |
| `checkUserInUserGroup(userCode, groupCode)` | `GET /user-groups/{groupCode}/members/{userCode}` | GET | path | `{ isMember: bool }` |
| Çalışma-takvimi: `getWorkDayHour` · `addWorkDay` · `findNextWorkDay` · `differenceWorkDay` | `GET /users/{userId}/working-schedule` | GET | path: `userId` | `WorkingSchedule` (client hesaplaması burada koşar; tatil günü `organization/vacation-days`'ten) |

**6.2 Ön-yüklenen veriden okuyan (ağ DEĞİL — `prepareEngine` cache'i):**
`getUserMail/FullName/Id/Code` · `getManagerUserId/Code` · `getUserCompany/Department/Profession(Code/Name)` ·
`getUserExpenseCenter(Code/Name)` · `getDepartmentManagerCode` · `getExpenseCenterAdditional` · `getUserEmploymentStartDate` ·
kredi-kartı sorguları (`getCreditCardNumber` · `getUserByCreditCardCode` · `getUserCreditCard*`) · `isHoliday`.
→ Bunlar **organizasyon kullanıcı listesi** (`GET /organization/users`) + §3 org depolarından **client-side** okunur; tekil çağrı yapmaz.

- 🟦 **AÇIK:** kesin fonksiyon kataloğu + hangi fonksiyon ağa/cache'e gider — **ifade dilinin somut seçimi** kararıyla netleşir → todo.

---

## 7. Kural yönetimi (ayar/tasarım — motor runtime'ı DEĞİL)
Tasarımcının kural CRUD'u (ayar ekranı). Motor yürütmesinden ayrıdır.

| Uç | Method | Amaç | İstek | Yanıt |
|---|---|---|---|---|
| `GET /services/{serviceId}/business-rules` | GET | Servisin kurallarını listele | — | `[BusinessRule]` |
| `POST /services/{serviceId}/business-rules` | POST | Kural ekle | `BusinessRule` (configuration dahil) | oluşturulan `BusinessRule` |
| `PUT /services/{serviceId}/business-rules/{id}` | PUT | Kural güncelle | `BusinessRule` | güncel `BusinessRule` |
| `DELETE /services/{serviceId}/business-rules/{id}` | DELETE | Kural sil | — | — |

- 🟦 **AÇIK:** ayar yazma uçları + **değişiklik loglaması** (→ todo · `research/settings-log/`).

---

## 8. Yeni motor farkları (özet)
| Konu | Karar |
|---|---|
| Kimlik | **Keycloak Bearer** + `organizationId` claim → RLS (eski `accountId`/`Ocp-Apim` yerine) |
| Dış kaynak | **yalnız `httpRequest`** (Eba `getintegrationqueryresult` **kaldırıldı**) |
| Veri seti | `serviceInstances` → `POST /instances/search` (Customer API ile ortak) |
| Kural yönetimi | REST CRUD (`PUT` dahil — eski motorda `put` yoktu) |
| Org kaynakları | masraf-spesifik uçlar **yok** (kapsam-dışı) |

## 9. Açık noktalar (→ [`../todo.md`](../todo.md))
`httpRequest` güvenliği (allowlist/sandbox) · `serviceInstances` sorgu dili (Customer API ortak) · ifade fonksiyon kataloğu → uç
eşlemesi · kural yönetimi ayar API + loglama · ortak hata sözleşmesi. _(prepareEngine veri stratejisi = hibrit, ÇÖZÜLDÜ v0.35.)_

---

*Oluşturma: 2026-08-27.*
