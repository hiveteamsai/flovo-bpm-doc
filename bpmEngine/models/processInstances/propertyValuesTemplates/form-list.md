# Değer Şablonu — `formList` (Form List)

> **Durum:** 🟡 TASLAK — ilk çıkarım; düzenlenecek.
> **Kapsam:** `formList` değerinin **`InstanceValue.data` içindeki şekli** + fihrist yansıması. **Diğer tiplerden farklı:** değer skaler değildir — alt-servis **kayıtları ayrı `Instance`**'lardır.
> **Alan davranışı:** → [`../../../service-settings/properties.md`](../../../service-settings/properties.md) §3.13 · **model:** [`../../service-settings/property.md`](../../service-settings/property.md) · **ilişki:** [`../associated-instance.md`](../associated-instance.md) · **child değer:** [`../instance-value.md`](../instance-value.md).

## 1. JSONB değer şekli — `data["<code>"]`
Form List satırları **ayrı child `Instance`'lardır** (gömülü kalem değil); ilişkinin kendisi [`AssociatedInstance`](../associated-instance.md)'te tutulur. Ancak satırın **seçilebilirlik (selectable) durumu** ve **red bilgisi**, child instance'ta da ilişki kaydında da bulunmadığından, formList değeri `data`'da **list-of-model** olarak tutulur (yalnız `list<int>` id listesi **yetmez**):

| Alan | Tip | Açıklama |
|---|---|---|
| `instanceId` | int | Satırın **child instance**'ı (→ [`../instance.md`](../instance.md)). |
| `status` | bool | **Selectable** checkbox değeri — satırın seçili/aktif durumu; `false` = **reddedilmiş** (ilişki **kaldırılmaz**, satır kalır). _(Profil ayarı `selectableVisible`/`selectedEditable` görünürlük/düzenlenebilirlik; **değer** burada.)_ |
| `rejectedBy` | obje? | `status=false` yapan (**reddeden**) kullanıcı — `{ userId: int, nameSurname: string }` (kullanıcı-referans konvansiyonu — Q11/Q13). `status=true` iken null. |
| `rejectedDate` | datetime? | Reddin (**`status=false`**) yapıldığı **tarih**. `status=true` iken null. |
| `rejectedByReason` | string? | Red **gerekçesi**. `status=true` iken null. |

```json
{ "expenseLines": [
  { "instanceId": 45821, "status": true },
  { "instanceId": 45822, "status": false,
    "rejectedBy": { "userId": 12, "nameSurname": "Ayşe Yılmaz" },
    "rejectedDate": "2026-08-06T14:30:00Z", "rejectedByReason": "Belge eksik" }
] }
```
> **`AssociatedInstance` ile senkron (KARAR — Q5):** Form List değeri `data`'da (instance value) tutulur; **her satır** aynı zamanda [`AssociatedInstance`](../associated-instance.md)'e **kayıt edilir**, form listeden **kaldırılan** instance ise `AssociatedInstance`'tan **silinir** → üyelik iki tarafta **senkron**. **`status=false` (reddedilme) ilişkiyi KALDIRMAZ** — satır hem `data`'da hem `AssociatedInstance`'ta **kalır**, yalnız seçili-değil/reddedilmiş işaretlenir.
- Boş: anahtar **yok** ya da `[]`.

## 2. Projeksiyon — `projectToAttr`
- **Child değerleri** parent'ın Attr'ına projekte **edilmez** — her child kendi `InstanceValue`/`InstanceAttr`'ıyla raporlanır; parent↔child ilişkisi `AssociatedInstance` üzerinden **join**'lenir.
- **Satır durumu fihriste projekte edilir** (Q6) → [`InstanceListItem`](../instance-list-item.md) (her satır = `itemIndex`):

| `attrCode` | Kolon(lar) |
|---|---|
| `instanceId` | `numValue` |
| `status` | `boolValue` |
| `rejectedBy` | `numValue`=userId · `textValue`=nameSurname |
| `rejectedDate` | `dateValue` |
| `rejectedByReason` | `textValue` |

## 3. Notlar
- `InstanceListItem` (liste-of-model, ör. `groupByTax`) ile **karıştırma**: o aynı JSON içindeki kalem; Form List ayrı Instance.
- Ana↔alt parametre aktarımı (`parameterTransfer`/`propertyTransferParameters`) child `InstanceValue`'ya **normal yazma** yapar (→ properties §3.13).

*Oluşturma: 2026-08-06.*
