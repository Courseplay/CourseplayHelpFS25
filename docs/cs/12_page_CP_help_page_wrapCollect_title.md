# Ovíjení a sběr balíků

  
Ovíjení a sběr balíků lze provádět dvěma různými způsoby.  
Prvním z nich je načíst stejnou dráhu, kterou jste použili pro svůj lis a nechat ovíječku nebo sběrač jet v této dráze.  
To však může být složité, protože některé balíky se rády kutálejí nebo sjedou z trasy.  
V tomto okamžiku může pomoci náš typ úlohy zabalit a vyzvednou, protože nepotřebuje trasu.  
Zůstaňte na poli a jednoduše nastartujte řidiče z HUD s ovíjením/sbíráním balíků nebo použijte AI mapu a pošlete ho na pole, aby začal pracovat.  


  
Ovíjení balíků je velmi jednoduché. Načtěte trasu svého lisu a začněte jako jakákoli jiná práce v terénu, nebo bez trasy,  
spusťte jej ovíjením/sběrem balíků z HUD nebo nabídky AI.  


  
Při použití trasy jede pomocník s přednastaveným odsazením, takže sběrač je uprostřed trasy.  
Bez trasy Courseplay prohledá pole, zda neobsahuje nezabalené balíky, a pomocí pathfinderu najde způsob, jak  
vyhledat nejbližší balík k ovíjení.  
Automatické couvání, pokud je balík před vozidlem nebo pokud jsme příliš blízko hranice pole, by mělo zabránit nehodám.  


  
Sběr balíků funguje stejně, s trasou nebo bez ní.  
Když je sběrač plný, zastaví práci a oznámí uživateli, že je třeba vyložit. Pokud máte  
nainstalován AutoDrive, můžete jej použít k automatickému spuštění vykládky sběrače balíků.  


