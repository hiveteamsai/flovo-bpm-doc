# Model — InstanceAttr (skaler fihrist / tipli projeksiyon)

> **Durum:** 🟡 TASLAK — değer-saklama mimarisinden türetildi (→ `../../research/property-value-storage/form-deger-saklama-v2.html`); alanlar gözden geçirilecek.
> **Yeni model.**
> **Amaç:** Her **sorgulanabilir skaler alan** → 1 satır. `InstanceValue.data`'dan **türetilen** rapor/arama/sıralama fihristi
> (tipli EAV projeksiyonu). **Formu göstermek için kullanılmaz** — yalnız liste/filtre/sıralama/aralık/isim-arama.
> **Yeniden üretilebilir:** silinse bile `InstanceValue`'dan aynen üretilir.

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `instanceId` | int | PK · FK → Instance.id | Kimlik. |
| `serviceId` | int | PK · FK → Service.id | Kimlik + izolasyon/partition. |
| `organizationId` | int | (denormalize) | Kiracı — RLS/tenant izolasyonu. |
| `propertyCode` | string | PK | Hangi alan (`Property.code`) — **`code`-keyed** (id-FK değil; kaynak JSONB de code-keyed, join yükü yok). |
| `numValue` | numeric? | — | Sayısal değer (aralık/sıra). |
| `textValue` | string? | — | Metin / seçim kodu (combobox `value`). |
| `dateValue` | datetime? | — | Tarih değeri. |
| `boolValue` | bool? | — | Checkbox değeri. |
| `display` | string? | — | Etiketli değerde **görünen ad** (`LabeledValue.display` — org varsayılan dili, `PropertyItem.definition`'dan). Kullanıcı dili org diliyle **aynıysa join'siz doğrudan** kullanılır; rapor **isim araması/sıralaması** için (`display ILIKE '%…%'`). Skaler (etiketsiz) satırlarda **null**. |
| `translationCode` | string? | — | `PropertyItem.translationCode`'dan (`→ Translation.code`). **Dil uyuşmazlığında** doğru dilin metni Translation'dan getirilir. Yoksa **null** (→ okuma kuralı: [`labeled-value.md`](./propertyValuesTemplates/labeled-value.md)). |

> **Birincil anahtar:** `(instanceId, serviceId, propertyCode)`. Tipli sorgu index'leri (öneri): `(serviceId, propertyCode, numValue)` · `(…, textValue)` · `(…, dateValue)` + `textValue` üzerinde trigram (ILIKE) — teknik detay araştırma dokümanında.

## İlişkiler
- **N – 1** → `Instance` (`instanceId`), `Service` (`serviceId`).
- **Türetilir** ← `InstanceValue.data` (projektör tarafından; `Property.projectToAttr=true` olan **skaler** alanlar).

## Notlar / açık noktalar
- **Yalnız `projectToAttr=true` alanlar yansır:** Fihristi şişirmemek için alanların tipik **%10–20'si** `true`'dur
  (tutar, tarih, fatura no, seçim kodu…). `false` alanlar yalnız JSONB'de kalır — **eşittir** sorgusu için `InstanceValue`
  üzerindeki **GIN** index yeter (Attr şart değil); Attr **aralık/sıra/prefix/ILIKE/aggregate** içindir.
- **Tam-yansıtma (delta değil):** projektör bir olayda o instance'ın Attr satırlarını **siler → metadata'ya göre yeniden
  yazar**; `version` idempotency ile duplicate/sırasız olaylar güvenli.
- **`display`/`translationCode` yalnız etiketli seçimlerde dolar** (combobox/radio/key-value value…). Sayı/metin/tarih/bool
  değerlerinde null.
- **Liste-of-model alanları buraya değil `InstanceListItem`'a** yansır (`groupByTax`, key-value list).
- **Kaynak mimari:** → `../../research/property-value-storage/form-deger-saklama-v2.html` (§6.3 · §9 okuma · §16 çeviri).

*Oluşturma: 2026-08-04.*
