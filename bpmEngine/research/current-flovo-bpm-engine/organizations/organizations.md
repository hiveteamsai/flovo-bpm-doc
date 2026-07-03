# Organizasyon Ayarları (Organization Settings)

Bu doküman seti, Flovo uygulamasındaki **Organizasyon Ayarları** modülünü (`Ayarlar > Organizasyon Ayarları`) analiz eder. Organizasyon ayarları, BPM motorunun üzerinde çalıştığı **organizasyonel altyapıyı** (şirketler, kullanıcılar, departmanlar, hiyerarşiler, takvimler vb.) tanımlar. Süreç adımlarındaki onay merci atamaları, zaman aşımı hesaplamaları ve yetkilendirmeler bu ayarlara dayanır.

> **Kapsam Notu:** Bu analiz **para birimleri, pozisyonlar, vergi oranları ve çeviriler** ayarlarını kapsam dışında bırakır.

---

## Giriş Noktası

Organizasyon ayarları ana sayfası, tüm alt ayarları kart (`SettingsCard`) olarak listeler:

```
lib/Pages/Settings/OrganizationSettings/SettingOrganizationPage.dart
```

Bazı kartlar yetki seviyesine göre koşullu gösterilir (örn. çeviriler `authorizationLevel >= 300`).

---

## Ortak Mimari İlkeler

Organizasyon ayarları bileşenleri tutarlı bir yapı izler:

- **Liste + Detay Deseni:** Her ayar bir `...Page.dart` (liste) ve bir `...DetailPage.dart` (düzenleme) sayfasından oluşur.
- **DTO Serileştirme:** Tüm modeller `fromJson` / `toJson` metodlarına sahiptir.
- **`IOrganizationParameter` Arayüzü:** Çoğu model bu arayüzü uygular; böylece iş kurallarındaki veri kaynaklarında (FillDataSource) ortak biçimde kullanılabilir. Arayüz `getCode`, `getName`, `companyCode`, `getSubText`, `getAdditionalQualification` gibi getter'lar sağlar.
- **REST API:** Tüm işlemler `RemoteApiService` üzerinden POST isteği ile yürütülür; `accountId`, `solutionid` ve `ServiceId` başlıkları gönderilir.
- **Çok Şirketlilik:** Bileşenler `selectedCompanyIds` / `accountCompanyDtos` ile bir veya birden fazla şirkete bağlanır.
- **Ek Nitelikler:** Kullanıcı, departman, ünvan, masraf merkezi ve çalışan seviyesi varlıkları dinamik ek alanlarla (ek nitelikler) genişletilebilir.

---

## Bileşenler ve Referanslar

### 1. [Şirketler](./companies.md)
Organizasyonun tüzel kişiliklerini tanımlar. Diğer tüm bileşenlerin şirket bağlantısının temelidir. Varsayılan şirket ve senkronizasyon desteği içerir.

### 2. [Departmanlar](./departments.md)
Hiyerarşik birim yapısı; departman yöneticisi, üst departman ve masraf merkezi bağlantıları. BPM'de "departman yöneticisi" atamalarında kullanılır.

### 3. [Ünvanlar](./titles.md)
Çalışan görev/meslek tanımları (kod içinde `Profession`). "Ünvana göre yönetici" atamalarında kullanılır.

### 4. [Kullanıcılar](./users.md)
Organizasyondaki kişiler; departman, ünvan, yönetici, masraf yeri, çalışma takvimi bağlantıları, yetki seviyesi, harcama limitleri ve çözüm erişimleri. BPM onay mercilerinin temelidir.

### 5. [Kullanıcı Grupları](./user-groups.md)
Toplu onay, bildirim ve aksiyon görünürlük yetkilendirmesi için kullanıcı toplulukları.

### 6. [Ek Nitelikler](./additional-qualifications.md)
Organizasyon varlıklarına eklenebilen dinamik/özel alanlar. Kullanıcı, departman, ünvan, masraf merkezi ve çalışan seviyesi ile ilişkilendirilebilir.

### 7. [Masraf Merkezi](./expense-center.md)
Maliyet takibi yapılan muhasebesel birimler (Cost Center). Departman ve kullanıcılara bağlanır.

### 8. [Çalışan Seviyeleri](./worker-levels.md)
Personel kademe/seviye tanımları. Kullanıcılara atanır.

### 9. [Çalışma Takvimleri](./working-schedules.md)
Haftalık çalışma saatleri (7 gün, iki periyot). BPM Timer/zaman aşımı hesaplamalarının temeli.

### 10. [Tatil Günleri](./vacation-days.md)
Resmi tatil/çalışılmayan günler (tam veya yarım gün). Çalışma takvimi ile birlikte süre hesaplamalarında kullanılır.

### 11. [Kredi Kartları](./credit-cards.md)
Masraf süreçlerinde kullanılan kurumsal kartlar. Şirket/kullanıcı bağlantısı ve ortak kart desteği.

### 12. [Süreç Transferi](./process-transfer.md)
Bir kullanıcının bekleyen süreç görevlerinin başka bir kullanıcıya servis bazında devredilmesi.

### 13. [Zamanlanmış Görevler](./scheduler-jobs.md)
Cron tabanlı arka plan görevleri; aktif/pasif yönetimi, log izleme ve manuel tetikleme.

---

## Bileşen İlişkileri

```
Şirket (Company)
  ├── Departman ──► Yönetici (User), Üst Departman, Masraf Merkezi
  ├── Ünvan (Profession)
  ├── Masraf Merkezi (Cost Center)
  ├── Kredi Kartı
  └── Kullanıcı (User)
        ├── Departman, Ünvan, Yönetici, Masraf Yeri
        ├── Çalışan Seviyesi
        ├── Çalışma Takvimi ──► Tatil Günleri (süre hesabı)
        ├── Kullanıcı Grupları (üyelik)
        ├── Kredi Kartları
        └── Ek Nitelikler (dinamik alanlar)

Ek Nitelikler ──► Kullanıcı / Departman / Ünvan / Masraf Merkezi / Çalışan Seviyesi
Süreç Transferi ──► Kullanıcı (from/to) + Servis
Zamanlanmış Görevler ──► BPM zaman tabanlı otomasyonlar
```

---

## BPM Motoru ile İlişki

| Organizasyon Bileşeni | BPM'deki Kullanımı |
|-----------------------|--------------------|
| Kullanıcılar / Yönetici zinciri | Süreç adımı onay merci atamaları (kullanıcı, yönetici, yönetici zinciri) |
| Departman / Departman yöneticisi | "Departman yöneticisi" tipi kullanıcı ataması |
| Ünvanlar | "Ünvana göre yönetici" ataması |
| Kullanıcı grupları | Grup onayı, bildirim hedefi, aksiyon görünürlük yetkisi |
| Çalışma takvimi + Tatil günleri | Timer/zaman aşımı adımlarının "çalışma takvimine göre" hesaplaması |
| Masraf merkezi / Kredi kartı / Harcama limiti | Masraf/harcama süreçlerinin verileri |
| Zamanlanmış görevler | Zaman tabanlı otomatik süreç işlemleri |

---

## Konsolide API Endpoint Özeti

| Bileşen | Listele | Ekle/Güncelle | Sil |
|---------|---------|---------------|-----|
| Şirketler | `GetAccountCompanies` | `AddAccountCompany` / `UpdateAccountCompany` | `DeleteAccountCompany/{id}` |
| Departmanlar | `GetAccountDepartments` | `AddAccountDepartment` / `UpdateAccountDepartment` | `DeleteAccountDepartment/{id}` |
| Ünvanlar | `GetAccountProfessions` | `AddAccountProfession` / `UpdateAccountProfession` | `DeleteAccountProfession/{id}` |
| Kullanıcılar | `GetAccountUsers` | `AddAccountUser` / `UpdateAccountUser` | `ActivateAccountUser/{id}` |
| Kullanıcı Grupları | `GetUserGroups` | `AddOrUpdateUserGroup` | `DeleteUserGroup/{id}` |
| Ek Nitelikler | `GetAccountAdditionalQualifications` | `AddOrUpdateAccountAdditionalQualification` | `DeleteAccountAdditionalQualification/{id}` |
| Masraf Merkezi | `GetAccountCostCenters` | `AddAccountCostCenter` / `UpdateAccountCostCenter` | `DeleteAccountCostCenter/{id}` |
| Çalışan Seviyeleri | `GetAccountWorkerLevels` | `AddOrUpdateAccountWorkerLevel` | `DeleteAccountWorkerLevel/{id}` |
| Çalışma Takvimleri | `GetWorkingSchedule` | `AddOrUpdateWorkingSchedule` | `DeleteWorkingSchedule/{id}` |
| Tatil Günleri | `accountvacationdaysget` | `accountvacationdaysadd` / `accountvacationdaysupdate` | `accountvacationdaysdelete` |
| Kredi Kartları | `GetAccountCreditCards` | `AddOrUpdateAccountCreditCard` | `DeleteAccountCreditCard/{id}` |
| Süreç Transferi | `GetProcessTransferData` | `ProcessTransfer` | — |
| Zamanlanmış Görevler | `scheduler-jobs` | `scheduler-jobs/{id}/toggle-status`, `scheduler-jobs/{id}/invoke` | — |

---

## Dizin Yapısı

```
lib/Models/Settings/OrganizationSettings/     # Tüm DTO modelleri
lib/Pages/Settings/OrganizationSettings/
├── SettingOrganizationPage.dart              # Ana giriş sayfası
├── Companies/
├── Departments/
├── Titles/
├── Users/
├── UserGroup/
├── AdditionalQualification/
├── ExpenseCenter/
├── AccountWorkerLevel/
├── WorkingSchedule/
├── VacationDay/
├── CreditCards/
├── ProcessTransfer/
└── SchedulerJobs/
```

---

> Bu doküman seti [Flovo BPM Engine](../bpm-engine.md) dokümantasyonunun bir parçasıdır.
