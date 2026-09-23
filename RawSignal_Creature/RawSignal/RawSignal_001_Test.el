{
//***** RawSignal_001_Test
// Testfil til RawSignal-Creature-automationen. Dækker typen: INGEN PARAMETRE.
//
// Filter: lukkekursen ligger under gårsdagens dagsluk.
//
// Filteret har ingen parametre, så der findes kun én variant. N1-kolonnen
// skrives alligevel (altid 1), så alle RawSignal-filer har samme format
// og kan læses af Python på samme måde.
//
//
// FILNUMMERET ER FORELØBIGT
//
// "001" er ikke et rigtigt filter_case_id. Filen er bygget uden adgang til
// TradingDB, ud fra en formel der er dokumenteret i BESLUTNINGSLOG_2026-09-18.
// Når databasen er tilgængelig, skal nummeret erstattes med det rigtige
// filter_case_id, og formlen bekræftes mod filter_case.filtere.
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
// FileAppend bruges IKKE. Print(File(...)) er hurtigere, fordi filen
// holdes åben hele kørslen i stedet for at blive åbnet og lukket for
// hver skrevet linje, som FileAppend gør.
//
//
// VIGTIGT: Kør som almindelig backtest - IKKE via Optimize.
// VIGTIGT: CSV-filen skal være lukket i Excel, mens der køres.
// VIGTIGT: Max Bars Back - filteret ser kun én dag tilbage (CloseD(1)),
//          så Auto Detect eller en lav værdi er nok.
}

Input:
	int    DataFilter_A( 2 );

Var:
	int    Filter1( 0 ),
	int    Filter1_Forrige( 0 ),
	int    SignalBars( 0 ),
	string StartTekst( "" );


//----- Engangsopsætning: nulstil filen og skriv overskriftsrække -----//

	Once
		Begin
		FileDelete( "C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal_001_Test.csv" );
		Print( File("C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal_001_Test.csv"), "RunID,N1,Starttid,AntalBars" );
		End;


//----- Selve filteret -----//

	If ( Close of data(DataFilter_A) - CloseD(1) ) < 0 Then
		Filter1 = 1
	Else
		Filter1 = 0;


//----- Signal-registrering -----//

	// TÆNDER
	If Filter1 = 1 and Filter1_Forrige = 0 Then
		Begin
		StartTekst = FormatDate( "yyyy-MM-dd", ELDateToDateTime( Date of data(DataFilter_A) ) )
		           + " "
		           + FormatTime( "HH:mm", ELTimeToDateTime( Time of data(DataFilter_A) ) );
		SignalBars = 1;
		End;

	// FORTSÆTTER
	If Filter1 = 1 and Filter1_Forrige = 1 Then
		SignalBars = SignalBars + 1;

	// SLUKKER — linjen skrives her
	If Filter1 = 0 and Filter1_Forrige = 1 Then
		Begin
		Print( File("C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal_001_Test.csv"),
		       "RawSignal_001_Test" + ","
		     + "1" + ","
		     + StartTekst + ","
		     + NumToStr( SignalBars, 0 ) );
		SignalBars = 0;
		End;

	Filter1_Forrige = Filter1;
