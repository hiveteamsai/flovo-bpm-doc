# İş Kuralları (Work Rules) Teknik Dokümantasyonu

## 1. Genel Bakış

İş kuralları (WorkRule), form (servis) üzerinde **koşul → aksiyon** mantığıyla çalışan dinamik davranış motorudur. Form açıldığında ve/veya bir alan değiştiğinde koşullar değerlendirilir; sonuca göre alan görünürlüğü değiştirme, değer atama, validasyon uygulama, veri kaynağı doldurma, mesaj gösterme ve stil değişikliği gibi aksiyonlar çalıştırılır.

Bir iş kuralı özünde şu soruyu cevaplar:

> "**Ne zaman** (runtime tipi + tetikleyici), **hangi şartlarda** (koşul ağacı), **ne yapılsın** (aksiyon tipi + aksiyon konfigürasyonu)?"

Sistem üç ana katmandan oluşur:

| Katman | Konum | Sorumluluk |
|--------|-------|------------|
| **Modeller (DTO)** | `lib/Models/Settings/FlvSettings/WorkRule/` | Kural tanımı, koşullar, aksiyon konfigürasyonları, enum'lar |
| **Çalışma Zamanı Motoru** | `lib/Services/WorkRuleService.dart` | Koşul değerlendirme, aksiyon çalıştırma, expression engine |
| **Yönetim Arayüzü** | `lib/Pages/Settings/FlvSettings/WorkRule/` | Kural oluşturma/düzenleme ekranları (admin) |

Kurallar backend'de saklanır, mobil uygulamaya **servis detay yanıtının içinde gömülü** olarak gelir ve tamamen istemci tarafında (mobil motorda) çalıştırılır. Bazı değer kaynakları (lazy veri seti, function çağrısı, entegrasyon sorgusu, kur bilgisi vb.) çalışma anında backend'e ek istek atar.

---

## 2. Mimari ve Dosya Yapısı

```
lib/
├── Services/
│   └── WorkRuleService.dart                  # Çalışma zamanı motoru:
│                                             #   init()               → organizasyon verisi ön yükleme
│                                             #   executeWorkRules()   → kural seçme + koşul + aksiyon çalıştırma
│                                             #   calculateExpression()→ hesaplama (expression) motoru
│                                             #   _compare()           → karşılaştırma motoru
│                                             #   _run...()            → aksiyon işleyicileri
│
├── Models/Settings/FlvSettings/WorkRule/
│   ├── WorkRule.dart                         # GetListWorkRulesDto, WorkRuleDto, WorkRuleConditionDto,
│   │                                         #   WorkRuleConditionCompareValueDto, ValueTypeOfList
│   ├── ActionTypeSetViewForFieldsWorkRuleDto.dart      # + FieldDto + WorkRuleFieldApperanceDto
│   ├── ActionTypeApplyValidationWorkRuleDto.dart
│   ├── ActionTypeAssignValueToFieldWorkRuleDto.dart    # + AssignValueToFieldDto, AssignValueFromDataSetDto,
│   │                                                   #   AssignValueFromDataSetParameterDto,
│   │                                                   #   AssignValueFromFunctionDto, FunctionParameterItem,
│   │                                                   #   FunctionMetod, GetDatasetSourceSortType
│   ├── ActionTypeAssignValueToPropertyFieldWorkRuleDto.dart
│   ├── ActionTypeShowMessageWorkRuleDto.dart
│   ├── ActionTypeSetStyleWorkRuleDto.dart
│   ├── DataSetDto.dart                       # Veri seti tanımı (ayar ekranı için)
│   ├── GetDatasetSourceInputDto.dart         # Basit veri seti sorgu girdisi
│   ├── GetWorkRuleDataSetDto.dart            # Lazy dataset istek/yanıt modelleri
│   ├── Enums/
│   │   ├── ActionType.dart
│   │   ├── CriteritionType.dart
│   │   ├── KosulTuru.dart
│   │   ├── PropertyType.dart
│   │   ├── ValueAssignType.dart
│   │   ├── WorkRuleConditionReferenceValue.dart      # WorkRuleConditionCompareType
│   │   └── WorkRuleRuntimeType.dart
│   └── FillDataSource/
│       ├── ActionTypeFillDataSourceWorkRuleDto.dart  # + SourceType, FillDataSoruceOrganizationParameter,
│       │                                             #   OrganizationParameter, SubTextType
│       ├── PropertyDataSourceFromOrganizationDataDto.dart  # + OrganizationDataSourceType
│       └── PropertyDataSourceFromUserDataDto.dart          # + UserDataSourceType
│
└── Pages/Settings/FlvSettings/WorkRule/      # Yönetim arayüzü
    ├── WorkRuleSettingsPage.dart             # Kural listesi, ekleme, silme, filtreleme
    ├── WorkRuleDetailPage.dart               # Kural detay editörü
    ├── WorkRuleConditionDetailPage.dart      # Koşul editörü
    ├── ConditionCompareValueDetailPage.dart  # Koşul tarafı (sol/sağ değer) editörü
    ├── ConditionView.dart                    # Koşul listesi widget'ı
    └── ActionTypeViews/                      # Aksiyon tipine özel konfigürasyon ekranları
        ├── SetViewForFieldsView.dart / SetViewForFieldsDetailPage.dart
        ├── ApplyValidayionView.dart
        ├── ShowMessageView.dart
        ├── SetStyleView.dart
        ├── AssignValueToPropertyFieldView.dart
        ├── AssignValueToField/
        │   ├── AssignValueToFieldView.dart
        │   ├── AssignToValueDetailPage.dart
        │   ├── FromCalculateView.dart
        │   ├── FromFunctionView.dart
        │   ├── FromDataSetView.dart
        │   └── FromDataSetParameterDetailPage.dart
        └── FillDataSource/
            ├── FillDataSourceView.dart
            ├── FillDataSourceDetailPage.dart
            ├── FillDataSourceParametersView.dart
            └── FillDataSourceParameterDetailPage.dart
```

Motorun etkileşimde olduğu diğer bileşenler:

| Bileşen | Rolü |
|---------|------|
| `Service` (`lib/Models/Utilities/Service.dart`) | Formun tamamı; `workRules`, `validationDtos`, `activeWorkruleCount`, `hasWorkRuleNetworkUserError` alanlarını taşır |
| `ItemProperty` (`lib/Models/Utilities/ItemProperty.dart`) | Tek bir form alanı; `setNewValue`, `setDataSource`, `setNewAppearance`, `setProperty`, `clearValue`, `getControlBaseValue` mutasyon/okuma metodları |
| `ChangeListProvider` (`lib/Pages/ServiceDetail/Providers/`) | Alan değişikliklerini toplayan provider; her değişiklikte kural motorunu tetikler |
| `ServiceDetailPage` | Form ekranı; açılışta `init` + ilk kural turunu başlatır |
| `ServiceControlDataGrid` | DataGrid kontrolü; satır bazlı kural çalıştırma için kendi tetikleyicisine sahiptir |
| `ServiceControlComboBox` | Lazy arama (`lazySearchDto`) isteklerini çalıştıran kontrol |
| `OrganizationDataService` | Kurum verisi depoları (şirket, departman, masraf merkezi, kredi kartı, tatil günleri…) |
| `NetworkPage.data` | Ağ (network) kullanıcı listesi; kullanıcı fonksiyonlarının veri kaynağı |
| `RemoteApiService` | Tüm HTTP çağrıları |
| `expressions` paketi | `FromCalculation` ifadelerinin parse/eval altyapısı |

---

## 3. Yaşam Döngüsü

```
┌──────────────────── TANIM (Admin) ────────────────────┐
│ WorkRuleSettingsPage → GetWorkRules                   │
│ Kural düzenleme      → AddOrUpdateWorkRule            │
│ Kural silme          → DeleteWorkRule/{id}            │
└───────────────────────────────────────────────────────┘
                          │  (backend'de saklanır)
                          ▼
┌──────────────────── TAŞIMA ───────────────────────────┐
│ Servis detay yanıtı (services/... , instances/...)    │
│ Service.fromJson → json["workRules"]                  │
│   = GetListWorkRulesDto                               │
│     (kurallar + gömülü veri seti satırları)           │
└───────────────────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────── ÇALIŞTIRMA (Mobil) ───────────────┐
│ 1. WorkRuleService.init()                             │
│      → gerekli organizasyon verilerini paralel yükle  │
│ 2. executeWorkRules(changedItem: null)                │
│      → ilk açılış turu (always + firstOpening)        │
│ 3. Kullanıcı bir alanı değiştirir                     │
│      → ChangeListProvider.addOrUpdate                 │
│      → executeWorkRules(changedItem: alan)            │
│      → kural bir alana değer atarsa aynı akış         │
│        yeniden tetiklenir (zincirleme)                │
└───────────────────────────────────────────────────────┘
```

Kurallar mobil tarafta ayrı bir istekle çekilmez; formun kendisiyle birlikte gelir. Bu sayede form açılır açılmaz kurallar (ek tur beklemeden) çalıştırılabilir.

---

## 4. Veri Modelleri

Tüm modeller `fromJson` / `toJson` ile serileşir. Enum'lar backend ile **index (int)** üzerinden taşınır.

### 4.1. GetListWorkRulesDto

Backend'in kural paketini taşıyan zarf. İki bağlamda kullanılır: çalışma zamanında servis yanıtının `workRules` alanı olarak, ayar ekranında `GetWorkRules` yanıtı olarak.

| Alan | Tip | Açıklama |
|------|-----|----------|
| `workRuleDtos` | `List<WorkRuleDto>` | Kuralların kendisi |
| `propertyDtos` | `List<PropertyDto>` | Servisin form alanları (ayar ekranındaki alan seçim listeleri için) |
| `dataGridPropertyDtos` | `List<PropertyDto>` | DataGrid alt alanları (childField seçimi için) |
| `modalListPropertyDtos` | `List<PropertyDto>` | ModalList alt alanları |
| `processViewProfileDtos` | `List<ProcessViewProfileDto>` | Görüntüleme profilleri |
| `dataSetDtos` | `List<DataSetDto>` | Tanımlı veri setleri |
| `accountCompanyDtos` | `List<AccountCompanyDto>` | Şirket listesi (FillDataSource şirket filtresi için) |
| `project` | `String` | Proje kodu |

**`getRequiredDataStorageTypes()`** — kuralların ihtiyaç duyduğu organizasyon verisi depolarını tespit eder. İki kaynaktan tarama yapar:

1. `FillDataSource` kurallarının kaynak tipleri (`organizationDataSourceType` / `userDataSourceType` → depo tipine eşlenir),
2. Kuraldaki **tüm hesaplama ifadeleri** (aksiyon değerleri, validasyon/mesaj metinleri ve koşul tarafları dahil, koşul grupları rekürsif taranır): ifade metni içinde belirli fonksiyon adları geçiyorsa (örneğin `getCreditCardNumber` → kredi kartı deposu, `isHoliday` → tatil günleri deposu) ilgili depo listeye eklenir.

Sonuç, formun açılışında `WorkRuleService.init` tarafından ön yükleme listesi olarak kullanılır.

### 4.2. WorkRuleDto

Bir iş kuralının tamamı.

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | `int` | Kural ID (backend üretir) |
| `accountId` | `String` | Hesap (tenant) ID |
| `serviceId` | `int` | Bağlı olduğu servis |
| `code` | `String` | Kural kodu; lazy veri seti isteklerinde `workruleCode` olarak gönderilir, loglarda görünür |
| `definition` | `String` | Kural tanımı/açıklaması (hata loglarında da kullanılır) |
| `icon` | `String` | Ayar ekranı ikonu |
| `environmentRestriction` | `String` | Ortam kısıtı — mobil motor bu alanı **uygulamaz**, yalnızca taşır (bölüm 15) |
| `actionType` | `ActionType` | Aksiyon tipi |
| `workRuleRuntimeType` | `WorkRuleRuntimeType` | Ne zaman değerlendirileceği; `null`/bilinmeyen değer `always` kabul edilir |
| `workRuleConditionType` | `KosulTuru` | Kök koşul grubunun VE/VEYA bağlacı |
| `workRuleConditions` | `List<WorkRuleConditionDto>` | Koşul ağacı |
| `activeViewProfiles` | `List<int>` | Doluysa kural yalnızca bu görüntüleme profili ID'lerinde çalışır |
| `dataSetItems` | `List<ServiceItem>` | Lazy olmayan `FromDataSet` kuralları için backend'in kurala gömdüğü veri seti satırları; her satır form alanları gibi `properties` listesi taşır |
| `value` | `String` | Aksiyon konfigürasyonunun **JSON-string** hali (4.2.1) |
| `applyValidationWorkRuleDto` | `ActionTypeApplyValidationWorkRuleDto` | `value`'dan çözülür — yalnızca `actionType == ApplyValidation` iken dolu |
| `setViewForFieldsWorkRuleDto` | `ActionTypeSetViewForFieldsWorkRuleDto` | `actionType == SetViewForFiels` iken dolu |
| `assignValueToFieldWorkRuleDto` | `ActionTypeAssignValueToFieldWorkRuleDto` | `actionType == AssignValueToField` iken dolu |
| `fillDataSourceWorkRuleDto` | `ActionTypeFillDataSourceWorkRuleDto` | `actionType == FillDataSource` iken dolu |
| `assignValueToPropertyFieldWorkRuleDto` | `ActionTypeAssignValueToPropertyFieldWorkRuleDto` | `actionType == AssignValueToPropertyField` iken dolu |
| `showMessageWorkRuleDto` | `ActionTypeShowMessageWorkRuleDto` | `actionType == ShowMessage` iken dolu |
| `setStyleWorkRuleDto` | `ActionTypeSetStyleWorkRuleDto` | `actionType == SetStyle` iken dolu |
| `shouldNotWorkInReadonlyMode` | `bool` | "Salt-okunur modda çalışmasın" bayrağı — motorda **kontrol edilmez** (bölüm 15) |

#### 4.2.1. `value` alanının polimorfik serileştirmesi

Aksiyon konfigürasyonu backend'de tek bir string kolonda tutulur; yani **JSON içinde JSON** taşınır.

Deserileştirme (`WorkRuleDto.fromJson`):

1. `actionType` index'ten çözülür.
2. `value` boş değilse **ve** `"null"` string'i değilse `jsonDecode(value)` yapılır.
3. `actionType`'a karşılık gelen aksiyon DTO'sunun `fromJson`'ı çağrılır ve **yalnızca o alan** doldurulur; diğer altı aksiyon alanı `null` kalır.

Serileştirme (`toJson`): aktif aksiyon DTO'su `jsonEncode` ile string'e çevrilip `value` olarak yazılır; tipli alanlar JSON'a **yazılmaz**.

Aynı desen `ActionTypeFillDataSourceWorkRuleDto` içinde tekrarlanır: onun da kendi `value` string alanı vardır ve `sourceType`'a göre dört farklı konfigürasyon DTO'sundan birine çözülür.

Örnek — "Onay tipi 'Avans' ise TUTAR alanına 0 ata" kuralının taşınma biçimi:

```json
{
  "id": 421,
  "accountId": "DEMO",
  "serviceId": 12,
  "code": "avansTutarSifirla",
  "definition": "Avans seçilince tutarı sıfırla",
  "actionType": 4,
  "workRuleRuntimeType": 0,
  "workRuleConditionType": 0,
  "workRuleConditions": [
    {
      "referenceValue":  { "compareType": 0, "propertyDto": { "propertyId": 55, "code": "ONAY_TIPI" } },
      "valueToCompare":  { "compareType": 2, "fixedValue": "Avans" },
      "criteritionType": 0
    }
  ],
  "value": "{\"field\":{\"propertyId\":73,\"code\":\"TUTAR\"},\"assignValueToFieldDto\":{\"valueAssignType\":0,\"fixedValue\":\"0\"},\"clearIfConditionNotTrue\":true}"
}
```

#### 4.2.2. `hasProperty(String propName)`

Kuralın — koşullarında **veya** aksiyon konfigürasyonunda — verilen alan kodunu kullanıp kullanmadığını döner. Ayar ekranındaki "alana göre filtrele" özelliği bunu kullanır. Kontrol edilen yerler:

* Koşul ağacındaki tüm `FormValue` tarafları (rekürsif),
* Aksiyonun hedef alanı (`field` / `property` / `modalProperty`),
* Değer kaynağındaki alanlar: `FieldValue` kaynak alanı, `FromDataSet` parametrelerindeki form alanları,
* `FromCalculation` ifadeleri: ifade `#` ile bölünüp her token'ın ilk kelimesindeki property kodu (`KOD__display` son eki ayıklanarak) karşılaştırılır.

### 4.3. WorkRuleConditionDto — Koşul Ağacı

Koşul ağacının düğümü. İki modda çalışır:

* **Yaprak koşul** (`isConditionList != true`): `referenceValue ⟨criteritionType⟩ valueToCompare` karşılaştırması.
* **Grup** (`isConditionList == true`): `workRuleConditions` alt listesi, `workRuleConditionType` bağlacıyla değerlendirilir. Sınırsız derinlikte iç içe geçebilir; böylece `(A VE B) VEYA (C VE D)` gibi karmaşık mantıklar kurulur.

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | `int` | Koşul ID |
| `workRuleId` | `int` | Bağlı olduğu kural |
| `referenceValue` | `WorkRuleConditionCompareValueDto` | Sol taraf (karşılaştırılan değer) |
| `valueToCompare` | `WorkRuleConditionCompareValueDto` | Sağ taraf (karşılaştırma değeri) |
| `criteritionType` | `CriteritionType` | Operatör |
| `isConditionList` | `bool` | `true` ise bu düğüm bir gruptur |
| `workRuleConditionType` | `KosulTuru` | Grubun VE/VEYA bağlacı |
| `workRuleConditions` | `List<WorkRuleConditionDto>` | Alt koşullar (grup modunda) |

Örnek — `(TUTAR > 1000 VE PARA_BIRIMI == "TRY") VEYA ACIL == "1"` ağacı:

```
kök (workRuleConditionType: IfAtLeastOneConditionProvided)
├── grup (isConditionList: true, workRuleConditionType: IfAllConditionAreProvided)
│   ├── TUTAR        DahaBuyuk  1000
│   └── PARA_BIRIMI  Esittir    "TRY"
└── ACIL             Esittir    "1"
```

### 4.4. WorkRuleConditionCompareValueDto

Bir koşulun sol veya sağ tarafındaki değerin **nereden** geleceğini tanımlar.

| Alan | Tip | Açıklama |
|------|-----|----------|
| `compareType` | `WorkRuleConditionCompareType` | Değer kaynağı |
| `propertyDto` | `PropertyDto` | `FormValue` ise okunacak form alanı |
| `fixedValue` | `String` | `FixedValue` ise sabit değer |
| `assignValueToFieldDto` | `AssignValueToFieldDto` | `FromCalculate` ise expression tanımı |
| `valueTypeOfList` | `ValueTypeOfList` | Liste tipli kontrollerde hangi değerin okunacağı |

Çalışma zamanında bu DTO şu şekilde bir değere çözülür:

| `compareType` | Çözülen değer |
|---------------|---------------|
| `FormValue` (0) | Alanın kontrol değeri (`getControlBaseValue`); `valueTypeOfList` verilmişse listeden o alan okunur. **Özel durum:** alan ModalList / RadioButtonList / FileControl ise değer yerine alanın kendisi (`ItemProperty`) döner — karşılaştırma motoru bu kontrolleri özel işler (bölüm 7.2). |
| `ViewProfile` (1) | Aktif görüntüleme profilinin `code` değeri |
| `FixedValue` (2) | `fixedValue` string'i (null ise `""`) |
| `FromCalculate` (3) | Expression sonucu; uygulama dili EN ise ve `fromCalculationValueEn` doluysa EN ifade, aksi halde TR ifade değerlendirilir |

#### ValueTypeOfList

Liste üreten kontrollerden hangi alanın okunacağını seçer (şu an `GroupByTaxReceiptController` için anlamlıdır; bu kontrol için seçilebilir değerler: `defaultValue`, `expenseTypeId`, `expenseTypeName`, `categoryCode`):

| Index | Değer | Açıklama |
|-------|-------|----------|
| 0 | `defaultValue` | Varsayılan değer |
| 1 | `value` | value alanı |
| 2 | `display` | Görünen metin |
| 3 | `expenseTypeId` | Masraf tipi ID |
| 4 | `expenseTypeName` | Masraf tipi adı |
| 5 | `categoryCode` | Kategori kodu |

### 4.5. AssignValueToFieldDto — Merkezi Değer Çözümleme

**Sistemin en çok yeniden kullanılan DTO'su.** "Buraya bir değer gelecek" olan her yerde kullanılır:

* `AssignValueToField` aksiyonunun atanacak değeri,
* `ApplyValidation` mesajı, `ShowMessage` başlık ve gövdesi,
* `AssignValueToPropertyField` özellik değeri,
* Koşul taraflarının `FromCalculate` tanımı,
* Veri seti parametrelerinin karşılaştırma değeri,
* Function çağrısının her bir parametresi,
* FillDataSource organizasyon filtrelerinin karşılaştırma değeri.

| Alan | Tip | Açıklama |
|------|-----|----------|
| `valueAssignType` | `ValueAssignType` | Değerin kaynağı |
| `assignValueFromPropertyDto` | `PropertyDto` | `FieldValue`: değeri okunacak form alanı |
| `fixedValue` / `fixedValueEn` | `String` | `FixedValue`: sabit değer (TR / EN) |
| `fromCalculationValue` / `fromCalculationValueEn` | `String` | `FromCalculation`: expression metni (TR / EN) |
| `assignValueFromDataSetDto` | `AssignValueFromDataSetDto` | `FromDataSet`: veri seti sorgusu |
| `propertyIntegratedAreaDto` | `PropertyIntegratedAreaDto` | `FromEba`: entegrasyon sorgusu (connection + query) |
| `assignValueFromFunctionDto` | `AssignValueFromFunctionDto` | `Function`: HTTP çağrısı tanımı |
| `useChildFieldForAssign` | `bool` | DataGrid satır bazlı çalıştırma işareti (bölüm 6.4) |
| `useDisplay` | `bool` | `FieldValue`'da value yerine display (görünen) metni oku |

**Dil davranışı:** uygulama dili EN ise ve `...En` alanı doluysa EN varyant, aksi tüm durumlarda TR varyant kullanılır. Bu kural sabit değerler ve expression'lar için aynıdır.

### 4.6. AssignValueFromDataSetDto — Veri Seti Sorgusu

Veri setinden tek değer (AssignValueToField) veya değer listesi (FillDataSource) çekme tanımı.

| Alan | Tip | Açıklama |
|------|-----|----------|
| `dataSetName` | `String` | Veri seti adı |
| `parameters` | `List<AssignValueFromDataSetParameterDto>` | Satır filtreleme parametreleri |
| `dataSetProperty` | `PropertyDto` | **Değer** olarak alınacak kolon |
| `definitionProperty` | `PropertyDto` | **Görünen metin** olarak alınacak kolon (liste doldururken) |
| `recordProcessStatusCodes` | `List<String>` | Yalnızca bu süreç durum kodlarındaki kayıtlar |
| `lazyLoading` | `bool` | `true`: veri, çalışma anında backend'den `GetDatasetSourceNew` ile çekilir. `false`: kural içindeki gömülü `dataSetItems` satırları kullanılır |
| `cacheDeactive` | `bool` | `true` ise lazy isteğin istemci cache'i kapatılır |
| `searchActive` | `bool` | `true` + `lazyLoading`: liste çekilmez, arama sunucu tarafında yapılır (bölüm 9.4.1) |
| `sortProperty` | `PropertyDto` | Sıralama kolonu |
| `sortType` | `GetDatasetSourceSortType` | `none` / `az` / `za` |

`hasSort` getter'ı: `sortType` var, `none` değil ve `sortProperty.propertyId` dolu ise `true`.

#### AssignValueFromDataSetParameterDto

| Alan | Tip | Açıklama |
|------|-----|----------|
| `parameter` | `PropertyDto` | Veri setindeki filtre kolonu |
| `assignValueToFieldDto` | `AssignValueToFieldDto` | Karşılaştırılacak değer (formdan veya sabit) |
| `criteritionType` | `CriteritionType` | Operatör; `null` ise doğrudan `==` uygulanır |
| `changeToCompare` | `bool` | `true` ise operatörün sol/sağ tarafları yer değiştirir (ör. "form değeri, satır değerini **içersin**" yerine "satır değeri, form değerini içersin") |

### 4.7. AssignValueFromFunctionDto — Harici HTTP Çağrısı

`ValueAssignType.Function` için istek tanımı.

| Alan | Tip | Açıklama |
|------|-----|----------|
| `metod` | `FunctionMetod` | `Post`(0) / `Get`(1) / `Put`(2) / `Delete`(3). Motor `Put` için istek **atmaz** (bölüm 15) |
| `url` | `String` | İstek URL'i; `{paramAdi}` şablonları desteklenir |
| `responseParameter` | `String` | Yanıt JSON'ından okunacak alan adı; boşsa yanıtın kendisi kullanılır |
| `templateParameters` | `List<FunctionParameterItem>` | URL şablon parametreleri (`{name}` → değer) |
| `queryParameters` | `List<FunctionParameterItem>` | Query string parametreleri |
| `headerParameters` | `List<FunctionParameterItem>` | HTTP header parametreleri |
| `bodyParameters` | `List<FunctionParameterItem>` | Body parametreleri (yalnızca `Post`'ta gönderilir; `Delete`'te body hazırlanmaz) |

`FunctionParameterItem`: `name` (parametre adı) + `value` (`AssignValueToFieldDto` — değer formdan, sabitten, hesaplamadan, veri setinden veya Eba'dan gelebilir). Çalışma zamanında çözülen değer geçici `parameterValue` alanına yazılır (serileşmez).

Çalıştırma adımları için bölüm 9.6.

### 4.8. Aksiyon Konfigürasyon DTO'ları

#### 4.8.1. ActionTypeSetViewForFieldsWorkRuleDto (Görünüm Ayarla)

Tek alanı vardır: `actionTypeSetViewForFieldsWorkRuleFieldDtos: List<ActionTypeSetViewForFieldsWorkRuleFieldDto>` — tek kuralla **birden çok** alanın görünümü yönetilebilir.

`ActionTypeSetViewForFieldsWorkRuleFieldDto`:

| Alan | Tip | Açıklama |
|------|-----|----------|
| `propertyDto` | `PropertyDto` | Hedef alan |
| `childField` | `PropertyDto` | DataGrid alt alanı (hedef bir grid ise) |
| `allConditionAreProvidedApperanceDto` | `WorkRuleFieldApperanceDto` | Koşul **sağlanınca** uygulanacak görünüm |
| `allConditionAreNotProvidedApperanceDto` | `WorkRuleFieldApperanceDto` | Koşul **sağlanmayınca** uygulanacak görünüm |
| `allConditionAreNotProvidedDeactive` | `bool` | `true` ise koşul sağlanmadığında alana hiç dokunulmaz (mevcut görünüm korunur) |

`WorkRuleFieldApperanceDto`: `isEnabled`, `isRequired`, `isVisible` — üçü de `bool`; verilmeyen değer `false` kabul edilir.

#### 4.8.2. ActionTypeApplyValidationWorkRuleDto (Validasyon)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `assignValueToFieldDto` | `AssignValueToFieldDto` | Validasyon mesajı — yalnızca `FixedValue` veya `FromCalculation` desteklenir |
| `canPassValidation` | `bool` | `true`: uyarı (kullanıcı devam edebilir); `false`: engelleyici (kaydetme/aksiyon bloklanır) |
| `showAsPopup` | `bool` | Mesajın popup olarak gösterilmesi |
| `withModal` | `bool` | `true`: validasyon ModalList satırları üzerinde satır-bazlı çalışır |
| `modalProperty` | `PropertyDto` | `withModal` ise hedef ModalList alanı |
| `withModalCondition` | `WorkRuleConditionDto` | Her modal satırında **ayrıca** değerlendirilecek koşul |

#### 4.8.3. ActionTypeShowMessageWorkRuleDto (Mesaj Göster)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `titleAssignValueToFieldDto` | `AssignValueToFieldDto` | Dialog başlığı; boş kalırsa "Bilgilendirme" kullanılır |
| `messageAssignValueToFieldDto` | `AssignValueToFieldDto` | Dialog mesajı (`FixedValue` veya `FromCalculation`) |

#### 4.8.4. ActionTypeAssignValueToFieldWorkRuleDto (Alana Değer Ata)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `field` | `PropertyDto` | Değer atanacak alan |
| `childField` | `PropertyDto` | DataGrid alt alanı |
| `assignValueToFieldDto` | `AssignValueToFieldDto` | Atanacak değerin kaynağı |
| `clearIfConditionNotTrue` | `bool` | Koşul sağlanmazsa hedef alan temizlensin |

#### 4.8.5. ActionTypeFillDataSourceWorkRuleDto (Veri Kaynağı Doldur)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `field` / `childField` | `PropertyDto` | Veri kaynağı doldurulacak alan (genellikle ComboBox) |
| `sourceType` | `SourceType` | Kaynak tipi |
| `value` | `String` | Kaynak konfigürasyonunun JSON-string hali; `sourceType`'a göre aşağıdaki dört DTO'dan birine çözülür |
| `companyId` | `int` | `Users` kaynağında şirket filtresi |
| `assignValueFromDataSetDto` | `AssignValueFromDataSetDto` | `sourceType == FromDataSet` iken dolu |
| `propertyDataSourceFromOrganizationDataDto` | `PropertyDataSourceFromOrganizationDataDto` | `sourceType == FromOrganizationData` iken dolu |
| `propertyDataSourceFromUserDataDto` | `PropertyDataSourceFromUserDataDto` | `sourceType == FromUsersData` iken dolu |
| `propertyIntegratedAreaDto` | `PropertyIntegratedAreaDto` | `sourceType == FromEba` iken dolu |

`PropertyDataSourceFromOrganizationDataDto`:

| Alan | Tip | Açıklama |
|------|-----|----------|
| `organizationDataSourceType` | `OrganizationDataSourceType` | Kurum verisi tipi (departmanlar, şirketler…) |
| `subTextType` | `SubTextType` | Liste öğelerinin alt metni |
| `parameters` | `List<FillDataSoruceOrganizationParameter>` | Kayıt filtreleri |

`PropertyDataSourceFromUserDataDto`: aynı yapı, `userDataSourceType` (`UserDataSourceType`) ile.

`FillDataSoruceOrganizationParameter` (kurum kaydı filtresi):

| Alan | Tip | Açıklama |
|------|-----|----------|
| `parameter` | `OrganizationParameter` | Kurum kaydından okunacak alan (name, code, company, userCode…) |
| `criteritionType` | `CriteritionType` | Operatör; `null` ise `==` |
| `changeToCompare` | `bool` | Sol/sağ değiş tokuşu |
| `value` | `AssignValueToFieldDto` | Karşılaştırılacak değer (formdan / sabitten) |
| `additionalQualificationCode` | `String` | `additionalQualification` parametresinde hangi ek niteliğin okunacağı |

Tipik kullanım: "Masraf Merkezi combosunu, formda seçili **şirketin** masraf merkezleriyle doldur" → parametre: `company == #SIRKET`.

#### 4.8.6. ActionTypeAssignValueToPropertyFieldWorkRuleDto (Alan Özelliğine Değer Ata)

Alanın **değerine** değil, **özelliğine** (meta) değer atar.

| Alan | Tip | Açıklama |
|------|-----|----------|
| `field` / `childField` | `PropertyDto` | Hedef alan |
| `propertyType` | `PropertyType` | Değiştirilecek özellik |
| `assignValueToFieldDto` | `AssignValueToFieldDto` | Özelliğe atanacak değer |

Örnek: "BITIS_TARIHI alanının MinDate özelliğine #BASLANGIC_TARIHI değerini ata" — böylece bitiş tarihi başlangıçtan önce seçilemez.

#### 4.8.7. ActionTypeSetStyleWorkRuleDto (Dekorasyon Ayarla)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `property` | `PropertyDto` | Hedef alan (ModalList olabilir) |
| `modalProperty` | `PropertyDto` | ModalList içinde stillenecek alt alan; boşsa satırın kendisi stillenır |
| `withModalCondition` | `WorkRuleConditionDto` | Her modal satırında değerlendirilecek koşul |
| `style` | `ServiceItemStyle` | Uygulanacak stil |
| `clearIfConditionNotTrue` | `bool` | Koşul sağlanmazsa stil temizlensin |

### 4.9. Lazy Dataset Modelleri

#### GetWorkRuleDataSetRequestDto — `GetDatasetSourceNew` isteği

| Alan | Tip | JSON'a yazılır | Açıklama |
|------|-----|:---:|----------|
| `dataSetName` | `String` | ✔ | Veri seti adı |
| `workruleCode` | `String` | ✔ | İsteği yapan kuralın kodu (backend log/izleme) |
| `parameters` | `List<GetWorkRuleDataSetParameter>` | ✔ | Filtreler |
| `recordProcessStatusCodes` | `List<String>` | ✔ | Durum filtresi |
| `wantedPropertyIds` | `List<int>` | ✔ | İstenen kolonlar (definition + value propertyId'leri) |
| `sortPropertyId` | `int` | ✔ | Sunucu tarafı sıralama kolonu |
| `sortType` | `GetDatasetSourceSortType` | ✔ | Sıralama yönü |
| `definitionProperty` / `dataSetProperty` / `sortProperty` | `PropertyDto` | ✖ | Yanıtı istemci tarafında işlemek için taşınır |

`GetWorkRuleDataSetParameter`: `parameterPropertyId` (int), `compareValue` (String), `criteritionType`, `changeToCompare`, `isSearchValue` (bool).

İstek üretimi (`_createGetWorkRuleDataSetRequestDto`):

1. Her parametrenin karşılaştırma değeri **o anki form değerlerinden** çözülür (`FixedValue` → sabit; diğer her şey → form alanı okuma).
2. Değer `DateTime` ise ISO-8601 string'e çevrilir.
3. `searchActive == true` ise `compareValue = null` + `isSearchValue = true` gönderilir; arama metnini çalışma anında ComboBox kontrolü doldurur.
4. `wantedPropertyIds` = definition + value kolon ID'leri.
5. İstek cache'i: `cacheActive = !cacheDeactive`.

#### GetWorkRuleDataSetResponseDto — yanıt

```
GetWorkRuleDataSetResponseDto
└── items: List<GetWorkRuleDataSetResponseItemDto>          # satırlar
    └── values: List<GetWorkRuleDataSetResponseItemValueDto> # hücreler
        ├── propertyId: int
        └── value: String                                    # her hücre string taşınır
```

`getPropValue(controlType)` — string hücre değerini hedef kontrol tipine göre gerçek tipe dönüştürür:

| ControlType | Dönüşüm |
|-------------|---------|
| `ModalList`, `FileController`, `DataGridControl` | Her zaman `null` (bu tiplere lazy dataset'ten değer atanmaz) |
| `ComboBox` | Değer JSON **liste** ise: `ComboBoxItem` listesine parse edilir, `isSelected == true` olanların `value`'ları virgülle birleştirilir. Liste değilse ham string |
| `DatePicker` | `DateTime.parse`; yıl `1` ise `null` (boş tarih kuralı) |
| `NumericTextbox` | TR sayı formatı normalize edilip `double` (başarısızsa `0`) |
| `CheckBox` | `"1"` → `"1"`, diğer her şey → `"0"` |
| `TimePicker` | Değer parse edilir, **bugünün tarihi** + parse edilen saat/dakika/saniye ile yeni `DateTime` üretilir |
| `GroupByTaxReceiptController` | Ham string |
| diğer | Ham string |

Boş değer (`""`) `CheckBox` hariç `null` döner.

### 4.10. DataSetDto ve GetDatasetSourceInputDto

`DataSetDto` — ayar ekranında veri seti seçimi ve kolon/durum listeleri için:

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` / `name` | `int` / `String` | Veri seti kimliği |
| `dataSetProperties` | `List<PropertyDto>` | Veri setinin kolonları |
| `dataSetServiceItems` | `List<ServiceItem>` | Örnek/gömülü satırlar |
| `processStatusDtos` | `List<ProcessStatusDto>` | Seçilebilir süreç durumları |

`GetDatasetSourceInputDto` — basit sorgu girdisi: `dataSetName`, `parameters (Map<String,String>)`, `recordProcessStatusCodes`, `wantedPropertyIds`.

---

## 5. Enum Referansı

### 5.1. ActionType — Aksiyon Tipi

| Index | Enum | UI Etiketi | Motor işleyicisi |
|-------|------|-----------|------------------|
| 0 | `SetViewForFiels` | Alanlar İçin Görünüm Ayarla | `_runSetViewRule` |
| 1 | `ChangeViewProfile` | Görüntüleme Profili Değiştir | **yok** — mobilde implement edilmemiş, sessizce atlanır |
| 2 | `ApplyValidation` | Validasyon Uygula | `_runApplyValidation` |
| 3 | `ShowMessage` | Mesaj Göster | `_showMessage` |
| 4 | `AssignValueToField` | Alana Değer Atama | `_runAssignValueToField` |
| 5 | `FillDataSource` | Veri Kaynağı Doldurma | `_runFillData` |
| 6 | `AssignValueToPropertyField` | Alana Özellik Atama | `_runAssignValueToPropertyField` |
| 7 | `SetStyle` | Dekorasyon Ayarla | `_runSetStyle` |

### 5.2. WorkRuleRuntimeType — Çalışma Zamanı Tipi

| Index | Enum | İlk açılışta çalışır | Değişimde çalışır |
|-------|------|:---:|:---:|
| 0 | `always` | ✔ | ✔ (koşulları değişen alanı içeriyorsa) |
| 1 | `firstOpening` | ✔ | ✖ |
| 2 | `whenChanging` | ✖ | ✔ (koşulları değişen alanı içeriyorsa) |

`null` veya bilinmeyen index → `always` kabul edilir.

### 5.3. KosulTuru — Koşul Bağlacı

| Index | Enum | Açıklama | Değerlendirme |
|-------|------|----------|---------------|
| 0 | `IfAllConditionAreProvided` | Tüm koşullar sağlanıyorsa (VE) | `conditions.every(...)` |
| 1 | `IfAtLeastOneConditionProvided` | En az biri sağlanıyorsa (VEYA) | `conditions.any(...)` |

Koşul listesi `null` ise sonuç **`true`** kabul edilir (koşulsuz kural her turda "sağlandı" sayılır).

### 5.4. CriteritionType — Karşılaştırma Operatörleri

Operatörün davranışı **sol değerin çalışma zamanı tipine** göre değişir (tip tespiti için bölüm 7.2):

| Index | Enum | String | Num | Date |
|-------|------|:-----:|:---:|:----:|
| 0 | `Esittir` | `==` | `==` | `compareTo == 0` |
| 1 | `EsitDegildir` | `!=` | `!=` | `compareTo != 0` |
| 2 | `Bos` | `isEmpty` veya `"[]"` | parse sonucu `null` | `year == 1` |
| 3 | `BosDegil` | `isNotEmpty` | parse sonucu var | `year != 1` |
| 4 | `DahaBuyuk` | — (daima `false`) | `>` | `>` |
| 5 | `DahaBuyukVeyaEsit` | — | `>=` | `>=` |
| 6 | `DahaKucuk` | — | `<` | `<` |
| 7 | `DahaKucukVeyaEsit` | — | `<=` | `<=` |
| 8 | `IleBaslar` | `startsWith` | — | — |
| 9 | `IleBiter` | `endWith` | — | — |
| 10 | `Icerir` | `contains` | — | — |
| 11 | `Icermez` | `!contains` | — | — |
| 12 | `Any` | sağ değer virgülle bölünür; parçalardan **herhangi biri** sol değerde geçiyorsa `true` | — | — |
| 13 | `Every` | sağ değer virgülle bölünür; parçaların **hepsi** sol değerde geçiyorsa `true` | — | — |

### 5.5. WorkRuleConditionCompareType — Koşul Değer Kaynağı

| Index | Enum | Açıklama |
|-------|------|----------|
| 0 | `FormValue` | Form alanı değeri |
| 1 | `ViewProfile` | Aktif görüntüleme profili kodu |
| 2 | `FixedValue` | Sabit değer |
| 3 | `FromCalculate` | Expression sonucu |

### 5.6. ValueAssignType — Değer Atama Kaynağı

| Index | Enum | UI Etiketi | Açıklama |
|-------|------|-----------|----------|
| 0 | `FixedValue` | Sabit Değer | TR/EN sabit string |
| 1 | `FieldValue` | Form Alanı | Başka alanın değeri (`useDisplay` destekli) |
| 2 | `FromCalculation` | Hesaplayarak | Expression engine (bölüm 10) |
| 3 | `FromDataSet` | Veri Setinden | Veri seti sorgusu (lazy veya gömülü) |
| 4 | `FromEba` | Eba'dan | Entegrasyon sorgusu |
| 5 | `Search` | Search | Sunucu tarafı arama bağlamı |
| 6 | `Function` | Function | Harici HTTP çağrısı |

### 5.7. SourceType — FillDataSource Kaynak Tipi

| Index | Enum | UI Etiketi |
|-------|------|-----------|
| 0 | `FromDataSet` | Veri Setinden |
| 1 | `FromOrganizationData` | Kurum Verisinden |
| 2 | `FromEba` | Eba'dan |
| 3 | `FromUsersData` | Kullanıcı Verisinden |

### 5.8. OrganizationDataSourceType — Kurum Verisi Kaynakları

| Index | Enum | Açıklama | Seçilebilir filtre parametreleri |
|-------|------|----------|----------------------------------|
| 0 | `Professions` | Unvanlar | name, code, company |
| 1 | `Departments` | Departmanlar | name, code, company |
| 2 | `Companies` | Şirketler | name, code |
| 3 | `CostCenters` | Masraf merkezleri | name, code, company |
| 4 | `Users` | Kullanıcılar (ağ kullanıcı listesinden) | name, code, company, userCode, additionalQualification, professionCode |
| 5 | `CreditCards` | Kredi kartları | name, code, company, userCode |
| 6 | `Tiers` | Kademeler | name, code |
| 7 | `FromUserGroupData` | Kullanıcı grupları | name, code, company |
| 8 | `Positions` | Pozisyonlar | name, code, company |
| 9 | `WorkingSchedule` | Çalışma takvimleri | name, code |
| 10 | `ExpenseType` | Masraf tipleri (depodan değil, çalışma anında API'den çekilir) | — |
| 11 | `ExpenseCategory` | Masraf kategorileri | name, code |

### 5.9. UserDataSourceType — Kullanıcı Verisi Kaynakları

| Index | Enum | Açıklama |
|-------|------|----------|
| 0 | `CreditCards` | Oturum kullanıcısının kredi kartları (`status == true` filtreli; tek kart varsa veya `selected` işaretli kart varsa otomatik seçilir) |
| 1 | `Companies` | Kullanıcının şirketleri |
| 2 | `CostCentes` | Kullanıcının masraf merkezleri |

### 5.10. OrganizationParameter — Kurum Kaydı Alanları

| Index | Enum | Kayıttan okunan değer |
|-------|------|----------------------|
| 0 | `company` | Şirket kodu |
| 1 | `name` | Ad/tanım |
| 2 | `code` | Kod |
| 3 | `userCode` | Kullanıcı kodu |
| 4 | `additionalQualification` | Ek nitelik değeri (`additionalQualificationCode` ile hangi nitelik olduğu belirtilir) |
| 5 | `professionCode` | Unvan kodu |

### 5.11. SubTextType — Liste Öğesi Alt Metni

| Index | Enum |
|-------|------|
| 0 | `code` |
| 1 | `username` |
| 2 | `departmant` |
| 3 | `profession` |
| 4 | `ref1` |
| 5 | `ref2` |

### 5.12. PropertyType — Özellik Atama Hedefleri

| Index | Enum | Geçerli kontrol tipi |
|-------|------|----------------------|
| 0 | `MinDate` | DatePicker |
| 1 | `MaxDate` | DatePicker |
| 2 | `HelperText` | Tüm kontroller |
| 3 | `SideText` | Entry, NumericTextbox |
| 4 | `AddNewEnable` | ModalList |
| 5 | `IsActiveKkegAttachment` | GroupByTaxReceiptController |

### 5.13. Diğer Enum'lar

| Enum | Değerler | Açıklama |
|------|----------|----------|
| `FunctionMetod` | `Post`(0), `Get`(1), `Put`(2), `Delete`(3) | HTTP metodu |
| `GetDatasetSourceSortType` | `none`(0), `az`(1), `za`(2) | Sıralama yönü |
| `CompareType` (motor içi, serileşmez) | `string`, `num`, `date` | Karşılaştırma tip kategorisi |

---

## 6. Tetiklenme (Triggering)

### 6.1. Form Açılışı

`ServiceDetailPage` servis yanıtını işledikten sonra ~200 ms gecikmeyle şu akışı çalıştırır:

```dart
await WorkRuleService.init(context: context, service: service);
workRuleExecute(null, (item) => changeListProvider.addOrUpdate(item, isManuelChangeFromUser: false));
```

* `init` — organizasyon verilerini ön yükler (bölüm 11).
* `executeWorkRules(changedItem: null)` — ilk açılış turu. `changedItem == null` olduğu için `workRuleRuntimeType != whenChanging` olan **tüm** kurallar (yani `always` + `firstOpening`) değerlendirilir; koşul-alan eşleşme filtresi uygulanmaz.
* Aynı akış, kısmi yenileme (formun sunucudan yeniden çekilmesi) sonrasında da tekrarlanır.
* `workRuleExecute` çağrısından 100 ms sonra ek bir `setState` planlanır (senkron aksiyonların UI'a yansıması için).

### 6.2. Alan Değişikliği

Her form kontrolü, değeri değiştiğinde `ChangeListProvider.addOrUpdate(item)` çağırır:

```dart
void addOrUpdate(ItemProperty item, {bool isManuelChangeFromUser = true}) {
  // 1. item, değişiklik listesine eklenir/güncellenir (objectTypeId ile eşleşme)
  // 2. isManuelChangeFromUser ise item üzerinde işaretlenir
  workRuleExecute(item, (ItemProperty i) => addOrUpdate(i, isManuelChangeFromUser: false));
  clearTargetParameter(item);
}
```

`workRuleExecute` → `executeWorkRules(changedItem: item)`.

**Kural seçim algoritması** (`executeWorkRules` girişinde):

```
her kural için:
  eğer changedItem != null (değişim turu):
      kural.runtimeType == firstOpening  → ELE
      _hasConditionChangeItem(changedItem, kural.workRuleConditions) == false → ELE
  eğer changedItem == null (açılış turu):
      kural.runtimeType == whenChanging  → ELE
```

`_hasConditionChangeItem` — koşul ağacını rekürsif tarar; herhangi bir yaprak koşulun **sol veya sağ tarafındaki** form alanı, değişen alanla eşleşiyorsa `true`. Eşleşme iki yoldan yapılır: `propertyDto.propertyId == changedItem.objectTypeId` veya `propertyDto.code == changedItem.propertyCode`.

> **Kritik davranış:** değişim tetiklemesi yalnızca **koşullara** bakar. Değişen alan kuralın *aksiyonunda* (örneğin `FromCalculation` ifadesinde veya dataset parametresinde) kullanılıyor ama koşullarında geçmiyorsa kural **tetiklenmez**. Bu nedenle hesaplama kuralı yazarken ifadede kullanılan alanların koşullara da eklenmesi gerekir (tipik desen: her ifade alanı için "X → Boş Değil" ya da yapay bir koşul).

### 6.3. Zincirleme (Cascade) Çalışma

Bir kuralın `addOrUpdate` callback'i `ChangeListProvider.addOrUpdate`'e geri döner (bu kez `isManuelChangeFromUser: false`). Bu da atanan alan için **yeni bir kural turu** başlatır:

```
Kullanıcı A alanını değiştirir
  → tur 1: koşulunda A geçen kurallar → kural K1, B alanına değer atar
      → tur 2: koşulunda B geçen kurallar → kural K2, C alanına değer atar
          → tur 3: koşulunda C geçen kurallar → değişiklik yok → zincir durur
```

Sonsuz döngü koruması **dolaylıdır**: `ItemProperty.setNewValue` / `setDataSource` / `setNewAppearance` / `setProperty` değer **gerçekten değiştiyse** `true` döner; değişmediyse `addOrUpdate` çağrılmaz ve zincir kendiliğinden durur. Birbirini karşılıklı besleyen ve her turda değeri gerçekten değiştiren kurallar teorik olarak döngü oluşturabilir — kural tasarımında kaçınılmalıdır.

Kural atamaları `isManuelChangeFromUser: false` ile değişiklik listesine girdiği için, kullanıcı değişiklikleriyle birlikte aynı kaydetme akışına dahil olur.

### 6.4. DataGrid Satır Bazlı Tetiklenme

DataGrid hücreleri form alanı olmadığı için ana motor onları göremez. `ServiceControlDataGrid` bu boşluğu **kopya servis** tekniğiyle kapatır; kendi `workRuleExecute` metoduna sahiptir:

1. **Kural filtresi:** yalnızca hedefi bu grid alanı olan (`assignValueToFieldWorkRuleDto.field.propertyId == grid.objectTypeId`) ve `assignValueToFieldDto.useChildFieldForAssign == true` işaretli kurallar seçilir.
2. **Kopya servis üretimi** (`createCopyService(rowIndex)`): servis JSON üzerinden derin kopyalanır; kopyanın `properties` listesi, grid header tanımlarının kopyaları + **ilgili satırın hücre kontrolleri** ile değiştirilir. Böylece satırın hücreleri, kural motoru için normal form alanları gibi görünür.
3. Kopya servis üzerinde `WorkRuleService.init` + `executeWorkRules` çalıştırılır.

Tetikleyiciler: bir satır hücresi değiştiğinde ve yeni satır eklendiğinde.

### 6.5. Kural Bazlı Ön Filtreler ve Hata Yalıtımı

`executeWorkRules` içinde her kural çalıştırılmadan önce sırayla:

1. `service.hasWorkRuleNetworkUserError == true` → **tüm** kurallar atlanır.
2. `activeViewProfiles` doluysa ve formun aktif görüntüleme profili ID'si listede yoksa → kural atlanır.
3. Koşullar değerlendirilir; koşul değerlendirmesi hata fırlatırsa `compareResult = false` kabul edilip devam edilir (konsola `_findCompareResult error <tanım>` yazılır).
4. Aksiyon çalıştırılır; kural bazında oluşan hatalar yutulur ve `<kod>!!workrule hata : <hata>` biçiminde loglanır. **Bir kuralın hatası diğer kuralları durdurmaz.**

Tur boyunca `service.activeWorkruleCount` artırılır, tur bitince azaltılır. Metod, en az bir kural formda değişiklik yaptıysa `true` döner.

---

## 7. Koşul Değerlendirme Motoru

### 7.1. Akış

```
_findCompareResult(conditions, kosulTuru):
    kosulTuru == IfAllConditionAreProvided     → conditions.every(_compareCondition)   // liste null → true
    kosulTuru == IfAtLeastOneConditionProvided → conditions.any(_compareCondition)     // liste null → true

_compareCondition(condition):
    condition.isConditionList == true:
        → _findCompareResult(condition.workRuleConditions, condition.workRuleConditionType)  // rekürsif grup
    değilse:
        value        = çöz(condition.referenceValue)      // bölüm 4.4 tablosu
        compareValue = çöz(condition.valueToCompare)
        → _compare(value, compareValue, condition.criteritionType)
```

### 7.2. `_compare` — Karşılaştırma Semantiği

Karşılaştırma kategorisi **sol değerin çalışma zamanı tipinden** belirlenir:

```
value is DateTime → date
value is num      → num
diğer             → string
```

Kategori belirlenmeden önce işlenen özel durumlar:

1. **`value == null`:** `Bos` → `true`, `BosDegil` → `false`; diğer operatörler normal akışa devam eder.
2. **Sol değer ModalList / RadioButtonList / FileControl taşıyan `ItemProperty` ise:**
   * `Bos` / `BosDegil` → kontrolün kendi `isEmpty()` metodu ile cevaplanır.
   * RadioButtonList'te diğer operatörler için **seçili radyonun adı** (`name`) değere dönüştürülüp string karşılaştırmaya sokulur.
3. **Sol değer `DataGridControl` ise:** yalnızca `Bos` (satır yok) / `BosDegil` (satır var) anlamlıdır; diğer tüm operatörler `false` döner.

Kategori bazlı kurallar:

* **string:** tablodaki string kolonuna göre. `Bos` için özel durum: değer `"[]"` (boş JSON listesi) de boş sayılır. Sayısal operatörler (`DahaBuyuk` vb.) string kategorisinde daima `false`tur.
* **num:** taraflardan biri string ise TR sayı formatı normalize edilerek parse edilir — `replaceAll(".", "")` (binlik ayraç silinir) + `replaceAll(",", ".")` (ondalık virgül noktaya çevrilir) + `double.tryParse`. `Bos` → parse sonucu `null` mü; `BosDegil` → tersi. Her iki taraf da sayıya çevrilemezse sonuç `false`.
* **date:** sağ taraf `DateTime` değilse `false`. "Boş tarih" kuralı: `year == 1` boş kabul edilir (backend'in boş tarihi `0001-01-01` göndermesi kuralı).

Tüm karşılaştırma `try/catch` içindedir; beklenmeyen tip kombinasyonları sessizce `false` üretir.

### 7.3. Örnek Değerlendirme

Bölüm 4.3'teki ağaç için — form durumu `TUTAR = "1.250,00"`, `PARA_BIRIMI = "TRY"`, `ACIL = "0"`:

```
kök (VEYA / any):
├── grup (VE / every):
│   ├── TUTAR DahaBuyuk 1000
│   │     sol: "1.250,00" → string ama sağ sabit... sol değer kontrol tipine göre num gelebilir;
│   │     num kategorisi: "1.250,00" → 1250.0 ; 1250.0 > 1000 → TRUE
│   └── PARA_BIRIMI Esittir "TRY" → string: "TRY" == "TRY" → TRUE
│   → grup TRUE
└── (kısa devre: any ilk TRUE'da durur) → kök TRUE
```

---

## 8. Aksiyon İşleyicileri (Çalışma Zamanı Davranışı)

Dağıtıcı `_runWorkRuleBussiness`, kuralın `actionType`'ına göre ilgili işleyiciyi çağırır. Tüm işleyiciler `bool hasChange` döner; `true`, UI'nin yeniden çizilmesi gereken bir form değişikliği anlamına gelir. Her işleyiciye koşul sonucu (`compareResult`) parametre olarak verilir — bazı aksiyonlar sonucu her iki dalda da kullanır, bazıları yalnızca `true` iken çalışır:

| Aksiyon | Koşul TRUE | Koşul FALSE |
|---------|-----------|-------------|
| SetViewForFiels | "sağlandı" görünümünü uygular | "sağlanmadı" görünümünü uygular (deactive bayrağı yoksa) |
| ApplyValidation | Validasyon girdisini ekler/günceller | Aynı kurala ait girdiyi **siler** |
| ShowMessage | Dialog gösterir | Hiçbir şey |
| AssignValueToField | Değeri atar | `clearIfConditionNotTrue` ise alanı temizler |
| FillDataSource | Kaynağı doldurur | Hiçbir şey |
| AssignValueToPropertyField | Özelliği atar | Hiçbir şey |
| SetStyle | Stili uygular | `clearIfConditionNotTrue` ise stili temizler |

### 8.1. SetViewForFiels — `_runSetViewRule`

Listedeki her alan tanımı için:

1. `allConditionAreNotProvidedDeactive == true` ve koşul `false` ise alana hiç dokunulmaz (o alan atlanır).
2. Hedef alan `_findTargetProperty` ile bulunur (bölüm 8.8); bulunamazsa atlanır.
3. Koşul sonucuna göre `Provided` veya `NotProvided` görünüm DTO'su seçilir ve `setNewAppearance(isEnable, isVisible, isRequired)` uygulanır.
4. **Salt-okunur mod:** form `readOnlyMode` ise `isEnable` her durumda `false`'a zorlanır (görünürlük ve zorunluluk kuraldan gelir, düzenlenebilirlik asla açılmaz).
5. Görünüm gerçekten değiştiyse alanın `globalKey`'i yenilenir → widget tamamen yeniden inşa edilir (görünürlük değişimlerinin güvenilir yansıması için).

### 8.2. ApplyValidation — `_runApplyValidation`

1. Mesaj üretilir: `FixedValue` (TR/EN seçimi) veya `FromCalculation` (expression sonucu string'e çevrilir). Mesaj boşsa işlem yapılmaz.
2. `ValidationDtoItem(validationMessages: [mesaj], canPassValidation, showAsPopup, workRuleId)` oluşturulur.
3. Girdi, `service.validationDtos` listesi üzerinde **kural ID'siyle durumsal** yönetilir (`_addOrUpdateValidation`):
   * Koşul sağlandı → girdi eklenir; aynı `workRuleId`'li eski girdi varsa değiştirilir.
   * Koşul sağlanmadı → aynı `workRuleId`'li girdi **silinir**; boşalan gruplar listeden temizlenir. Yani koşul düzelince uyarı otomatik kalkar.
4. **`withModal == true` (satır bazlı validasyon):**
   * `modalProperty` koduyla hedef ModalList bulunur (ModalList değilse çıkılır).
   * Her satır (`serviceItem`) için `withModalCondition`, satırın **kendi alanları** üzerinde tek koşulluk bir liste olarak değerlendirilir.
   * Girdi `serviceItemId` bazlı tutulur (grup başlığı `"#<satırId>"`); ana koşul **VE** satır koşulu birlikte sağlanmalıdır.
   * `withModal` olmayan kurallar `"Form"` başlıklı ortak grupta tutulur.

Validasyonların etkisi: `canPassValidation == false` içeren bir girdi varken aksiyon butonları formu göndermeyi engeller; `showAsPopup` işaretli girdiler aksiyon öncesi popup olarak da gösterilir. Expression motorundaki `isServiceValidate()` fonksiyonu da aynı listeyi kontrol eder.

### 8.3. ShowMessage — `_showMessage`

1. Koşul sağlanmadıysa hiçbir şey yapılmaz.
2. Mesaj çözülür (`FixedValue`/`FromCalculation`, TR/EN); boşsa çıkılır.
3. Başlık aynı şekilde çözülür; boşsa "Bilgilendirme" başlığı kullanılır.
4. Kaydırılabilir gövdeli bir dialog gösterilir. Dönüş her zaman `false` (form durumu değişmez).

Not: "bir kez göster" mekanizması yoktur — kural her tetiklendiğinde koşul hâlâ sağlanıyorsa dialog tekrar açılır. Pratikte kural, yalnızca koşulundaki alan değiştiğinde tetiklendiği için mesaj genellikle alan değişimi başına bir kez görünür.

### 8.4. AssignValueToField — `_runAssignValueToField`

* **Koşul sağlanmadı:** `clearIfConditionNotTrue == true` ise hedef alan `clearValue` ile temizlenir (temizlik gerçek değişiklik yaptıysa `addOrUpdate` → zincirleme). Değilse hiçbir şey yapılmaz.
* **Koşul sağlandı:** hedef alan bulunur ve `valueAssignType`'a göre değer üretilir (bölüm 9). Değer `setNewValue(value, targetChild)` ile yazılır; kontrol "değişti" derse `addOrUpdate` çağrılır → zincirleme tur.

Asenkron kaynaklar (lazy dataset, async expression, Eba, Function) için değer atama, ilgili istek tamamlandığında yapılır (bölüm 9 ve 12).

### 8.5. FillDataSource — `_runFillData`

Ön şartlar: koşul sağlanmalı **ve** `field` dolu olmalı. Hedef ComboBox ise önce `lazySearchDto` sıfırlanır (eski lazy arama konfigürasyonu temizlenir).

`sourceType`'a göre:

**FromDataSet — üç mod:**

1. `lazyLoading && searchActive`: liste hiç çekilmez. ComboBox'a hazır bir `GetWorkRuleDataSetRequestDto` (`lazySearchDto`) atanır. Kullanıcı combo açıp arama yazdıkça kontrol, bu DTO'daki `isSearchValue` parametresine arama metnini koyarak sunucudan sayfalı sonuç çeker.
2. `lazyLoading`: `GetDatasetSourceNew` çağrılır (asenkron; alan `isBusy`, sayaç `activeWorkruleCount` artar). Yanıt satırları `SetDataSourceItem(value, text)` listesine çevrilir: `definitionProperty` → metin, `dataSetProperty` → değer. Sayısal değerlerde tam sayıya eşit `num`'lar `"5"` gibi (ondalıksız) yazılır.
3. Gömülü (`lazyLoading` değil): `workRule.dataSetItems` satırları; parametre listesi doluysa `_assignValueParameterCondition` ile filtrelenir (bölüm 9.5), `hasSort` ise `_valueCompareTo` ile sıralanır. `definition` değeri `null` veya `value` boş olan satırlar atlanır.

**FromOrganizationData:**

* `ExpenseType` özel: liste `GetCustomerExpenseTypes` API'sinden asenkron çekilir; öğe metni `tanım + "(alt metin)"` biçiminde kurulur (`subTextType` verilmişse o alan, verilmemişse değer).
* `Users`: kaynak `NetworkPage.data.networkUserDtos` (ağ kullanıcıları). Veri yüklü değilse `hasWorkRuleNetworkUserError = true`. `companyId` verilmişse yalnızca o şirkete bağlı kullanıcılar.
* Diğer tipler: ilgili `OrganizationDataService` deposundan okunur; depo `error` durumundaysa hata bayrağı kalkar ve işlem yapılmaz.
* `parameters` doluysa kayıtlar `_organizationParameterCondition` ile filtrelenir: her parametrede kayıttan okunan alan (`OrganizationParameter.getValue`) ile formdan/sabitten çözülen değer, `criteritionType` (boşsa `==`, `changeToCompare` ile taraf değişimi) üzerinden karşılaştırılır; **tüm** parametreler sağlanmalıdır.
* Kodu boş kayıtlar atlanır; öğeler `value = kod`, `text = ad`, `subText = subTextType'a göre` olarak üretilir.

**FromUsersData:**

* `CreditCards`: kullanıcı kredi kartı deposu; yalnızca `status == true` kartlar. Tek kart varsa veya bir kart `selected` işaretliyse `selectedItemCode` ile birlikte atanır → combo otomatik seçili gelir.
* `Companies`: kullanıcı şirket deposu.
* Depo `error` durumundaysa hata bayrağı kalkar.

**FromEba:** liste anlık çekilmez; ComboBox'a `workRuleSourceConfig` (entegrasyon sorgu konfigürasyonu; form alanı eşlemeleri o anki değerlerle doldurulmuş halde) atanır. Kontrol, açıldığında sorguyu kendisi çalıştırır.

Sonuç `targetProp.setDataSource(values, targetChild, selectedItemCode)` ile yazılır; kaynak gerçekten değiştiyse `addOrUpdate` çağrılır.

### 8.6. AssignValueToPropertyField — `_runAssignValueToPropertyField`

1. Koşul sağlanmalı; hedef alan bulunmalı; `propertyType` dolu olmalı.
2. Değer üretimi `AssignValueToField` ile aynı mekanizmaları kullanır: `FixedValue` / `FieldValue` / `FromDataSet` (gömülü satırlar) / `FromCalculation` (async destekli) / `FromEba`.
3. `targetProp.setProperty(value, propertyType, targetChild)` çağrılır — örneğin DatePicker'ın `MinDate`'i, alanın `HelperText`'i değişir. Değişiklik olduysa `addOrUpdate` → zincirleme.

### 8.7. SetStyle — `_runSetStyle`

Hedef alan `property.code` ile bulunur.

* **Hedef ModalList ise** (`property.controlTypeId == ModalList`):
  * `withModalCondition` zorunludur (yoksa işlem yapılmadan çıkılır).
  * Her satır için satır koşulu, satırın kendi alanları üzerinde değerlendirilir.
  * Ana koşul **VE** satır koşulu sağlanırsa: `modalProperty` boşsa satırın kendisi (`serviceItem.itemStyle = style`), doluysa satırdaki o alt alan (`itemStyle = style`) stillenir.
  * Sağlanmazsa ve `clearIfConditionNotTrue` ise: satır stili **ve** satırın tüm alt alan stilleri `null` yapılır.
* **Diğer kontrollerde:** koşul sağlandı → `targetProp.itemStyle = style`; sağlanmadı + `clearIfConditionNotTrue` → `null`.

Her zaman `false` döner; stil değişimi izleyen `setState` turlarında görünür.

### 8.8. Hedef Alan Çözümleme — `_findTargetProperty`

Sıralı arama:

1. `field.propertyId == alan.objectTypeId`
2. bulunamazsa `field.code == alan.propertyCode`
3. hâlâ yoksa `childField.propertyId` ile arama
4. son olarak `childField.code` ile arama

Ek kural: ana alan bulunmuş **ve** `childField` verilmişse hedef kontrol `DataGridControl` olmak zorundadır; değilse sonuç `null`dur (child hedefleme yalnızca grid alt alanları için anlamlıdır — mutasyon metodları `targetChild` parametresiyle grid kolonuna yönlendirilir).

---

## 9. Değer Kaynakları (ValueAssignType Mekanizmaları)

Hem `AssignValueToField` işleyicisinde hem yardımcı çözümlemelerde (function parametreleri vb.) ortak davranış:

| Tip | Mekanizma | Asenkron mu |
|-----|-----------|:-----------:|
| `FixedValue` | TR/EN sabit string | Hayır |
| `FieldValue` | Kaynak alanın değeri okunur; `useDisplay` ile görünen metin okunabilir | Hayır |
| `FromCalculation` | Expression engine; sonuç `Future` ise beklenir | Olabilir |
| `FromDataSet` | Lazy: sunucu sorgusu; gömülü: kural içi satırlar | Lazy'de evet |
| `FromEba` | Entegrasyon sorgusu | Evet |
| `Function` | Harici HTTP çağrısı | Evet |

### 9.1. FixedValue / FieldValue

İçeride geçici bir koşul-değer DTO'suna çevrilerek ortak `_getValue` yolundan çözülür: sabit değer doğrudan döner; alan değeri `getControlBaseValue(useDisplay: ...)` ile okunur. `FieldValue`'da kaynak alan ModalList/RadioButtonList/FileControl ise alanın kendisi döner (bu tipler atama kaynağı olarak genellikle kullanılmaz).

### 9.2. FromCalculation

İfade `calculateExpression` ile değerlendirilir (bölüm 10). Sonuç:

* **Senkron değer** → doğrudan atanır.
* **`Future`** (ifade async fonksiyon içeriyorsa) → `activeWorkruleCount++`, hedef alan `isBusy = true`, `setState`; Future çözülünce değer atanır, sayaç ve bayrak geri alınır, tekrar `setState`.

### 9.3. FromDataSet — Tek Değer Çekme

* **Lazy (`lazyLoading == true`):** `GetDatasetSourceNew` isteği atılır; yanıtın **ilk satırından** `dataSetProperty` kolonunun değeri, hedef kontrol tipine göre dönüştürülerek alınır (bölüm 4.9 dönüşüm tablosu). Async busy deseni uygulanır.
* **Gömülü:** `workRule.dataSetItems` satırları (`hasSort` ise önce sıralanır) içinde, tüm parametre koşullarını sağlayan **ilk satır** bulunur; o satırdan `dataSetProperty` kolonunun değeri okunur. Eşleşen satır yoksa atama yapılmaz.

### 9.4. FromDataSet — Liste Doldurma ve Lazy Arama

Bölüm 8.5'te anlatıldı. Ek detay:

#### 9.4.1. Lazy Arama Akışı (`searchActive`)

1. Kural motoru ComboBox'a `lazySearchDto` (parametreleri `isSearchValue: true` işaretli hazır istek) atar.
2. Kullanıcı combo'yu açıp yazmaya başlar; kontrol, arama metnini `isSearchValue` parametrelerinin `compareValue`'suna koyup `GetDatasetSourceNew`'i çağırır.
3. Yanıt, definition/value kolonlarıyla listeye çevrilip combo'da gösterilir.

Bu modda ilk açılışta liste boştur; veri tamamen sunucu taraflı aranır (büyük veri setleri için).

### 9.5. Gömülü Veri Setinde Parametre Eşleşmesi — `_assignValueParameterCondition`

Her satır için, kuralın tüm parametreleri üzerinde:

1. Karşılaştırma değeri formdan/sabitten çözülür.
2. Satırdaki ilgili kolonun değeri okunur (`parameter.propertyId` ile satırın `properties` listesinden).
3. `criteritionType == null` → doğrudan `==`; dolu → `_compare` motoru (bölüm 7.2); `changeToCompare` sol/sağı çevirir.
4. **Tüm** parametreler sağlanmalıdır (`every`); parametre listesi `null` ise sonuç `false`tur. (Liste doldurma tarafında boş parametre listesi "filtre yok" anlamına gelir ve tüm satırlar alınır.)

### 9.6. Function — Harici HTTP Çağrısı Adımları

1. Tüm parametre grupları (`template`, `query`, `header`, `body`) için değerler `AssignValueToFieldDto` üzerinden çözülür; async kaynaklar `Future` olarak saklanır.
2. `activeWorkruleCount++`, hedef alan `isBusy = true`.
3. **URL şablonu:** her template parametresi için URL'deki `{name}` geçişleri, çözülmüş değerle değiştirilir.
4. **Query / header:** ad-değer haritalarına yazılır (değerler string'e çevrilir; `null` değerli parametreler atlanır).
5. **Body:** yalnızca `Post`'ta hazırlanır.
6. Parametre değeri son işlemede: `Future` ise beklenir; `List` ise ilk eleman alınır; `DateTime` ise ISO-8601 string'e çevrilir.
7. İstek atılır: `Post` (query + header + body), `Get` (query), `Delete` (query + body). **`Put` dalı yoktur** — `Put` seçili kural istek atmaz.
8. Yanıt işleme: gövde boşsa çıkılır; `jsonDecode`; sonuç `List` ise `[0]`; `responseParameter` doluysa o alan okunur.
9. Değer `setNewValue` ile atanır; `isBusy`/sayaç geri alınır.

### 9.7. FromEba

Entegrasyon konfigürasyonundaki form alanı eşlemeleri o anki değerlerle doldurulur ve `getintegrationqueryresult` ucuna gönderilir (header'da servis platformu). Yanıt `ComboBoxItem` listesidir; tek değer atamada ilk öğenin `value`'su kullanılır, sonuç boşsa hedefe `null` atanır. Hata durumunda boş liste döner (sessiz).

### 9.8. Sıralama — `_valueCompareTo`

Gömülü veri seti sıralamasında kullanılır:

1. `sortType == none` → `0` (sıra korunur).
2. `null` değerler: `az`'da başa, `za`'da sona.
3. Aynı tipler: string'ler küçük harfe çevrilerek, `num` ve `DateTime` doğal `compareTo` ile.
4. Farklı tipler: tip önceliği `num < DateTime < String`; aynı kategori/bilinmeyen için string temsilleri karşılaştırılır.
5. `za` ise sonuç negatiflenir.

---

## 10. Expression Engine (`calculateExpression`)

`FromCalculation` (değer üretimi) ve `FromCalculate` (koşul tarafı) ifadeleri, `expressions` Dart paketiyle değerlendirilir. İfade dili; aritmetik (`+ - * /`), karşılaştırma (`== != > >= < <=`), mantık (`&& || !`), üçlü operatör (`kosul ? a : b`), string sabitleri ve aşağıdaki fonksiyon kataloğunu destekler.

### 10.1. Form Alanı Token'ları

* Form alanları ifadeye `#PROPKODU` biçiminde yazılır.
* Değerlendirme öncesi ifade metnindeki `#` işaretleri silinir ve gereksiz parantez boşlukları normalize edilir.
* İfade `#` karakterinden bölünür; ilk parça hariç her parçanın **ilk kelimesinin ilk `.` öncesi** property kodu kabul edilir ve ifade bağlamına (context) o alanın `getControlBaseValue()` sonucu bağlanır.
* `#PROPKODU__display` → alanın display (görünen) metni bağlanır.
* İfadede geçen bir property kodu formda yoksa değerlendirme hata fırlatır (kural motoru yakalar, loglar, kural o tur çalışmaz).

`DateTime` değerlerinde üye erişimi desteklenir: `.year`, `.month`, `.day`, `.hour`, `.minute`.

Boolean dönen yardımcı fonksiyonlar genellikle `1`/`0` (int) döner; koşullar `isWeekend(#TARIH) == 1` biçiminde yazılır.

Bir fonksiyon `Future` dönerse tüm ifadenin sonucu `Future` olur; motor bunu asenkron atama desenine sokar (bölüm 9.2). Async değer bir başka fonksiyona verilecekse `toStringAsync` gibi async-uyumlu sarmalayıcılar kullanılır.

Örnekler:

```
#TUTAR * getExchange(#TARIH, #DOVIZ, 'TRY')
toStringDouble(#BIRIM_FIYAT * #ADET, 2)
day(#BASLANGIC, #BITIS) + 1
isHoliday(#TARIH) == 1 ? 'Tatil' : 'İş Günü'
sumDatagrid(#KALEMLER, 'TUTAR')
getUserFullName(#PERSONEL_KODU)
```

### 10.2. Fonksiyon Kataloğu

#### Tarih / Saat

| Fonksiyon | İmza → Dönüş | Açıklama |
|-----------|--------------|----------|
| `now()` | → DateTime | Şu an |
| `today()` | → DateTime | Bugün, saat 00:00 |
| `DateTime(y, [m=1, d=1, h=0, min=0, s=0, ms=0, us=0])` | → DateTime | Tarih üretir |
| `Duration([days=1, hours=0, minutes=0, seconds=0, ms=0, us=0])` | → Duration | Süre üretir |
| `dateTimeAdd(date, duration)` | → DateTime | Tarihe süre ekler |
| `day(x, y)` | → int | İki tarih arasındaki gün farkı (saat bileşenleri kırpılır: `y - x`) |
| `dateTimeWithTime(date, time)` | → DateTime | `date`'in tarihi + `time`'ın saati; `date` null ise null |
| `timeCompare(x, y)` | → int | Yalnızca saat/dakika karşılaştırır (`-1/0/1`) |
| `toStringDateTime(date, format)` | → String | Tarih biçimlendirme (format deseni + uygulama dili locale'i) |
| `dayOfWeek(date)` | → int | Haftanın günü (1=Pzt … 7=Paz; null → 0) |
| `isWeekend(date)` | → 1/0 | Cumartesi/Pazar mı |
| `isHoliday(date)` | → 1/0 | Kurumsal tatil takviminde mi (tatil günleri deposundan; saat kırpılarak aralık kontrolü) |

#### Çalışma Takvimi (hepsi async — kullanıcının çalışma takvimi sunucudan alınır)

| Fonksiyon | Açıklama |
|-----------|----------|
| `getWorkDayHour(userId, date, isStart)` | Kullanıcının o günkü mesai başlangıç (`isStart=true`) / bitiş saati |
| `addWorkDay(userId, day, date)` | Tarihe iş günü ekler |
| `findNextWorkDay(userId, date)` | Verilen tarihten sonraki ilk iş günü |
| `differenceWorkDay(userId, start, end, hourly)` | İş günü farkı (tatil günleri düşülür). `hourly=0`: yarım güne yukarı yuvarlanır; `hourly=1`: saatlik küsuratlı; diğer: tam güne yukarı yuvarlanır |

#### String / Sayı

| Fonksiyon | Açıklama |
|-----------|----------|
| `toString(obj)` | String'e çevirir |
| `toStringAsync(future)` | Async değeri bekleyip string'e çevirir |
| `toStringDouble(num, [decimalDigit=2])` | TR biçimli sayı: binlik `.`, ondalık `,`; `decimalDigit=0` ise yalnız tam kısım |
| `intTryParse(s)` / `doubleTryParse(s)` | TR biçimli string'i sayıya çevirir (başarısızsa `0`) |
| `toUpperCase(s)` / `toLowerCase(s)` | Büyük/küçük harf |
| `toUpperCaseTR(s)` / `toLowerCaseTR(s)` | Türkçe karakter duyarlı (İ/ı) dönüşüm |
| `replace(value, from, to)` | Tüm geçişleri değiştirir |
| `subString(value, start, [end])` | Alt string |
| `split(value, separator, index)` | Ayırıcıyla bölüp `index`'teki parçayı döner; ayırıcı yoksa değerin kendisi; index taşarsa `null` |
| `count(item, [onlySelected=false, stringSplit=false])` | ModalList: satır sayısı (`onlySelected` ile yalnız seçililer); String: uzunluk (`stringSplit=true` ile virgül parça sayısı); Iterable: eleman sayısı |
| `isMail(s)` | → 1/0 e-posta biçim kontrolü |
| `isForbiddenCharacters(s)` | → 1/0 yasaklı karakter var mı: `/ \ : * ? < > \| % # & = + , ; "` |
| `isAlnumTR(s)` | → 1/0 yalnızca harf/rakam (Türkçe harfler dahil) mı |

#### Kullanıcı / Organizasyon

Çoğu asenkrondur. Ağ kullanıcı listesi (`NetworkPage.data`) gerektiren fonksiyonlar, liste yüklenmemişse `hasWorkRuleNetworkUserError` bayrağını kaldırır (bölüm 12). Parametresiz çağrılarda oturum kullanıcısı esas alınır.

| Fonksiyon | Açıklama |
|-----------|----------|
| `getUserMail([userCode])` | E-posta (parametresiz: oturum kullanıcısının kimliği) |
| `getUserFullName([userCode])` | Ad soyad |
| `getUserId([userCode])` | Ağ kullanıcı ID'si |
| `getUserCode([userId])` | ID'den kullanıcı kodu |
| `getManagerUserId([userCode])` | Yönetici kullanıcı ID'si (parametresiz: oturum kullanıcısının "YoneticiUserId" özelliğinden) |
| `getManagerUserCode([userCode])` | Yönetici kullanıcı kodu |
| `getUserManagerByProfession(userCode, professions)` | Verilen unvan listesine göre kullanıcının yöneticisinin kodu (sunucu sorgusu + e-posta eşleşmesi) |
| `getUserAdditional(userId, additionalCode)` | Kullanıcının ek nitelik değeri (sunucudan kullanıcı kaydı çekilir) |
| `getUserWorkerLevelCode(userId)` | Kullanıcının kademe kodu (sunucu + kademe deposu) |
| `getUserCompanyCode/Name([userCode])` | İlk şirketinin kodu/adı |
| `getUserDepartmentCode/Name([userCode])` | Departman kodu/adı |
| `getDepartmentManagerCode(departmentCode)` | Departman yöneticisinin kullanıcı kodu (departman deposu + ağ kullanıcıları) |
| `getUserProfessionCode/Name(userCode)` | Unvan kodu/adı |
| `getUserExpenseCenterCode/Name([userCode])` | Masraf merkezi kodu/adı |
| `getExpenseCenterAdditional(code, qualificationId)` | Masraf merkezinin ek nitelik değeri (masraf merkezi deposundan) |
| `getUserEmploymentStartDate([userCode])` | İşe giriş tarihi |
| `checkUserInUserGroup(userCode, userGroupCode)` | → 1/0 kullanıcı grupta mı (sunucu sorgusu; hata → 0) |

#### Kredi Kartı

| Fonksiyon | Açıklama |
|-----------|----------|
| `getCreditCardNumber(code, [getLast4=false, getFirst4=false])` | Kart koduna göre kart numarası; son/ilk 4 hane seçenekli |
| `getUserCreditCardNumber([userCode, getLast4, getFirst4])` | Kullanıcının kartının numarası |
| `getUserCreditCardCode([userCode])` | Kullanıcının kartının kodu |
| `getUserCreditCardDesc([userCode])` | Kullanıcının kartının tanımı |
| `getUserByCreditCardCode(code)` | Kart kodundan kart sahibinin kullanıcı kodu (kartın e-postası üzerinden) |

#### Form / Kontrol

| Fonksiyon | Açıklama |
|-----------|----------|
| `isServiceValidate()` | Form geçerli mi: form validasyonu **ve** engelleyici (`canPassValidation=false`) iş kuralı validasyonu yok mu |
| `isPropertyValidate(propCode, [ignoreAppearance=false])` | → `"1"`/`"0"`; alan zorunlu değilse (ve `ignoreAppearance` verilmemişse) `"1"` |
| `sumDatagrid(#GRID, kolonKodu)` | Grid kolonunun toplamı (sayı ve sayısal string hücreler) |
| `avgDatagrid(#GRID, kolonKodu)` | Grid kolonunun ortalaması |
| `findPropValueFromDatagrid(#GRID, hedefKolon, kıyasKolon, isFirst)` | Kıyas kolonuna göre sıralayıp en küçük (`true`) / en büyük (`false`) satırın hedef kolon değeri |
| `sumModalList(#MODAL, propKodu)` | Modal satırlarının toplamı (seçim aktifse yalnız seçili satırlar) |
| `sumModalListWithOrElse(#MODAL, propKodu, yedekPropKodu)` | Değer boş/0 ise yedek kolonun değeri toplanır |
| `combineModalList(#MODAL, propKodu, [splitPattern])` | Satır değerlerini tekilleştirip virgülle birleştirir; `splitPattern` verilirse önce parçalara bölerek |
| `findPropValueFromModalList(#MODAL, hedefProp, kıyasProp, isFirst)` | Modal'da kıyas alanına göre en küçük/büyük satırın hedef alan değeri (klon üzerinde sıralanır, orijinal bozulmaz; CheckBox kolonu seçili-önce sıralanır) |
| `replaceTypeOfGroupByTax(propCode, hedefTipAdı, yeniTipAdı)` | GroupByTax kontrolünde, adı `hedefTipAdı` içeren masraf tipli satırların tipini `yeniTipAdı` içeren tiple değiştirir |
| `comboboxItem(value, text, selected, [ref1, ref2])` | Programatik `ComboBoxItem` üretir (combo alanına atama için; async) |

#### Diğer

| Fonksiyon | Açıklama |
|-----------|----------|
| `getExchange(date, from, to)` | Verilen tarihteki kur (async, sunucu sorgusu). `from == to` → `1.0`; sunucu `0` dönerse `null`; hata → snackbar uyarısı |

---

## 11. Organizasyon Verisi Ön Yüklemesi (`WorkRuleService.init`)

Kurallar çalışmadan önce ihtiyaç duyacakları kurum verileri belleğe alınır:

1. Kural paketi boşsa hiçbir şey yapılmaz.
2. `getRequiredDataStorageTypes()` (bölüm 4.1) hangi depoların gerektiğini çıkarır. Örnek eşlemeler:
   * FillDataSource `Departments` kaynağı → Departman deposu,
   * herhangi bir ifadede `getCreditCardNumber` geçmesi → Kredi kartı deposu,
   * `isHoliday` → Tatil günleri deposu, `getUserWorkerLevelCode` → Kademe deposu, `getExpenseCenterAdditional` → Masraf merkezi deposu…
3. Gerekli depolar **paralel** yüklenir (`Future.wait`); yükleme süresince `activeWorkruleCount` artırılır (aksiyon butonları bekletilir).
4. Herhangi bir yükleme hatasında `hasWorkRuleNetworkUserError = true` yapılır.

Depo tipleri: `Companies, Departments, CostCenters, Professions, CreditCards, VacationDays, Tiers, UserGroups, Positions, WorkingSchedule, ExpenseCategory, UserCreditCards, UserCompanies`. (Ağ kullanıcı listesi bu depolardan ayrıdır ve ayrıca yönetilir; `ExpenseType` deposuz olup çalışma anında API'den çekilir.)

---

## 12. Eşzamanlılık ve Durum Yönetimi

| Durum | Tanımlandığı yer | Etki |
|-------|------------------|------|
| `Service.activeWorkruleCount` | `Service` modeli (değişimde dinleyicileri bilgilendiren sayaç) | `> 0` iken: form ekranında "İş Kuralları Çalışıyor" göstergesi görünür; aksiyon butonu basıldığında "işlemler bitene kadar bekleyin" uyarısı gösterilip aksiyon **engellenir**. Sayaç `init` süresince, her `executeWorkRules` turu süresince ve her asenkron değer çözümlemesi (lazy dataset, async expression, function, masraf tipi yükleme) süresince artar/azalır. |
| `ItemProperty.isBusy` | Alan bazlı bayrak | Asenkron atama/doldurma sırasında ilgili kontrol üzerinde yükleniyor göstergesi. |
| `Service.hasWorkRuleNetworkUserError` | `Service` modeli (set edildiğinde `notifyhasWorkRuleNetworkUserError` callback'i tetiklenir) | Organizasyon/ağ kullanıcı verisi yüklenememiştir. Sonraki kural turları tamamen atlanır; aksiyon butonları engellenir. Bayrağı kaldıran yerler: `init` hatası, `Users` kaynağı veya kullanıcı fonksiyonları çağrıldığında ağ kullanıcı listesinin yüklü olmaması, depo `error` durumu. |
| `ChangeListProvider.changeList` | Form ekranı provider'ı | Kural atamaları `isManuelChangeFromUser: false` ile listeye girer; kullanıcı değişiklikleriyle aynı kaydetme akışına dahil olur. |

`executeWorkRules` senkron döner; asenkron aksiyonlar kendi `then/whenComplete` zincirlerinde tamamlanır ve her aşamada `setState` çağırarak UI'yi günceller. Bu nedenle bir turun "bitmesi" iki aşamalıdır: senkron kısım hemen, asenkron kısımlar istekler döndükçe. `activeWorkruleCount` bu iki aşamayı tek bir "meşgul" sinyalinde birleştirir.

---

## 13. Backend API Uçları

### 13.1. Kural Yönetimi (Ayar Ekranı)

Ortak header'lar: `accountId`, `solutionid`, `serviceId`.

| Uç | HTTP | İstek | Yanıt |
|----|------|-------|-------|
| `GetWorkRules` | POST | header'lar | `GetListWorkRulesDto` (kurallar + form alanları + profiller + veri setleri + şirketler) |
| `AddOrUpdateWorkRule` | POST | body: `WorkRuleDto` (aksiyon konfigürasyonu `value` string'inde) | Kaydedilmiş `WorkRuleDto` (ID atanmış) |
| `DeleteWorkRule/{id}` | POST | — | — |

### 13.2. Çalışma Zamanı

| Uç | Kullanım | İstek / Yanıt |
|----|----------|----------------|
| `services/...`, `instances/...` (servis detay) | Kural paketinin taşınması | Yanıt gövdesindeki `workRules` alanı = `GetListWorkRulesDto` |
| `GetDatasetSourceNew` | Lazy veri seti sorgusu (istemci cache destekli) | body: `GetWorkRuleDataSetRequestDto` → `GetWorkRuleDataSetResponseDto` |
| `GetCustomerExpenseTypes` | FillDataSource → `ExpenseType` listesi | header: `accountId` → masraf tipi listesi |
| `getintegrationqueryresult` | `FromEba` sorguları | body: entegrasyon konfigürasyonu, header: `platform` → `ComboBoxItem` listesi |
| `GetExchangeRate/{gün}/{ay}/{yıl}` | `getExchange` fonksiyonu | query: `convertedcurrency`, `currentcurrency` → kur (double) |
| `GetAccountUserByUserId/{id}` | `getUserAdditional`, `getUserWorkerLevelCode` | → kullanıcı kaydı |
| `GetUsersManagerByProfession` | `getUserManagerByProfession` | body: `UserCode`, `ProfessionCodes` → kullanıcı |
| `CheckIfUserInGroup` | `checkUserInUserGroup` | body: `userCode`, `userGroupCode` → `{ "isInGroup": bool }` |

---

## 14. Yönetim Arayüzü (Ayar Ekranları)

* **WorkRuleSettingsPage** — kural listesi. Özellikler: görüntüleme profili filtresi (kuralın `activeViewProfiles`'ına göre; boş olanlar her profilde listelenir), **alan kullanımı filtresi** (`WorkRuleDto.hasProperty` — bir alanın hangi kurallarda geçtiğini bulur), metin arama, yeni kural ekleme (kod + tanım zorunlu; kayıt `AddOrUpdateWorkRule` ile, hata olursa listeden geri alınır), silme (onaylı, `DeleteWorkRule`), düzenleme.
* **WorkRuleDetailPage** — kuralın temel bilgileri: kod, tanım, ikon, runtime tipi, aktif profiller; koşul listesi ve aksiyon tipi seçimi. Aksiyon tipi seçilince ilgili konfigürasyon görünümü açılır.
* **WorkRuleConditionDetailPage / ConditionView / ConditionCompareValueDetailPage** — koşul ağacı düzenleme: yaprak koşul (sol taraf + operatör + sağ taraf) veya grup (bağlaç + alt koşullar) ekleme; her taraf için kaynak seçimi (form alanı / sabit / profil / hesaplama).
* **ActionTypeViews/** — aksiyon tipine özel konfigürasyon ekranları; düzenleme sırasında DTO'lar JSON kopya (encode+decode) üzerinden düzenlenip onaylanınca kurala yazılır (iptalde orijinal bozulmaz). `AssignValueToField` altındaki alt görünümler değer kaynağına göre değişir (`FromCalculateView` ifade editörü, `FromFunctionView` HTTP tanımı, `FromDataSetView` + parametre sayfası).

Kaydetme her zaman `WorkRuleDto.toJson` üzerinden yapılır; aksiyon konfigürasyonu `value` string'ine gömülür (bölüm 4.2.1).

---

## 15. Davranış Notları ve Bilinen Sınırlamalar

1. **`ChangeViewProfile` mobilde çalışmaz.** Enum'da tanımlıdır (index 1) ancak aksiyon dağıtıcısında dalı yoktur; bu tipte bir kural mobil motorda sessizce atlanır.
2. **`shouldNotWorkInReadonlyMode` motor tarafından kontrol edilmez.** Alan serileşir ama kural seçimi/çalıştırması sırasında okunmaz. Salt-okunur davranış yalnızca `SetViewForFiels` içinde uygulanır (`isEnable` zorla `false`).
3. **Kural düzeyindeki `environmentRestriction` mobilde filtre olarak uygulanmaz.** Yalnızca taşınır; ortam kısıtının uygulanması diğer katmanlardadır.
4. **`FunctionMetod.Put` çalıştırılmaz.** Enum'da vardır; function çalıştırıcısında yalnızca Post/Get/Delete dalları bulunur. `Put` seçili kural istek atmadan biter.
5. **Değişim tetiklemesi yalnızca koşul alanlarına bakar.** Kuralın aksiyonunda kullanılan ama koşullarında geçmeyen bir alan değiştiğinde kural tetiklenmez. Hesaplama kurallarında ifadedeki alanlar koşullara da eklenmelidir.
6. **Koşul listesi boş/null ise sonuç `true`dur.** Koşulsuz kural, seçildiği her turda "sağlandı" kabul edilir ve aksiyonu çalışır.
7. **Hatalar yutulur.** Kural, koşul, karşılaştırma ve aksiyon hataları `try/catch` ile yakalanıp konsola yazılır; kullanıcıya yansımaz. Hata ayıklarken konsolda şu kalıplar aranmalıdır: `workrule hata`, `_findCompareResult error`, `workrule calculate hata`, `run assing FromDataSet hata`, `work rule _runSetViewRule hata`, `error GetDatasetSourceNew`.
8. **Sayı ve tarih temsil kuralları:** sayısal string'lerde TR formatı varsayılır (binlik `.`, ondalık `,`); "boş tarih" `year == 1` (`0001-01-01`) ile temsil edilir.
9. **Zincir sonlanması, mutasyon metodlarının "değişti" dönmesine bağlıdır.** Her turda değeri gerçekten değiştiren karşılıklı bağımlı kurallar döngü oluşturabilir; ayrıca özel bir tur/derinlik limiti yoktur.
10. **Kurallar liste sırasıyla çalışır; öncelik alanı yoktur.** Aynı alana yazan kurallarda son çalışan kazanır; zincirleme turlar etkin sırayı değiştirebilir.
11. **`ShowMessage` durum tutmaz.** Koşulu sağlayan her tetiklenmede dialog yeniden gösterilir.
12. **`value` alanında `"null"` string kontrolü vardır.** Backend'in `"null"` metni göndermesi durumunda konfigürasyon çözülmeden atlanır.
13. **Lazy dataset yanıtı tek satır varsayımı:** `AssignValueToField`'ın lazy modunda yanıtın ilk satırı kullanılır; sıralama/parametrelerle tekilleştirme kural tasarımcısının sorumluluğundadır.
14. **DataGrid kural desteği sınırlıdır:** satır bazlı çalıştırma yalnızca `AssignValueToField` + `useChildFieldForAssign` kombinasyonunu kapsar; diğer aksiyon tipleri grid satırları üzerinde satır-bazlı çalışmaz.

---

## 16. Uçtan Uca Örnek Senaryolar

### Senaryo 1 — Koşullu Görünürlük

**İstek:** "Avans talebi seçilirse AÇIKLAMA alanı zorunlu ve görünür olsun; değilse gizlensin."

Kural kurulumu:

* `actionType`: `SetViewForFiels`, `workRuleRuntimeType`: `always`
* Koşul: `TALEP_TIPI` (`FormValue`) `Esittir` `"AVANS"` (`FixedValue`)
* Alan tanımı: `propertyDto = ACIKLAMA`; sağlanınca `{isVisible: true, isEnabled: true, isRequired: true}`; sağlanmayınca `{isVisible: false}`

Çalışma: form açılışında ve `TALEP_TIPI` her değiştiğinde kural tetiklenir (koşulda geçtiği için); görünüm değişirse alan widget'ı yeniden inşa edilir.

### Senaryo 2 — Zincirleme Hesaplama

**İstek:** "TUTAR veya KUR değişince TL_TUTAR hesaplansın; TL_TUTAR 50.000'i aşarsa MUDUR_ONAYI alanı '1' olsun."

* Kural A: `AssignValueToField` → `TL_TUTAR`; değer `FromCalculation`: `#TUTAR * #KUR`; koşullar: `TUTAR BosDegil` **VE** `KUR BosDegil` (ifade alanları koşullara eklendi — bölüm 6.2'deki kritik davranış).
* Kural B: `AssignValueToField` → `MUDUR_ONAYI`; değer `FixedValue "1"`; `clearIfConditionNotTrue: true`; koşul: `TL_TUTAR DahaBuyuk 50000`.

Çalışma: `TUTAR` değişir → Kural A tetiklenir, `TL_TUTAR`'a yazar → yazma `addOrUpdate` üzerinden yeni tur başlatır → Kural B (koşulunda `TL_TUTAR` geçtiği için) tetiklenir → eşik aşıldıysa `MUDUR_ONAYI = "1"`, aşılmadıysa alan temizlenir.

### Senaryo 3 — Bağımlı Combo Doldurma (Lazy)

**İstek:** "ŞİRKET seçilince MASRAF_MERKEZİ combosu, o şirketin masraf merkezleriyle sunucudan doldurulsun."

* `actionType`: `FillDataSource`, kaynak `FromDataSet`, `lazyLoading: true`
* `dataSetName`: `"MasrafMerkezleri"`; `definitionProperty`: AD kolonu; `dataSetProperty`: KOD kolonu
* Parametre: dataset SIRKET_KODU kolonu `Esittir` form `#SIRKET` alanı
* Koşul: `SIRKET BosDegil`

Çalışma: `SIRKET` değişir → kural tetiklenir → combo `isBusy` olur, `GetDatasetSourceNew` isteği atılır (parametre değeri o anki `SIRKET`) → yanıt `SetDataSourceItem` listesine çevrilip combo'ya atanır → `activeWorkruleCount` süresince aksiyon butonları bekletilir.
