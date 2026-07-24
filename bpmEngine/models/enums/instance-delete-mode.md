# Enum — InstanceDeleteMode

> **Kullanan model:** [`process-step.md`](../service-settings/process-step.md) — **Instance Deleter** adımı ayarı, alan `deleteMode`, tip **InstanceDeleteMode**
> **Amaç:** Instance Deleter adımının **silme davranışını** belirler — ilişkili formlar da silinsin mi, yoksa yalnız ilişki mi kaldırılsın.
> **Davranış:** → [`../../service-settings/process-step.md`](../../service-settings/process-step.md) §3.10.

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `withRelated` | Formu ve ilişkili formları sil | Sürecin instance'ı **ve** ilişkili instance'lar `deleted = true` yapılır. |
| `unlinkRelated` | Formu sil, ilişkili formların ilişkisini kaldır | Sürecin instance'ı `deleted = true` yapılır; `AssociatedInstance` kayıtları **silinir** (ilişki kaldırılır); **ilişkili instance'ların `deleted` durumuna dokunulmaz**. |

## Notlar
- Formlar arası ilişki `AssociatedInstance` üzerinden tutulur (→ [`../processInstances/index.md`](../processInstances/index.md)).

*Oluşturma: 2026-07-16.*
