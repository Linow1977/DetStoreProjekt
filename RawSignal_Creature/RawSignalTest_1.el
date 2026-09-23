{
//***** RawSignalTest_1
// Råt signal: registrerer KUN hvornår filteret tænder, og hvor længe det er tændt.
//
// Filter (Thomas' oprindelige formel, uændret):
//   Average( MACD(C, N1*2, N1*2*maxlist(2, floor(N2/2))), 9 ) of data(A)
//     < MACD(C, N1*2, N1*2*maxlist(2, floor(N2/2))) of data(A)
//   altså: MACD ligger over sin 9-bars signallinje.
//
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
// KENDT PROBLEM 2
//
// maxlist(2, floor(N2/2)) giver kun 11 forskellige værdier for N2 = 1-25,
// så mange kombinationer bliver nøjagtige dubletter af hinanden.
// N2 = 1, 2, 3, 4 og 5 giver fx alle præcis det samme signal.
//
//
// FAST FILNAVN — kun én universal fil pr. filter (ændret 2026-09-22)
//
// Print(File("...")) kræver et fast, bogstaveligt filnavn i anførselstegn
// og kan IKKE tage en variabel — en variabel giver compile-fejlen
// "File name expected here". Filnavnet er derfor skrevet direkte i hvert
// Print-kald nedenfor, ikke bygget dynamisk ud fra tidsramme/dato.
//
// Navngivning af den færdige CSV-fil i forhold til workspace/tidsramme,
// og flytning til den rigtige mappe, håndteres eksternt af det separate
// EdgeFinder-programmet — ikke i denne kode. Se NOTER.md.
//
// FileAppend bruges IKKE. Print(File(...)) er hurtigere, fordi filen
// holdes åben hele kørslen i stedet for at blive åbnet og lukket for
// hver skrevet linje, som FileAppend gør.
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
// VIGTIGT: Skift filnavnet i de to Print-kald nedenfor, hvis denne fil
//          bruges som udgangspunkt for en anden RawSignal-fil.
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
		FileDelete( "C:\RawSignal_2026_TS\RawSignalTest_1.csv" );
		Print( File("C:\RawSignal_2026_TS\RawSignalTest_1.csv"), "RunID,N1,N2,Starttid,AntalBars" );
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

			// Selve filteret
			If Average( MACD( C, N1 * 2, N1 * 2 * MaxList( 2, Floor( N2 / 2 ) ) ), 9 ) of data(DataFilter_A)
			     < MACD( C, N1 * 2, N1 * 2 * MaxList( 2, Floor( N2 / 2 ) ) ) of data(DataFilter_A) Then
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
				Print( File("C:\RawSignal_2026_TS\RawSignalTest_1.csv"),
				       "RawSignalTest_1" + ","
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
