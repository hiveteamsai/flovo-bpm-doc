# Enum — FormType

> **Kullanan model:** [`service.md`](../service-settings/service.md) — alan `formType`, tip **FormType**
> **Amaç:** Servisin **davranış türünü** belirler — akış olup olmadığını, instance oluşup oluşmadığını ve sahiplik/onay davranışını.
> **Ayrıntılı davranış:** → [`service.md`](../service-settings/service.md) `## formType` bölümü.

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `form` | Akışı olan, akıştaki **Instance Creator** adımıyla **instance** oluşan, `Instance.creatorUserId` **genelde dolu** (API/webhook başlatımında **null olabilir** → `ProcessInstance.createdByApiKeyId`), onay akışı işleyen ve `InstanceAwaitingUser` kaydı olabilen servis. | Sahipli, onaya tabi standart süreçler (ör. masraf formu); API ile başlatılıp gruba yönlendirilen süreçler. |
| `parameter` | Akışı olan fakat oluşan instance'lar **onay gerektirmeyen**, veri kaynağı amaçlı; instance oluşur ama `creatorUserId` **boş** (sahipsiz veri); yetkili kullanıcılar `InstanceAwaitingUser`'dan bağımsız işlem yapabilir. | Referans/veri kaynağı listeleri (ör. bayiler, şehirler, plakalar). |
| `eventForm` | Akışı **olmayan** ve instance **oluşmayan** servis; görüntüleme profili `eventForm` aksiyonunda pop-up olarak açılır, sonuç `parameters` ile döner. | Aksiyon anında geçici veri toplama (kalıcı instance yok). |

*Oluşturma: 2026-07-10.*
