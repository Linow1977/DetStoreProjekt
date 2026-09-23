{
//***** RawSignal069_MedPlot
// Alt-i-én udgave af RawSignal069: tegner på chartet OG skriver CSV-filen.
//
// TYPE: Dette er en SHOWME - ikke en strategi og ikke en indicator.
//       Indsættes i TradeStation som: File -> New -> ShowMe
//
//       En ShowMe sætter en prik på baren og forbinder ikke punkterne med
//       en linje. Det er derfor den ser rigtig ud uden at skulle stilles om
//       i Format-dialogen.
//
// Kilde: TradingDB, tabellen filter_case, filter_case_id = 69
//
// Formel fra databasen (uændret):
//   Average( MACD(C, (Filter1_N1 * 2), (Filter1_N1 * 2 * maxlist(2, floor(Filter1_N2/2)))), 9) of data(DataFilter_A)
//     > MACD(C, (Filter1_N1 * 2), (Filter1_N1 * 2 * maxlist(2, floor(Filter1_N2/2)))) of data(DataFilter_A)
//   and Average( MACD(C, (Filter1_N1 * 2), (Filter1_N1 * 2 * maxlist(2, floor(Filter1_N2/2)))) , 9) of data(DataFilter_A) < 0;
//
//
// HVAD DEN GØR - TO TING PÅ ÉN GANG
//
// 1. PRIKKERNE sættes på hver bar, hvor filteret er tændt - hele perioden,
//    ikke kun den første bar. Dermed kan begge dele af det rå signal
//    aflæses direkte på chartet:
//       Starttid  = den første prik i en sammenhængende række
//       AntalBars = hvor mange prikker rækken består af
//    Hvilket parametersæt der vises, vælges med Vis_N1 og Vis_N2.
//
// 2. LØKKEN skriver CSV-filen med alle kombinationer af N1 og N2, præcis
//    som strategien RawSignal069 gør.
//
//
// HVORFOR DE TO KAN VISE FORSKELLIGE TING - OG HVORFOR DET ER POINTEN
//
// MACD husker sin egen forrige værdi, og hukommelsen hører til kodelinjen,
// ikke til parameterværdien (se NOTER.md punkt 3). Inde i løkken kaldes
// samme linje 625 gange med forskellige længder, så de deler hukommelse,
// og tallene kan blive forkerte.
//
// Prikken herunder regnes på sin egen kodelinje, én gang pr. bar med faste
// længder. Den har sin egen hukommelse og er derfor korrekt.
//
// SÅDAN BRUGES FORSKELLEN:
//   - Sæt Vis_N1 og Vis_N2 til fx 1 og 1. Læg mærke til hvor prikkerne står.
//   - Skift til fx 25 og 25. Prikkerne SKAL flytte sig - en MACD på 4 bars
//     og en på 600 bars kan ikke give samme signal.
//   - Slå så de samme to kombinationer op i CSV-filen. Står de stille dér,
//     mens prikkerne flytter sig, er fejlen bekræftet - synligt på chartet.
//
//
// SKRIVCSV - KONTAKTEN DER AFGØR HVAD DEN LAVER
//
// SkrivCSV = 0  (standard)  Kun prikker. Løkken springes helt over, og
//                           CSV-filen røres ikke. Chartet tegnes med det
//                           samme, så du kan klikke dig gennem Vis_N1 og
//                           Vis_N2 uden ventetid.
//
// SkrivCSV = 1              Skriver CSV-filen med alle 625 kombinationer,
//                           ud over prikkerne.
//
// HVORFOR DEN STÅR PÅ 0 SOM STANDARD:
// TradeStation genberegner hele studiet, hver gang du ændrer ET input -
// også Vis_N1 og Vis_N2. Med SkrivCSV = 1 betyder det, at CSV-filen
// slettes og skrives forfra hver eneste gang. Ved 114 MB tager det tid,
// hver gang du bare ville flytte en prik.
//
// ARBEJDSGANG: sæt SkrivCSV = 1, tryk OK, lad den skrive filen én gang.
// Sæt den så tilbage til 0. Derefter kan du arbejde frit på chartet.
//
//
// VIGTIGT: CSV-filen skal være lukket i Excel, mens der køres.
// VIGTIGT: Max Bars Back skal dække den længste MACD-længde. Ved N1_Til=25
//          og N2_Til=25 er den 25*2*12 = 600 bars, plus 9 til signallinjen.
//          Sæt den til mindst 650, eller Auto Detect.
// VIGTIGT: Arrays herunder er sat til [25,25]. Sættes N1_Til eller N2_Til
//          højere end 25, SKAL array-størrelsen hæves tilsvarende.
}

Input:
	int    DataFilter_A( 2 ),

	int    Vis_N1( 1 ),
	int    Vis_N2( 1 ),

	int    SkrivCSV( 0 ),

	int    N1_Fra( 1 ),
	int    N1_Til( 25 ),
	int    N1_Step( 1 ),

	int    N2_Fra( 1 ),
	int    N2_Til( 25 ),
	int    N2_Step( 1 );

// Én plads pr. kombination af N1 og N2.
Arrays:
	int    Filter1[25,25]( 0 ),
	int    Filter1_Forrige[25,25]( 0 ),
	int    SignalBars[25,25]( 0 ),
	string StartTekst[25,25]( "" );

Var:
	int    N1( 0 ),
	int    N2( 0 ),
	int    Vis_Taendt( 0 ),
	int    Vis_Forrige( 0 ),
	string BarTekst( "" );


//----- Engangsopsætning: nulstil filen og skriv overskriftsrække -----//

	Once
		Begin
		If SkrivCSV = 1 Then
			Begin
			FileDelete( "C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal069.csv" );
			Print( File("C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal069.csv"), "RunID,N1,N2,Starttid,AntalBars" );
			End;
		End;


//----- PRIKKEN: ét fast parametersæt, egen kodelinje -----//

	// Er filteret tændt på denne bar?
	If Average( MACD(C, (Vis_N1 * 2), (Vis_N1 * 2 * maxlist(2, floor(Vis_N2/2)))), 9) of data(DataFilter_A)
	     > MACD(C, (Vis_N1 * 2), (Vis_N1 * 2 * maxlist(2, floor(Vis_N2/2)))) of data(DataFilter_A)
	   and Average( MACD(C, (Vis_N1 * 2), (Vis_N1 * 2 * maxlist(2, floor(Vis_N2/2)))) , 9) of data(DataFilter_A) < 0 Then
		Vis_Taendt = 1
	Else
		Vis_Taendt = 0;

	// Der sættes en prik på HVER bar, hvor filteret er tændt - ikke kun på
	// den første. Dermed kan begge dele af signalet aflæses direkte på
	// chartet, præcis som de står i CSV-filen:
	//
	//   Starttid  = den første prik i en sammenhængende række
	//   AntalBars = hvor mange prikker rækken består af
	//
	// En ShowMe forbinder ikke prikkerne, så en tændt periode ses som en
	// række enkeltprikker - ikke som en streg.
	If Vis_Taendt = 1 Then
		Plot1( Low of data(DataFilter_A), "Taendt" );

	Vis_Forrige = Vis_Taendt;


//----- LØKKEN: skriver CSV-filen, som strategien gør -----//

If SkrivCSV = 1 Then
	Begin

	BarTekst = FormatDate( "yyyy-MM-dd", ELDateToDateTime( Date of data(DataFilter_A) ) )
	         + " "
	         + FormatTime( "HH:mm", ELTimeToDateTime( Time of data(DataFilter_A) ) );

	N1 = N1_Fra;
	While N1 <= N1_Til
		Begin

		N2 = N2_Fra;
		While N2 <= N2_Til
			Begin

			// Selve filteret - formlen fra databasen, uændret
			If Average( MACD(C, (N1 * 2), (N1 * 2 * maxlist(2, floor(N2/2)))), 9) of data(DataFilter_A)
			     > MACD(C, (N1 * 2), (N1 * 2 * maxlist(2, floor(N2/2)))) of data(DataFilter_A)
			   and Average( MACD(C, (N1 * 2), (N1 * 2 * maxlist(2, floor(N2/2)))) , 9) of data(DataFilter_A) < 0 Then
				Filter1[N1,N2] = 1
			Else
				Filter1[N1,N2] = 0;

			// TÆNDER
			If Filter1[N1,N2] = 1 and Filter1_Forrige[N1,N2] = 0 Then
				Begin
				StartTekst[N1,N2] = BarTekst;
				SignalBars[N1,N2] = 1;
				End;

			// FORTSÆTTER
			If Filter1[N1,N2] = 1 and Filter1_Forrige[N1,N2] = 1 Then
				SignalBars[N1,N2] = SignalBars[N1,N2] + 1;

			// SLUKKER — linjen skrives her
			If Filter1[N1,N2] = 0 and Filter1_Forrige[N1,N2] = 1 Then
				Begin
				Print( File("C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal069.csv"),
				       "RawSignal069" + ","
				     + NumToStr( N1, 0 ) + ","
				     + NumToStr( N2, 0 ) + ","
				     + StartTekst[N1,N2] + ","
				     + NumToStr( SignalBars[N1,N2], 0 ) );
				SignalBars[N1,N2] = 0;
				End;

			Filter1_Forrige[N1,N2] = Filter1[N1,N2];

			N2 = N2 + N2_Step;
			End;

		N1 = N1 + N1_Step;
		End;

	End;
