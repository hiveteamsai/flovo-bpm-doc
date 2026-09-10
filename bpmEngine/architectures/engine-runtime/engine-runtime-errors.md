# Flovo BPM Motoru — Hata & Dayanıklılık (retry · onFail · dead-letter · kurtarma · korumalar · compensation)

> **Durum:** 📝 TASLAK v0.44 — **onay bekliyor**. Kararlar/öneriler **R8–R12, R17**, açık sorular **Q7–Q13, Q21** → [`engine-runtime-plan.md`](./engine-runtime-plan.md).
> **Kapsam:** [`engine-runtime.md`](./engine-runtime.md) §6'nın tam spesifikasyonu; [`flovo-bpm-engine.md`](../engine-core/flovo-bpm-engine.md) §7 (`onFail`) ve
> [`service-settings/process-step-action.md`](../../service-settings/process-step-action.md) §5 (retry/onFail satırları) buraya delege eder.
> **Modeller:** [`WorkflowEvent`](../../models/processInstances/workflow-event.md) (`stepFailed`/`failed`/`recovered`/`cancelled`) ·
> [`WorkflowProjection`](../../models/processInstances/workflow-projection.md) (`attempt`/`lastError`/`autoStepRun`) · [`WorkflowTimer`](../../models/processInstances/workflow-timer.md) (`retry`) ·
> [`WorkflowErrorClass`](../../models/enums/workflow-error-class.md).
> **Kapsam dışı:** iş-kuralı (frontend) hata görünürlüğü → `service-settings/business-rule-engine.md`; sistem logları (Loki/OTel) → todo "denetim izi/loglama".

---

## 0. İlke (bir paragraf)
Hata, **adımın** bir çıktısıdır: her deneme ya `stepCompleted` ya `stepFailed` olayı üretir. `stepFailed` **sınıflandırılır**
(`transient` / `permanent` / `design` / `inDoubt` / `guard`); yalnız `transient` **yeniden denenir** (BPM-düzeyi backoff timer'ı). Denemeler bitince
veya sınıf kalıcıysa **adımın `onFail` aksiyonu** varsa akış o dala döner (hata bilgisi `parameters.error` ile taşınır); yoksa süreç **`failed`**
(dead-letter) olur — motor durur, **admin kurtarır** (`retry` / `skip` / `cancel`). Her şey **olay**dır; sessiz yutma yoktur.

## 1. Hata sınıflandırması (adım yürütücüsü karar verir)
Sınıf → [`WorkflowErrorClass`](../../models/enums/workflow-error-class.md). Adım tipine göre **tespit kuralları**:

| Adım tipi | `transient` | `permanent` | `design` |
|---|---|---|---|
| **HTTP Request** | 5xx · 408 · 429 · bağlantı/DNS/TLS hatası · istek zaman aşımı (`timeoutSeconds`, vars. 30 s) | 4xx (408/429 hariç) · response JSON parse/şema hatası · `action` kodu response'ta var ama adımda yok → **design** | `endpoint` boş · `DynamicParameter` çözümlenemedi |
| **Değer Atama / Karşılaştırma / Switch** | — (saf hesap) | ifade çalışma hatası (null bölme, tip uyumsuz) · `changeList` JSON Schema reddi | ifade derlenmiyor · property `code` yok |
| **Kullanıcı / Grup / Üst Form** (atama çözümü) | DB geçici hatası | atanan **boş** (yönetici tanımsız, property boş, grup boş) → `permanent` (→ process-step §3.15 KARAR) | `processViewProfileId` yok |
| **Bildirim** | kanal geçici hatası (SMTP 4xx, push servis 5xx) | alıcı çözülemedi · içerik şablon hatası | kanal tanımsız |
| **Instance Creator / Deleter / Custom ID** | DB geçici (deadlock, lock timeout) | hedef servis/instance yok · `deleteMode` uygulanamaz | ayar eksik |
| **Flovo AI** (post-MVP) | AI servisi 5xx/timeout | içerik reddi/şema | model tanımsız |
| **Süreç Adımı Tetikleme / Alt Süreç** | — | hedef süreç `failed` (async=false beklerken) | hedef adım/servis yok |
| **Herhangi** | NATS publish hatası · Postgres bağlantı düşmesi | — | aksiyonun `targetProcessStepId` eksik/arşivli |

- **Bilinmeyen exception** (yürütücü sınıflandıramadı) → `transient` sayılır **ama** en fazla **1** ek deneme; tekrar aynıysa `permanent`.
- **`guard`** motor tarafından üretilir (§7) — adım yürütücüsünden gelmez.

## 2. Retry politikası (yalnız `transient`)
### 2.1 Varsayılan değerler (öneri — Q7)
| Parametre | Varsayılan | Not |
|---|---|---|
| `maxAttempts` | **5** (ilk deneme dâhil → 4 retry) | |
| `initialDelaySeconds` | **10** | |
| `multiplier` | **3** | 10 s → 30 s → 90 s → 270 s |
| `maxDelaySeconds` | **600** | üst sınır |
| `jitter` | **±20 %** | thundering-herd önleme |
| Toplam en kötü süre | ≈ **6,7 dk** | ERP bakım penceresi için **kısa** olabilir → adım-bazlı override |

```text
delay(attempt) = min(maxDelaySeconds, initialDelaySeconds × multiplier^(attempt-1)) × U(0.8, 1.2)
```

### 2.2 Adım-bazlı override (öneri — Q7)
`ProcessStep`'e **ortak, nullable JSONB kolon** `retryPolicy { maxAttempts, initialDelaySeconds, multiplier, maxDelaySeconds }`
(tipe-özel `settings`'in **dışında** — her adım tipi için geçerli). `null` → sistem varsayılanı. `maxAttempts = 1` → retry kapalı.
_(Model dosyasına **onaydan sonra** eklenecek: `models/service-settings/process-step.md` §1.)_

### 2.3 Retry nerede bekler (R8)
- **BPM-düzeyi timer**, JetStream NAK-delay **değil**: `stepFailed(retryable=true, nextRetryAt)` + `suspended(waitReason=retry)` + `WorkflowTimer(kind=retry, dueAt=nextRetryAt)`.
  Timer dolunca `resume.v1` → worker `stepStarted(attempt+1)`.
- **Gerekçe:** dayanıklı (stream limitinden bağımsız) · **görünür** (admin: "3/5 deneme, sonraki 14:32") · timer/timeout ile **aynı mekanizma** · süreç
  `waiting`'de → worker serbest.
- **JetStream `MaxDeliver`** yalnız **altyapı çöküşü** korumasıdır (§3): aynı mesaj `MaxDeliver` (öneri **3**) kez teslim edilip hiç ACK'lenmediyse → worker
  mesajı **terminate** eder ve `failed(reason=inDoubt)` yazar (crash-loop). Retry sayacıyla **karışmaz** (Q8).

### 2.4 Retry sırasında durum
`executionState = waiting` · `waitReason = retry` · `WorkflowProjection.attempt` mevcut deneme · `nextRetryAt` dolu. Kullanıcı formu görür (`Instance.statusId`
değişmez), aksiyon **alamaz** (`InstanceAwaitingUser` boş). Admin "retry bekleyenler" listesinde görür; **erken tetikleme** (`retry now`) = kurtarma modu `retry` (§6).

## 3. Yan-etki güvenliği (`stepStarted` · in-doubt) — R4
Otomatik adım **iki TX**'tir (→ workflow-event §3.2): `stepStarted` commit → yan etki → `stepCompleted`/`stepFailed` commit. Redelivery geldiğinde:

| Görülen | Anlam | Davranış |
|---|---|---|
| `stepStarted` yok | ilk teslim | normal çalıştır |
| `stepStarted` var, sonuç var | zaten işlendi | ACK, atla (idempotency) |
| `stepStarted` var, **sonuç yok** | worker yan etki sırasında/sonrasında çöktü → **in-doubt** | adım tipi **idempotent** ise yeniden koş (`attempt` aynı, `stepStarted` tekrar yazılmaz); değilse `stepFailed(errorClass=inDoubt)` → `onFail`/`failed` |

**İdempotent kabul edilen adımlar** (öneri — Q21): Değer Atama · Karşılaştırma · Switch · Kullanıcı/Grup atama çözümü · Süreç Bitişi · Timer Start/End ·
Custom ID Creator (**aynı** id'yi üretiyorsa). **İdempotent olmayan:** HTTP Request (hedef `Idempotency-Key` desteklemiyorsa) · Bildirim · Instance Creator/Deleter ·
Flovo AI. HTTP Request'te **`idempotencyKeyHeader`** ayarı (öneri) verilirse motor `attempt`-bağımsız sabit anahtar gönderir → idempotent sayılır.

## 4. `onFail` çözümleme sırası (R9)
`stepFailed` **retry edilmeyecekse** (kalıcı sınıf **veya** `maxAttempts` tükendi):

1. **Adımın `onFail` kodlu `ProcessStepAction`'ı var mı?** → var: o aksiyon **seçilir** (`stepCompleted(selectedActionCode=onFail)`), hedef adım için `step_ready`.
   Hata bilgisi **`ActionTransfer.parameters.error`** ile taşınır (§4.1). `onFail` hedefi geçersizse (`design`) → 3.
2. **Servis-düzeyi global hata adımı** (`Service.onFailProcessStepId`, **post-MVP** — Q10): tanımlıysa 1 gibi davranır; hedef adım servisin herhangi bir adımı.
3. **Yok** → **`failed`** (§5).

- **`onFail` opsiyoneldir** (zorunlu değil) — build-plan §6.5 önerisiyle uyumlu. Designer uyarısı: yan etkili adımlarda (HTTP Request) `onFail` tanımlanmamışsa **tasarım-zamanı uyarı** (engel değil).
- **`guard`** sınıfı `onFail`'e **gitmez** (döngü onFail dalında da sürebilir) → doğrudan `failed`.
- **`onFail` dalı da hata verirse** → aynı kural o adım için çalışır (onFail zinciri); zincir `autoStepRun` limitiyle (§7) sınırlıdır.

### 4.1 Hata parametreleri (R10)
`onFail` ile ilerleyen `ActionTransfer`:
```jsonc
{
  "parameters": {
    "error": {
      "stepCode": "callErp",            // hatayı üreten adım
      "errorClass": "permanent",
      "errorCode": "http.4xx",          // motor kataloğu (http.5xx · http.4xx · http.timeout · expr.runtime · assign.unresolved · schema.changeList …)
      "message": "ERP returned 422",    // kısa, kişisel-veri-siz
      "httpStatus": 422,
      "attempts": 1,
      "at": "2026-08-31T11:02:14Z"
    }
  },
  "changeList": {},                     // onFail forma yazmaz (istenirse hedef adım Değer Atama ile yazar)
  "action": null
}
```
`mergeParameter=true` ise gelen parametreler korunur, `error` eklenir. `parameters.error` **rezerve anahtar**dır (Değer Atama ile okunabilir: `parameters.error.message`).

## 5. Dead-letter → `failed` (R9)
- Olay: `failed{ reason: noOnFail | retryExhausted | design | guard | inDoubt }` · `executionState = failed` · `WorkflowProjection.lastError` · `InstanceAwaitingUser` **temizlenir** ·
  bekleyen `WorkflowTimer`'lar `cancelled(processEnded)` **değil** → `failed`'da timer'lar **askıya alınmaz, iptal edilir** (kurtarma yeniden kurar).
- NATS: `flovo.workflow.failed.v1` → **bildirim**: organizasyon **süreç yöneticisi** grubuna (permissions'ta yeni yetki → Q12) + designer'a (`design` sınıfında).
- Kullanıcı görünümü: form **açılır**, `Instance.statusId` **değişmez** (son iş durumu kalır); banner "süreç hatası — yönetici inceliyor" (FE; `executionState` okur).
- `failed` süreç **kaynak tutmaz**; süresiz bekleyebilir (retention: `failed` süreçler saklama hesabında **aktif** sayılır → retention §2).

## 6. Kurtarma (recovery) — R11
Yalnız `failed` (ve iptal için `waiting`) süreçlerde; **yetkili** admin (Q12). Her kurtarma bir **olaydır** — projeksiyon elle düzenlenmez.

| Mod | Ne yapar | Olaylar | Kısıt |
|---|---|---|---|
| **`retry`** | Hatalı adımı **yeniden koşar** (`attempt` = son+1; sayaç sıfırlanmaz ama limit **yeniden** uygulanır) | `recovered(mode=retry)` → `stepStarted` … | `inDoubt`'ta admin "yan etki oldu mu" bilgisini **kendisi** teyit eder |
| **`skip`** | Hatalı adımı **atlar**, admin'in seçtiği **aksiyon koduyla** ilerler (adımın mevcut aksiyonlarından biri; `onFail` dâhil) | `recovered(mode=skip, selectedActionCode)` → `step_ready` | `changeList` boş; istenirse admin `parameters` verir |
| **`cancel`** | Süreci **iptal** eder (BİTİŞ'e ulaşmaz) | `cancelled` · `executionState = cancelled` (Q6) | `Instance.statusId` **değişmez** (iş durumu ayrı); istenirse ayrı "iptal" statüsü **tasarımda** verilir |
| **`retry now`** | `waiting(retry)` süreçte backoff'u beklemeden dener | timer `cancelled(rearmed)` → `recovered(mode=retry)` | `failed` değil, `waiting` |

- API (öneri, Customer/Admin API'de sonra somutlanır): `POST /process-instances/{id}/recover { mode, selectedActionCode?, parameters?, note? }`.
- **Kim yapabilir:** yeni org-yetkisi **`processAdminUserGroupId`** (öneri; permissions genişletilebilirlik sorusuyla birlikte → Q12).

## 7. Döngü / derinlik korumaları (`guard`) — R17
| Koruma | Sayaç | Varsayılan limit (öneri — Q13) | Aşılınca |
|---|---|---|---|
| **Ardışık otomatik adım** (insan/timer beklemesi olmadan) | `WorkflowProjection.autoStepRun` (her `suspended`'da 0) | **200** | `failed(guard)` — aksiyon zinciri sonsuz döngüsü (A→B→A) |
| **Toplam adım** | `WorkflowProjection.totalSteps` | **10 000** | `failed(guard)` |
| **Alt süreç derinliği** | `parentProcessInstanceId` zincir uzunluğu (startRequested anında) | **8** | alt süreç **başlatılmaz**; tetikleyen adım `stepFailed(guard)` |
| **Senkron (`async=false`) bekleme derinliği** | iç içe `waitReason=subProcess` | **3** | tetikleme `permanent` hata |
| **ServiceTrigger kaskadı** (A→B→A) | aynı `correlationId` içinde aynı `serviceTriggerId` tetik sayısı | **20** | trigger **ateşlenmez**, `failed(guard)` **değil** — yalnız log + admin bildirimi (ana süreç zarar görmez) |
| **Worker turu süresi** | adım yürütme zaman aşımı | **60 s** (HTTP `timeoutSeconds` ≤ 30 s vars.) | `stepFailed(transient, errorCode=step.timeout)` |

Limitler **sistem konfigürasyonu**dur (org-bazlı değil); `guard` sınıfı `onFail`'e gitmez (§4).

## 8. Compensation / telafi — post-MVP (R12)
MVP'de **yok**: `onFail` yönlendirmesi + `failed` durağı + admin kurtarma yeterli. Post-MVP iskelet (kararı şimdi almak, tasarımı sonra):
- Adım tasarımına **opsiyonel** `compensationProcessStepId` (aynı serviste bir adım) — "bu adım başarıyla koştuysa ve süreç sonradan `cancelled`/`failed→cancel` olursa şunu koş".
- Motor `cancel`'da tamamlanan adımları **ters sırayla** gezer, compensation tanımlı olanlar için ayrı bir **compensation kolu** (`ProcessInstance` içinde `compensating` alt durumu) koşar; her biri normal adım gibi olay üretir.
- Saga koordinasyonu için `workflow_events` zaten yeterli (hangi adımlar tamamlandı = `stepCompleted` listesi).

## 9. İzleme (özet)
Metrikler: `stepFailed` oranı (sınıf × adım tipi) · `failed` süreç sayısı (org) · retry kuyruğu (`waitReason=retry`) · in-doubt sayısı · guard tetik sayısı.
Alarm: `design` sınıfı ilk görüldüğünde (designer'a) · `failed` > eşik/saat · crash-loop (`MaxDeliver` aşımı).

## 10. Açık noktalar → [`engine-runtime-plan.md`](./engine-runtime-plan.md) §3
Q7 retry değerleri + `retryPolicy` kolonu · Q8 `MaxDeliver` · Q10 global hata adımı MVP/post-MVP · Q11 compensation iskeleti · Q12 kurtarma yetkisi ·
Q13 guard limitleri · Q21 idempotent adım listesi + HTTP `idempotencyKeyHeader`.

---

*Oluşturma: 2026-08-31 (v0.44). engine-runtime §6 doldurma.*
