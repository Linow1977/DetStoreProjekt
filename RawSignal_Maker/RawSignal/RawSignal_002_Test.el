{
//***** RawSignal_002_Test
// Testfil til RawSignal-Creature-automationen. Dækker typen: ÉN PARAMETER (N1).
//
// Filter:
//   RSI( Close, Filter1_N1 * 3 ) of data(DataFilter_A) > 50
//
// Formlen bruger kun Filter1_N1. Der er derfor kun én løkke, ét sæt
// Fra/Til/Step-inputs og ét array-index. N2 skrives ikke i CSV-filen.
//
//
// FILNUMMERET ER FORELØBIGT
//
// "002" er ikke et rigtigt filter_case_id. Filen er bygget uden adgang til
// TradingDB, ud fra en formel der er dokumenteret i BESLUTNINGSLOG_2026-09-18.
// Når databasen er tilgængelig, skal nummeret erstattes med det rigtige
// filter_case_id, og formlen bekræftes mod filter_case.filtere.
//
//
// KENDT PROBLEM - LÆS DETTE FØR TALLENE BRUGES
//
// RSI bygger på XAverage, som husker sin egen forrige værdi for at kunne
// regne den næste. TradeStation gemmer den hukommelse ét sted pr. kodelinje -
// ikke ét sted pr. parameterværdi. Når RSI kaldes her i en løkke med mange
// forskellige længder, deler alle kombinationerne den samme hukommelse.
//
// Resultatet kan derfor være forkert, UDEN at der kommer nogen fejlmeddelelse.
// Filen kompilerer, kører og leverer tal, der ser rigtige ud.
//
// Dette er en bevidst beslutning: filen er bygget sådan efter aftale, for at
// komme videre. Tallene bør kontrolleres, før de lægges til grund for noget.
//
//
// FAST FILNAVN — kun én universal fil pr. filter (jf. beslutning 2026-09-22)
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
// FileAppend bruges IKKE.
//
//
// VIGTIGT: Kør som almindelig backtest - IKKE via Optimize.
// VIGTIGT: CSV-filen skal være lukket i Excel, mens der køres.
// VIGTIGT: Max Bars Back skal dække den længste RSI-længde. Ved N1_Til=25
//          er den 25*3 = 75 bars. Sæt den til mindst 100, eller Auto Detect.
// VIGTIGT: Arrayet herunder er sat til [25]. Sættes N1_Til højere end 25,
//          SKAL array-størrelsen hæves tilsvarende, ellers fejler kørslen.
//          Den endelige størrelse skal følge den største filter1_n1_end
//          i hele filter_case-tabellen - se ARBEJDSBESKRIVELSE_RawSignal.md.
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
		FileDelete( "C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal_002_Test.csv" );
		Print( File("C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal_002_Test.csv"), "RunID,N1,Starttid,AntalBars" );
		End;


//----- Tidsstempel for den aktuelle bar (samme for alle varianter) -----//

	BarTekst = FormatDate( "yyyy-MM-dd", ELDateToDateTime( Date of data(DataFilter_A) ) )
	         + " "
	         + FormatTime( "HH:mm", ELTimeToDateTime( Time of data(DataFilter_A) ) );


//----- Alle værdier af N1 gennemløbes på hver bar -----//

	N1 = N1_Fra;
	While N1 <= N1_Til
		Begin

		// Selve filteret
		If RSI( Close, N1 * 3 ) of data(DataFilter_A) > 50 Then
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
			Print( File("C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal_002_Test.csv"),
			       "RawSignal_002_Test" + ","
			     + NumToStr( N1, 0 ) + ","
			     + StartTekst[N1] + ","
			     + NumToStr( SignalBars[N1], 0 ) );
			SignalBars[N1] = 0;
			End;

		Filter1_Forrige[N1] = Filter1[N1];

		N1 = N1 + N1_Step;
		End;
