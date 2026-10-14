{
//***** RawSignal266
// Råt signal: registrerer KUN hvornår filteret tænder, og hvor længe det er tændt.
//
// Kilde: TradingDB, tabellen filter_case, filter_case_id = 266
//
// Filter (formlen fra databasen, uændret):
//   TrueRange of data(DataFilter_A) > Average(TrueRange of data(DataFilter_B), Filter1_N1);
//
// altså: udsvinget på den ene tidsramme er større end gennemsnitsudsvinget
// på den anden tidsramme.
//
// Filteret bruger kun Filter1_N1. Der er derfor én løkke, ét sæt
// Fra/Til/Step-inputs og ét array-index. N2 skrives ikke i CSV-filen.
//
//
// TO DATASTRØMME - LÆS DETTE FØR KØRSEL
//
// Formlen bruger både DataFilter_A og DataFilter_B. Standardværdierne er
// 2 og 3, så chartet SKAL have mindst tre datastrømme (data1, data2, data3).
// Har chartet kun to, kan strategien ikke køre.
//
// Tallene i DataFilter_A og DataFilter_B henviser til data-nummeret på
// chartet, ikke til en tidsramme i minutter. De kan ændres i Inputs.
//
//
// KENDT PROBLEM - LÆS DETTE FØR TALLENE BRUGES
//
// Average er en indbygget seriefunktion, som husker sin egen forrige værdi
// for at kunne regne den næste. TradeStation gemmer den hukommelse ét sted
// pr. kodelinje - ikke ét sted pr. parameterværdi. Når den kaldes her i en
// løkke med 25 forskellige længder, deler alle varianterne den samme
// hukommelse.
//
// Resultatet kan derfor være forkert, UDEN at der kommer nogen fejlmeddelelse.
// Det er målt på RawSignal069, hvor alle 625 kombinationer gav nøjagtig det
// samme resultat. Forvent at N1 heller ikke gør nogen forskel her.
//
// Se NOTER.md punkt 3.
//
//
// VIGTIGT: Kør som almindelig backtest - IKKE via Optimize.
// VIGTIGT: CSV-filen skal være lukket i Excel, mens der køres.
// VIGTIGT: Max Bars Back skal dække den længste Average-længde. Ved
//          N1_Til=25 er den 25 bars. Sæt den til mindst 50, eller
//          Auto Detect.
// VIGTIGT: Arrayet herunder er sat til [25]. Sættes N1_Til højere end 25,
//          SKAL array-størrelsen hæves tilsvarende, ellers fejler kørslen.
}

Input:
	int    DataFilter_A( 2 ),
	int    DataFilter_B( 3 ),

	int    N1_Fra( 1 ),
	int    N1_Til( 25 ),
	int    N1_Step( 1 );

// Én plads pr. værdi af N1. Se advarsel i filens hoved, hvis N1_Til hæves.
Arrays:
	int    Filter1[25]( 0 ),
	int    Filter1_Forrige[25]( 0 ),
	int    SignalBars[25]( 0 ),
	string StartTekst[25]( "" );

Var:
	int    N1( 0 ),
	string BarTekst( "" );


//----- Engangsopsætning: nulstil filen og skriv overskriftsrække -----//

	Once
		Begin
		FileDelete( "C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal266.csv" );
		Print( File("C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal266.csv"), "RunID,N1,Starttid,AntalBars" );
		End;


//----- Tidsstempel for den aktuelle bar (samme for alle varianter) -----//

	BarTekst = FormatDate( "yyyy-MM-dd", ELDateToDateTime( Date of data(DataFilter_A) ) )
	         + " "
	         + FormatTime( "HH:mm", ELTimeToDateTime( Time of data(DataFilter_A) ) );


//----- Alle værdier af N1 gennemløbes på hver bar -----//

	N1 = N1_Fra;
	While N1 <= N1_Til
		Begin

		// Selve filteret - formlen fra databasen, uændret
		If TrueRange of data(DataFilter_A) > Average(TrueRange of data(DataFilter_B), N1) Then
			Filter1[N1] = 1
		Else
			Filter1[N1] = 0;

		// TÆNDER
		If Filter1[N1] = 1 and Filter1_Forrige[N1] = 0 Then
			Begin
			StartTekst[N1] = BarTekst;
			SignalBars[N1] = 1;
			End;

		// FORTSÆTTER
		If Filter1[N1] = 1 and Filter1_Forrige[N1] = 1 Then
			SignalBars[N1] = SignalBars[N1] + 1;

		// SLUKKER — linjen skrives her
		If Filter1[N1] = 0 and Filter1_Forrige[N1] = 1 Then
			Begin
			Print( File("C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal266.csv"),
			       "RawSignal266" + ","
			     + NumToStr( N1, 0 ) + ","
			     + StartTekst[N1] + ","
			     + NumToStr( SignalBars[N1], 0 ) );
			SignalBars[N1] = 0;
			End;

		Filter1_Forrige[N1] = Filter1[N1];

		N1 = N1 + N1_Step;
		End;
