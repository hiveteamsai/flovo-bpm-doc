# Property Settings — `parentProperty` (Parent Property)

> **propertyType:** `parentProperty` · **Kontrol:** **düzenlenemez** salt-okunur **yansıma**; bağlı olduğu **üst (parent)** süreç/formdaki seçili alanı `reflectionMode`'a göre forma getirir. Ana↔alt değer akışının taşıyıcısıdır (eski `parameterTransfer` kaldırıldı → properties §3.13).
> **Değer şekli:** → [`../../../processInstances/propertyValuesTemplates/parent-property.md`](../../../processInstances/propertyValuesTemplates/parent-property.md) (referans alınan üst alanın tipiyle **aynı** şekil) ·
> **Davranış:** → [`../../../../service-settings/properties.md`](../../../../service-settings/properties.md) §3.15 · **Çekirdek model:** [`../../property.md`](../../property.md) · **İndeks:** [`index.md`](./index.md).

## 1. `settings` (JSONB) — tipe-özel ayarlar
- **Yok — `settings` boştur (`{}`).** `parentProperty` düzenlenebilir bir kontrol **değildir** ve tüm tipe-özel alanları (referans/ilişki FK'leri + yansıma metadata'sı) **projektör/sorgu/motor katmanının ilişkisel okuduğu** metadata olduğundan **hepsi çekirdek kolonda** yaşar (§2). Bu tip için ayrı bir render/istemci-davranışı ayarı **tanımlı değildir**; `settings` şeması yalnız **kapalı boş nesneyi** doğrular.

## 2. Çekirdek kolonda (esas modelleme burada)
- **`parentPropertyId`** (int) — **üst alan** (bağlanılan parent property).
- **`refPropertyId`** (int) — üst formda **referans alınan** (getirilecek) alan.
- **`relatedPropertyIds`** (List\<int\>) — ilişkili alanlar.
- **`reflectionMode`** ([`ReflectionMode`](../../../enums/reflection-mode.md)) — üst değerin **nasıl takip edileceği**: `snapshot` (kopyala+**dondur**; **vars.**) · `live` (kopyalamaz — `data`'ya yazmaz, okurken üst instance'tan **join/referans**) · `materialized` (kopyala **ve** üst değiştikçe **`AssociatedInstance` üzerinden yayılımla tazele** — **yalnız `parentProperty`**). Değer şekli üst alanın tipiyle aynı (skaler/`LabeledValue`/liste).
- **`reflectionPropagation`** ([`ReflectionPropagation`](../../../enums/reflection-propagation.md)) — **yalnız `reflectionMode=materialized`** iken anlamlı; kopyanın **ne zaman** tazeleneceği: `async` (arka planda, **vars.**) · `sync` (yazma anında, guardrail'li — 1-hop + fan-out eşiği). `snapshot`/`live`'da **yok sayılır**.
- **`isReflectionSource`** (bool) — **karşı taraf** metadata'sı: üst alan, `materialized` bir `parentProperty` tarafından yansıtılıyorsa `true` (değeri değişince yayılım tetiklenir); türetilen `parentProperty`'nin **kendisi** için tipik olarak `false`.
- Değer-saklama/projeksiyon metadata'sı: `savePropertyToDb` · `projectToAttr` · `saveChangeLog` · `hasTranslation` (§1.3). `snapshot`/`materialized`'da değer `data`'da → **projekte edilebilir** (referans alanın tipinin kuralıyla); `live`'da `data`'da değer olmadığından **projekte edilmez**.

## 3. Profil-bazlı
- Yok (`parentProperty` için profil-özel ayar tanımlı değil; görünürlük genel profil alanıdır → [`../../view-profile-property.md`](../../view-profile-property.md)).

## 4. Yansıma mekanizması (özet)
- `materialized` yayılımı için ayrı bir "link" tablosu **yoktur**: child'lar **`AssociatedInstance`** ters aramasıyla bulunur, üst↔child alan eşlemesi **`Property.refPropertyId`/`code`** ile çözülür. **Derinlik limiti · döngü tespiti · async** zorunludur (→ [`../../../processInstances/reflection-propagation.md`](../../../processInstances/reflection-propagation.md), motor **O3**).
- `async` (vars.) → üst commit'i ile child tazeleme arasında kısa **eventual consistency**; anında tutarlılık için `sync` (guardrail'li).

## 5. JSON Schema (`settings`)
```json
{
  "$id": "property-settings/parentProperty",
  "type": "object",
  "additionalProperties": false,
  "properties": {}
}
```
> Not: Bu tipin tüm alanları (`parentPropertyId`, `refPropertyId`, `relatedPropertyIds`, `reflectionMode`, `reflectionPropagation`, `isReflectionSource`) **çekirdek kolon** olduğundan `settings` şemasında **yer almaz**; şema yalnızca `settings`'in **boş ve kapalı** (bilinmeyen anahtar reddedilir) olduğunu doğrular.

## 6. Örnek
```json
{}
```

*Oluşturma: 2026-08-28.*
