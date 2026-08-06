# Model — ReflectionLink (yansıma yayılım bağı — parentProperty A′)

> **Durum:** 🟡 TASLAK — değer-saklama mimarisinden türetildi (→ `../../research/property-value-storage/form-deger-saklama-v2.html`); alanlar gözden geçirilecek.
> **Yeni model.**
> **Amaç:** Bir **üst (parent) alan** değişince hangi **alt (child) alan kopyalarının** tazeleneceğini bulmak için tutulan
> bağ. Yalnız `parentProperty` tipi + `reflectionMode=materialized` (**A′**) alanlar için geçerlidir — üst değer değiştikçe
> child'daki materialized kopya arka planda güncellenir (hem canlı hem raporlanabilir yansıma).

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Bağ kaydı ID'si. |
| `organizationId` | int | (denormalize) | Kiracı — **RLS/tenant izolasyonu** (yayılım sorgusu tenant'a scope'lanır; kardeş değer tablolarıyla hizalı). |
| `parentInstanceId` | int | FK → Instance.id | Kaynak (üst) form. |
| `parentPropertyCode` | string | — | Kaynak alan (`Property.code`) — **`code`-keyed**. |
| `childInstanceId` | int | FK → Instance.id | Hedef (alt) form — kopyanın tazeleneceği. |
| `childPropertyCode` | string | — | Hedef kopya alanı (`Property.code`) — **`code`-keyed**. |

> **Benzersizlik:** `(parentInstanceId, parentPropertyCode, childInstanceId, childPropertyCode)` **benzersiz** — aynı bağ mükerrer
> eklenmemeli (aksi hâlde tazeleme/fan-out tekrarlanır).

## İlişkiler
- **N – 1** → `Instance` (`parentInstanceId` = kaynak, `childInstanceId` = hedef).
- **N – 1** (mantıksal) → `Property` (`parentPropertyCode`/`childPropertyCode` — `code` üzerinden, id-FK değil).

## Notlar / açık noktalar
- **Yalnız `materialized` (A′) için:** Yansıma varsayılanı **A′ değildir**. `parentProperty.reflectionMode`
  (→ [`../enums/reflection-mode.md`](../enums/reflection-mode.md)) yalnızca **`materialized`** seçildiğinde bu bağ kurulur.
  Diğerleri: **`snapshot`** (A) = yazımda kopyalanıp dondurulur (bağ gerekmez) · **`live`** (B) = okurken join/referans (kopya yok).
- **Yayılım akışı (A′):** parent `InstanceValue` update → outbox → **reflection-propagation consumer** `ReflectionLink`'ten
  child'ları bulur → her child'ın `InstanceValue`'sunu tazeler → child'ın kendi outbox'ı → Attr yeniden yansır.
- **Zorunlu sınırlar:** **derinlik limiti · döngü tespiti · asenkron** yürütme (fan-out maliyeti pahalıdır; sınır tasarımı
  → `../../todo.md`, motor döngü koruması **O3** ile bağlantılı).
- **Kaynak mimari:** → `../../research/property-value-storage/form-deger-saklama-v2.html` (§6.6 · §14 yansıma).

*Oluşturma: 2026-08-04.*
