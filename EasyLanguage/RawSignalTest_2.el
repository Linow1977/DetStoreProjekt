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
// VIGTIGT: Kør som almindelig backtest - IKKE via Optimize.
// VIGTIGT: CSV-filen skal være lukket i Excel, mens der køres.
}

Input:
	int    DataFilter_A( 2 ),
	string RunID( "RawSignalTest_2" );

Var:
	int    Filter1( 0 ),
	int    Filter1_Forrige( 0 ),
	int    SignalBars( 0 ),
	string StartTekst( "" );


//----- Start forfra, så gentagne beregninger af chartet ikke dubler linjerne -----//

	Once
		Begin
		FileDelete( "C:\Test\RawSignalTest_2.csv" );
		Print( File ("C:\Test\RawSignalTest_2.csv"), "RunID,N1,Starttid,AntalBars" );
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
		Print( File ("C:\Test\RawSignalTest_2.csv"),
		       RunID, ",",
		       1:0:0, ",",
		       StartTekst, ",",
		       SignalBars:0:0 );
		SignalBars = 0;
		End;

	Filter1_Forrige = Filter1;
