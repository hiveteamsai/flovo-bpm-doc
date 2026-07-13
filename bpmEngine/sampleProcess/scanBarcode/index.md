# Örnek Süreç — Barkod Tara / Var Olanı Aç (scanBarcode) — İndeks

> **Amaç:** Bir **barkod** ile çalışan örnek süreç: kullanıcı barkodu tarar veya elle girer. Barkodla daha önce form oluşturulmuşsa **var olan form açılır** (Form Yönlendirme), yoksa **yeni form** üretilir. Karar, müşteri sunucusunun yanıtındaki **`response.action`** koduyla (`createForm` ↔ `yonlendir`) verilir.

## Dökümanlar
| Döküman | Özet |
|---|---|
| [`process.md`](./process.md) | Barkod akışı: `scanBarcode`/`eventForm` başlatma → HTTP Request → **`response.action` zinciri**; `yonlendir` → **Form Yönlendirme** (var olan form), `createForm` → **Instance Creator** (barkod init'li yeni form) → Kullanıcı. Detaylı spec (amaç · diyagram · adım/ayar/aksiyon · parametre akışı). |

> **Görsel:** `scanBarcode.jpg`.
