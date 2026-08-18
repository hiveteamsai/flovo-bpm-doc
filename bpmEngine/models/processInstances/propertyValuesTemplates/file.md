# Değer Şablonu — `file` (File)

> **Durum:** 🟡 TASLAK — ilk çıkarım; düzenlenecek.
> **Kapsam:** `file` değerinin **`InstanceValue.data` içindeki şekli** + **`projectToAttr=true`** iken fihriste yansıması.
> **Alan davranışı:** → [`../../../service-settings/properties.md`](../../../service-settings/properties.md) §3.8 · **model:** [`../../service-settings/property.md`](../../service-settings/property.md) · **değer modeli:** [`../instance-value.md`](../instance-value.md) · **altyapı:** MinIO (`../../../tech-stack/minio.md`).

## 1. JSONB değer şekli — `data["<code>"]`
**Her zaman `list-of-model`** — tekil dosyada bile **tek elemanlı dizi** (`allowMultiple=false` yalnız UI'da dosya sayısını sınırlar; şekil yine dizidir). Binary **JSONB'ye gömülmez**; `data`'da her eleman **URL + file info** tutar:

| Alan | Tip | Açıklama |
|---|---|---|
| `url` | string | MinIO **URL / object key** (asıl binary MinIO'da). |
| `fileInfo` | obje | Dosya meta bilgisi (alt-alanlar ↓). |
| `fileInfo.user` | obje | **Yükleyen kullanıcı** — `{ userId: int, nameSurname: string }` (id + ad-soyad birlikte; **kullanıcı-referans konvansiyonu** — Q11/Q13). |
| `fileInfo.date` | datetime | **Yükleme** tarihi. |
| `fileInfo.location` | string? | Yükleme/çekim **konumu** — adres **string** (Q10). |

```json
{ "attachments": [
  { "url": "minio://org/2026/08/fatura-45821.pdf",
    "fileInfo": {
      "user": { "userId": 12, "nameSurname": "Ayşe Yılmaz" },
      "date": "2026-08-06T10:00:00Z",
      "location": "İstanbul, Kadıköy"
    } }
] }
```
- Boş: değer **`[]`** (anahtar her zaman bulunur — `code` ile; → [`../instance-value.md`](../instance-value.md)).

## 2. Projeksiyon — `projectToAttr=true`
Çoğunlukla **`projectToAttr=false`** (dosya nadiren aranır). Gerekirse **InstanceListItem** (her dosya = `itemIndex`):

| `attrCode` | Kolon(lar) |
|---|---|
| `url` | `textValue` |
| `user` | `numValue`=userId · `textValue`=nameSurname |
| `date` | `dateValue` |
| `location` | `textValue` (adres string) |

## 3. Notlar
- **Şekil her zaman dizidir** (tekil = tek elemanlı) — tekil/çoklu ayrımı için özel-durum kodu gerekmez; `allowMultiple` yalnız UI sınırıdır.
- **`fileInfo`** (user/date/location) her dosyayla birlikte tutulur (kim, ne zaman, nereden yükledi).
- JSONB küçük kalsın diye binary **MinIO'da**; `data` yalnız referans + meta tutar (yazma ucuzlar, TOAST baskısı azalır).
- Flovo AI dosyayı bu alandan/thumbnail'den alır (→ properties §3.8).

*Oluşturma: 2026-08-06.*
