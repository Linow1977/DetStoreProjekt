{
//***** RawSignal_004_Test
// Testfil til RawSignal-Creature-automationen. Dækker typen: KUN N2 BRUGES
// (N1 optræder slet ikke i formlen) + indbygget seriefunktion.
//
// Filter:
//   ChaikinMoneyFlow( 3 * Filter1_N2 ) of data(DataFilter_A) > 0
//
//
// HVORFOR NETOP DENNE TYPE ER MED I TESTEN
//
// Det er den kendte faldgrube fra NOTER.md: man kan IKKE gå ud fra, hvilke
// parametre en formel bruger, ud fra om databasekolonnerne er udfyldt.
// Nogle formler bruger kun Filter1_N2 og slet ikke Filter1_N1, selvom begge
// sæt kolonner har værdier i filter_case. Formlens tekst skal læses.
//
// Denne fil har derfor KUN N2-inputs og ét array-index, og CSV-filen har
// ingen N1-kolonne. Bygges den forkert (med en tom N1-løkke udenom), laver
// den samme arbejde 25 gange for ingenting.
//
//
// FILNUMMERET ER FORELØBIGT
//
// "004" er ikke et rigtigt filter_case_id. Filen er bygget uden adgang til
// TradingDB, ud fra en formel der er dokumenteret i BESLUTNINGSLOG_2026-09-18
// (dér skrevet med Filter1_N1; her brugt med Filter1_N2 for at få
// kun-N2-tilfældet med i testen). Når databasen er tilgængelig, skal der
// findes et rigtigt kun-N2-filter i filter_case, og denne fil erstattes.
//
//
// KENDT PROBLEM - LÆS DETTE FØR TALLENE BRUGES
//
// ChaikinMoneyFlow er en indbygget seriefunktion, der husker sin egen forrige
// værdi for at kunne regne den næste. TradeStation gemmer den hukommelse ét
// sted pr. kodelinje - ikke ét sted pr. parameterværdi. Når den kaldes her i
// en løkke med mange forskellige længder, deler alle varianterne den samme
// hukommelse.
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
// VIGTIGT: Max Bars Back skal dække den længste ChaikinMoneyFlow-længde.
//          Ved N2_Til=25 er den 3*25 = 75 bars. Sæt den til mindst 100,
//          eller Auto Detect.
// VIGTIGT: Arrayet herunder er sat til [25]. Sættes N2_Til højere end 25,
//          SKAL array-størrelsen hæves tilsvarende, ellers fejler kørslen.
//          Den endelige størrelse skal følge den største filter1_n2_end
//          i hele filter_case-tabellen - se ARBEJDSBESKRIVELSE_RawSignal.md.
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
		FileDelete( "C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal_004_Test.csv" );
		Print( File("C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal_004_Test.csv"), "RunID,N2,Starttid,AntalBars" );
		End;


//----- Tidsstempel for den aktuelle bar (samme for alle varianter) -----//

	BarTekst = FormatDate( "yyyy-MM-dd", ELDateToDateTime( Date of data(DataFilter_A) ) )
	         + " "
	         + FormatTime( "HH:mm", ELTimeToDateTime( Time of data(DataFilter_A) ) );


//----- Alle værdier af N2 gennemløbes på hver bar -----//

	N2 = N2_Fra;
	While N2 <= N2_Til
		Begin

		// Selve filteret
		If ChaikinMoneyFlow( 3 * N2 ) of data(DataFilter_A) > 0 Then
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
			Print( File("C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal_004_Test.csv"),
			       "RawSignal_004_Test" + ","
			     + NumToStr( N2, 0 ) + ","
			     + StartTekst[N2] + ","
			     + NumToStr( SignalBars[N2], 0 ) );
			SignalBars[N2] = 0;
			End;

		Filter1_Forrige[N2] = Filter1[N2];

		N2 = N2 + N2_Step;
		End;
