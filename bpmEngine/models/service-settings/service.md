# Model — Service (servis / form)

> **Durum:** 🟡 TASLAK (alanlar başlangıç — detaylandırılacak)
> **Amaç:** Bir **iş sürecinin/formun** tamamı (örn. İzin Talebi, Masraf). Motorun temel birimi. Bir **solution
> altında** oluşturulur; **kendi ayarlarını** (property, görüntüleme profili, süreç adımı, iş kuralı) barındırır.
> **Hiyerarşi:** `Organization → Solution → Service → {Property · ProcessViewProfile · ProcessStep · WorkRule}`.

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Servis ID'si. |
| `solutionId` | int | FK → Solution.id | Bağlı solution (organizasyon buradan türetilir). |
| `code` | string | benzersiz | Servis kodu (izolasyon başlığı `serviceId`; dış referans). |
| `definition` | string | — | Servis (form) adı/tanımı. |

## İlişkiler
- **N – 1** → `Solution` (`solutionId`) → (dolaylı) `Organization`.
- **1 – N** ← `Property`, `ProcessViewProfile`, `ProcessStep`, `WorkRule` (hepsi `serviceId`).
- **Kullanır (organizasyon havuzu):** `Action`, `Status`, `Style`, `Translation` — organizasyona bağlı bu veriler,
  bu servisin modellerinde **kullanılabilir** (örn. adıma aksiyon eklerken `Action` alanları `ProcessStepAction`'a
  **kopyalanır**; durum `ProcessStepAction.changeStatusId` ile atanır).

## İzolasyon
Çalışma zamanı kayıt izolasyonu **üç başlık**: `organizationId` · `solutionId` · `serviceId` (→ `../../flovo-bpm-engine.md` §9).

## Notlar / açık noktalar
- Ek alanlar (ikon, thumbnail, durum, versiyon, yetki) ve **Solution** modeli detaylandırılacak → `../../todo.md`.

*Oluşturma: 2026-07-02.*
