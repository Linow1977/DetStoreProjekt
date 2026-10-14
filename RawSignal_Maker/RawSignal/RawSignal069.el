{
//***** RawSignal069
// Råt signal: registrerer KUN hvornår filteret tænder, og hvor længe det er tændt.
//
// Kilde: TradingDB, tabellen filter_case, filter_case_id = 69
//
// Filter (formlen fra databasen, uændret):
//   Average( MACD(C, (Filter1_N1 * 2), (Filter1_N1 * 2 * maxlist(2, floor(Filter1_N2/2)))), 9) of data(DataFilter_A)
//     > MACD(C, (Filter1_N1 * 2), (Filter1_N1 * 2 * maxlist(2, floor(Filter1_N2/2)))) of data(DataFilter_A)
//   and Average( MACD(C, (Filter1_N1 * 2), (Filter1_N1 * 2 * maxlist(2, floor(Filter1_N2/2)))) , 9) of data(DataFilter_A) < 0;
//
// Filteret bruger begge parametre: Filter1_N1 og Filter1_N2.
// N1 og N2 styres som Fra/Til/Step - matcher TradingDB's kolonner
// filter1_n1_start/end/step og filter1_n2_start/end/step.
//
//
// KENDT PROBLEM - LÆS DETTE FØR TALLENE BRUGES
//
// MACD bygger på XAverage, som husker sin egen forrige værdi for at kunne
// regne den næste. TradeStation gemmer den hukommelse ét sted pr. kodelinje -
// ikke ét sted pr. parameterværdi. Når MACD kaldes her i en løkke med mange
// forskellige længdesæt, deler alle kombinationerne den samme hukommelse.
//
// Resultatet kan derfor være forkert, UDEN at der kommer nogen fejlmeddelelse.
// Filen kompilerer, kører og leverer tal, der ser rigtige ud.
//
// Dette er en bevidst beslutning: filen er bygget sådan efter aftale, for at
// komme videre. Tallene bør kontrolleres, før de lægges til grund for noget.
//
//
// KENDT PROBLEM 2 - BEREGNINGSTID
//
// Formlen kalder MACD tre gange pr. kombination. Med N1 og N2 fra 1 til 25
// er det 625 kombinationer, altså ca. 1875 MACD-beregninger pr. bar.
// Det er tungt, og en backtest over lang historik kan tage meget lang tid.
//
// Vil man teste hurtigere, kan man hæve N1_Step og N2_Step (fx til 5), så
// kun hver femte værdi regnes igennem. Det ændrer ikke koden - kun de tal,
// der sættes i Inputs før kørslen.
//
//
// KENDT PROBLEM 3
//
// maxlist(2, floor(N2/2)) giver kun 11 forskellige værdier for N2 = 1-25,
// så mange kombinationer bliver nøjagtige dubletter af hinanden.
// N2 = 1, 2, 3, 4 og 5 giver fx alle præcis det samme signal.
//
//
// VIGTIGT: Kør som almindelig backtest - IKKE via Optimize.
// VIGTIGT: Max Bars Back skal sættes højt nok til den længste MACD-længde.
//          Ved N1_Til=25 og N2_Til=25 er den 25*2*12 = 600 bars, plus 9
//          bars til signallinjen. Sæt den til mindst 650.
// VIGTIGT: CSV-filen skal være lukket i Excel, mens der køres.
// VIGTIGT: Arrays herunder er sat til [25,25]. Sættes N1_Til eller N2_Til
//          højere end 25, SKAL array-størrelsen hæves tilsvarende, ellers
//          fejler kørslen.
}

Input:
	int    DataFilter_A( 2 ),

	int    N1_Fra( 1 ),
	int    N1_Til( 25 ),
	int    N1_Step( 1 ),

	int    N2_Fra( 1 ),
	int    N2_Til( 25 ),
	int    N2_Step( 1 );

// Én plads pr. kombination af N1 og N2. Se advarsel i filens hoved, hvis
// N1_Til eller N2_Til hæves over 25.
Arrays:
	int    Filter1[25,25]( 0 ),
	int    Filter1_Forrige[25,25]( 0 ),
	int    SignalBars[25,25]( 0 ),
	string StartTekst[25,25]( "" );

Var:
	int    N1( 0 ),
	int    N2( 0 ),
	string BarTekst( "" );


//----- Engangsopsætning: nulstil filen og skriv overskriftsrække -----//

	Once
		Begin
		FileDelete( "C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal069.csv" );
		Print( File("C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal069.csv"), "RunID,N1,N2,Starttid,AntalBars" );
		End;


//----- Tidsstempel for den aktuelle bar (samme for alle kombinationer) -----//

	BarTekst = FormatDate( "yyyy-MM-dd", ELDateToDateTime( Date of data(DataFilter_A) ) )
	         + " "
	         + FormatTime( "HH:mm", ELTimeToDateTime( Time of data(DataFilter_A) ) );


//----- Alle kombinationer gennemløbes på hver bar -----//

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
