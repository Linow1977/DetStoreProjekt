{
//***** RawSignal174
// Råt signal: registrerer KUN hvornår filteret tænder, og hvor længe det er tændt.
//
// Kilde: TradingDB, tabellen filter_case, filter_case_id = 174
//
// Filter (formlen fra databasen, uændret):
//   (AbsValue(Open[1] - Close[1]) > (0.1 * Filter1_N2 ) * (High[1] - Low[1]));
//
// altså: gårsdagens krop er større end en andel af gårsdagens samlede
// udsving. Andelen styres af N2 og går fra 0,1 til 2,5.
//
// Filteret bruger KUN Filter1_N2 - ikke Filter1_N1. Der er derfor én løkke,
// ét sæt Fra/Til/Step-inputs og ét array-index, og CSV-filen har ingen
// N1-kolonne.
//
// Bemærk: N1-kolonnerne i filter_case er tomme for dette filter, men det er
// ikke dét, der afgør sagen - formlens tekst er facit. Se NOTER.md.
//
//
// INGEN SERIEFUNKTION
//
// Formlen bruger kun almindelige kursreferencer (Open, Close, High, Low) og
// AbsValue. Ingen af dem husker tidligere værdier, så problemet beskrevet i
// NOTER.md punkt 3 gælder ikke her. De 25 N2-værdier bør give forskellige
// resultater - gør de ikke det, er der noget andet galt.
//
//
// VIGTIGT: Kør som almindelig backtest - IKKE via Optimize.
// VIGTIGT: CSV-filen skal være lukket i Excel, mens der køres.
// VIGTIGT: Max Bars Back - filteret ser kun én bar tilbage, så Auto Detect
//          eller en lav værdi er nok.
// VIGTIGT: Arrayet herunder er sat til [25]. Sættes N2_Til højere end 25,
//          SKAL array-størrelsen hæves tilsvarende, ellers fejler kørslen.
}

Input:
	int    DataFilter_A( 2 ),

	int    N2_Fra( 1 ),
	int    N2_Til( 25 ),
	int    N2_Step( 1 );

// Én plads pr. værdi af N2. Se advarsel i filens hoved, hvis N2_Til hæves.
Arrays:
	int    Filter1[25]( 0 ),
	int    Filter1_Forrige[25]( 0 ),
	int    SignalBars[25]( 0 ),
	string StartTekst[25]( "" );

Var:
	int    N2( 0 ),
	string BarTekst( "" );


//----- Engangsopsætning: nulstil filen og skriv overskriftsrække -----//

	Once
		Begin
		FileDelete( "C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal174.csv" );
		Print( File("C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal174.csv"), "RunID,N2,Starttid,AntalBars" );
		End;


//----- Tidsstempel for den aktuelle bar (samme for alle varianter) -----//

	BarTekst = FormatDate( "yyyy-MM-dd", ELDateToDateTime( Date of data(DataFilter_A) ) )
	         + " "
	         + FormatTime( "HH:mm", ELTimeToDateTime( Time of data(DataFilter_A) ) );


//----- Alle værdier af N2 gennemløbes på hver bar -----//

	N2 = N2_Fra;
	While N2 <= N2_Til
		Begin

		// Selve filteret - formlen fra databasen, uændret
		If (AbsValue(Open[1] - Close[1]) > (0.1 * N2 ) * (High[1] - Low[1])) Then
			Filter1[N2] = 1
		Else
			Filter1[N2] = 0;

		// TÆNDER
		If Filter1[N2] = 1 and Filter1_Forrige[N2] = 0 Then
			Begin
			StartTekst[N2] = BarTekst;
			SignalBars[N2] = 1;
			End;

		// FORTSÆTTER
		If Filter1[N2] = 1 and Filter1_Forrige[N2] = 1 Then
			SignalBars[N2] = SignalBars[N2] + 1;

		// SLUKKER — linjen skrives her
		If Filter1[N2] = 0 and Filter1_Forrige[N2] = 1 Then
			Begin
			Print( File("C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal174.csv"),
			       "RawSignal174" + ","
			     + NumToStr( N2, 0 ) + ","
			     + StartTekst[N2] + ","
			     + NumToStr( SignalBars[N2], 0 ) );
			SignalBars[N2] = 0;
			End;

		Filter1_Forrige[N2] = Filter1[N2];

		N2 = N2 + N2_Step;
		End;
