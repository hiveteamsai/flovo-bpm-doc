# CLAUDE.md

Bu dosya, bu çalışma alanında Claude Code'a (claude.ai/code) rehberlik eder.

## Bu Klasör Ne İçin?

Bu klasör bir **kod deposu değildir**. Burada **kod yazılmaz**.

Amaç: **Flovo'nun yeni BPM motorunun tasarım/analiz dökümanlarını** oluşturarak analizi tamamlamak.
Çıktılar **Markdown doküman/analiz** formatındadır. Gerçek kod, ayrı bir repoda geliştirilecektir.

## Flovo Nedir? (Kısa)

Flovo, **Coden** tarafından geliştirilen, **bulut tabanlı, yapay zeka destekli** bir
**kurumsal iş süreçleri yönetim platformudur**. Çekirdeği **masraf yönetimi** olup
**görev, İK, envanter ve denetim** modülleriyle genişler.

## Mevcut Projenin Kaynak Kodu

Mevcut (eski) Flovo'nun **mobil kaynak kodu** şurada:
`/Users/osmancanguven/Documents/GitHub/Pratico.Apps` — **Flutter** projesi, paket adı `flovo`,
sürüm `4.14.12+443`. iOS + Android + Web (PWA) tek kod tabanı. Bu klasörde **kod değiştirilmez**;
yalnızca **analiz** için okunur.

## Klasör Yapısı

### `bpmEngine/` — ASIL ÇALIŞMA (yeni BPM motoru tasarımı)
Yeni BPM motoru tasarım dökümanları **doğrudan `bpmEngine/` altındadır.**
İndeks → **[`bpmEngine/README.md`](bpmEngine/README.md)**.

| Öğe | İçerik |
|---|---|
| `flovo-bpm-engine.md` · `flovo-customer-api.md` | Motor çalışma prensibi · Customer API. |
| `genel-ayarlar/` | Tüm servislerde kullanılan ayarlar (**action** · **style** · **status** · **translation** · **organization**). |
| `servis-ayarlari/` | Servise bağlı ayarlar (**process-step** · **process-step-action** · **properties** · **work-rule** · **view-profile**). |
| `sampleProcess/` | Uçtan uca **örnek süreçler** (görselli, self-servis). |
| `research/` | **BPM referansları + karşılaştırmalar:** `current-flovo-bpm-engine/` (mevcut/eski Flovo BPM) · `n8n/` (referans analizleri) · `compare/` (**new-vs-current** · **new-vs-n8n** farkları + başarılı/başarısız). |

### `archive/` (ana dizin) — Önceki Araştırma & Sunum (arşiv)
Daha önce yapılan **pazar/ürün araştırmaları, ESN vakaları, vizyon ve sunum** çıktıları burada durur.
> **BPM motoru analizinde bu araştırmalar aktif kullanılmaz.** İhtiyaç olursa, kullanılacak araştırmayı
> **kullanıcı ayrıca referans olarak iletir.** (İçerik indeksi gerekirse: `archive/archive.md`.)

> **Not:** `bpmEngine/research/` = **BPM referansları** (current-flovo-bpm-engine + n8n); ana dizindeki
> **`archive/`** = **pazar/ürün araştırma + sunum arşivi**.

## Çalışma Kuralları (Claude için)

1. **Kod yazma.** Bu klasörde uygulama kodu üretme; çıktılar Markdown/doküman olsun.
2. **Dil:** Kullanıcı Türkçe konuşuyor; doküman ve yanıtları **Türkçe** üret.
3. **Asıl odak:** `bpmEngine/` — yeni BPM motoru tasarımı. İndeks: `bpmEngine/README.md`.
4. **Yeni-uygulama dökümanları kendi başına** yeni uygulamayı anlatır; eski uygulamayla **farklar yalnız**
   `bpmEngine/research/compare/new-vs-current.md`'de, diğer platform kıyasları `bpmEngine/research/compare/` altında
   tutulur. Tasarım dökümanlarına eski-app karşılaştırması / "eski adı …" ifadeleri **konmaz**.
5. **Mevcut (eski) Flovo BPM referansı:** `bpmEngine/research/current-flovo-bpm-engine/`.
6. **Kaynak göster:** internet araştırmasında kullanılan kaynakları doküman sonunda linkle.
