# Växling av körfält

Lane switching används på multitool-banor och talar om för hjälparen i vilket körfält han ska köra efter svängen. När körfältsomkopplaren är aktiv byter fordonet sida efter varje sväng. Det här är lite svårt att förstå, så låt oss titta på två exempel.

![Image](../assets/images/regularchange_0_0_1020_765.png)

Om filbytet är avstängt stannar fordonet på samma sida under hela körningen där det startade. Om fordonet startade i det vänstra körfältet kommer det alltid att ligga kvar i det vänstra körfältet. Detta undviker konflikter med andra förare, men fordon på insidan av svängen (längst till vänster för vänstersvängar, längst till höger för högersvängar) måste göra snävare svängar när de fortsätter på det intilliggande körfältet.

![Image](../assets/images/symetricchange_0_0_1020_765.png)

Om körfältsbytet är aktivt, t.ex. för två fordon, fordon A till vänster och fordon B till höger, byts körfälten efter svängen. Det innebär att A då befinner sig till höger och B till vänster. Fördelen är att alla fordon har samma svängbredd och därmed samma avstånd att köra. För skördetröskor är denna inställning viktig, eftersom den ser till att röret håller sig utanför frukten och inte når in i ett annat körfält. Nackdelen är att fordonen har en chans att kollidera med varandra när de kör mot varandra på närliggande körfält.  Om du tittar på ordningen på körfälten från vänster till höger blir det tydligt: Utan symmetrisk förändring: vänster, höger, vänster, höger - det är nästan som att hoppa över ett körfält. Med symmetrisk förändring: vänster, höger, höger, vänster - från vänster till höger, en bana efter den andra. I exemplet med Combine betyder det att ingen Combine kommer att ha frukt till vänster och höger om sitt körfält.

