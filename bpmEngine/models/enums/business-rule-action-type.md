# Enum — businessRuleActionType (BusinessRule)

> **Kullanan model:** [`business-rule.md`](../service-settings/business-rule.md) (`businessRuleActionType`)
> **Amaç:** İş kuralı koşulu sağlandığında formda **hangi frontend etkisinin** uygulanacağını belirler.
> **Davranış/kullanım:** → [`../../service-settings/business-rule.md`](../../service-settings/business-rule.md)

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `SetViewForProperties` | Seçili alan(lar)ın görünürlük/erişim durumunu ayarlar (visible/enabled/required). | Koşula göre alan göster/gizle/kilitle/zorunlu yap. |
| `ChangeViewProfile` | Aktif görüntüleme profilini değiştirir. | Koşula göre farklı alan setine/düzene geçmek. |
| `ApplyValidation` | Ek validasyon uygular. | Koşullu doğrulama kuralı devreye almak. |
| `ShowMessage` | Kullanıcıya mesaj/uyarı gösterir. | Koşul oluşunca bilgilendirme/uyarı. |
| `AssignValueToProperty` | Bir alana değer atar (kaynak: `ValueAssignType`). | Koşula göre alan değeri doldurmak/hesaplamak. |
| `FillDataSource` | Bir alanın veri kaynağını doldurur/yeniler. | Koşula göre seçenek listesini beslemek. |
| `AssignValueToPropertyAttribute` | Bir alanın özniteliğine (ör. hint/format) değer atar. | Koşula göre alan metadata'sını değiştirmek. |
| `SetStyle` | Bir alana/öğeye stil uygular. | Koşula göre renk/görünüm değiştirmek. |

## Notlar
- **İsim çakışması giderildi (v0.7):** Bu alan önceden `actionType` idi; [`action-type.md`](./action-type.md) (`Action.actionType`) ile
  karışmaması için **`businessRuleActionType`** olarak yeniden adlandırıldı. İki enum ayrı varlıklardır.
- `AssignValueToProperty` için değer kaynağı → [`value-assign-type.md`](./value-assign-type.md).

*Oluşturma: 2026-07-10.*
