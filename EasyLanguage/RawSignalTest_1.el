{
//***** RawSignalTest_1
// Råt signal: registrerer KUN hvornår filteret tænder, og hvor længe det er tændt.
//
// Filter (Thomas' formel, uændret):
//   Average( MACD(C, N1*2, N1*2*maxlist(2,floor(N2/2))), 9 ) < MACD(C, ...)
//   altså: MACD ligger over sin 9-bars signallinje.
//
// Alle 625 kombinationer skrives ud: N1 fra 1 til 25, N2 fra 1 til 25.
//
// HVORFOR KODEN IKKE BARE KALDER MACD I EN LØKKE:
// MACD bygger på XAverage, som husker sin egen forrige værdi for at kunne
// regne den næste. TradeStation gemmer den hukommelse ét sted pr. kodelinje -
// ikke ét sted pr. parameterværdi. Kaldes MACD i en løkke med skiftende
// længder, roder alle kombinationer rundt i den samme hukommelse, og
// resultatet bliver forkert UDEN at der kommer en fejlmeddelelse.
// Derfor regnes de eksponentielle gennemsnit her i hånden, med egen
// hukommelse pr. kombination.
//
// HVORFOR 275 UDREGNINGER OG IKKE 625:
// Den langsomme MACD-længde er N1*2*maxlist(2,floor(N2/2)). Ganger-leddet
// giver kun 11 forskellige værdier (2 til 12) for de 25 N2-værdier, så der
// findes kun 25 * 11 = 275 forskellige udregninger. De regnes én gang hver,
// og resultatet genbruges til at fylde alle 625 linjer ud.
//
// VIGTIGT: Kør som almindelig backtest - IKKE via Optimize.
// VIGTIGT: CSV-filen skal være lukket i Excel, mens der køres.
}

Input:
	int    DataFilter_A( 2 ),
	string RunID( "RawSignalTest_1" ),
	// De eksponentielle gennemsnit skal have tid til at falde på plads, før
	// signalerne kan bruges. Længste langsomme længde er 25*2*12 = 600 bars.
	int    VarmOpBars( 1800 );

Arrays:
	// Hurtig EMA afhænger kun af N1 (længde = N1 * 2)
	double HurtigEMA[25]( 0 ),

	// Langsom EMA, MACD og signallinje afhænger af N1 og af ganger-leddet (2-12)
	double LangsomEMA[25,12]( 0 ),
	double MACDVaerdi[25,12]( 0 ),
	double MACDSum[25,12]( 0 ),
	double MACDHistorik[25,12,9]( 0 ),

	// Signal-tilstand pr. kombination af N1 og N2
	int    Filter1[25,25]( 0 ),
	int    Filter1_Forrige[25,25]( 0 ),
	int    SignalBars[25,25]( 0 ),
	string StartTekst[25,25]( "" );

Var:
	int    N1( 0 ),
	int    N2( 0 ),
	double Ganger( 0 ),
	double Slot( 0 ),
	double Pris( 0 ),
	double Udglatning( 0 ),
	double Signallinje( 0 ),
	string BarTekst( "" );


//----- Start forfra, så gentagne beregninger af chartet ikke dubler linjerne -----//

	Once
		Begin
		FileDelete( "C:\Test\RawSignalTest_1.csv" );
		Print( File ("C:\Test\RawSignalTest_1.csv"), "RunID,N1,N2,Starttid,AntalBars" );
		End;


//----- Fælles værdier for denne bar -----//

	Pris = Close of data(DataFilter_A);

	// Pladsen i den rullende 9-bars historik, der skal overskrives på denne bar
	Slot = Mod( CurrentBar, 9 ) + 1;

	BarTekst = FormatDate( "yyyy-MM-dd", ELDateToDateTime( Date of data(DataFilter_A) ) )
	         + " "
	         + FormatTime( "HH:mm", ELTimeToDateTime( Time of data(DataFilter_A) ) );


//----- Trin 1: de 25 hurtige EMA'er -----//

	For N1 = 1 to 25
		Begin
		Udglatning = 2 / ( N1 * 2 + 1 );

		If CurrentBar = 1 Then
			HurtigEMA[N1] = Pris
		Else
			HurtigEMA[N1] = HurtigEMA[N1] + Udglatning * ( Pris - HurtigEMA[N1] );
		End;


//----- Trin 2: de 275 langsomme EMA'er, MACD-værdier og rullende 9-bars summer -----//

	For N1 = 1 to 25
		Begin
		For Ganger = 2 to 12
			Begin
			Udglatning = 2 / ( N1 * 2 * Ganger + 1 );

			If CurrentBar = 1 Then
				LangsomEMA[N1,Ganger] = Pris
			Else
				LangsomEMA[N1,Ganger] = LangsomEMA[N1,Ganger]
				                      + Udglatning * ( Pris - LangsomEMA[N1,Ganger] );

			MACDVaerdi[N1,Ganger] = HurtigEMA[N1] - LangsomEMA[N1,Ganger];

			// Rullende sum: træk den værdi fra, der falder ud af vinduet, læg den nye til
			MACDSum[N1,Ganger] = MACDSum[N1,Ganger]
			                   - MACDHistorik[N1,Ganger,Slot]
			                   + MACDVaerdi[N1,Ganger];

			MACDHistorik[N1,Ganger,Slot] = MACDVaerdi[N1,Ganger];
			End;
		End;


//----- Trin 3: alle 625 kombinationer registreres -----//

	If CurrentBar > VarmOpBars Then
		Begin

		For N1 = 1 to 25
			Begin
			For N2 = 1 to 25
				Begin

				Ganger = MaxList( 2, Floor( N2 / 2 ) );
				Signallinje = MACDSum[N1,Ganger] / 9;

				// Selve filteret: signallinjen ligger under MACD
				If Signallinje < MACDVaerdi[N1,Ganger] Then
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

		End;
