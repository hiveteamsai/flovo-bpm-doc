# Property Settings — `formList` (Form List)

> **propertyType:** `formList` · **Kontrol:** başka bir **servisin (alt-süreç)** formlarını bu alan altında **yenisini oluşturarak** ya da **var olandan ekleyerek** ilişkilendirip listeleyen **alt-servis** alanı.
> **Değer şekli:** → [`../../../processInstances/propertyValuesTemplates/form-list.md`](../../../processInstances/propertyValuesTemplates/form-list.md) (**list-of-model**: her satır ayrı child `Instance` — `instanceId`/`selected`/`rejected*`) ·
> **Davranış:** → [`../../../../service-settings/properties.md`](../../../../service-settings/properties.md) §3.13 · **Çekirdek model:** [`../../property.md`](../../property.md) · **Profil-bazlı:** [`../../view-profile-property.md`](../../view-profile-property.md) · **İndeks:** [`index.md`](./index.md).

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `lazyLoading` | bool | hayır | `false` | Alt-servis satırları **tembel** (scroll/arama ile parça parça) yüklenir; çok kayıtlı listelerde ilk açılışı hafifletir. Yalnız render/istemci davranışı → `settings`. |

> _Alan-düzeyi `settings`'te **yalnız** `lazyLoading` vardır. Alt-servis bağı (FK) çekirdek kolonda (§2); yeni oluşturma / var olandan ekleme / seçim / sıralama davranışı **profil-bazlı** (§3)._

## 2. Çekirdek kolonda (settings'e girmez)
- **`childServiceId`** (int, FK → Service) — satırların ait olduğu **alt servis (süreç)**; Form List'in kayıt kaynağı. Motor/projektör ilişkisel okuduğundan çekirdek kolonda (§1.5).
- **`serviceItemControlId`** (int) — alt-servis **öğe kontrolü**: listede her satırın özet/başlık olarak hangi alt-servis alanıyla gösterileceği.
- **Projeksiyon:** child değerleri parent'ın Attr'ına projekte **edilmez** — her child kendi `InstanceValue`/`InstanceAttr`'ıyla raporlanır; parent↔child ilişkisi **`AssociatedInstance`** üzerinden join'lenir (→ [`../../../processInstances/associated-instance.md`](../../../processInstances/associated-instance.md)). Satır durumu (`selected`/`rejected*`) fihriste `InstanceListItem`'a yansır → değer şablonu §2. `savePropertyToDb` · `projectToAttr` · `saveChangeLog` (§1.3).
- **Kaldırıldı (v0.33):** `parameterTransfer` / `propertyTransferParameters` **tamamen kaldırıldı** — ana↔alt değer akışı artık **`parentProperty`** (properties §3.15, salt-okunur yansıma) ile sağlanır.

## 3. Profil-bazlı
Görüntüleme profiline göre değişen tipe-özel ayarlar → [`../../view-profile-property.md`](../../view-profile-property.md) (`ProcessViewProfilePropertySetting {key, value}`):

| key | value tipi | Ne yapar |
|---|---|---|
| `activeStartActions` | list\<int\> (ProcessStepAction id) | Yeni kayıt oluştururken **hangi başlangıç aksiyonlarının** sunulacağı — `childService`'in **Süreç Başlangıcı** adımına bağlı [`ProcessStepAction`](../../process-step-action.md)'lardan seçilenler butonlaşır. **Boş liste = yeni oluşturma yok** (kullanıcı yalnız var olanı ekler). Eski alan-düzeyi `addNewEnabled` bool'unun yerini alır — artık **hangi** başlangıç yollarının açılacağı da profilde seçilir. |
| `addFromExistingStatusIds` | list\<int\> ([Status](../../../organization-settings/status.md) id) | **Var olandan ekle**: bu Form List'e, alt-servisin **hangi durumdaki** mevcut formlarının eklenebileceği. **Boş liste = "var olandan ekle" pasif** (yalnız yeni oluşturulur). Durum-filtresi olmasının nedeni: örn. yalnız "onaylı" alt-kayıtlar eklensin. Eski `addFromExistingRecordsIsActive` bool'unun yerini alır. |
| `selectableVisible` | bool | Satır **seçim/tik kutusunun** bu profilde **görünür** olup olmadığı (seçim/onay modu). **Boş/false = seçim modu kapalı.** Kutu değeri, değer şablonundaki satır `selected` bayrağını yazar (`false` = **reddedilmiş**; ilişki kaldırılmaz, satır kalır). Eski **alan-düzeyi** `Property.selectableModeActive`'in yerini alır — artık **profil bazında**. |
| `selectedEditable` _(öneri)_ | bool | `selectableVisible` açıksa, **tiklerin bu profilde değiştirilebilir** olup olmadığı (örn. yönetici profili ✓ işaretleyip kaldırabilir, süreç başlatan ✗ salt-görür). |
| `reOrder` | bool | Form List **satır sıralamasının** bu profilde (sürükle-bırak ile) değiştirilebilir olup olmadığı (**profil-bazlı**, **KARAR v0.33**; eski alan-düzeyi `Property.reOrder`'in yerini alır). |

> **Süreç Adımı Tetikleme / Değer Atama ile ilişki:** Form List **alt-servis** kayıtlarını bağlar; alt-servisin süreç adımları **Süreç Adımı Tetikleme** (process-step §3.5) adımıyla tetiklenebilir, **Değer Atama** (§3.4) bu alt-servisin değerleriyle çalışır. Alt-servisin **görüntülenecek alanları / seçilebilirliği** yine view-profile ile ayarlanır.
> **Açık nokta — red akışı bayrakları:** Eski kontrolde satır reddi için `isRejectReasonRequired` (red gerekçesi zorunlu mu) ve `isReapprovalLockedAfterReject` (reddedilen satır yeniden onaya kapalı mı) bayrakları vardı; bunlar değer şablonundaki `rejectedByReason`/`selected` alanlarıyla eşleşir ama **yeni tasarımda henüz bir katmana yerleştirilmemiştir** (aday: `settings` veya profil-bazlı) → [`../../../../todo.md`](../../../../todo.md).

## 4. JSON Schema (`settings`)
```json
{
  "$id": "property-settings/form-list",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "lazyLoading": { "type": "boolean", "default": false }
  }
}
```
> Not: İlişki FK'leri (`childServiceId`/`serviceItemControlId`) **çekirdek kolon**, seçim/oluşturma/sıralama ayarları **profil-bazlı** (`ProcessViewProfilePropertySetting`) olduğundan bu şemada **yer almaz**; şema yalnız alan-düzeyi `settings` JSONB'yi doğrular.

## 5. Örnek
```json
{ "lazyLoading": true }
```
> Profil-bazlı ayar örneği (bu şemaya değil, `ProcessViewProfilePropertySetting`'e ait): `activeStartActions=[101]` · `addFromExistingStatusIds=[3]` · `selectableVisible=true` · `reOrder=false`.

*Oluşturma: 2026-08-28.*
