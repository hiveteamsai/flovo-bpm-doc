# Flovo — Durumlar (Statuses) Tasarımı

> **Durum:** 🟢 DETAYLANIYOR
> **Amaç:** Bir kaydın **mevcut aşamasını** gösteren **durum (status)** varlığını tanımlamak.
> (Adım tipleri → `../servis-ayarlari/process-step.md`; aksiyonlar → `../servis-ayarlari/process-step-action.md`; renk/görünüm → `style.md`.)
>
> **İlişki:** Aksiyon tetiklendiğinde durum değişebilir (`../servis-ayarlari/process-step-action.md` §1.2); durumun rengi/görünümü bir
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
| `code` | string | Durum kodu (benzersiz tanımlayıcı) |
| `definition` | string | Durum **adı** — kullanıcıya görünen (örn. "Beklemede", "Onaylandı") |
| `icon` | string | İkon |
| `style` | ref → Style | Renk/görünüm (bg + font) — **Style** varlığına referans (`style.md`) |

---

## 2. Durum Nasıl Oluşturulur?
1. Durum **`definition`** ile adlandırılır (örn. *Beklemede*, *Onaylandı*, *Reddedildi*).
2. Bir **`style`** seçilir (`style.md`'den — renk/görünüm).
3. Durum **servise eklenir** (servis-bazlı tanımlanır).

---

## 3. Durum Değişimi (aksiyonla)
- Bir **aksiyon** tetiklendiğinde kaydın durumu otomatik değişebilir (adım-aksiyon binding'inde **`changeStatusId`**
  → `../servis-ayarlari/process-step-action.md` §1.2).
- Kayıtlar listelenirken durum **ikon + renk (style)** ile gösterilir; kullanıcılar duruma göre **filtreleyebilir**.

**Örnek akış:**
```
[Taslak] ──Onaya Gönder──▶ [Onay Bekliyor] ──Onayla──▶ [Onaylandı]
                                            └─Reddet──▶ [Reddedildi]
```

---

## 4. Açık Kararlar / Sorular
- [ ] **`icon` ↔ `style`** — ikon ayrı alan; style bg+font. İkon rengi style'dan mı gelir, ayrı mı? (→ `style.md` §4)
- [ ] Raporlama/filtreleme için bir **kategori/grup** boyutu gerekir mi, yoksa `code`/`definition` yeterli mi?
- [ ] Durumlar servis-bazlı mı, paylaşımlı (çözüm/hesap) mı tanımlanır?

---

## 5. Notlar / Ham Düşünceler
> _(Buraya ham düşünceler; sonra yukarı işlenir.)_

---

*Oluşturma: 2026-06-26.*
