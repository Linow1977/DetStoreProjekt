{
//***** RawSignal069_ShowMe
// Viser på chartet, hvor filteret fra RawSignal069 er tændt.
//
// TYPE: Dette er en ShowMe - IKKE en strategi.
//       Indsæt den i TradeStation som "New ShowMe" (ikke New Strategy),
//       og læg den på chartet ved siden af RawSignal069.
//
// Kilde: TradingDB, tabellen filter_case, filter_case_id = 69
//
// Filter (formlen fra databasen, uændret):
//   Average( MACD(C, (Filter1_N1 * 2), (Filter1_N1 * 2 * maxlist(2, floor(Filter1_N2/2)))), 9) of data(DataFilter_A)
//     > MACD(C, (Filter1_N1 * 2), (Filter1_N1 * 2 * maxlist(2, floor(Filter1_N2/2)))) of data(DataFilter_A)
//   and Average( MACD(C, (Filter1_N1 * 2), (Filter1_N1 * 2 * maxlist(2, floor(Filter1_N2/2)))) , 9) of data(DataFilter_A) < 0;
//
//
// FORSKELLEN FRA STRATEGIEN - OG HVORFOR DEN ER NYTTIG
//
// Strategien RawSignal069 løber 625 parameterkombinationer igennem i en
// løkke. Det betyder, at MACD kaldes 625 gange fra samme kodelinje, og de
// deler intern hukommelse - derfor kan dens tal blive forkerte (se NOTER.md
// punkt 3).
//
// Denne ShowMe viser ÉT parametersæt ad gangen. MACD kaldes derfor kun én
// gang pr. kodelinje, og problemet opstår ikke. Det, du ser her, er det
// korrekte signal for netop de N1 og N2, du indtaster.
//
// Brug den til at kontrollere strategien: sæt N1 og N2 til en kombination,
// find de samme værdier i RawSignal069.csv, og se om starttidspunkt og
// varighed passer med det, der tegnes på chartet.
//
//
// SÅDAN BRUGES DEN
//
// 1. Indsæt som ShowMe i TradeStation Development Environment.
// 2. Læg den på samme chart som strategien.
// 3. Sæt N1 og N2 i Inputs til den kombination, du vil se.
// 4. Der sættes en prik over hver bar, hvor filteret er tændt.
//
// VIGTIGT: Max Bars Back skal dække den længste MACD-længde. Ved N1=25 og
//          N2=25 er den 25*2*12 = 600 bars, plus 9 til signallinjen.
//          Sæt den til mindst 650, eller Auto Detect.
}

Input:
	int    DataFilter_A( 2 ),
	int    N1( 1 ),
	int    N2( 1 );

Var:
	int    Taendt( 0 ),
	int    Forrige( 0 );


//----- Selve filteret - samme formel som strategien, ét parametersæt -----//

	If Average( MACD(C, (N1 * 2), (N1 * 2 * maxlist(2, floor(N2/2)))), 9) of data(DataFilter_A)
	     > MACD(C, (N1 * 2), (N1 * 2 * maxlist(2, floor(N2/2)))) of data(DataFilter_A)
	   and Average( MACD(C, (N1 * 2), (N1 * 2 * maxlist(2, floor(N2/2)))) , 9) of data(DataFilter_A) < 0 Then
		Taendt = 1
	Else
		Taendt = 0;

	// Prikken sættes KUN hvor filteret tænder - altså ved overgangen fra
	// slukket til tændt. Er filteret tændt i 40 bars i træk, kommer der
	// én prik, ikke fyrre. Det svarer til kolonnen Starttid i CSV-filen.
	If Taendt = 1 and Forrige = 0 Then
		Plot1( Low of data(DataFilter_A), "Start" );

	Forrige = Taendt;
