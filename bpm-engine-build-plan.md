# BPM Motoru — İki Fazlı Geliştirme Planı (dökümantasyon yol haritası)

> **Durum:** 🟡 AÇIK — plan hazır, doküman tamamlama başlamadı.
> **Amaç:** BPM motorunu **iki fazda** çalışır hâle getirmek için hangi **tasarım dökümanlarının** hangi **sırayla** tamamlanacağını,
> ne durumda olduğumuzu ve eksikleri **izlenebilir görevlere** bölerek tek yerde tutmak.
> **Faz 1 = motor çalışır** (DB'deki verilerle, **backend-only**, frontend YOK) · **Faz 2 = frontend entegrasyonu** (instance görüntüleme + aksiyon,
> **DTO ile seçici veri aktarımı** — response boyutu + DB performansı).
> **Nasıl devam edilir:** Önce §6'daki kararları ver → sonra §3 (Faz 1) görevlerini **sıra**ya göre tamamla → §4 (Faz 2).
> Her görev tamamlanınca kutusunu ✅ yap ve §2.0 durum panosunu güncelle.
> **Oluşturma:** 2026-08-31. **Bağlam:** Üç keşif ajanının bulguları (motor runtime · veri modelleri · API/DTO) §2'ye işlendi — yeniden analiz gerekmez.

---

## 0. Bu dosya ne için?

Bu depo **kod değil, tasarım dokümanı** üretir; gerçek motor ayrı bir repoda geliştirilecek. Bu plan, **"motoru çalıştırmak için hangi
dökümanlar eksik ve hangi sırayla yazılmalı"** sorusunu iki faza bölerek yanıtlar ve **ilerlemeyi işaretleyerek takip** etmeyi sağlar.

- **Bir görevin "tamam" olması** = ilgili **tasarım dökümanının** (model / davranış / API sözleşmesi) yazılıp `🟢`'a çekilmesi.
- **Konvansiyon:** Açık **kararlar** normalde yalnız [`bpmEngine/todo.md`](bpmEngine/todo.md)'de tutulur. Bu dosya **plan/çalışma dosyasıdır**;
  §6 kararları netleşince ilgili maddeler `todo.md` + tasarım dökümanlarına taşınır. Görev listesi burada, açık sorular todo'da kalır.
- **Kilometre taşı ilkesi:** Faz 1 dökümanları bitmeden Faz 1 motoru **kodlanamaz**; Faz 2 dökümanları Faz 1'e bağımlıdır (aşağıda §5).

---

## 1. İki fazın tanımı (kapsam sınırı)

| | **Faz 1 — Motor çalışır** | **Faz 2 — Frontend entegrasyonu** |
|---|---|---|
| **Hedef** | DB'deki süreç tanımı + instance verisiyle motor **uçtan uca koşar** | Oluşan instance'lar **görüntülenir** + kullanıcı **aksiyon alır** |
| **Arayüz** | Frontend YOK — API / webhook / test-harness ile sürülür | Next.js UI (gelen kutusu · form detay · aksiyon) |
| **Öz gereksinim** | Yürütme + kalıcılık + suspend/resume + hata/retry + tetikleme | **DTO ile seçici veri aktarımı** (response boyutu + backend DB perf) |
| **İş kuralları** | **Koşmaz** — iş kuralları frontend'de çalışır (bkz. §2.3 mimari not). Backend yalnız `changeList`'i JSON Schema ile doğrular | Frontend iş-kuralı motoru devrede |
| **Bitiş tanımı (DoD)** | Bir süreç DB'den okunur → `ProcessInstance` başlar → otomatik adımlar koşar → insan/timer/processing durağında **suspend** → external event ile **resume** → hata/retry uygulanır → `workflow_events`'e yazılır. **Hepsi frontend olmadan.** | Bekleyen formlar **listelenir**, detay **seçici DTO ile** açılır, aksiyon alınır → motor ilerler; response boyutu + DB yükü optimize |

---

## 2. Ne durumdayız? (üç ajan bulgusu — birleşik değerlendirme)

> **Pilot gerçeği (v0.41-1 · [`bpmEngine/implementation-status.md`](bpmEngine/implementation-status.md)):** **Tasarım-zamanı (config authoring)
> katmanı = INŞA EDİLDİ + dağıtıldı** (Settings-API çatısı · Service/Property/ViewProfile CRUD + Designer'lar · **Draft/Publish/Versiyonlama** ·
> **Süreç Arşivleme** → Azure Container Apps + Vercel + Azure-PG + Keycloak). Bu katman, bu planın **her iki fazının da üstünde** (upstream)
> kalır: **Faz 1 (motor runtime)** ve **Faz 2 (instance frontend)** hâlâ önümüzde. Yani aşağıdaki "🟢 hazır" değerlendirmesi, tasarım-zamanı
> için artık "🟢 **inşa edildi**" olarak okunmalı. *(Numaralandırma: implementation-status'un "Bölüm-1 = design-time / Motor runtime" ekseni,
> bu planın "Faz 1 = motor runtime / Faz 2 = frontend" ekseninden farklıdır; pilotun "Motor runtime henüz yok" tespiti ≈ bu planın **Faz 1**'idir.)*

### 2.0 Durum panosu (ilerledikçe güncelle)

| Faz | Grup | Konu | Durum |
|---|---|---|---|
| — | Karar | §6 açık kararlar (Tier 0 iki-katman sınırı dâhil) | ⬜ bekliyor |
| **F1** | A | Kalıcılık çekirdeği (event-sourcing + değer saklama) | ⬜ 0/4 |
| **F1** | B | Hata & dayanıklılık (retry / onFail / compensation) | ⬜ 0/4 |
| **F1** | C | Zamanlama & tetikleme altyapısı (scheduler / SchedulerJob / döngü koruması) | ⬜ 0/3 |
| **F1** | D | Adım-içi yürütme spec'leri (işiniYap algoritmaları) | ⬜ 0/4 |
| **F1** | E | Kimlik & yetki (motor tarafı: ApiKey / aksiyon-yetki / resume ucu) | ⬜ 0/3 |
| **F2** | G | Okuma / görüntüleme uçları (gelen kutusu · detay · liste) | ⬜ 0/3 |
| **F2** | H | DTO / seçici veri aktarımı (asıl performans gereksinimi) | ⬜ 0/4 |
| **F2** | I | Sözleşme & tutarlılık (hata · sayfalama · Customer API · proto) | ⬜ 0/4 |

> **Lejant:** ⬜ yapılacak · 🟡 devam · ✅ tamam. Grup satırındaki `x/y` = tamamlanan görev / toplam.

### 2.1 HAZIR olan (🟢 — sağlam zemin, motoru bloklamaz)

**Yürütme mekanizması (motor "nasıl koşar"):**
- **Yürütme durum makinesi** — `new/running/waiting/failed/done` + geçişler tanımlı; iş-durumu (`Instance.statusId`) ile ayrık.
  → [`bpmEngine/engine-runtime.md`](bpmEngine/engine-runtime.md) §1 · [`process-execution-state.md`](bpmEngine/models/enums/process-execution-state.md)
- **Suspend / resume** — atananı çöz → `InstanceAwaitingUser` senkronla → `waiting` (worker serbest); external event → doğrula → `running`. Günlerce bekleme kaynak tutmaz. → engine-runtime §4.3/§4.4
- **Kontrol-akışı / ilerleme** — **22 adım tipinin** her biri için "işini yapınca hangi aksiyon koduyla ilerler" tanımlı (Karşılaştırma→`true`/`false`, Switch→eşleşen/default, HTTP→`response.action`, terminal→break). → [`bpmEngine/service-settings/process-step.md`](bpmEngine/service-settings/process-step.md) §3 · flovo-bpm-engine §4.3
- **ActionTransfer veri akışı** — `parameters`/`changeList`/`action` + `mergeParameter` birleştirme sırası + forma JSONB merge + `ProcessStepInstance` kaydı. → [`bpmEngine/service-settings/process-step-action.md`](bpmEngine/service-settings/process-step-action.md) §2
- **İnsan-görev ailesi** — Kullanıcı/Grup/Üst-Form/Processing ortak iskelet; atama-fallback (`onFail`), dinamik üyelik, kenar durumlar çözülü.
- **ServiceTrigger** — associate tespiti (DB-katmanı çekirdek) + timer (cron→yeni ana süreç); kaynak↔hedef invariant + `async` bekleme + parent zinciri. → [`service-trigger.md`](bpmEngine/models/service-settings/service-trigger.md)

**Modeller:**
- **Runtime çekirdek (🟢):** `ProcessInstance` · `ProcessStepInstance` · `Instance` · `InstanceAwaitingUser` · `AssociatedInstance` · `ActionTransfer` (DTO).
- **Tasarım-zamanı (🟢, v0.36):** Solution · Service · Property · ProcessStep · ProcessStepAction · ServiceTrigger · ProcessViewProfile(+property+setting) · tüm organization-settings (User/UserGroup/Status/Action/Style/…).
- **Ayar şemaları (🟢):** Property 18 tip + ProcessStep 22 tip `settings` JSON Schema; runtime değer şablonları (18 tip) olgun.

### 2.2 EKSİK olan (motoru bloklayan boşluklar — faz bazında §3/§4'te göreve dönüştü)

**Faz 1 blokları (öncelik sırasıyla):**
1. 🔴 **`workflow_events` + `workflow_projection` model dosyaları YOK** — motorun ilan edilen **kaynak-hakikati** (append-only olay log'u); `executionState`/idempotency/replay/audit hepsi buna dayanıyor. Yalnız `engine-runtime.md`/tech-stack'te **kavram**; `models/` altında dosya yok. **En kritik boşluk.**
2. 🔴 **`instance-value.md` 🟡 TASLAK** — motor her adımda form değerini buradan **okur ve tek-TX yazar**; alan-düzeyi kilitlenmeli. Ek 4 projeksiyon (`instance-attr`/`instance-list-item`/`instance-value-outbox`/`instance-value-change`) da 🟡 TASLAK.
3. 🔴 **Hata & dayanıklılık kararsız** — retry değerleri (max deneme/backoff/hangi hata sınıfı), `onFail` zorunlu mu, dead-letter→`failed` geçişi, süreç-seviye global hata yakalayıcı → hepsi açık. `process-step-action.md` §5 boş.
4. 🟠 **Scheduler lider-seçim** seçilmemiş (NATS KV ↔ Postgres advisory) + **`SchedulerJob` modeli** "sonraya" ertelenmiş → timer beklemesi tam koşamaz.
5. 🟠 **`ApiKey` modeli yok** (geçici) — webhook/Customer API ile başlatma + trigger kimliği için gerekli (`createdByApiKeyId`/`atApiKeyId` FK'leri boşta).
6. 🟡 **Adım-içi yürütme spec'leri** — settings şemaları var ama "girdi→işlem→ActionTransfer çıktısı" algoritması düzyazı düzeyinde. **`triggerProcessStep` + `formRedirect` settings HİÇ modellenmemiş** (yürütme davranışı tanımsız). Instance Deleter/Flovo AI detayı eksik.
7. 🟡 **Aksiyon-seviyesi yetkilendirme** runtime'da nasıl zorlanır (authorizationLevel) — spec yok.
8. 🟢 **Fork/join** = bilinçli **ertelendi** (boşluk değil; MVP tek aktif kol, eşzamanlılık ayrı `ProcessInstance`'larla).

**Faz 2 blokları:**
1. 🔴 **"Gelen kutusu / bekleyen formlar" liste ucu belgelenmemiş** — model var (`InstanceAwaitingUser`), endpoint (`GET /me/awaiting-instances` benzeri) yok.
2. 🔴 **Response daraltma / sparse-fieldset DTO yok** — genel detay/form okuması **tüm `InstanceValue.data`'yı** döndürüyor; **ViewProfile client-side görünürlük**, response'u küçültmüyor. Faz 2'nin asıl gereksinimini (yalnız gereken veri) karşılayan mekanizma yalnız `POST /instances/search`'te (`wantedPropertyIds[]`) var, genel okumada yok.
3. 🟡 **Customer API request/response şemaları TASLAK** — token kapsam/süre, webhook güvenliği (secret/imza)+idempotency, search sorgu dili, rate-limit/sayfalama.
4. 🟡 **Ortak hata + sayfalama sözleşmesi** üç API'de de açık; ekran-bazlı DTO (liste-kartı vs detay) formalize değil.

### 2.3 Kritik mimari not (Faz 1 kapsamını daraltır)

**İş kuralları (`business-rule-engine.md`) "tam frontend" çalışır — backend BPM motoru iş kurallarını İŞLEMEZ.** Dolayısıyla "backend-only" Faz 1'de
iş kuralları **hiç koşmaz**; bu bir eksiklik değil, **mimari karar**. Backend'in tek dokunuşu: `changeList` değerlerinin **JSON Schema kapısıyla
doğrulanması**. → Faz 1 görev listesinde iş-kuralı motoru **yer almaz**; yalnız §6.1 "iki-katman sınırı" kararı (değer atama & karşılaştırma:
hangisi motor-adımı, hangisi frontend-kuralı) motorun kapsamını netleştirdiği için **önce** verilmeli.

### 2.4 Sağlam tasarlanmış ama Faz 2'de somutlanacak temeller (🟢 mimari)

- **CQRS okuma-modeli ayrımı** (performansın en olgun kararı): `InstanceValue`=tam tapu (detay) · `InstanceAttr`=skaler fihrist (yalnız `projectToAttr=true`, alanların ~%10-20'si → liste/filtre/sıra) · `InstanceListItem`=kalem projeksiyonu. **"Liste ekranı ≠ detay ekranı" seçici okuma bilinçli.**
- **Transport:** iç trafik gRPC/Protobuf (binary, ~7-10x az bandwidth), dış REST/JSON; Protobuf→codegen ile contract-drift sıfır. → [`api-contract.md`](bpmEngine/tech-stack/api-contract.md)
- **DB perf:** partition `HASH(service_id)` + RLS Pattern B; dosya/binary MinIO+URL (JSONB küçük tutulur).

---

## 3. FAZ 1 — Motor çalışır (görev listesi)

> **Sıra:** §6 kararları (özellikle §6.1 iki-katman sınırı) → **Grup A** (her şey buna bağlı) → **Grup D** (paralel **Grup B** ile) →
> **Grup C** → **Grup E**. Bağımlılık detayı §5.

### Grup A — Kalıcılık çekirdeği (event-sourcing + değer saklama) · **EN KRİTİK**
- [ ] **F1.A.1 — `workflow_events` model dosyası** (yeni, `models/processInstances/`): kolonlar, olay tipleri (`Start`/`StepCompleted`/`Suspended`/`ActionTaken`/`Failed`/`Ended`), payload yapısı, `version` (optimistic concurrency), idempotency (`Nats-Msg-Id`), indeksler. → engine-runtime §5/§8/§9
- [ ] **F1.A.2 — `workflow_projection` model dosyası** (yeni): türetilmiş yürütme durumu deposu; `ProcessInstance.executionState` bunun üzerinden okunur. → engine-runtime §9
- [ ] **F1.A.3 — [`instance-value.md`](bpmEngine/models/processInstances/instance-value.md) 🟡→🟢**: kaynak-hakikat JSONB `data` (code-keyed); motorun "Yükle → İşle → tek-TX Kalıcılaştır" yolu (merge + outbox aynı TX). Alan-düzeyi kilitle.
- [ ] **F1.A.4 — Projeksiyon/audit modelleri 🟡→🟢**: `instance-value-outbox` · `instance-value-change` · `instance-attr` · `instance-list-item` (async projeksiyon + append-only audit). *Faz 1 çekirdek akışını tam bloklamaz ama rapor/filtre/yansıma/denetim için gerekir.* `parentProperty` **`materialized`** yayılımı bu gruba bağlı; öncesinde yalnız `snapshot`/`live` ve Designer `materialized`'ı reddeder (KARAR v0.45 → `reflection-propagation.md` §10; tek seferlik backfill görevi bu gruba dahil).

### Grup B — Hata & dayanıklılık (resilience)
- [ ] **F1.B.1 — Retry politikası**: max deneme sayısı + backoff eğrisi + hangi hata sınıfı retry edilir (HTTP 5xx / DB lock vs kalıcı hata). → engine-runtime §6 + process-step-action §5 (boş) doldur
- [ ] **F1.B.2 — `onFail` zorunluluğu + dead-letter**: her adımda `onFail` zorunlu mu/opsiyonel mi; yoksa ne olur (→ `failed`); **süreç-seviye global hata yakalayıcı** kararı. → flovo-bpm-engine §7.1 · engine-runtime §6
- [ ] **F1.B.3 — Compensation / telafi**: çok-adımlı süreç yarıda hata alırsa geri-alma. **Karar:** MVP mi post-MVP mi + (MVP ise) iskelet. → engine-runtime §6
- [ ] **F1.B.4 — Optimistic-concurrency çakışma davranışı**: `workflow_events.version` çakışınca retry/UX. → engine-runtime §11

### Grup C — Zamanlama & tetikleme altyapısı
- [ ] **F1.C.1 — Scheduler lider-seçim mekanizması SEÇ**: NATS KV lock ↔ Postgres advisory lock (çok-örneklilikte "en-fazla-bir-kez" timer). → engine-runtime §7
- [ ] **F1.C.2 — [`SchedulerJob`](bpmEngine/models/organization-settings/scheduler-job.md) modelini tamamla**: timer/cron kalıcı kayıtları ("altyapı, sonraya" durumundan çıkar); `...At`/`...Time` adlandırma + enum kararları. → todo Tier 3
- [ ] **F1.C.3 — Trigger döngü koruması**: A→B→A recursion derinlik/çevrim sınırı + `async` kaskad derinlik sınırı + timer DST kenar durumu. → service-trigger §Açık noktalar

### Grup D — Adım-içi yürütme spec'leri (işiniYap algoritmaları)
- [ ] **F1.D.1 — Yürütme-spec şablonu + çekirdek otomatik adımlar**: "girdi→işlem→ActionTransfer çıktısı" algoritması — `httpRequest` · `valueAssignment` · `customIdCreator` · `instanceCreator`. (Settings şemaları var; **icra algoritması** yazılacak.) → process-step-settings/
- [ ] **F1.D.2 — `triggerProcessStep` settings + yürütme davranışı** (şu an HİÇ modellenmemiş): hangi associatedInstance'lar seçilir (ilişki/yön) + alt süreç/aksiyon tetikleme. → process-step §3.5/§3.20
- [ ] **F1.D.3 — `formRedirect` settings + yürütme davranışı** (şu an HİÇ modellenmemiş). → process-step §3.19
- [ ] **F1.D.4 — Kalan adım detayları**: Instance Deleter (§3.10) icra + Flovo AI **post-MVP** işaretle (motor-seviyesi AI entegrasyonu flovo-bpm-engine §11 boş; MVP dışı). → process-step §3.10 · flovo-ai.md

### Grup E — Kimlik & yetki (motor tarafı — minimum)
- [ ] **F1.E.1 — `ApiKey` modeli** (yeni): kapsam/süre/rotasyon/`organizationId`/oluşturan + 3 FK bağı (`createdByApiKeyId`/`atApiKeyId`/`changedByApiKeyId`). *Detay Customer API'ye bağlı; iskelet Faz 1'de.* → todo `apiKeyId`
- [ ] **F1.E.2 — Aksiyon-seviyesi yetkilendirme runtime kontrolü**: `authorizationLevel` / `actionDisplayAuthorizedUserGroupId` API'de aksiyon tetiklenirken nasıl zorlanır. → process-step-action §5 (boş)
- [ ] **F1.E.3 — Motoru ilerleten minimal runtime uç sözleşmesi**: `POST /instances/{id}/actions/{code}` request/response (RESUME yolu — aktör `InstanceAwaitingUser`'a karşı doğrulanır). *Customer API'nin motor için gereken alt-kümesi; tam Customer API Faz 2.* → engine-runtime §4.4

---

## 4. FAZ 2 — Frontend entegrasyonu (görev listesi)

> **Sıra:** §6.2 (ViewProfile→response daraltma) kararı **önce** — tüm okuma uçlarını etkiler → **Grup H** DTO kararları → **Grup G** okuma uçları
> → **Grup I** sözleşme. Faz 1'in Grup A (değer modelleri) 🟢 olması ön koşuldur.

### Grup G — Okuma / görüntüleme uçları
- [ ] **F2.G.1 — Gelen kutusu / bekleyen formlar liste ucu** (belgelenmemiş boşluk): `GET /me/awaiting-instances` benzeri — `InstanceAwaitingUser` üzerinden **hafif** liste (DTO). → typescript-nextjs "Görev Gelen Kutusu"
- [ ] **F2.G.2 — Instance detay/form okuma ucu sözleşmesi**: `GET /instances/{id}` — dağınık tanım tek yerde toplanır (form açılışı `businessRules[]` gömülü + değerler). → business-rule-endpoints §1 · engine §6.3
- [ ] **F2.G.3 — Servis instance liste ucu + sayfalama**: `GET /services/{id}/instances` (liste-kartı DTO'su). → flovo-customer-api §1

### Grup H — DTO / seçici veri aktarımı · **ASIL PERFORMANS GEREKSİNİMİ**
- [ ] **F2.H.1 — Seçici alan aktarımı (sparse-fieldset DTO)**: genel okuma uçlarına `wantedPropertyIds[]` benzeri mekanizma (bugün yalnız `POST /instances/search`'te var → genelleştir). → business-rule-endpoints §2
- [ ] **F2.H.2 — ViewProfile → server-side response daraltma KARARI**: yalnız profilde görünür alanları döndür → response boyutu. (Bugün client-side; §6.2 kararına bağlı.) → flovo-bpm-engine §3.1 · view-profile §4
- [ ] **F2.H.3 — Ekran-bazlı response DTO'ları**: liste-kartı DTO vs detay DTO — hangi ekran hangi alan alt-kümesini alır, formalize et.
- [ ] **F2.H.4 — CQRS okuma-modeli ↔ endpoint eşlemesi**: liste/rapor → `InstanceAttr`/`InstanceListItem` (hafif fihrist) · detay → `InstanceValue` (tapu). Somut endpoint bağı + hangi sorgu hangi tabloyu vurur (DB perf).

### Grup I — Sözleşme & tutarlılık
- [ ] **F2.I.1 — Ortak hata sözleşmesi + sayfalama sözleşmesi** (üç API ortak). → settings-api §7 · todo
- [ ] **F2.I.2 — Customer API request/response şemaları**: token kapsam/süre/yenileme · webhook güvenliği (secret/imza)+idempotency · rate-limit. → flovo-customer-api §3
- [ ] **F2.I.3 — Search sorgu dili hizalama**: Customer API `POST /instances/search` ↔ business-rule uçları tek dile. → todo
- [ ] **F2.I.4 — Protobuf `.proto` mesaj şekilleri**: somut mesajlar (api-contract kaynak-hakikat → codegen). *İç/dış tüm uçların tipli sözleşmesi.* → api-contract.md

---

## 5. Sıra & bağımlılıklar (kritik yol)

```
KARARLAR (§6)
  └─ §6.1 iki-katman sınırı ──► Faz 1 kapsamını kilitler (motor neyi yürütür)
        │
        ▼
FAZ 1  A (kalıcılık çekirdeği)  ◄── HER ŞEYİN TEMELİ (workflow_events önce)
        ├─► D (adım-içi yürütme spec'leri)   ┐ paralel
        ├─► B (hata & dayanıklılık)          ┘
        ├─► C (zamanlama & tetikleme)
        └─► E (kimlik & yetki, resume ucu)
        ▼
   ✅ Faz 1 DoD: motor DB'den koşar (frontend yok)
        │
        ▼
KARAR §6.2 (ViewProfile→response daraltma) ──► tüm okuma uçlarını etkiler
        ▼
FAZ 2  H (DTO / seçici aktarım)  ◄── önce karar, sonra uçlar
        ├─► G (okuma / görüntüleme uçları)
        └─► I (sözleşme & tutarlılık)
        ▼
   ✅ Faz 2 DoD: instance görüntüleme + aksiyon, seçici DTO ile
```

**Kesin ön koşullar:**
- **F1.A.1 (`workflow_events`)** tüm Faz 1'in temeli — ilk yazılacak doküman.
- **§6.1 (iki-katman sınırı)** Grup D'den önce (motorun hangi adımı yürüteceğini belirler).
- **Faz 1 Grup A (değer modelleri 🟢)** Faz 2 okuma uçlarının ön koşulu.
- **§6.2 kararı** Faz 2 Grup H/G'den önce (sparse-fieldset vs client-side filtre).

---

## 6. Karar bekleyen açık sorular (dökümana geçmeden) — numaralı + öneri

> Bu kararlar **hangi dökümanın nasıl yazılacağını** belirler. "Önerilerin uygun" → önerilen varsayılanlarla ilerlenir.

1. **İki-katman sınırı (Tier 0 · Faz 1 kapsamı):** "değer atama & karşılaştırma" hem süreç adımı (motor) hem iş kuralı (frontend) olarak var. Sınır: **iş kuralı = anlık form UX (frontend) · adım = kalıcı/akış kararı (motor)** olarak kesinleşsin mi?
   → *Öneri: evet — motor yalnız adım-tipi değer/karşılaştırmayı yürütür; form-anı hesap frontend iş-kuralında kalır.*
2. **ViewProfile → response daraltma (Faz 2 çekirdek perf):** Detay/form okuması **server-side** olarak yalnız profilde görünür alanları mı döndürsün (sparse fieldset), yoksa tam `InstanceValue.data` dönüp client mı filtrelesin?
   → *Öneri: server-side sparse fieldset — istek `viewProfileId`/`wantedPropertyIds[]` verir, backend yalnız gerekeni döndürür (response boyutu + DB perf).*
3. **Compensation (F1.B.3):** Çok-adımlı geri-alma MVP'de mi, post-MVP mi?
   → *Öneri: post-MVP — MVP'de `onFail` yönlendirme + `failed` durak yeterli; compensation iskeleti sonra.*
4. **Scheduler lider-seçim (F1.C.1):** NATS KV lock mu, Postgres advisory lock mu?
   → *Öneri: Postgres advisory lock (durum zaten Postgres'te; ek altyapı yok) — NATS KV alternatif olarak notlanır.*
5. **`onFail` zorunluluğu (F1.B.2):** Her adımda `onFail` **zorunlu** mu, yoksa opsiyonel + varsayılan dead-letter→`failed` mi?
   → *Öneri: opsiyonel; tanımsızsa hata → süreç `failed` (dead-letter), global handler sonra.*
6. **`ApiKey` (F1.E.1):** Şimdi iskelet model mi, yoksa Customer API mekanizması kesinleşene kadar yer-tutucu mu?
   → *Öneri: şimdi iskelet (3 FK'yi bağlar) + detay Customer API fazına link.*
7. **Flovo AI (F1.D.4):** Motor-seviyesi AI adımı MVP'de mi?
   → *Öneri: post-MVP — Faz 1 kapsam dışı; §11 sonra doldurulur.*

---

## 7. İlgili dosyalar / kaynaklar

- **Motor:** [`bpmEngine/engine-runtime.md`](bpmEngine/engine-runtime.md) · [`bpmEngine/flovo-bpm-engine.md`](bpmEngine/flovo-bpm-engine.md)
- **API:** [`bpmEngine/settings-api.md`](bpmEngine/settings-api.md) · [`bpmEngine/flovo-customer-api.md`](bpmEngine/flovo-customer-api.md) · [`bpmEngine/service-settings/business-rule-endpoints.md`](bpmEngine/service-settings/business-rule-endpoints.md)
- **Davranış:** [`process-step.md`](bpmEngine/service-settings/process-step.md) · [`process-step-action.md`](bpmEngine/service-settings/process-step-action.md) · [`view-profile.md`](bpmEngine/service-settings/view-profile.md)
- **Modeller:** [`models/index.md`](bpmEngine/models/index.md) · [`processInstances/`](bpmEngine/models/processInstances/index.md) (runtime) · [`instance-value.md`](bpmEngine/models/processInstances/instance-value.md) · [`process-instance.md`](bpmEngine/models/processInstances/process-instance.md) · [`service-trigger.md`](bpmEngine/models/service-settings/service-trigger.md) · [`scheduler-job.md`](bpmEngine/models/organization-settings/scheduler-job.md)
- **Ayar şemaları:** [`process-step-settings/`](bpmEngine/models/service-settings/jsonTemplateModels/process-step-settings/index.md) · [`property-settings/`](bpmEngine/models/service-settings/jsonTemplateModels/property-settings/index.md)
- **Teknoloji:** [`nats-jetstream.md`](bpmEngine/tech-stack/nats-jetstream.md) · [`postgresql.md`](bpmEngine/tech-stack/postgresql.md) · [`api-contract.md`](bpmEngine/tech-stack/api-contract.md)
- **Açık kararlar:** [`bpmEngine/todo.md`](bpmEngine/todo.md) (Tier 0–3)

---

## 8. İlerleme takibi / sonraki adım

- **Nasıl işaretlenir:** Bir görev bitince `[ ]`→`[x]` yap + §2.0 durum panosundaki grup `x/y`'yi güncelle. Faz DoD sağlanınca panoda faz satırını ✅'le.
- **Devam noktası:** ➡️ **§6'daki 7 kararı ver** (ya da "önerilerin uygun") → ardından **F1.A.1 (`workflow_events` model dosyası)** ile Faz 1 yazımına başla.
- **📝 v0.44 (2026-08-31) — Faz 1 Grup A/B/C dokümanları TASLAK olarak yazıldı, kullanıcı incelemesi bekliyor:** F1.A.1 `workflow-event.md` · F1.A.2 `workflow-projection.md` ·
  F1.B.1–B.4 `engine-runtime-errors.md` (+ engine-runtime §5.2 çakışma sözleşmesi) · F1.C.1 `engine-runtime-scheduler.md` + `workflow-timer.md` (lider seçimi **gereksiz** — claim modeli;
  §6.4 önerisinin yerine geçer) · retention `engine-runtime-retention.md`. §6.3 (compensation post-MVP) ve §6.5 (`onFail` opsiyonel) önerileri **doğrultusunda** yazıldı.
  Kararlar/açık sorular ve bu konunun adım planı → **[`bpmEngine/engine-runtime-plan.md`](bpmEngine/engine-runtime-plan.md)**; inceleme bitince buradaki `[ ]`'ler ve §2.0 panosu güncellenir.

*Oluşturma: 2026-08-31. Bu plan dosyası ana dizindedir; motor geliştirmesine dönünce buradan başla.*
