# Enum — BusinessRuleActionType

> **Kullanan model:** [`business-rule.md`](../service-settings/business-rule.md) — alan `businessRuleActionType`, tip **BusinessRuleActionType**
> **Amaç:** İş kuralı koşulu sağlandığında formda **hangi frontend etkisinin** uygulanacağını belirler.
> **Davranış/kullanım:** → [`../../service-settings/business-rule.md`](../../service-settings/business-rule.md)

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `setViewForProperties` | Seçili alan(lar)ın görünürlük/erişim durumunu ayarlar (visible/enabled/required). | Koşula göre alan göster/gizle/kilitle/zorunlu yap. |
| `changeViewProfile` | Aktif görüntüleme profilini değiştirir. | Koşula göre farklı alan setine/düzene geçmek. |
| `applyValidation` | Ek validasyon uygular. | Koşullu doğrulama kuralı devreye almak. |
| `showMessage` | Kullanıcıya mesaj/uyarı gösterir. | Koşul oluşunca bilgilendirme/uyarı. |
| `assignValueToProperty` | Bir alana değer atar (kaynak: **ValueAssignType**). | Koşula göre alan değeri doldurmak/hesaplamak. |
| `fillDataSource` | Bir alanın veri kaynağını doldurur/yeniler. | Koşula göre seçenek listesini beslemek. |
| `assignValueToPropertyAttribute` | Bir alanın özniteliğine (ör. hint/format) değer atar. | Koşula göre alan metadata'sını değiştirmek. |
| `setStyle` | Bir alana/öğeye stil uygular. | Koşula göre renk/görünüm değiştirmek. |

## Notlar
- **İsim çakışması giderildi (v0.7):** Bu alan önceden `actionType` idi; [`action-type.md`](./action-type.md) (`Action.actionType`) ile
  karışmaması için **`businessRuleActionType`** olarak yeniden adlandırıldı. İki enum ayrı varlıklardır.
- `assignValueToProperty` için değer kaynağı → [`value-assign-type.md`](./value-assign-type.md) (**ValueAssignType**).

*Oluşturma: 2026-07-10.*
