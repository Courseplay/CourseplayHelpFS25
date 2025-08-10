# Hat Değişimi

  
Hat değiştirme, çoklu araç rotalarında kullanılır ve yardımcının dönüş sonrası hangi hat üzerinde gitmesi gerektiğini belirtir.  
Hat değiştirme aktifken, araç her dönüşten sonra taraf değiştirir.  
Bu biraz kafa karıştırıcı olabilir, o yüzden aşağıdaki iki örneğe bakalım.  


![Image](../assets/images/regularchange_0_0_1020_765.png)

  
Eğer hat değiştirme kapalıysa, araç tüm rota boyunca başladığı tarafta kalır.  
En sol tarafta başladıysa, hep en sol tarafta devam eder. Diğer şoförlerle çarpışma önlenir,  
ancak iç tarafta kalan araçlar daha dar dönüş yapmak zorunda kalır.(sola dönüşlerde en soldaki, sağa dönüşlerde en sağdaki)  
  


![Image](../assets/images/symetricchange_0_0_1020_765.png)

  
Hat değiştirme aktifse, örneğin iki araç için, A aracı solda ve B aracı sağda başlıyorsa, dönüşten sonra hatlar değiştirilir.  
Bu durumda A aracı sağa, B aracı ise sola geçer.  
Avantajı, tüm araçların aynı dönüş genişliğine sahip olması ve dolayısıyla aynı mesafeyi kat etmeleridir.  
Biçerdöverler için bu ayar önemlidir, boşaltma borusunun ekinin dışında kalmasını ve başka bir hatta ulaşmamasını sağlar.  
Dezavantajı ise, yan yana hatlardaki araçların dönüşlerde birbirlerini geçerken çarpışma ihtimalinin olmasıdır.  
  
Hatların sırasını soldan sağa doğru incelerseniz, biraz daha netleşir:  
Simetrik değişim olmadan: sol, sağ, sol, sağ — sanki bir satır atlanıyor gibi görünüyor.  
Simetrik değişimle: sol, sağ, sağ, sol — soldan sağa, bir satırdan diğer satıra.  
Biçerdöver örneğinde şu anlama gelir: hiçbir biçerdöverin hattının solunda ve sağında ekin bulunmaz.  


