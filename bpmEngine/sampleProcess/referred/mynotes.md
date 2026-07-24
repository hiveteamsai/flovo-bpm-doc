Süreç Açıklaması

EventForm aksiyonlar: Yönelendi, Onayla ve Yönlendir aksiyonları Yönelendir Evet Form kullanır, Reddet, Geri Gönder aksiyonları Reddet Event Form kullanır.

Süreç webhook ile başlayarak webhookta gelen parametreler ile birlikte Formda yer alan değerler bu parametreler ile ilk değer atanır ve "Kontrol Grubu" kullanıcı grubuna "Kontrol Grubunda" durumu ile ilerler

Kontrol Grubu onaylaması durumunda Muhasebe Grubu Kullanıcısına gider veya Bu Form ile ilgili onay vermesi gereken bir kişi var ise Yönlendir aksiyonu alır. aksiyon alır iken popup ile birlikte bir kullanıcı seçer. seçtiği kullanıcı parametre olarak "Yönelendirilen Kullanıcı Atama"  Adımına ilerler

"Yönlendirilen Kullanıcı Atama" süreç adımı değer atama süreç adımındır. parametre olarak gelen transferUser verisini Formda yer alan "Yönelndirilen Kullanıcı" alanına değer olarak atar ve default aksiyon ile ilerleyerek "Yönlendirilen Kullanıcı" adımına "Yönlendirilen Sorumlu Onayında" durumu ile ilerler

"Yönlendirilen Kullanıcı" adımı dinamik kullanıcı süreç adımıdır. Formda yer alan "Yönlendirilen Kullanıcı" alanında yazan kullanıcıya form aksiyon beklemede olarak atanır. Kullanıcı Formu onayla aksiyonu alması durumunda "Yönetici" adımına "Yönetici Onayında" durumunda ilerler. bu aksiyon bu form ile ilgili bilgileri onayladığı anlamına gelir. Kullanıcı Yönlendir aksiyonu alması durumunda kullanıcının karışısına çıkan popup ile birlikte kullanıcı seçimi yapar ve seçilen kullanıcıyı parametre ile birlikte "Yönlendirilen Kullanıcı Atama" adımına ilerler . bu aksiyon ile birlikte kullanıcı bu form benim ile ilgili değil diyerek farklı bir kullanıcıya yönlendirmiş olur. Kullanıcı onayla ve yönelendir aksiyonu alması durumunda yine kullanıcı seçim popup ı çıkar ve seçmiş olduğu kullanıcıyı parametre ile birlikte "Yönetici"  adımına "yönetici onayında" olarak ilerletir.

Yönetici adımın Kullanıcı Yöneticisi Adımıdır ve hedef süreç adımı olarak Yönlendirilen Kullanıcı Adımı seçilmiştir. Yönelendirilen Kullanıcı adımında aksiyon alan kullanıcı kim ise Yönetici 1 Adımında o kullanıcının yöneticisine aksiyon alabilir olur. Yönetici Onayla aksiyonu alması durumunda "TransferUser Kontrol" adımına ilerler. onayla aksiyonunda mergeParameter aktiftir ve Yönetici adımına aktarılan parametreler onayla aksiyonu ile birlikte bir "TransferUserKontrol" adıma iletilir(trasnferUser). Yönetici "Geri Gönder" aksiyonu alması durumunda karşısına çıkan popup ile birlikte Red Nedenini girerek aksiyonu tetiktir ve "Yönlendirilen Kullanıcı" adımına "Geri Gönderildi" durumu ile ilerler.

"TransferUser Kontrol" adımı bir karşılaştırma adımıdır. parametre olarak gelen transferUser verisini kontrol eder. transferUser verisi boş ise true aksiyonu tetiklenir. transferUser boş değil ise false aksiyonu tetiklenir. true aksiyonu tetiklenmesi durumunda "Muhasebe Grubu" süreç adımına "Muhasebe Onayında" durumunda ilerler. false aksiyonu alınması durumunda "Yöneldirilen Kullanıcı Atama"  adımına ilerler. false aksiyonunda mergeParameter özelliği aktiftir ve "TransferUser Kontrol" adımına gelen parametre "Yöneldirilen Kullanıcı Atama" adımına ilerlerken aktarılır(trasnferUser)

"Muhasebe Grubu" adımı statik kullanıcı grubu süreç adımıdır ve Muhasebe kullanıcı grubunda yer alan kullanıcılar aksiyon alabilir durudadır. Onayla aksiyonu alınması durumunda  "Tamamlandı" Durumu iler süreç bitişine ilerler. Reddet Aksiyonu alınması durumunda çıkan popup ile birlikte red Nedeni girilerek aksiyon alınır ve reddedildi durumu ile birlikte süreç bitişine ilerler



