{
//***** RawSignal020
// Råt signal: registrerer KUN hvornår filteret tænder, og hvor længe det er tændt.
//
// Kilde: TradingDB, tabellen filter_case, filter_case_id = 20
//
// Filter (formlen fra databasen, uændret):
//   DMIplus( Filter1_N1 * 10 ) of data(DataFilter_A) < DMIminus(Filter1_N1 * 10) of data(DataFilter_A);
//
// Filteret bruger kun Filter1_N1. Der er derfor én løkke, ét sæt
// Fra/Til/Step-inputs og ét array-index. N2 skrives ikke i CSV-filen.
//
//
// KENDT PROBLEM - LÆS DETTE FØR TALLENE BRUGES
//
// DMIplus og DMIminus er indbyggede seriefunktioner, som husker deres egen
// forrige værdi for at kunne regne den næste. TradeStation gemmer den
// hukommelse ét sted pr. kodelinje - ikke ét sted pr. parameterværdi. Når de
// kaldes her i en løkke med 25 forskellige længder, deler alle varianterne
// den samme hukommelse.
//
// Resultatet kan derfor være forkert, UDEN at der kommer nogen fejlmeddelelse.
// Filen kompilerer, kører og leverer tal, der ser rigtige ud.
//
// Dette er en bevidst beslutning (se NOTER.md punkt 3): risikoen accepteres
// for at komme videre, men tallene bør kontrolleres, før de lægges til grund
// for noget.
//
//
// VIGTIGT: Kør som almindelig backtest - IKKE via Optimize.
// VIGTIGT: CSV-filen skal være lukket i Excel, mens der køres.
// VIGTIGT: Max Bars Back skal dække den længste DMI-længde. Ved N1_Til=25
//          er den 25 * 10 = 250 bars. Sæt den til mindst 300, eller
//          Auto Detect.
// VIGTIGT: Arrays herunder er sat til [25]. Sættes N1_Til højere end 25,
//          SKAL array-størrelsen hæves tilsvarende, ellers fejler kørslen.
}

Input:
	int    DataFilter_A( 2 ),

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
		FileDelete( "C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal020.csv" );
		Print( File("C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal020.csv"), "RunID,N1,Starttid,AntalBars" );
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
		If DMIplus( N1 * 10 ) of data(DataFilter_A) < DMIminus( N1 * 10 ) of data(DataFilter_A) Then
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
			Print( File("C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal020.csv"),
			       "RawSignal020" + ","
			     + NumToStr( N1, 0 ) + ","
			     + StartTekst[N1] + ","
			     + NumToStr( SignalBars[N1], 0 ) );
			SignalBars[N1] = 0;
			End;

		Filter1_Forrige[N1] = Filter1[N1];

		N1 = N1 + N1_Step;
		End;
