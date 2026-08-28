# İş Kuralı — Veri Kaynağı Modelleri (`data-source/`)

> **Amaç:** `fillDataSource` (liste doldurma) ve `fromDataSet` (tek değer) kaynaklarının **sorgu/filtre** şekilleri.
> **Üst indeks:** [`../index.md`](../index.md)

| Döküman | Özet |
|---|---|
| [`assign-value-from-dataset.md`](./assign-value-from-dataset.md) | Başka servisin instance'larından değer/liste sorgusu (`fromDataSet` / `serviceInstances`). |
| [`assign-value-from-dataset-parameter.md`](./assign-value-from-dataset-parameter.md) | Yukarıdaki sorgunun satır filtresi. |
| [`fill-data-source-organization.md`](./fill-data-source-organization.md) | `organizationData` kaynağı (kurum master-verisi + `companyId`). |
| [`fill-data-source-user.md`](./fill-data-source-user.md) | `userData` kaynağı (oturum kullanıcısının verisi). |
| [`fill-data-source-parameter.md`](./fill-data-source-parameter.md) | org/user kaynaklarının **ortak** satır filtresi (`parameter` + `value` + operatör). |

> Kaynakları tüketen aksiyon: **`../actions/fill-data-source.md`**. Değer modeli: **`../shared/assign-value.md`**.

*Oluşturma: 2026-08-26.*
