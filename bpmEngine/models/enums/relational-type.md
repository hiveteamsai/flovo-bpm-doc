# Enum — RelationalType (AdditionalQualification)

> **Kullanan model:** [`additional-qualification.md`](../organization-settings/additional-qualification.md) (`AdditionalQualificationRelation.relationalType`)
> **Amaç:** Bir ek niteliğin **hangi organizasyon varlığına** uygulanacağını belirler; değerin saklanacağı `...QualificationValue` alt modelini seçer.

## Değerler
| Index | Değer | Hedef varlık | Ne için |
|---|---|---|---|
| 0 | `Users` | [`user.md`](../organization-settings/user.md) | Niteliği kullanıcılara iliştirmek. |
| 1 | `Departments` | [`department.md`](../organization-settings/department.md) | Niteliği departmanlara iliştirmek. |
| 2 | `Professions` | [`profession.md`](../organization-settings/profession.md) | Niteliği mesleklere iliştirmek. |
| 3 | `CostCenters` | [`cost-center.md`](../organization-settings/cost-center.md) | Niteliği masraf merkezlerine iliştirmek. |
| 4 | `WorkerLevels` | [`worker-level.md`](../organization-settings/worker-level.md) | Niteliği çalışan seviyelerine iliştirmek. |

*Oluşturma: 2026-07-10.*
