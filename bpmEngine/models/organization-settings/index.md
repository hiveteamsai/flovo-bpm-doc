# Organizasyon Ayarları Modelleri — İndeks

> **Amaç:** Organizasyona (tenant) bağlı **yapısal veri** ve **organizasyon havuzu** modelleri (eski "Account Settings"
> DTO'larından türetildi). Tümü **`organizationId` (int)** ile kiracıya bağlıdır. Veri modeli/şema odaklı; davranış → `../../organization-settings/`.

## Dökümanlar
| Döküman | Özet |
|---|---|
| [`organization.md`](./organization.md) | Flovo'yu kullanan **kurumu (tenant)** temsil eder; verinin en üst kapsayıcısı. |
| [`company.md`](./company.md) | Organizasyonun **tüzel kişilikleri** (şirketler); çok-şirket temeli. |
| [`department.md`](./department.md) | **Hiyerarşik birim** yapısı; "departman yöneticisi" atamalarında kullanılır. |
| [`profession.md`](./profession.md) | Çalışan **görev/meslek** (ünvan) tanımları; "ünvana göre yönetici" atamaları. |
| [`position.md`](./position.md) | Organizasyonel **görev yeri** (şirkete bağlı) + **Staff (kadro)** alt modeli (1 kadro ↔ 1 kullanıcı). |
| [`user.md`](./user.md) | Organizasyondaki **kişiler**; BPM onay mercilerinin (kullanıcı/yönetici/…) temeli. |
| [`user-group.md`](./user-group.md) | **Kullanıcı grubu**; bildirim hedefi, aksiyon görünürlük yetkisi. |
| [`worker-level.md`](./worker-level.md) | Personel **kademe/seviye** tanımları; kullanıcılara atanır. |
| [`cost-center.md`](./cost-center.md) | **Masraf merkezi** (Cost Center); masraf süreçlerinde maliyet yansıtma birimi. |
| [`credit-card.md`](./credit-card.md) | Harcama süreçlerinde kullanılan **kurumsal kartlar**; şirkete/kullanıcıya bağlanır. |
| [`additional-qualification.md`](./additional-qualification.md) | Organizasyon varlıklarına eklenen **dinamik/özel alanlar** (+ RelationalType · QualificationValueType · QualificationItem). |
| [`action.md`](./action.md) | Yeniden kullanılabilir **aksiyon şablonu** (ActionDto); adıma eklenince kopyalanır. |
| [`status.md`](./status.md) | BPM kaydının **mevcut aşamasını** temsil eden etiket (örn. Beklemede, Onaylandı). |
| [`style.md`](./style.md) | Bir öğenin **renk/görünümünü** tanımlayan yeniden-kullanılabilir varlık (bg + font). |
| [`translation.md`](./translation.md) | Bir **`code`**'a bağlı metnin **çok dilli** karşılıkları (ortak + organizasyon). |
| [`working-schedule.md`](./working-schedule.md) | **Haftalık çalışma takvimi**; Timer/zaman aşımı "çalışma takvimine göre" hesabının temeli. |
| [`vacation-day.md`](./vacation-day.md) | Resmi tatil / **çalışılmayan günler**; iş günü/süre hesaplarında kullanılır. |
| [`process-transfer.md`](./process-transfer.md) | Bekleyen süreç görevlerinin **servis bazında devri** (operasyon). |
| [`scheduler-job.md`](./scheduler-job.md) | Cron tabanlı **arka plan görevleri** (+ log); zaman tabanlı otomasyon. |

*Oluşturma: 2026-07-13.*
