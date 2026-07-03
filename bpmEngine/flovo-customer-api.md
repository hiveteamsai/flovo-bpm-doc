# Flovo Customer API — Tasarım (Taslak)

> **Durum:** 🟡 TASLAK — şimdilik **endpoint listesi + teorik iş özeti**; request/response detayları sonra.
> **Amaç:** Müşterilerin/kullanıcıların **custom code** geliştirebilmesi için Flovo'nun sağlayacağı **API servisi.**
> Süreç adımlarındaki **HTTP Request** (→ `servis-ayarlari/process-step.md` §3.2) müşteri sunucusundaki custom code'a istek atar;
> custom code da **Flovo Customer API** ile Flovo formlarını okur/yazar ve **Webhook** aksiyonlarını (→ `servis-ayarlari/process-step-action.md` §3.6) tetikler.
>
> **İlişki:** Örnekler → `sampleProcess/` (createPdf, createPdfAsync, integration, scanBarcode bu API'ye dayanır).

---

## 0. Genel İlkeler (teorik)
- **Kimlik:** custom code, bir **token** ile kimliklenir; kapsam **organization / solution / service** bazlıdır
  (header'lar: `organizationId` / `solutionId` / `serviceId`). _(**Geçici**: dış referans anahtarının int `organizationId` mi yoksa string `organizationCode` mi olacağı **açık** → §3.)_
- **Birim:** çoğu uç **servis (form)** ve **form id** etrafında çalışır.
- **Yön:** custom code → Flovo (okuma/yazma) **ve** custom code → Flovo (**webhook aksiyonu tetikleme**).

---

## 1. Endpoint'ler (özet)
> İmza/yol **temsilîdir**; isimlendirme sonra netleşecek. Her satır = **uç + teorik iş**.

### Kimlik
| Uç (temsilî) | Ne yapar |
|---|---|
| `POST /auth/token` | Custom code için **erişim token'ı** üretir (organization/solution/service kapsamlı). |

### Form okuma
| Uç (temsilî) | Ne yapar |
|---|---|
| `GET /forms/{formId}` | Bir formun **tüm alan değerlerini + meta**'sını (durum, oluşturan, tarih) getirir. _(PDF üretimi form bilgisini buradan çeker.)_ |
| `POST /forms/search` | Bir serviste **alan değerine göre form arar** (örn. `barcode = X` olan form var mı). _(scanBarcode.)_ |
| `GET /services/{serviceId}/forms` | Bir servisin formlarını **listeler** (filtre/sayfalama). |
| `GET /services/{serviceId}/schema` | Servisin **alan (property) şemasını** getirir (custom code alan adlarını/tiplerini bilsin). |

### Form yazma
| Uç (temsilî) | Ne yapar |
|---|---|
| `POST /forms` | **Yeni form oluşturur** (servis + başlangıç alan değerleri). |
| `PATCH /forms/{formId}` | Formun **alan değerlerini günceller** (`changeList` benzeri). |
| `POST /forms/{formId}/status` | Formun **durumunu** değiştirir (→ `genel-ayarlar/status.md`). |
| `DELETE /forms/{formId}` | Formu **siler** (`deleted` durumuna çeker). |

### Dosya
| Uç (temsilî) | Ne yapar |
|---|---|
| `POST /files` | **Dosya/görsel yükler** (thumbnail vb.); erişim **url**'i döner. |
| `GET /files/{fileId}` | Dosyayı **indirir**. |

### Aksiyon / Webhook tetikleme
| Uç (temsilî) | Ne yapar |
|---|---|
| `POST /forms/{formId}/actions/{actionCode}` | Bir formda **aksiyon tetikler** (Webhook aksiyonu) — **`parameters`** ile. Süreci ilerletir. _(createPdfAsync, integration.)_ |

### Kullanıcı / organizasyon
| Uç (temsilî) | Ne yapar |
|---|---|
| `GET /users/{userId}` | Kullanıcı bilgisi (ad, e-posta, departman, ünvan, yönetici). |
| `GET /me` | Token sahibinin/aktif bağlamın bilgisi. |

---

## 2. Örneklerle Eşleşme
| Örnek | Kullanılan uç(lar) (teorik) |
|---|---|
| **createPdf / createPdfAsync** | `GET /forms/{id}` (form bilgisi) · `POST /files` (PDF) · `POST .../actions/{code}` (async'te webhook) |
| **integration** | `GET /forms/{id}` / `PATCH /forms/{id}` (aktarım) · `POST .../actions/{code}` (webhook → süreç bitişi) |
| **scanBarcode** | `POST /forms/search` (barcode'la form ara) |

---

## 3. Açık Kararlar / Sorular
- [ ] Kimlik/yetki modeli: token kapsamı, süresi, yenileme; per-service mi per-solution mı?
- [ ] **Dış referans anahtarı:** API çağrılarında kiracı `organizationId` (int) ile mi yoksa `organizationCode` (string) ile mi belirtilmeli? (`genel-ayarlar/organization.md` §2 dış referanslarda `code` diyor.)
- [ ] **Webhook tetikleme** güvenliği (secret/imza) ve **idempotency** (aynı webhook iki kez gelirse).
- [ ] `POST /forms/search` sorgu dili (alan + operatör — `servis-ayarlari/properties.md` / `servis-ayarlari/work-rule.md` operatörleriyle hizalı mı?).
- [ ] Rate limit / sayfalama / hata sözleşmesi (standart response zarfı).
- [ ] Request/response **şemalarının** detayı (sonraki aşama).

---

*Oluşturma: 2026-06-30 · `sampleProcess/` örneklerinden türetilen ihtiyaçlarla; endpoint + teorik iş özeti (detay sonra).*
