# Model — LabeledValue (etiketli değer şekli — tablo değil)

> **Durum:** 🟡 TASLAK — değer-saklama mimarisinden türetildi (→ `../../../research/property-value-storage/form-deger-saklama-v2.html`); alanlar gözden geçirilecek.
> **Yeni model.** ⚠️ **Ayrı tablo DEĞİLDİR** — `InstanceValue.data` JSONB'ye **gömülü** yazılan ve `InstanceAttr`/
> `InstanceListItem`'a (`display`/`translationCode` kolonlarına) **açılan** bir **değer şeklidir** (value object).
> **Amaç:** Kodu ile görünen adı **farklı** olan her seçim değeri (combobox, radio, key-value value, liste alt-seçimi,
> multi-select…) `{value, display, translationCode}` üçlüsüyle taşınır. Sayı/metin/tarih/bool **sarılmaz** (düz skaler).

## Alanlar (JSONB şekli)
| Alan | Tip | Açıklama / amaç |
|---|---|---|
| `value` | string | **Kod** — dile bağlı olmayan teknik değer (ör. combobox kodu `"2"`). Rename-safe: gösterim değişse de sabit. |
| `display` | string | **Organizasyon varsayılan dilindeki** görünen ad (ör. `"elma"`). Statik seçimlerde **`PropertyItem.definition`**'dan kopyalanır. **Amaç → join'siz okuma:** kullanıcının dili org varsayılan diliyle **aynıysa** bu değer PropertyItem/Translation'a **join atılmadan doğrudan** kullanılır. |
| `translationCode` | string? | **`PropertyItem.translationCode`**'dan kopyalanır (`→ Translation.code`) veya **null**. **Dil uyuşmazlığında** (kullanıcı dili ≠ org varsayılan dili) **ve dolu** ise, istenen dilin metni buradan **Translation**'dan getirilir. |

> **Okuma kuralı (dil çözümü — neden hem `display` hem `translationCode`):**
> 1. **kullanıcı dili == org varsayılan dili** → `display` **doğrudan** kullanılır (PropertyItem/Translation'a **join yok** — asıl performans kazancı).
> 2. **kullanıcı dili ≠ org varsayılan dili** **ve** `translationCode != null` → istenen dilin metni **Translation**'dan çözülür.
> 3. `translationCode == null` (çeviri yok) → her dilde `display` kullanılır.
>
> Yani `translationCode` çeviriyi **değiştirmez**, `display` da onu **gereksizleştirmez**: `display` = ortak-dil hızlı yolu (join'siz), `translationCode` = farklı-dil çözüm köprüsü.

## Nerede kullanılır
- **`InstanceValue.data`** (JSONB): etiketli seçim alanı düz `"2"` yerine `{ "value":"2", "display":"elma", "translationCode":"apple…" }` olarak yazılır.
- **`InstanceAttr`** / **`InstanceListItem`**: projektör `value`→`textValue`, `display`→`display`, `translationCode`→`translationCode` kolonlarına açar (rapor **isim araması** `display ILIKE '%…%'` — `projectToAttr=true` gerekir).

## Notlar / açık noktalar
- **Neden kataloglu değerlerde de kaynağa yazılır (KARAR):** `display`/`translationCode` kataloglu (`PropertyItem`) değerlerde
  koddan **türetilebilir** olsa da, LabeledValue nesnesi **her etiketli değerde** `InstanceValue.data`'ya yazılır. Gerekçe:
  **tek/generic yol** — projektör ve form-detay hem statik hem **dinamik/katalogsuz** (dataSource/iş-kuralı/API) seçenekleri
  **aynı** şekilde, **join'siz** işler; statik/dinamik ayrımı için özel-durum kodu gerekmez. **Bilinçli kabul edilen bedel:**
  kataloglu durumda kaynakta ufak **fazlalık** + `PropertyItem.definition`/Translation sonradan değişirse **snapshot bayatlaması**
  (gerekince re-project/çeviri-rebuild ile tazelenir). _(Değerlendirilip elenen alternatif: kaynağa yalnız kod yazıp display'i
  yalnız dinamikte tutmak — reddedildi: iki-yollu karmaşıklık.)_
- **`display` kaynağı — `PropertyItem` şart değil:**
  - **Statik liste** (`PropertyItem`): backend `value`→item→`definition`/Translation'dan `display` doldurur.
  - **Dinamik liste** (iş kuralı / API / dataSource): sunucu kataloğu bilmeyebilir → istek gövdesinde **`LabeledValue`
    zorunlu** (`value`+`display`). Backend `PropertyItem` aramaz, JSONB'ye olduğu gibi yazar.
  - **Hibrit:** bulursa statik, bulamazsa istekteki display.
- **Çeviri DB'de değişirse** JSONB/`Attr.display` **otomatik güncellenmez** (snapshot kalır — outbox tetiklenmez); istenirse
  çeviri-rebuild job. Form UI, `translationCode` ile Translation'dan **taze** okuyabilir.
- **`Property.hasTranslation`** = alanın değer seçenekleri çeviri kullanıyor mu (yardımcı bayrak → `../../service-settings/property.md`).
- **Kaynak mimari:** → `../../../research/property-value-storage/form-deger-saklama-v2.html` (§16 çeviri/LabeledValue · §7 değer şekilleri).

*Oluşturma: 2026-08-04.*
