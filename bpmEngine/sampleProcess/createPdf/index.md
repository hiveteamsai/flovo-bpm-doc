# Örnek Süreç — PDF Oluşturma / Senkron (createPdf) — İndeks

> **Amaç:** Bir formun bilgisinden **müşteri sunucusunda** PDF üretip sonucu kullanıcıya bildiren örnek süreç. **HTTP Request `async = false`** (senkron) kullanımını gösterir: süreç PDF üretimi bitene kadar **bekler**, sonucu alıp ilerler.

## Dökümanlar
| Döküman | Özet |
|---|---|
| [`process.md`](./process.md) | Senkron PDF üretimi: HTTP Request (`async=false`) ile dış sunucuya istek → **bekle** → başarıda `default` → Bildirim → Kullanıcı. Detaylı spec (amaç · diyagram · adım/ayar/aksiyon · parametre akışı). |

> **Görsel:** `createPdf.jpg` (PDF üretim bölümü).
