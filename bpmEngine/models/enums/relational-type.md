# Enum — RelationalType

> **Kullanan model:** [`additional-qualification.md`](../organization-settings/additional-qualification.md) — alan `AdditionalQualificationRelation.relationalType`, tip **RelationalType**
> **Amaç:** Bir ek niteliğin **hangi organizasyon varlığına** uygulanacağını belirler; değerin saklanacağı `...QualificationValue` alt modelini seçer.

## Değerler
| Index | Değer | Hedef varlık | Ne için |
|---|---|---|---|
| 0 | `users` | [`user.md`](../organization-settings/user.md) | Niteliği kullanıcılara iliştirmek. |
| 1 | `departments` | [`department.md`](../organization-settings/department.md) | Niteliği departmanlara iliştirmek. |
| 2 | `professions` | [`profession.md`](../organization-settings/profession.md) | Niteliği mesleklere iliştirmek. |
| 3 | `costCenters` | [`cost-center.md`](../organization-settings/cost-center.md) | Niteliği masraf merkezlerine iliştirmek. |
| 4 | `workerLevels` | [`worker-level.md`](../organization-settings/worker-level.md) | Niteliği çalışan seviyelerine iliştirmek. |

*Oluşturma: 2026-07-10.*
