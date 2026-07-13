# Örnek Süreç — PDF Oluşturma / Asenkron (createPdfAsync) — İndeks

> **Amaç:** `createPdf` ile aynı işi (PDF üretimi) **kullanıcıyı bekletmeden** yapan örnek süreç. **HTTP Request `async = true`** ile istek atılıp dönüş beklenmez; müşteri sunucusu PDF'i bitirince **Flovo Customer API** üzerinden **bağımsız bir alt süreci** (webhook) tetikleyerek bildirim kolunu çalıştırır.

## Dökümanlar
| Döküman | Özet |
|---|---|
| [`process.md`](./process.md) | Asenkron PDF: HTTP Request (`async=true`) → beklemeden ilerle; PDF hazır olunca Customer API → **Webhook** → bağımsız alt süreç (Alt Süreç Başlangıcı) → Bildirim. Detaylı spec (amaç · diyagram · adım/ayar/aksiyon · parametre akışı). |

> **Görsel:** `createPdfAsync.jpg` (asenkron akış + webhook geri dönüş kolu).
