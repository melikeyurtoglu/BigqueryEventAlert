# BigqueryEventAlert

Bigquery üzerindeki bir takımın yaptığıkları eventlerin tutulduğu bir tablodaki event artış azalışına göre alarm oluşturmak için bir yapı kurdum. 

 Yapı'da alarmları oluşturup opsgenie ile entegrasyonunu sağlayabilmek için python'ı abstract layer olarak kullandım. İlerde alarm oluşturmak isteyebilceğimiz eventler oldukça kolay entegrasyon sağlaması amacıyla query'leri dosyadan okuyup bigquery'den sonuçları aldıktan sonra alarm olup olmamasına göre opsgenie'ye api call yaparak alarm oluşturmasını sağladım.
 
 Yapı şu şekilde:
 
![image](https://user-images.githubusercontent.com/6206561/146657957-9ce620e4-5cab-40ec-a8f1-eeb57d555783.png)

Peki yapı tam olarak nasıl çalışıyor? 

Adım adım süreç şu şekilde;

1) İlgili event için bir özet tablo oluşturuyoruz. Bu tablo son 3 aylık datanın gün ve saat bazlı  ortalama gelen event sayısını tutuyor. 
2) Jenkins üzerinde her event kontrolü için ayrı bir job tanımlı ve saatlik olarak çalışıyorlar.
3) Her event kontrolü için ayrı bir query dosyası var. Ben repoya bir tane query dosyası ekledim. Siz query'lerinizi istediğiniz dosya ismi ile dosya içinde tutup jenkinsfile içinden python'a verebilirsiniz.


*****Tabi burda unutulmamalıdır ki kendi tablo yapınıza query sonucunuza  göre sütun isimleriniz ve buna bağlı olarakta bigquery.py dosyasındaki row.${sutunadı} alanları değişecektir. Bigquery.py 'de if elif statement'i bizim takımlarımıza ait eventlerin state ve type içermeyen query sonuçlarına göre eklenmiştir. 

