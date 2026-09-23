{
//***** RawSignal126
// Råt signal: registrerer KUN hvornår filteret tænder, og hvor længe det er tændt.
//
// Kilde: TradingDB, tabellen filter_case, filter_case_id = 126
//
// Filter (formlen fra databasen, uændret):
//   close of data(DataFilter_A) > OpenD(0);
//
// altså: lukkekursen ligger over dagens åbningskurs.
//
// Filteret bruger ingen parametre, så der findes kun én variant. N1-kolonnen
// skrives alligevel (altid 1), så alle RawSignal-filer har samme format
// og kan læses af Python på samme måde.
//
//
// VIGTIGT: Kør som almindelig backtest - IKKE via Optimize.
// VIGTIGT: CSV-filen skal være lukket i Excel, mens der køres.
// VIGTIGT: Max Bars Back - filteret ser kun på dagens egen åbningskurs,
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
		FileDelete( "C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal126.csv" );
		Print( File("C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal126.csv"), "RunID,N1,Starttid,AntalBars" );
		End;


//----- Selve filteret - formlen fra databasen, uændret -----//

	If close of data(DataFilter_A) > OpenD(0) Then
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
		Print( File("C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal126.csv"),
		       "RawSignal126" + ","
		     + "1" + ","
		     + StartTekst + ","
		     + NumToStr( SignalBars, 0 ) );
		SignalBars = 0;
		End;

	Filter1_Forrige = Filter1;
