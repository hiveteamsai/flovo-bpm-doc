# Model — ServiceTrigger (servis tetikleyicisi)

> **Durum:** 🟡 TASLAK (ilk inşa — alanlar/kenar durumlar detaylandırılacak)
> **Amaç:** Bir servise bağlı, **olay/zaman-güdümlü otomatik** tetikleyici. Servisin instance'larında **belirli bir
> değişiklik** olduğunda (ilişki eklenir/kaldırılır) **veya bir süre dolduğunda**, başka bir servisteki bir **süreç/alt-süreç
> başlangıcını** otomatik çalıştırır. Böylece bir formdaki değişiklik ya da bir zamanlama, bir süreci **akıştan bağımsız**
> başlatabilir (senkronizasyon/performans yükü olmadan).
> **Hiyerarşi:** `Service → ServiceTrigger` (bir servis **N** trigger'a sahip olabilir).

## Konum / farkı
- **`triggerProcessStep` (akış üzeri):** bir **süreç adımıdır**; akış bu adıma **girdiğinde**, ayarlarına göre tetiklemesi
  gereken **alt süreci veya aksiyonu** tetikler. Tetikleme **akışın o adıma gelmesine** bağlıdır (sürece elle yerleştirilir).
- **`ServiceTrigger` (akış dışı — bu model):** servisin **otomatik** tetikleyicileridir; **belirli bir eylem gerçekleştiğinde**
  (ilişki eklenir/kaldırılır) **veya bir zamanlamada** (cron) **kendiliğinden** çalışır — akışın bir adıma gelmesini beklemez.
- **Tetiklenen hedef — tipe göre değişir:** `timer` → hedef servisin **`processStart`** (ana süreç başlangıcı) düğümünü,
  **yeni bağımsız bir ana süreç** olarak başlatır; associate tipleri → **`subProcessStart`** (alt süreç) düğümünü, kaynak
  instance'a **bağlı bir alt süreç** olarak başlatır (→ [`process-step.md`](./process-step.md) §2).

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Trigger ID'si. |
| `serviceId` | int | FK → Service.id | Trigger'ın **bağlı olduğu** servis — tetikleyici olay **bu servisin instance'larında** izlenir (kaynak servis). |
| `code` | string | benzersiz `(serviceId, code)` | Trigger kodu (iç/dış referans). |
| `definition` | string | — | Trigger adı/tanımı (yönetim ekranında görünen). |
| `serviceTriggerType` | ServiceTriggerType | — | **Hangi olayda** tetikleneceği — `timer` / `whenAddedAssociate` / `whenRemoveAssociate` (→ [`../enums/service-trigger-type.md`](../enums/service-trigger-type.md)). |
| `cronExpression` | string? | — | **(yalnız `timer`)** Zamanlamayı belirleyen **cron ifadesi** (ör. `0 9 * * 1` = her Pazartesi 09:00). `timer` dışındaki tiplerde boş. |
| `targetPropertyId` | int? | FK → Property.id | **(yalnız `whenAddedAssociate`/`whenRemoveAssociate`)** İzlenen **ilişki alanı** (Form List / `isAssociatedCombobox` Combobox). Bir `AssociatedInstance` satırının `associatedPropertyId`'si buna eşit olduğunda trigger ateşlenir. **Değişmez:** `Property(targetPropertyId).serviceId == serviceId` (trigger'ın **kendi** servisinin ilişki alanı). Associate dışı tiplerde boş. |
| `targetServiceId` | int | FK → Service.id | Tetiklendiğinde **hangi servisin** alt süreç başlangıcı çalıştırılacak (hedef servis). |
| `targetStarterProcessStepId` | int | FK → ProcessStep.id | `targetServiceId` içindeki **hangi başlangıç adımının** tetikleneceği. **Adım tipi `serviceTriggerType`'a göre:** `timer` → **`processStart`** (ana süreç başlangıcı); `whenAddedAssociate`/`whenRemoveAssociate` → **`subProcessStart`** (alt süreç). **Değişmez:** `ProcessStep(targetStarterProcessStepId).serviceId == targetServiceId` **ve** `stepType == (timer ? processStart : subProcessStart)`. |
| `async` | bool | — | Tetikleme sonrası **beklenip beklenmeyeceği**: `true` → tetiklenen alt süreç **beklenmez** (fire-and-forget; tetikleyen işlem hemen devam eder); `false` → tetikleyen işlem, tetiklenen alt süreç **Süreç Bitişi'ne** (alt süreçte `subProcessEnd`) **ilerleyene kadar bekler** (o ana dek bloke olur). |
| `parameters` | DynamicParameter[] | — | Tetiklenen alt sürece **kaynak servis instance'ından** aktarılacak veri (ad → değer kaynağı). Alt-model **`DynamicParameter`** → [`process-step.md`](./process-step.md) §3.1 (`name` + `value`: `fixedValue`/`propertyValue`/`fromCalculation`). |
| `order` | int | — | Servis içindeki tetikleyici **sırası** (aynı olayda birden çok trigger eşleşirse yürütme/gösterim sırası). |
| `active` | bool | — | Pasif (`false`) trigger motor tarafından **kullanılmaz** (varsayılan `true`). |
| `deleted` | bool | — | Silinmiş (`true`) trigger **gizli/kullanılmaz** (varsayılan `false`). |

## Çalışma zamanı (davranış — özet)
**Olay tespiti (associate) — çekirdek (core):** `whenAddedAssociate`/`whenRemoveAssociate` tespiti, **`AssociatedInstance`
tablosuna yazım (AddOrUpdate / silme) sırasında** — yani **DB güncelleme katmanında** — yapılır. Böylece tetikleme **çekirdek
bir özellik** olur; ilişki kuran/kaldıran her yerde (Form List ekleme, `isAssociatedCombobox` seçimi, silme…) bu işi **ayrıca
tekrarlamak gerekmez**. Yazılan/silinen satır için, **`AssociatedInstance.associatedPropertyId == trigger.targetPropertyId`**
olan (ve tipi eşleşen, **aktif**) trigger'lar ateşlenir. `targetPropertyId` trigger'ın **kendi servisine** ait bir ilişki
alanı olduğundan (değişmez: `Property(targetPropertyId).serviceId == serviceId == Instance(associatedInstanceId).serviceId`),
**kaynak instance = `AssociatedInstance.associatedInstanceId`** — yani ilişki alanını **içeren üst form**.

> _Örnek:_ **masraf formu**'nda **masraf**'ları tutan bir Form List var; trigger `serviceId = masraf formu`, `targetPropertyId =
> Form List`. Bir masraf listeye eklenince satır `{instanceId=masraf, associatedInstanceId=masraf formu, associatedPropertyId=Form List}`
> yazılır → `associatedPropertyId == targetPropertyId` → trigger, **masraf formu** instance'ı üzerinden ateşlenir.

**Zamanlama (timer):** `serviceTriggerType == timer` iken tetikleme, **`cronExpression`** ile belirlenen takvime göre yapılır
(olay/kaynak instance yok; servis-global zamanlayıcı). Her cron tetiğinde hedef servisin **`processStart`** düğümü çalışır →
**yeni, bağımsız bir ana `ProcessInstance`** (`parentProcessInstanceId = null`). Kaynak instance olmadığından timer'ın
`parameters`'ı yalnız `fixedValue`/`fromCalculation` olabilir (`propertyValue` çözülemez).

Ateşlenince:
1. **Associate tipleri:** `parameters` **kaynak instance** (`associatedInstanceId`) üzerinden hesaplanır; `targetStarterProcessStepId` (**`subProcessStart`**) çalışır → yeni bir **alt** `ProcessInstance` (soy/lineage: `parentProcessInstanceId` = kaynak instance'ın süreci).
2. **`timer`:** `parameters` (sabit/hesaplanmış) hazırlanır; `targetStarterProcessStepId` (**`processStart`**) çalışır → yeni bir **bağımsız ana** `ProcessInstance` (`parentProcessInstanceId = null`).
3. `async=false` ise başlatan işlem, başlatılan süreç **Süreç Bitişi'ne** (alt süreçte `subProcessEnd`) ulaşana kadar **bekler**; `async=true` ise **beklemeden** devam eder.

## İlişkiler
- **N – 1** → `Service` (`serviceId` = kaynak servis; `targetServiceId` = hedef servis — ikisi de Service'e bağlanır, farklı olabilir).
- **N – 1** → `ProcessStep` (`targetStarterProcessStepId`; **`timer` → `processStart`**, **associate → `subProcessStart`** tipli adım).
- **N – 1** → `Property` (`targetPropertyId`; izlenen ilişki alanı — Form List / `isAssociatedCombobox`; `serviceId` ile aynı serviste).
- **İçerir:** `parameters` (DynamicParameter[] — ayrı tablo değil, ayarın parçası).

## Çözülen kararlar (v0.23)
- **Associate tespiti = çekirdek, AssociatedInstance yazımında** (yukarı "Çalışma zamanı"). Ayrı yerlerde tekrarlanmaz.
- **Associate filtresi = `targetPropertyId`:** yalnız `associatedPropertyId == targetPropertyId` olan yazımlar tetikler; **kaynak instance = `associatedInstanceId`** (ilişki alanını içeren üst form). "Hangi taraf" belirsizliği de böylece kapandı.
- **`timer` = `cronExpression` + `processStart`:** zamanlama cron ile belirlenir; timer **alt süreç değil**, hedef servisin **`processStart`** düğümünü çalıştırıp **yeni bağımsız bir ana süreç** başlatır (kaynak instance yok; `parentProcessInstanceId = null`). Associate tipleri ise `subProcessStart` (alt süreç) başlatır.
- **`async` semantiği:** `true` → beklenmez; `false` → başlatılan süreç **Süreç Bitişi'ne** ulaşana kadar beklenir.
- **Karşı instance parametresi gereksiz:** tetiklenen alt süreç zaten o instance'ın verisine erişebildiğinden `parameters`'a karşı-instance eklemeye gerek yok.
- **Kimlik/yaşam-döngüsü alanları eklendi:** `code` · `definition` · `order` · `active` · `deleted`.
- **`triggerProcessStep` ile sınır (netleşti):** `triggerProcessStep` = **akış üzeri** adım — akış girince ayarına göre **alt süreç veya aksiyon** tetikler; **ServiceTrigger** = **akış dışı otomatik** — olay (associate) / cron ile kendiliğinden çalışır. Tamamlayıcı; çakışma yok.

## Açık noktalar (→ `../../todo.md`)
- **`timer` saat dilimi/DST (ince nokta):** cron'un hangi **saat dilimi**nde değerlendirileceği (Organization timezone alanı henüz açık) + DST geçişleri netleştirilecek. _(Kapsam çözüldü: timer servis-global, her tetikte yeni ana süreç.)_
- **Döngü koruması:** tetiklenen alt süreç yeni ilişki kurup **aynı trigger'ı** yeniden ateşlerse (A→B→A) sonsuz döngü riski — recursion/derinlik koruması.

*Oluşturma: 2026-07-29.*
