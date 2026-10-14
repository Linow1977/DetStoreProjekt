{
//***** RawSignal332_MedPlot
// Alt-i-én udgave af RawSignal332: tegner på chartet OG skriver CSV-filen.
//
// TYPE: Dette er en SHOWME - ikke en strategi og ikke en indicator.
//       Indsættes i TradeStation som: File -> New -> ShowMe
//
// Kilde: TradingDB, tabellen filter_case, filter_case_id = 332
//
// Formel fra databasen (uændret):
//   Close of data(DataFilter_A) > (Close of data(DataFilter_B) + Filter1_N2);
//
// altså: lukkekursen på den ene tidsramme ligger mere end N2 over
// lukkekursen på den anden.
//
//
// DENNE FIL ER ANDERLEDES END DE ØVRIGE - FIRE TING
//
// 1. DECIMALTAL. N2 går fra 0,25 til 3 i skridt af 0,25 - altså 12 trin.
//    Det er kun 8 af de 381 filtre, der har decimaltal.
//
// 2. KUN N2. Filter1_N1 optræder slet ikke i formlen, så der er hverken
//    N1-input, N1-løkke eller N1-kolonne i CSV-filen.
//
// 3. TO DATASTRØMME. Både DataFilter_A og DataFilter_B bruges. Chartet SKAL
//    derfor have mindst tre datastrømme (data1, data2, data3).
//
// 4. INGEN SERIEFUNKTION. Formlen bruger kun lukkekurser. Ingen MACD, RSI
//    eller lignende, der husker tidligere værdier. Problemet fra NOTER.md
//    punkt 3 gælder altså IKKE her - de 12 N2-værdier bør give forskellige
//    resultater. Gør de ikke det, er der noget andet galt.
//
//
// HVORFOR DER ER TO VARIABLER PR. PARAMETER
//
// Et array kan ikke slås op med et decimaltal - Filter1[1,25] findes ikke.
// Derfor holdes to ting adskilt:
//
//   N2_Vaerdi  - selve tallet, fx 1,25. Bruges i formlen.
//   N2_Indeks  - et helt tal 1, 2, 3 ... Bruges til at slå op i arrayet.
//
// Indekset tæller bare trin; værdien er den rigtige parameter. Det er den
// eneste afvigelse fra skabelonen i RawSignalTest_1, og den er nødvendig.
//
//
// SKRIVCSV - KONTAKTEN DER AFGØR HVAD DEN LAVER
//
// SkrivCSV = 0  (standard)  Kun prikker. Løkken springes helt over, og
//                           CSV-filen røres ikke. Chartet tegnes med det
//                           samme, så du kan klikke dig gennem Vis_N2
//                           uden ventetid.
//
// SkrivCSV = 1              Skriver CSV-filen med alle 12 trin, ud over
//                           prikkerne.
//
// ARBEJDSGANG: sæt SkrivCSV = 1, tryk OK, lad den skrive filen én gang.
// Sæt den så tilbage til 0. Derefter kan du arbejde frit på chartet.
//
//
// PRIKKERNE sættes på hver bar, hvor filteret er tændt - hele perioden,
// ikke kun den første bar:
//    Starttid  = den første prik i en sammenhængende række
//    AntalBars = hvor mange prikker rækken består af
// Hvilken parameterværdi der vises, vælges med Vis_N2.
//
//
// VIGTIGT: CSV-filen skal være lukket i Excel, mens der køres.
// VIGTIGT: Max Bars Back - filteret ser ikke tilbage i tid, så Auto Detect
//          eller en lav værdi er nok.
// VIGTIGT: Arrayet herunder rummer 25 trin. Giver Fra/Til/Step flere end
//          25 trin, SKAL størrelsen hæves tilsvarende.
}

Input:
	int    DataFilter_A( 2 ),
	int    DataFilter_B( 3 ),

	double Vis_N2( 0.25 ),

	int    SkrivCSV( 0 ),

	double N2_Fra( 0.25 ),
	double N2_Til( 3 ),
	double N2_Step( 0.25 );

// Én plads pr. trin. Indekset tæller 1, 2, 3 ... uafhængigt af parameterens
// værdi, så decimal-skridt også kan bruges.
Arrays:
	int    Filter1[25]( 0 ),
	int    Filter1_Forrige[25]( 0 ),
	int    SignalBars[25]( 0 ),
	string StartTekst[25]( "" );

Var:
	double N2_Vaerdi( 0 ),
	int    N2_Indeks( 0 ),
	int    Vis_Taendt( 0 ),
	int    Vis_Forrige( 0 ),
	string BarTekst( "" );


//----- Engangsopsætning: nulstil filen og skriv overskriftsrække -----//

	Once
		Begin
		If SkrivCSV = 1 Then
			Begin
			FileDelete( "C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal332.csv" );
			Print( File("C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal332.csv"), "RunID,N2,Starttid,AntalBars" );
			End;
		End;


//----- PRIKKEN: én fast parameterværdi, egen kodelinje -----//

	// Er filteret tændt på denne bar?
	If Close of data(DataFilter_A) > (Close of data(DataFilter_B) + Vis_N2) Then
		Vis_Taendt = 1
	Else
		Vis_Taendt = 0;

	// En prik på hver bar, filteret er tændt. En ShowMe forbinder ikke
	// prikkerne, så en tændt periode ses som en række enkeltprikker.
	If Vis_Taendt = 1 Then
		Plot1( Low of data(DataFilter_A), "Taendt" );

	Vis_Forrige = Vis_Taendt;


//----- LØKKEN: skriver CSV-filen -----//

If SkrivCSV = 1 Then
	Begin

	BarTekst = FormatDate( "yyyy-MM-dd", ELDateToDateTime( Date of data(DataFilter_A) ) )
	         + " "
	         + FormatTime( "HH:mm", ELTimeToDateTime( Time of data(DataFilter_A) ) );

	N2_Vaerdi = N2_Fra;
	N2_Indeks = 1;
	While N2_Vaerdi <= N2_Til
		Begin

		// Selve filteret - formlen fra databasen, uændret
		If Close of data(DataFilter_A) > (Close of data(DataFilter_B) + N2_Vaerdi) Then
			Filter1[N2_Indeks] = 1
		Else
			Filter1[N2_Indeks] = 0;

		// TÆNDER
		If Filter1[N2_Indeks] = 1 and Filter1_Forrige[N2_Indeks] = 0 Then
			Begin
			StartTekst[N2_Indeks] = BarTekst;
			SignalBars[N2_Indeks] = 1;
			End;

		// FORTSÆTTER
		If Filter1[N2_Indeks] = 1 and Filter1_Forrige[N2_Indeks] = 1 Then
			SignalBars[N2_Indeks] = SignalBars[N2_Indeks] + 1;

		// SLUKKER — linjen skrives her
		If Filter1[N2_Indeks] = 0 and Filter1_Forrige[N2_Indeks] = 1 Then
			Begin
			Print( File("C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal332.csv"),
			       "RawSignal332" + ","
			     + NumToStr( N2_Vaerdi, 2 ) + ","
			     + StartTekst[N2_Indeks] + ","
			     + NumToStr( SignalBars[N2_Indeks], 0 ) );
			SignalBars[N2_Indeks] = 0;
			End;

		Filter1_Forrige[N2_Indeks] = Filter1[N2_Indeks];

		N2_Vaerdi = N2_Vaerdi + N2_Step;
		N2_Indeks = N2_Indeks + 1;
		End;

	End;
