{
//***** RawSignalTest_1
// Råt signal: registrerer KUN hvornår filteret tænder, og hvor længe det er tændt.
//
// Filter:
//   Average( MACD(C, N1*2, N1*2*maxlist(2, N2/1.8)), 9 ) < MACD(C, ...)
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
// VIGTIGT: Kør som almindelig backtest - IKKE via Optimize.
// VIGTIGT: CSV-filen skal være lukket i Excel, mens der køres.
}

Input:
	int    DataFilter_A( 2 ),
	string RunID( "RawSignalTest_1" ),

	// Ganger-leddet er N2 divideret med dette tal. Bemærk at EasyLanguage
	// altid skriver kommatal med punktum - 1.8, ikke 1,8.
	double N2_Divisor( 1.8 ),

	// Nedre grænse for ganger-leddet. SKAL være større end 1: ved præcis 1
	// bliver de to gennemsnit lige lange, og MACD'en er så altid nul.
	// Under 1 bliver det "langsomme" gennemsnit kortest, og filteret måler
	// det modsatte af hensigten.
	double Ganger_Minimum( 2 ),

	// De eksponentielle gennemsnit skal have tid til at falde på plads, før
	// signalerne kan bruges. Længste langsomme længde er ca. 25*2*13.9 = 695 bars.
	int    VarmOpBars( 1800 );

Arrays:
	// Hurtig EMA afhænger kun af N1 (længde = N1 * 2)
	double HurtigEMA[25]( 0 ),

	// Alt det øvrige afhænger af både N1 og N2
	double LangsomEMA[25,25]( 0 ),
	double MACDVaerdi[25,25]( 0 ),
	double MACDSum[25,25]( 0 ),
	double MACDHistorik[25,25,9]( 0 ),

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

	// Pladsen i den rullende 9-bars historik, der overskrives på denne bar
	Slot = Mod( CurrentBar, 9 ) + 1;

	BarTekst = FormatDate( "yyyy-MM-dd", ELDateToDateTime( Date of data(DataFilter_A) ) )
	         + " "
	         + FormatTime( "HH:mm", ELTimeToDateTime( Time of data(DataFilter_A) ) );


//----- Alle 625 kombinationer -----//

	For N1 = 1 to 25
		Begin

		// Den hurtige EMA afhænger kun af N1, så den regnes én gang pr. N1
		Udglatning = 2 / ( N1 * 2 + 1 );

		If CurrentBar = 1 Then
			HurtigEMA[N1] = Pris
		Else
			HurtigEMA[N1] = HurtigEMA[N1] + Udglatning * ( Pris - HurtigEMA[N1] );

		For N2 = 1 to 25
			Begin

			// Ganger-leddet holdes oppe på minimum, så det langsomme gennemsnit
			// altid er længere end det hurtige. Ellers vender MACD'en på hovedet.
			Ganger = MaxList( Ganger_Minimum, N2 / N2_Divisor );

			Udglatning = 2 / ( N1 * 2 * Ganger + 1 );

			If CurrentBar = 1 Then
				LangsomEMA[N1,N2] = Pris
			Else
				LangsomEMA[N1,N2] = LangsomEMA[N1,N2]
				                  + Udglatning * ( Pris - LangsomEMA[N1,N2] );

			MACDVaerdi[N1,N2] = HurtigEMA[N1] - LangsomEMA[N1,N2];

			// Rullende 9-bars sum: træk den værdi fra, der falder ud af
			// vinduet, og læg den nye til
			MACDSum[N1,N2] = MACDSum[N1,N2]
			               - MACDHistorik[N1,N2,Slot]
			               + MACDVaerdi[N1,N2];

			MACDHistorik[N1,N2,Slot] = MACDVaerdi[N1,N2];


			//----- Signal-registrering (først når opvarmningen er ovre) -----//

			If CurrentBar > VarmOpBars Then
				Begin

				Signallinje = MACDSum[N1,N2] / 9;

				If Signallinje < MACDVaerdi[N1,N2] Then
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
