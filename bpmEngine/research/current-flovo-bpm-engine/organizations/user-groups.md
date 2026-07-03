# Kullanıcı Grupları (User Groups)

## Genel Bakış

Kullanıcı grupları, birden fazla kullanıcıyı bir arada toplayan yapılardır. BPM süreçlerinde toplu onay (grup onayı), bildirim gönderimi ve aksiyon görünürlük yetkilendirmesi gibi senaryolarda kullanılır. Örneğin "Kullanıcı Grubu" tipi süreç adımı bir gruba atanabilir.

---

## Veri Modeli (AccountUserGroupDto)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Grup ID'si |
| `code` | String | Grup kodu |
| `definition` | String | Grup adı/tanımı |
| `accountId` | String | Hesap ID'si |
| `accountUserGroupMembers` | List\<AccountUserGroupMemberDto\> | Grup üyeleri |
| `accountCompanyDtos` | List\<AccountCompanyDto\> | İlişkili şirketler |

`AccountUserGroupDto`, `IOrganizationParameter` arayüzünü uygular.

---

## Grup Üyesi (AccountUserGroupMemberDto)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Üyelik kayıt ID'si |
| `accountUserGroupId` | int | Bağlı grup ID'si |
| `userId` | int | Kullanıcı ID'si |
| `fullName` | String | Kullanıcı adı-soyadı |
| `photoUrl` | String | Profil fotoğrafı |
| `companyId` | int | Üyenin şirket ID'si |

---

## Liste Yanıtı (GetAccountUserGroupDto)

| Alan | Açıklama |
|------|----------|
| `accountUserGroupDtos` | Kullanıcı grupları listesi |
| `accountCompanyDtos` | Şirket seçimi için şirketler |

---

## Çalışma Prensibi

1. **Grup Tanımlama:** Kod ve tanım ile grup oluşturulur.
2. **Üye Ekleme:** `accountUserGroupMembers` listesi ile kullanıcılar gruba eklenir (`UserMemberDetailPage`).
3. **BPM Kullanımı:**
   - **Grup Onayı:** "Kullanıcı Grubu" süreç adımında gruba görev atanır; `groupApproval` ile toplu onay davranışı belirlenir.
   - **Bildirim:** Bildirim adımlarında hedef alıcı grubu olarak seçilebilir.
   - **Aksiyon Görünürlüğü:** Aksiyonların `actionDisplayAuthorizedUserGroupId` alanı ile bir aksiyonu sadece belirli grubun görmesi sağlanabilir.
   - **Rapor Erişimi:** Görüntüleme profili raporları belirli gruplara açılabilir.

---

## API Endpoint'leri

| Endpoint | HTTP | Açıklama |
|----------|------|----------|
| `GetUserGroups` | POST | Grupları listele |
| `AddOrUpdateUserGroup` | POST | Grup ekle/güncelle |
| `DeleteUserGroup/{id}` | POST | Grup sil |

---

## Dosya Yapısı

```
lib/Models/Settings/OrganizationSettings/
└── AccountUserGroupDto.dart   # GetAccountUserGroupDto, AccountUserGroupDto, AccountUserGroupMemberDto

lib/Pages/Settings/OrganizationSettings/UserGroup/
├── UserGroupPage.dart          # Liste sayfası
├── UserGroupDetailPage.dart    # Grup detay sayfası
└── UserMemberDetailPage.dart   # Üye ekleme/düzenleme
```
