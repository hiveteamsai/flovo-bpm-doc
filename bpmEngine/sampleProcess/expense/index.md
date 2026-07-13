# Örnek Süreç — Masraf Oluşturma (expense) — İndeks

> **Amaç:** Kullanıcının bir masrafı **üç yolla** oluşturmasını gösteren örnek süreç: **fotoğraf çekerek**, **dosya seçerek** veya **belgesiz** (boş form). Fotoğraf/dosya yolunda belge **Flovo AI (Masraf)** ile taranır, form otomatik doldurulur; AI hatasında yarım form silinir (telafi).

## Dökümanlar
| Döküman | Özet |
|---|---|
| [`process.md`](./process.md) | Masraf akışı: 3 başlatma (`takePhoto`/`selectFile`/`manual`) → Instance Creator → **Processing (loading)** → **Flovo AI (Masraf)** → Bildirim → Kullanıcı; `onFail` → Bildirim → **Instance Deleter**. Detaylı spec (amaç · diyagram · adım/ayar/aksiyon · parametre akışı). |

> **Görsel:** `expense.jpg`.
