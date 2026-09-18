{
//***** RawSignalTest_1
// Råt signal: registrerer KUN hvornår filteret tænder, og hvor længe det er tændt.
//
// Filter (Thomas' oprindelige formel, uændret):
//   Average( MACD(C, N1*2, N1*2*maxlist(2, floor(N2/2))), 9 ) of data(A)
//     < MACD(C, N1*2, N1*2*maxlist(2, floor(N2/2))) of data(A)
//   altså: MACD ligger over sin 9-bars signallinje.
//
// Alle 625 kombinationer skrives ud: N1 fra 1 til 25, N2 fra 1 til 25.
// Samme opbygning som EdgeFinder_F5_SIGNAL, der kører uden problemer.
//
//
// KENDT PROBLEM - LÆS DETTE FØR TALLENE BRUGES
//
// MACD bygger på XAverage, som husker sin egen forrige værdi for at kunne
// regne den næste. TradeStation gemmer den hukommelse ét sted pr. kodelinje -
// ikke ét sted pr. parameterværdi. Når MACD kaldes her i en løkke med 625
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
// maxlist(2, floor(N2/2)) giver kun 11 forskellige værdier for de 25 N2-tal,
// så 350 af de 625 kombinationer er nøjagtige dubletter af hinanden.
// N2 = 1, 2, 3, 4 og 5 giver fx alle præcis det samme signal.
//
//
// VIGTIGT: Kør som almindelig backtest - IKKE via Optimize.
// VIGTIGT: Max Bars Back skal sættes højt nok til den længste MACD-længde.
//          Længste langsomme længde er 25 * 2 * 12 = 600 bars, plus 9 bars
//          til signallinjen. Sæt den til mindst 650.
// VIGTIGT: CSV-filen skal være lukket i Excel, mens der køres.
}

Input:
	int    DataFilter_A( 2 ),
	string RunID( "RawSignalTest_1" );

// Én plads pr. kombination af N1 og N2
Arrays:
	int    Filter1[25,25]( 0 ),
	int    Filter1_Forrige[25,25]( 0 ),
	int    SignalBars[25,25]( 0 ),
	string StartTekst[25,25]( "" );

Var:
	int    N1( 0 ),
	int    N2( 0 ),
	string BarTekst( "" );


//----- Start forfra, så gentagne beregninger af chartet ikke dubler linjerne -----//

	Once
		Begin
		FileDelete( "C:\Test\RawSignalTest_1.csv" );
		Print( File ("C:\Test\RawSignalTest_1.csv"), "RunID,N1,N2,Starttid,AntalBars" );
		End;


//----- Tidsstempel for den aktuelle bar (samme for alle kombinationer) -----//

	BarTekst = FormatDate( "yyyy-MM-dd", ELDateToDateTime( Date of data(DataFilter_A) ) )
	         + " "
	         + FormatTime( "HH:mm", ELTimeToDateTime( Time of data(DataFilter_A) ) );


//----- Alle kombinationer gennemløbes på hver bar -----//

	For N1 = 1 to 25
		Begin
		For N2 = 1 to 25
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
				Print( File ("C:\Test\RawSignalTest_1.csv"),
				       RunID, ",",
				       N1:0:0, ",",
				       N2:0:0, ",",
				       StartTekst[N1,N2], ",",
				       SignalBars[N1,N2]:0:0 );
				SignalBars[N1,N2] = 0;
				End;

			Filter1_Forrige[N1,N2] = Filter1[N1,N2];

			End;
		End;
