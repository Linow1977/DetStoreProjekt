{
//***** @EdgeFinder_F5_SIGNAL
// "Volatility Filters" "Case 5"
// Registrerer KUN hvornår filteret tænder, og hvor længe det er tændt.
//
// Denne udgave kører ALLE varianter af Filter1_N1 (1 til 25) i ÉT gennemløb.
// Årsag: under en TradeStation-optimering kører flere pas parallelt, og de kan
// ikke dele den samme udfil - kun det første pas får lov at skrive, resten
// fejler med OpenFileException/WriteFileException. Med ét gennemløb er der
// kun én der rører filen, og problemet forsvinder.
//
// VIGTIGT: Kør den som en almindelig backtest - IKKE via Optimize.
// VIGTIGT: Max Bars Back skal sættes til mindst 130 (længste ATR er 25 * 5 = 125 bars).
}

Input:
	int    N1_Fra( 1 ),
	int    N1_Til( 25 ),
	int    DataFilter_A( 2 ),
	string RunID( "RUN0001" );

// Én plads pr. variant af N1. Skal N1_Til over 25, skal tallet her hæves tilsvarende.
Arrays:
	int    Filter1[25]( 0 ),
	int    Filter1_Forrige[25]( 0 ),
	int    SignalBars[25]( 0 ),
	string StartTekst[25]( "" );

Var:
	int    N1( 0 ),
	string BarTekst( "" );


//----- Start forfra, så gentagne beregninger af chartet ikke dubler linjerne -----//

	Once
		FileDelete( "C:\Test\signals_test.csv" );


//----- Tidsstempel for den aktuelle bar (samme for alle varianter) -----//

	BarTekst = FormatDate( "yyyy-MM-dd", ELDateToDateTime( Date of data(DataFilter_A) ) )
	         + " "
	         + FormatTime( "HH:mm", ELTimeToDateTime( Time of data(DataFilter_A) ) );


//----- Alle varianter af N1 gennemløbes på hver bar -----//

	For N1 = N1_Fra to N1_Til
		Begin

		// Selve filteret
		If Range of data(DataFilter_A) > AvgTrueRange(N1 * 5) of data(DataFilter_A) Then
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
			Print( File ("C:\Test\signals_test.csv"),
			       RunID, ",",
			       N1:0:0, ",",
			       StartTekst[N1], ",",
			       SignalBars[N1]:0:0 );
			SignalBars[N1] = 0;
			End;

		Filter1_Forrige[N1] = Filter1[N1];

		End;
