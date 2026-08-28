# Enum — SyncStatus

> **Kullanan modeller:** organizasyon-ayarı **text-entity**'leri — alan `synchronizationStatus`, tip **SyncStatus**:
> [`company.md`](../organization-settings/company.md) · [`department.md`](../organization-settings/department.md) ·
> [`cost-center.md`](../organization-settings/cost-center.md) · [`credit-card.md`](../organization-settings/credit-card.md) ·
> [`position.md`](../organization-settings/position.md) · [`profession.md`](../organization-settings/profession.md) ·
> [`user.md`](../organization-settings/user.md) · [`worker-level.md`](../organization-settings/worker-level.md) ·
> [`vacation-day.md`](../organization-settings/vacation-day.md)
> **Amaç:** Bir organizasyon-ayarı kaydının **harici sistemle (ERP / muhasebe) senkron durumunu** belirtir — kaydın son
> senkronizasyonda başarıyla eşlenip eşlenmediğini, beklemede mi yoksa hatalı mı olduğunu ayırt eder.

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `synced` | Senkron | Kayıt harici sistemle **başarıyla eşlenmiş**; güncel. |
| `pending` | Beklemede | Kayıt oluşturuldu/değişti ama harici senkron **henüz tamamlanmadı** (kuyrukta). |
| `error` | Hata | Son senkronizasyon **başarısız** oldu; yeniden denenmeli / incelenmeli. |

## Notlar
- **3-state string-enum** — eski **bool** (yalnız oldu/olmadı) temsili yerini bu enum'a bıraktı (v0.36); tüm org-ayarı
  text-entity'lerinde **tek tip** kullanılır.
- Senkronizasyonun kendisi (hangi harici sistem, tetikleme, retry) org-ayarı model kapsamı dışıdır → entegrasyon fazı.

*Oluşturma: 2026-08-28.*
