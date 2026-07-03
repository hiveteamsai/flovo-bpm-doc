# Flovo — Yetkilendirme (Permissions) Tasarımı

> **Durum:** 🟢 DETAYLANIYOR
> **Amaç:** Organizasyon içindeki **yetkileri** tanımlamak. Yetkiler **organizasyon bazında**, **admin kullanıcılar** ve
> **kullanıcı grupları** üzerinden **dinamik** yönetilir.
> **İlişki:** Ayarlar **Organization** varlığında tutulur/ilişkilendirilir (→ `organization.md`); yetki grupları →
> `../models/organization-settings/user-group.md`. Model → `../models/organization-settings/organization.md`.

---

## 0. Neden değişti? (eski → yeni)
- **Eski:** Yetki **kullanıcı bazında** `authorizationLevel` (sayısal) idi; yetki artırmak sayıyı büyütmekti ve
  **dinamik ayarlanamıyordu** (sabit seviye eşikleri).
- **Yeni:** `User.authorizationLevel` **kaldırıldı**. Yetkiler **organizasyon bazında**, **admin** + **grup-bazlı** olarak
  **dinamik** tanımlanır.

---

## 1. Admin Kullanıcılar (`adminUserIds`)
- Organizasyonun **`adminUserIds`** listesi vardır (bir veya çok kullanıcı).
- **En az 1 aktif admin** bulunmak zorundadır (aktif = `User.active = true` ve `deleted = false`).
- **Adminler:**
  - Bu sayfadaki **tüm yetki yapılandırmasını** (admin listesi + grup atamaları) **değiştirebilen tek kullanıcılardır**.
  - **Yetki yapılandırması sayfasına** (bu sayfa) girip değiştirebilir — **yalnız adminler**. _(Yapısal organizasyon
    verisine erişim ise `organizationSettings` yetki grubuyla verilir.)_
  - **Diğer TÜM yetkilere** de örtük olarak sahiptir (aşağıdaki 4 yetki dahil).

---

## 2. Grup-Bazlı Yetkiler
Admin dışındaki yetkiler **kullanıcı bazında değil, kullanıcı grubu bazında** yönetilir. Her yetki için **bir kullanıcı
grubu** seçilir; **seçilen gruptaki kullanıcılar** o yetkiye sahip olur.

| Yetki | Organization alanı | Ne sağlar |
|---|---|---|
| **Kullanıcı yerine geçme** | `impersonationUserGroupId` | Bir kullanıcının **yerine geçip** onun adına işlem yapma. |
| **Organizasyon ayarları erişimi** | `organizationSettingsUserGroupId` | **Yapısal organizasyon ayarlarına** (şirket, departman, kullanıcı, ünvan, masraf merkezi, çalışma takvimi…) erişim/yönetim. |
| **Servis ayarları erişimi** | `serviceSettingsUserGroupId` | **Servis tasarım ayarlarına** (property, süreç adımı, görüntüleme profili, iş kuralı…) erişim. |
| **Tüm raporları görme** | `viewAllReportsUserGroupId` | Organizasyondaki **tüm raporları** görüntüleme. |

> **Yapılandırma vs erişim:** Yetki **yapılandırmasını** (admin listesi + grup atamaları) yalnız **adminler** değiştirir.
> `OrganizationSettings` yetkisi ise gruba **yapısal veriyi** yönetme erişimi verir; **admin/yetki yapılandırması** yine admin'e özeldir.

---

## 3. Yetki Çözümleme (resolution)
Bir kullanıcının **P yetkisi** var mı?

```
hasPermission(user, P):                                   # P: impersonation / organizationSettings / serviceSettings / viewAllReports
  if (user ∈ organization.adminUserIds):   return true      # admin → TÜM yetkiler
  groupId = organization.{P}UserGroupId                   # P için seçilen tek grup alanı
  return (groupId != null) AND (user ∈ members(groupId))
```

- **Admin** ⟹ tüm yetkiler **+ yetki yapılandırmasını düzenleme**.
- Aksi hâlde: kullanıcı, **P için seçilen grubun üyesiyse** yetkiye sahiptir.
- Pasif/silinmiş kayıtlar (`active=false` / `deleted=true`) yetki hesabında dikkate alınmaz.

---

## 4. Organizasyon Modeliyle İlişki
Bu ayarlar **Organization** varlığında **doğrudan alanlar** olarak tutulur ve **organizasyon ayarları sayfasında listelenir**:
- **`adminUserIds`** — admin kullanıcılar (List → `User`).
- Her yetki için **tek** kullanıcı grubu alanı (FK → `UserGroup`): `impersonationUserGroupId` · `organizationSettingsUserGroupId` ·
  `serviceSettingsUserGroupId` · `viewAllReportsUserGroupId`.

Model → `../models/organization-settings/organization.md`.

---

## 5. Açık Kararlar / Sorular
- [ ] **Eski `authorizationLevel` bağımlılıkları:** `ProcessStepAction.authorizationLevel` (sayısal aksiyon yetkisi) bu
  modelle nasıl uyumlanacak? (Aksiyon görünürlüğü zaten `actionDisplayAuthorizedUserGroupId` ile grup-bazlı.)
- [ ] **Impersonation** kapsamı/denetimi (kimin yerine geçilebilir, log/audit).
- [ ] Yetki setinin **genişletilebilirliği** (yeni yetki = Organization'a yeni `*UserGroupId` alanı).
- [ ] "Organizasyon ayarları sayfası"nda **admin-only yetki yapılandırması** ↔ `OrganizationSettings` grubu erişimi sınırı netleşmeli.

---

*Oluşturma: 2026-07-03.*
