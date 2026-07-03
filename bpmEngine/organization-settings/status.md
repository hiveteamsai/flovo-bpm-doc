# Flovo — Durumlar (Statuses) Tasarımı

> **Durum:** 🟢 DETAYLANIYOR
> **Amaç:** Bir kaydın **mevcut aşamasını** gösteren **durum (status)** varlığını tanımlamak.
> (Adım tipleri → `../service-settings/process-step.md`; aksiyonlar → `../service-settings/process-step-action.md`; renk/görünüm → `style.md`.)
>
> **İlişki:** Aksiyon tetiklendiğinde durum değişebilir (`../service-settings/process-step-action.md` §1.2); durumun rengi/görünümü bir
> **Style** varlığıdır (`style.md`).

---

## 0. Durum Nedir?
Bir **durum (status)**, BPM sürecindeki bir kaydın **mevcut aşamasını** temsil eden etikettir (örn. *Beklemede*,
*Onaylandı*, *Reddedildi*). Görsel gösterim, **filtreleme** ve **raporlama** için kullanılır. Bir **aksiyon**
tetiklendiğinde kaydın durumu değişebilir.

---

## 1. Durum Veri Modeli
| Alan | Tip | Açıklama |
|---|---|---|
| `id` | int | Durum ID'si (primary key) |
| `organizationId` | int | Sahibi organizasyon (FK → `organization.md` `id`); **organizasyon havuzu** — tüm servislerde kullanılır |
| `code` | string | Durum kodu (benzersiz tanımlayıcı) |
| `definition` | string | Durum **adı** — kullanıcıya görünen (örn. "Beklemede", "Onaylandı") |
| `icon` | string | İkon |
| `styleId` | int | Renk/görünüm (bg + font) — **Style** varlığına FK referans (`style.md`) |

---

## 2. Durum Nasıl Oluşturulur?
1. Durum **`definition`** ile adlandırılır (örn. *Beklemede*, *Onaylandı*, *Reddedildi*).
2. Bir **`styleId`** seçilir (`style.md`'den — renk/görünüm).
3. Durum **organizasyona eklenir** (organizasyon havuzu; o organizasyonun tüm servislerinde kullanılır).

---

## 3. Durum Değişimi (aksiyonla)
- Bir **aksiyon** tetiklendiğinde kaydın durumu otomatik değişebilir (adım-aksiyon binding'inde **`changeStatusId`**
  → `../service-settings/process-step-action.md` §1.2).
- Kayıtlar listelenirken durum **ikon + renk (style)** ile gösterilir; kullanıcılar duruma göre **filtreleyebilir**.

**Örnek akış:**
```
[Taslak] ──Onaya Gönder──▶ [Onay Bekliyor] ──Onayla──▶ [Onaylandı]
                                            └─Reddet──▶ [Reddedildi]
```

---

## 4. Açık Kararlar / Sorular
- [x] **`icon` ↔ `styleId`** — `icon` **ve** `definition` frontend'de `styleId`'nin **`fontColor`**'ını kullanır (`bgColor` = etiket arka planı). Ayrı renk alanı yok.
- [ ] Raporlama/filtreleme için bir **kategori/grup** boyutu gerekir mi, yoksa `code`/`definition` yeterli mi?
- [x] Durumlar **organizasyon-bazlı** (havuz) tanımlanır; organizasyonun tüm servislerinde kullanılır.

---

## 5. Notlar / Ham Düşünceler
> _(Buraya ham düşünceler; sonra yukarı işlenir.)_

---

*Oluşturma: 2026-06-26.*
