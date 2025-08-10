# Vinice

  
Práce na vinici je o něco složitější než práce na normálním poli.  
Chcete-li dosáhnout nejlepšího výsledku, měly by být všechny řádky vinice vedle sebe ve výchozí mřížce.  
Konec a začátek každé révy by měly být také přibližně stejně dlouhé.  
Pokud jsou vinice na stávajícím poli, můžete generátor otevřít přímo jako obvykle.  
Pokud nejsou na poli, musíte přejít přes nabídku AI a umístit značku pole na vinici.  


  
Generátor pro vinnou révu má méně možností.  
V závislosti na nástroji si musíte vybrat, zda budete pracovat na vinicích nebo vedle nich.  
Např. výchozí harvestor potřebuje řídit a pracovat na révě.  
      Prořezávač potřebuje jet vlevo od révy, ale pracuje na révě, takže si musíte vybrat, že budete pracovat na révě, ale řídit s odsazením.  
      Postřikovače musí jet vedle révy a musí přeskočit jednu řadu, protože stříká doleva a doprava.  


![Image](../assets/images/vineworkgen_0_0_765_510.png)

  
Na vinicích musí být vytvořena trasa pro vinice, protože umožní práci na vinicích.  


![Image](../assets/images/vineworkharvest_0_0_765_510.png)

  
Prořezávač pracuje na vinicích, takže trasa musí být generována na vinicích.  
Nástroje jsou dodávány s odsazením pro traktor, takže traktor jezdí mezi révou.  


![Image](../assets/images/vineworkpruner_0_0_765_510.png)

  
Postřikovač pracuje vedle vinné révy, takže musí od vinné révy jet buď vlevo, nebo vpravo.  
Vzhledem k tomu, že postřikovač může pracovat na levé i pravé révě současně, můžeme řadu přeskočit.  


![Image](../assets/images/vineworkspray_0_0_765_510.png)

