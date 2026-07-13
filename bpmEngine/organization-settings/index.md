# Organizasyon Ayarları (Davranış) — İndeks

> **Amaç:** Tüm servislerde ortak kullanılan **genel ayarların davranış/kullanım** dokümanları. Bir kez tanımlanır,
> tüm servislerde kullanılır. **Şema/model karşılığı** ayrı tutulur → [`../models/organization-settings/index.md`](../models/organization-settings/index.md).

## Dökümanlar
| Döküman | Özet |
|---|---|
| [`action.md`](./action.md) | **Aksiyon şablonu (`ActionDto`)** — yeniden kullanılabilir aksiyon tanımı; adıma eklenince kopyalanır. |
| [`organization.md`](./organization.md) | **Organizasyon (tenant)** — Flovo'yu kullanan kurum; kullanıcı/servis/çevirilerin üst kapsayıcısı. |
| [`permissions.md`](./permissions.md) | **Yetkilendirme** — org-bazlı yetkiler: admin kullanıcılar + grup-bazlı (impersonation, ayar erişimi, raporlar). |
| [`status.md`](./status.md) | **Durum (status)** — bir kaydın mevcut aşamasını gösteren durum varlığı (etiket). |
| [`style.md`](./style.md) | **Style (renk/görünüm)** — çapraz-kesen renk/görünüm varlığı; aksiyon/durumda kullanılır (form alanları kullanmaz). |
| [`translation.md`](./translation.md) | **Çeviri (translation)** — `code`-bazlı çok dilli metinler; Flovo (ortak) + organizasyon çevirileri, override çözümlemesi. |

*Oluşturma: 2026-07-13.*
