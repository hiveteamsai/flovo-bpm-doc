# Model — Service (servis / form)

> **Durum:** 🟡 TASLAK (alanlar başlangıç — detaylandırılacak)
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
| `formType` | FormType | — | Servisin **davranış türü** — [`../enums/form-type.md`](../enums/form-type.md): `form` · `parameter` · `eventForm` (varsayılan **`form`**). Bkz. "formType — Servis davranış türü". |

## `formType` — Servis davranış türü
Enum tanımı → [`../enums/form-type.md`](../enums/form-type.md). Bir servis, `formType` değerine göre **üç farklı davranış** sergiler:

### `form` — standart iş süreci (varsayılan)
- **Akışı vardır**; akış ilerledikçe **`Instance` oluşabilir**.
- Oluşan `Instance`'ın **sahibi vardır**: **`Instance.creatorUserId` dolu**.
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
- **1 – N** ← `Property`, `ProcessViewProfile`, `ProcessStep`, `BusinessRule` (hepsi `serviceId`).
- **Kullanır (organizasyon havuzu):** `Action`, `Status`, `Style`, `Translation` — organizasyona bağlı bu veriler,
  bu servisin modellerinde **kullanılabilir** (örn. adıma aksiyon eklerken `Action` alanları `ProcessStepAction`'a
  **kopyalanır**; durum `ProcessStepAction.changeStatusId` ile atanır).

## İzolasyon
Çalışma zamanı kayıt izolasyonu **üç başlık**: `organizationId` · `solutionId` · `serviceId` (→ `../../flovo-bpm-engine.md` §9).

## Notlar / açık noktalar
- Ek alanlar (ikon, thumbnail, durum, versiyon, yetki) ve **Solution** modeli detaylandırılacak → `../../todo.md`.

*Oluşturma: 2026-07-02.*
