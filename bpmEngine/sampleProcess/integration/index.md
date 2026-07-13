# Örnek Süreç — Entegrasyon / Asenkron Aktarım (integration) — İndeks

> **Amaç:** Bir kaydı **dış bir sisteme aktaran** (entegrasyon) örnek süreç. Aktarım uzun sürebildiğinden **asenkron** yürütülür: **HTTP Request `async = true`** ile başlatılır, kayıt **"Aktarım Bekleniyor"** durumuna alınır (loading yok, kullanıcı formu normal görür) ve dış sistemden **Webhook** ile sonuç beklenir.

## Dökümanlar
| Döküman | Özet |
|---|---|
| [`process.md`](./process.md) | Asenkron entegrasyon: HTTP Request (`async=true`) → **Processing (`showLoading=false`, durum güncelle)** → **Webhook** ile sonuç; başarı → Süreç Bitişi, başarısız → başa dön. Detaylı spec (amaç · diyagram · adım/ayar/aksiyon · parametre akışı). |

> **Görsel:** `integration.jpg`.
