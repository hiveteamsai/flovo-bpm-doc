# Property Settings — `groupByTaxReceipt` (Group By Tax Receipt)

> **propertyType:** `groupByTaxReceipt` · **Kontrol:** masraf/fiş kalemlerini **vergiye göre gruplandıran** özel masraf alanı; kullanıcı **satır satır** kalem ekler (gider türü + vergi oranı + tutar), kalem ve vergi toplamları türetilir.
> **Değer şekli:** → [`../../../processInstances/propertyValuesTemplates/group-by-tax-receipt.md`](../../../processInstances/propertyValuesTemplates/group-by-tax-receipt.md) (**obje dizisi / kalem listesi**: `expenseType` · `taxRate` · `amount` · `isKkeg`) ·
> **Davranış:** → [`../../../../service-settings/properties.md`](../../../../service-settings/properties.md) §3.17 · **Çekirdek model:** [`../../property.md`](../../property.md) · **Değer modeli:** [`../../../processInstances/instance-list-item.md`](../../../processInstances/instance-list-item.md) · **İndeks:** [`index.md`](./index.md).

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `disableTaxAttachmentView` | bool | hayır | `false` | **Vergi eki (fiş/belge görseli) görünümünü gizle.** `true` iken kalemlerin vergi eki alanı formda gösterilmez — belge iliştirme beklenmeyen masraf tiplerinde arayüzü sadeleştirir. |
| `isActiveKkegAttachment` | bool | hayır | `false` | **KKEG** (kanunen kabul edilmeyen gider) **eki aktif.** `true` iken KKEG işaretli (`isKkeg=true`) kalemler için ek belge iliştirme akışı açılır. |

## 2. Çekirdek kolonda (settings'e girmez)
- **Değer** = kalem listesi (`expenseType` etiketli seçim + `taxRate` sayısal oran + `amount` sayı + opsiyonel `isKkeg` bool) → değer `InstanceValue.data`'da **obje dizisi** olarak tutulur (değer şablonu §1).
- **Projeksiyon** (`projectToAttr=true`): **kalem × alt-alan** → [`InstanceListItem`](../../../processInstances/instance-list-item.md) (her kalem `itemIndex`, her alt-alan `attrCode`); `SUM(amount) GROUP BY taxRate` bu fihrist üzerinden — değer şablonu §2. `savePropertyToDb` · `saveChangeLog` (§1.3).
- **Gider türü / vergi oranı listeleri** kalem girişinde **organizasyon ayarlarından** (şirketin gider türü + vergi tanımları) yüklenir; kullanıcının seçtiği tekil değer kaleme yazılır. Bu listeler **alan `settings`'ine gömülmez** — runtime'da org verisinden gelir.
- ⏸️ **Tax / Currency askıya alındı (KARAR v0.47):** organizasyon vergi ayarı **modellenmeyeceğinden** vergi-oranı listesi org verisinden gelemez → bu alan tipinin kaderi (askıya alma ↔ `taxRate` serbest sayı) **açık** → [`../../../../todo.md`](../../../../todo.md) "Kapsam-dışı varlıklar".
- **Toplamlar** (kalem/vergi dip toplamı) `data`'da **saklanmaz** — gerektiğinde türetilir (değer şablonu §3).

## 3. Profil-bazlı
- Yok (`groupByTaxReceipt` için profil-özel ayar tanımlı değil; görünür/düzenlenebilir/zorunlu genel profil alanlarıdır → [`../../view-profile-property.md`](../../view-profile-property.md)).

## 4. Zorunluluk (required) davranışı
- Alan **required** ise (profilde `required=true`): **en az bir** kalem satırı bulunmalı **ve her satır tamamlanmış** olmalıdır — gider türü seçili, vergi oranı seçili/girili ve tutar `> 0`. Boş/eksik satır varken form geçerli sayılmaz (properties §3.17). Tutarların sayısal geçerliliği ve seçili gider türü/vergi oranının org listesinde bulunması **uygulama-katmanı** doğrulamasıdır.

## 5. JSON Schema (`settings`)
```json
{
  "$id": "property-settings/group-by-tax-receipt",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "disableTaxAttachmentView": { "type": "boolean", "default": false },
    "isActiveKkegAttachment":   { "type": "boolean", "default": false }
  }
}
```
> Not: Kalem değerleri (gider türü / vergi / tutar) ve org gider-türü/vergi listeleri **çekirdek/değer katmanında** olduğundan bu şemada yer almaz; şema yalnız alan-düzeyi `settings` JSONB'yi doğrular.

## 6. Örnek
```json
{ "disableTaxAttachmentView": false, "isActiveKkegAttachment": true }
```

*Oluşturma: 2026-08-28.*
