# Mevcut (Eski) Flovo BPM Motoru — Analiz İndeksi

> **Amaç:** Pratico/Flovo uygulamasının **mevcut (eski) BPM motorunun** analizi — motor çalışma prensibi, süreç adımları,
> aksiyonlar, form alanları, durumlar, görüntüleme profilleri ve iş kuralları. Yeni tasarım için **referans** kaynağıdır.

## Dökümanlar
| Döküman | Özet |
|---|---|
| [`bpm-engine.md`](./bpm-engine.md) | Eski Flovo BPM Engine genel dokümantasyonu — iş akışı yönetimi, onay koordinasyonu, koşullu dallanma, dinamik davranış. |
| [`process-steps.md`](./process-steps.md) | Süreç adımları (Process Step) — servis bazlı iş akışının adım + aksiyon yapısı. |
| [`actions.md`](./actions.md) | Aksiyonlar — bir adımda alınabilen, olay tetikleyip süreci ilerleten servis-bazlı eylemler. |
| [`properties.md`](./properties.md) | Form alanları (Property) — veri girişi/görüntüleme öğeleri ve kontrol tipleri. |
| [`statuses.md`](./statuses.md) | Durumlar (Status) — kaydın aşamasını temsil eden, gösterim/filtreleme/raporlama etiketleri. |
| [`view-profiles.md`](./view-profiles.md) | Görüntüleme profilleri — formun adım-bazlı görünümü (görünür/düzenlenebilir/zorunlu). |
| [`work-rules.md`](./work-rules.md) | İş kuralları (WorkRule) — form üzerinde koşul-aksiyon tabanlı dinamik davranış. |

## Alt klasörler
| Klasör | İçerik (özet) | İndeks |
|---|---|---|
| **organizations/** | Eski **Organizasyon Ayarları** modülünün analizi — şirketler, kullanıcılar, departmanlar, hiyerarşiler, takvimler ve diğer org-ayar DTO'ları. | [`organizations/index.md`](./organizations/index.md) |
