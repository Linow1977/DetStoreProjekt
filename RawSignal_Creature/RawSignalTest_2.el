{
//***** RawSignalTest_2
// Råt signal: registrerer KUN hvornår filteret tænder, og hvor længe det er tændt.
//
// Filter: lukkekursen ligger under gårsdagens dagsluk.
//
// Filteret har ingen parametre, så der findes kun én variant. N1-kolonnen
// skrives alligevel (altid 1), så alle RawSignal-filer har samme format
// og kan læses af Python på samme måde.
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
// VIGTIGT: CSV-filen skal være lukket i Excel, mens der køres.
// VIGTIGT: Skift filnavnet i de to Print-kald nedenfor, hvis denne fil
//          bruges som udgangspunkt for en anden RawSignal-fil.
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
		FileDelete( "C:\RawSignal_2026_TS\RawSignalTest_2.csv" );
		Print( File("C:\RawSignal_2026_TS\RawSignalTest_2.csv"), "RunID,N1,Starttid,AntalBars" );
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
		Print( File("C:\RawSignal_2026_TS\RawSignalTest_2.csv"),
		       "RawSignalTest_2" + ","
		     + "1" + ","
		     + StartTekst + ","
		     + NumToStr( SignalBars, 0 ) );
		SignalBars = 0;
		End;

	Filter1_Forrige = Filter1;
