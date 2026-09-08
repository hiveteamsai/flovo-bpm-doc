# Flovo Customer API — Tasarım (Taslak)

> **Durum:** 🟡 TASLAK — şimdilik **endpoint listesi + teorik iş özeti**; request/response detayları sonra.
> ⏭️ **Kapsam: MVP-sonrası (Faz 2, KARAR v0.47)** — bu API MVP'de inşa edilmez; açık soruları [`todo-phase2.md`](./todo-phase2.md) §13'te. Frontend'in kullandığı motor runtime uçları bu dokümanın kapsamı **değildir** (→ `bpm-engine-build-plan.md` F1.E.3 · F2.G).
> **Amaç:** Müşterilerin/kullanıcıların **custom code** geliştirebilmesi için Flovo'nun sağlayacağı **API servisi.**
> Süreç adımlarındaki **HTTP Request** (→ `service-settings/process-step.md` §3.2) müşteri sunucusundaki custom code'a istek atar;
> custom code da **Flovo Customer API** ile Flovo **instance**'larını (doldurulmuş form kayıtları) okur/yazar ve **Webhook** aksiyonlarını (→ `service-settings/process-step-action.md` §3.6) tetikler.
>
> **İlişki:** Örnekler → `sampleProcess/` (createPdf, createPdfAsync, integration, scanBarcode bu API'ye dayanır).

---

## 0. Genel İlkeler (teorik)
- **Kimlik:** custom code, bir **token** ile kimliklenir; kapsam **organization / solution / service** bazlıdır
  (header'lar: `organizationId` / `solutionId` / `serviceId`). _(**Geçici**: dış referans anahtarının int `organizationId` mi yoksa string `organizationCode` mi olacağı **açık** → §3.)_
- **Birim:** çoğu uç **servis (form)** ve **instance id** etrafında çalışır.
- **Yön:** custom code → Flovo (okuma/yazma) **ve** custom code → Flovo (**webhook aksiyonu tetikleme**).
- **İş kuralları çalışmaz (İki-katman sınırı):** API/webhook ile oluşturulan/güncellenen instance'lar **frontend'den geçmediğinden**
  iş kuralları (değer atama, validasyon, veri-kaynağı doldurma) **çalışmaz** — yazılan değerler yalnız **JSON Schema** ile doğrulanır.
  Akış-kritik hesap/validasyon gerekiyorsa bunları **motor süreç adımı** olarak kurmak **süreç tasarımcısının sorumluluğundadır**
  (→ `service-settings/business-rule.md` §0.1, karar S3).

---

## 1. Endpoint'ler (özet)
> İmza/yol **temsilîdir**; isimlendirme sonra netleşecek. Her satır = **uç + teorik iş**.

### Kimlik
| Uç (temsilî) | Ne yapar |
|---|---|
| `POST /auth/token` | Custom code için **erişim token'ı** üretir (organization/solution/service kapsamlı). |

### Instance okuma
| Uç (temsilî) | Ne yapar |
|---|---|
| `GET /instances/{instanceId}` | Bir instance'ın **tüm alan değerlerini + meta**'sını (durum, oluşturan, tarih) getirir. _(PDF üretimi instance bilgisini buradan çeker.)_ |
| `POST /instances/search` | Bir serviste **alan değerine göre instance arar** (örn. `barcode = X` olan instance var mı). _(scanBarcode.)_ |
| `GET /services/{serviceId}/instances` | Bir servisin instance'larını **listeler** (filtre/sayfalama). |
| `GET /services/{serviceId}/schema` | Servisin **alan (property) şemasını** getirir (custom code alan adlarını/tiplerini bilsin). |

### Instance yazma
| Uç (temsilî) | Ne yapar |
|---|---|
| `POST /instances` | **Yeni instance oluşturur** (servis + başlangıç alan değerleri). |
| `PATCH /instances/{instanceId}` | Instance'ın **alan değerlerini günceller** (`changeList` benzeri). |
| `POST /instances/{instanceId}/status` | Instance'ın **durumunu** değiştirir (→ `organization-settings/status.md`). |
| `DELETE /instances/{instanceId}` | Instance'ı **siler** (`deleted` durumuna çeker). |

### Dosya
| Uç (temsilî) | Ne yapar |
|---|---|
| `POST /files` | **Dosya/görsel yükler** (thumbnail vb.); erişim **url**'i döner. |
| `GET /files/{fileId}` | Dosyayı **indirir**. |

### Aksiyon / Webhook tetikleme
| Uç (temsilî) | Ne yapar |
|---|---|
| `POST /instances/{instanceId}/actions/{actionCode}` | Bir instance'ta **aksiyon tetikler** (Webhook aksiyonu) — **`parameters`** ile. Süreci ilerletir. _(createPdfAsync, integration.)_ **📝 v0.44 çakışma/idempotency sözleşmesi (öneri):** header **`Idempotency-Key`** (zorunlu — plan Q17) → aynı anahtar **200 replay**; başkası ilerletmiş → **409 `processAlreadyAdvanced`**; eski görünüm → **409 `staleView`**; atanmamış → **403 `notAssigned`**; süreç beklemiyor → **409 `notAwaitingAction`**; aksiyon kodu yok → **422 `unknownAction`**. Tam tablo → [`engine-runtime.md`](./engine-runtime.md) §5.2. |
| `POST /process-instances/{processInstanceId}/recover` | **📝 v0.44 (öneri, admin):** `failed` süreçte kurtarma — `{ mode: retry \| skip \| cancel, selectedActionCode?, parameters?, note? }`; her mod bir **olay** (`recovered`/`cancelled`). Yetki → plan Q12. Tam kural → [`engine-runtime-errors.md`](./engine-runtime-errors.md) §6. |

### Kullanıcı / organizasyon
| Uç (temsilî) | Ne yapar |
|---|---|
| `GET /users/{userId}` | Kullanıcı bilgisi (ad, e-posta, departman, ünvan, yönetici). |
| `GET /me` | Token sahibinin/aktif bağlamın bilgisi. |

---

## 2. Örneklerle Eşleşme
| Örnek | Kullanılan uç(lar) (teorik) |
|---|---|
| **createPdf / createPdfAsync** | `GET /instances/{id}` (instance bilgisi) · `POST /files` (PDF) · `POST .../actions/{code}` (async'te webhook) |
| **integration** | `GET /instances/{id}` / `PATCH /instances/{id}` (aktarım) · `POST .../actions/{code}` (webhook → süreç bitişi) |
| **scanBarcode** | `POST /instances/search` (barcode'la instance ara) |

---

## 3. Açık Kararlar / Sorular

> **Açık sorular tek yerde:** Bu dokümanın açık kararları/soruları, tutarsızlığı önlemek için **yalnız** merkezi
> [`todo.md`](todo.md) dosyasında toplanır (önceliklendirilmiş tüm-doküman listesi). İlgili maddeler orada `(flovo-customer-api §..)`
> atfıyla bulunur; verilen kararlar bu dokümanın **gövdesinde** anlatılır.

---

*Oluşturma: 2026-06-30 · `sampleProcess/` örneklerinden türetilen ihtiyaçlarla; endpoint + teorik iş özeti (detay sonra).*
