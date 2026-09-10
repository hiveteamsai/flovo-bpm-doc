# Model — Service (servis / form)

> **Durum:** 🟢 Gözden geçirildi (v0.36)
> **Amaç:** Bir **iş sürecinin/formun** tamamı (örn. İzin Talebi, Masraf). Motorun temel birimi. Bir **solution
> altında** oluşturulur; **kendi ayarlarını** (property, görüntüleme profili, süreç adımı, iş kuralı) barındırır.
> **Hiyerarşi:** `Organization → Solution → Service → {Property · ProcessViewProfile · ProcessStep · BusinessRule}`.

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Servis ID'si. |
| `solutionId` | int | FK → Solution.id | Bağlı solution (organizasyon buradan türetilir). |
| `code` | string | benzersiz | Servis kodu (izolasyon başlığı `serviceId`; dış referans). |
| `definition` | string | — | Servis (form) adı/tanımı. |
| `translationCode` | string? | çeviri anahtarı | **Çeviri eşleşme anahtarı** (→ [`../organization-settings/translation.md`](../organization-settings/translation.md) `code`). `null` = çeviri **es geçilir**, doğrudan `definition` kullanılır. |
| `formType` | FormType | — | Servisin **davranış türü** — [`../enums/form-type.md`](../enums/form-type.md): `form` · `parameter` · `eventForm` (varsayılan **`form`**). Bkz. "formType — Servis davranış türü". |
| `currentVersion` | int? | — | **Yayınlanmış geçerli versiyon** numarası (`null` = henüz yayınlanmadı). Çalışan instance'lar başlatıldıkları versiyonun tanımını kullanır. → "Versiyonlama & yayınlama". |
| `hasUnpublishedChanges` | bool | — | Son yayından beri **taslak (draft) değişiklik** var mı (Designer'da düzenlendi, henüz publish edilmedi). |
| `lastPublishedAt` | datetime? | — | **Son yayınlama** zamanı (`null` = hiç yayınlanmadı). |
| `archivedAt` | datetime? | — | **Arşivlenme** zamanı (`null` = aktif). Soft + geri-alınabilir → "Arşivleme". |
| `archivedBy` | int? | FK → User.id | **Arşivleyen** kullanıcı. |

## `formType` — Servis davranış türü
Enum tanımı → [`../enums/form-type.md`](../enums/form-type.md). Bir servis, `formType` değerine göre **üç farklı davranış** sergiler:

### `form` — standart iş süreci (varsayılan)
- **Akışı vardır**; akış içindeki **Instance Creator** adımlarıyla **`Instance` oluşturulur** (`Instance` yalnız Instance Creator ile oluşur).
- Oluşan `Instance`'ın **genelde bir sahibi vardır**: **`Instance.creatorUserId` dolu**. Ancak süreç **API/webhook ile
  başlatılıp** (tek bir oluşturan kullanıcı olmadan, ör. bir gruba yönlendirilerek) çalışabilir; bu durumda
  **`creatorUserId` null olabilir** ve başlatan **`ProcessInstance.createdByApiKeyId`** ile izlenir. Yani `form` tipinde
  `creatorUserId` **zorunlu dolu değildir**. _(örn. `../../sampleProcess/referred`.)_
- **`InstanceAwaitingUser`** tablosunda kayıt oluşabilir — aksiyonu **belirli kişiler** alır (ör. yönetici onayı, muhasebe onayı).
- Bir **onay akışına** sahiptir.
- Örn: İzin Talebi, Masraf, Satın Alma.

### `parameter` — veri kaynağı (onaysız)
- **Akışı vardır** fakat oluşan `Instance`'lar **onay akışı gerektirmez**. Amaç: başka servisleri (combobox / Form List
  vb.) besleyen **veri kaynağı** kayıtları oluşturmak.
- **`Instance` oluşur** ancak **sahibi yoktur**: **`Instance.creatorUserId` boş (null)**.
- **`InstanceAwaitingUser` kaydına bakılmaksızın**, **yetkili kullanıcılar** yeni `Instance` **oluşturma / güncelleme /
  aksiyon alma** yetkisine sahiptir _(yetki → `../../organization-settings/permissions.md`)_.
- Örn: Bayiler, Şehirler, Plakalar.

### `eventForm` — akışsız / instance'sız pop-up formu
- **Akışı yoktur** ve **`Instance` oluşmaz**. Servis ayarlarında yine **`Property` · `ProcessViewProfile` · `BusinessRule`**
  oluşturulabilir (süreç adımı anlamlı değildir).
- **`eventForm` actionType** ile kullanılır: bir aksiyon `eventForm` türünde tanımlanırken **`formType = eventForm`** olan
  servislerin **görüntüleme profilleri listelenir**; kullanıcı aksiyonu alırken **seçili profildeki alanlar (property)
  pop-up** olarak çıkar, **iş kuralları (`BusinessRule`)** ile alanlara özellik kazandırılabilir.
- Pop-up sonucu girilen değerler **aksiyon parametresi (`parameters`)** ile iletildiğinden, eventForm servisi için
  **`Instance` oluşturulmasına veya akışa gerek yoktur**.
- → `../../service-settings/process-step-action.md` §3.2 (eventForm aksiyonu).

## İlişkiler
- **N – 1** → `Solution` (`solutionId`) → (dolaylı) `Organization`.
- **1 – N** ← `Property`, `ProcessViewProfile`, `ProcessStep`, `BusinessRule`, `ServiceTrigger` (hepsi `serviceId`).
- **← `ServiceTrigger.targetServiceId`:** başka servislerin tetikleyicileri bu servisi **hedef** alabilir (bir `subProcessStart`'ı başlatarak) → [`service-trigger.md`](./service-trigger.md).
- **Kullanır (organizasyon havuzu):** `Action`, `Status`, `Style`, `Translation` — organizasyona bağlı bu veriler,
  bu servisin modellerinde **kullanılabilir** (örn. adıma aksiyon eklerken `Action` alanları `ProcessStepAction`'a
  **kopyalanır**; durum `ProcessStepAction.changeStatusId` ile atanır).

## İzolasyon
Çalışma zamanı kayıt izolasyonu **üç başlık**: `organizationId` · `solutionId` · `serviceId` (→ `../../architectures/engine-core/flovo-bpm-engine.md` §9).

## Versiyonlama & yayınlama (draft / publish)
> **Durum:** 🟢 Pilotta inşa edildi (v0.41-1) → [`../../implementation-status.md`](../../implementation-status.md).

Servis ayarları **taslak → yayınla (draft/publish)** akışıyla yönetilir:
- **Taslak (draft):** Designer'da yapılan değişiklikler doğrudan canlıya gitmez; `hasUnpublishedChanges = true` olur.
- **Yayınla (publish):** taslak değişiklikler yeni bir **versiyon** olarak sabitlenir → `currentVersion` artar, `lastPublishedAt`
  güncellenir, `hasUnpublishedChanges = false` olur.
- **Versiyon geçmişi = `ServiceVersion`** (fiziksel `service_version`): her yayın bir satır; yayınlanan servis tanımının **anlık
  görüntüsü (snapshot)**. Çalışan instance'lar **başlatıldıkları versiyonun** tanımını kullanır (yayın sonrası eski instance'lar etkilenmez).
- **Kod kilidi (code-lock):** bir kaynak **yayınlandıktan** sonra `code` **değişmez** (taslak penceresi dışında rename yok →
  [`../../architectures/api/settings-api.md`](../../architectures/api/settings-api.md) §5 · [`property.md`](./property.md) §1.1).

**`ServiceVersion` modeli (özet):**
| Alan | Tip | Anahtar | Açıklama |
|---|---|---|---|
| `id` | int | PK | Versiyon kaydı. |
| `serviceId` | int | FK → Service.id | Hangi servisin versiyonu. |
| `version` | int | — | Sıra numarası (`Service.currentVersion` bunu işaret eder). |
| `publishedAt` | datetime | — | Yayın zamanı. |
| `publishedByUserId` | int? | FK → User.id | Yayınlayan kullanıcı. |

> Alan detayları pilot uygulama reposundan türetildi (implementation-status.md); **snapshot içeriği** (yayınlanan tanımın hangi
> alanları saklanır) + **ortamlar-arası kopya** tasarımda genişletilecek → `../../todo.md` ("Ortam modeli").

## Arşivleme
> **Durum:** 🟢 Pilotta inşa edildi (v0.41-1) → implementation-status.

- **Soft + geri-alınabilir:** servis `archivedAt`/`archivedBy` ile işaretlenir, **silinmez** (Archive / Unarchive ile geri alınır).
- **`ArchivedChecker` (cross-domain guard, read-only):** arşivli bir servisin (parent) alt kaynaklarına — **property · view-profile ·
  service · publish** — **yazma yolları reddedilir** (`FailedPrecondition`); okuma serbest.
- **`archiveFilter`** (liste sorgularında): `active` (varsayılan) · `archived` · `all`.

## Notlar / açık noktalar
- Ek alanlar (ikon, thumbnail, durum, yetki) ve **Solution** modeli detaylandırılacak → `../../todo.md`. (**Versiyonlama & arşivleme**
  yukarıda modellendi — pilotta inşa edildi; kalan detaylar todo'da.)
- **Pilot sadeleştirmesi — `Process ≡ Service` (1:1):** pilotta bir servis tek bir sürece karşılık gelir; tasarım ise bir Service içinde
  **alt-süreç** (subProcessStart · `ProcessInstance.parentProcessInstanceId`) ile **çok ProcessInstance** modeller. 1:1, pilotun **kapsam
  sınırıdır**; alt-süreç tasarım hedefinde kalır. → `../../implementation-status.md`.

*Oluşturma: 2026-07-02.*
