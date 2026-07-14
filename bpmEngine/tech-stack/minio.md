# MinIO — Nesne Depolama (Object Storage) (Flovo iBPM v2)

> **Rol:** Form ekleri, fatura görselleri ve tüm binary/dosya içeriğinin S3-uyumlu, self-host nesne deposu.
> **Karar:** **MinIO** (embed, S3 API) · ✅ canlı (F-Infra SI.4) · tam gerekçe/karşılaştırma → [`../research/tech-stack/tech_rating.md`](../research/tech-stack/tech_rating.md)

## Ne için kullanıyoruz?

BPM formlarında **dosya/görsel** (fatura, sözleşme eki, imza görseli, belge) yoğun kullanılır. Bu binary içeriği **veritabanına koymak yerine** MinIO'da tutuyoruz. Sebep:

- **On-prem + Private Cloud** hedefiyle uyumlu, **S3-uyumlu** (kod S3 API'sine yazar; bulutta da taşınabilir).
- Veritabanını (PostgreSQL/JSONB) **küçük ve hızlı** tutar — binary DB'de değil.
- Müşteri kendi data-center'ında çalıştırabilir (KVKK, veri egemenliği).

## Sürüm & bileşenler

- **MinIO** (embed dağıtım, S3 API uyumlu).
- **Bucket-per-tenant** izolasyon modeli.
- **KMS** ile sunucu-tarafı şifreleme (encryption-at-rest).
- İç iletişim: Go backend → MinIO S3 SDK (presigned URL üretimi dahil).

## Projemizde kullanım

- **Yükleme akışı:** kullanıcı formda dosya seçer → backend (veya presigned URL ile FE doğrudan) MinIO'ya yazar → geri dönen **nesne adresi (URL/anahtar)** forma yazılır.
- **property-value-storage ile bağ (kritik):** Form değeri saklama mimarisinde **binary asla JSONB'ye konmaz**; JSONB yalnız **referans/URL** tutar:

  ```json
  { "receipt": { "url": "minio://tenant-5/expenses/2026/abc.jpg" } }
  ```

  Bu, depolama değerlendirmesindeki **D8** gereksinimidir ([`form_attr_scenerios_rating.md`](../research/property-value-storage/form_attr_scenerios_rating.md)). Faydası:
  - **JSONB küçük kalır** → her form güncellemesinde tüm satırın yeniden yazılma (MVCC) maliyeti düşer (bkz. depolama S9).
  - `form-value-scenarios.md` **§7-22** "yavaş belge yükleme" şikâyeti çözülür — belge akışı DB'den ayrışır.
- **Erişim/gösterim:** dosya render/indirme anında **presigned URL** ile; DB yalnız anahtarı taşır.

## Konfigürasyon / desen notları

- **Bucket-per-tenant:** her organizasyona ayrı bucket (`tenant-<organizationId>`) → izolasyon + kota + yaşam-döngüsü politikası tenant bazında.
- **Yol deseni:** `tenant-<orgId>/<domain>/<yıl>/<nesne>` — servis/tarih bazlı düzen, arşiv/pruning kolaylığı.
- **Şifreleme:** KMS ile at-rest; erişim yalnız presigned/kısa-ömürlü URL.
- **Yaşam döngüsü:** soğuyan/silinen form ekleri için retention + pruning politikası (KVKK saklama süreleriyle uyumlu).

## İlişkili tasarım

- [`../research/property-value-storage/form-value-scenarios.md`](../research/property-value-storage/form-value-scenarios.md) — §7-22 dosya/binary; §11 değer tipleri (File referansı).
- [`../research/property-value-storage/form_attr_scenerios_rating.md`](../research/property-value-storage/form_attr_scenerios_rating.md) — **D8 (MinIO entegrasyonu)**.
- [`./postgresql.md`](./postgresql.md) — JSONB'de yalnız URL tutma; DB'nin küçük kalması.
- [`../research/tech-stack/tech_rating.md`](../research/tech-stack/tech_rating.md) — storage katmanı kararı (MinIO vs Azure Blob/Supabase).

## Dikkat / açık noktalar

- **URL kalıcılığı:** JSONB'de tutulan anahtar/URL şeması **stabil** olmalı (nesne taşınırsa referans kırılır); taşıma/rehost bir migrasyon olayıdır.
- **Presigned URL TTL** ve erişim yetkisi (tenant izolasyonu) güvenlik açısından titiz ayarlanmalı.
- **Büyük dosya** yükleme/indirme için multipart + doğrudan-FE presigned akışı önerilir (backend'i bypass ederek yük azaltır).
