{
//***** @EdgeFinder_F5_SIGNAL
// "Volatility Filters" "Case 5"
// Registrerer KUN hvornår filteret tænder, og hvor længe det er tændt.
}

Input:
	int    Filter1_N1( 1 ),
	int    Filter1_N2( 1 ),
	int    DataFilter_A( 2 ),
	string RunID( "RUN0001" ),
	string ExportFile( "C:\Test\signals_test.csv" );

Var:
	bool   Filter1( False ),
	bool   Filter1_Forrige( False ),
	int    SignalBars( 0 ),
	string StartTekst( "" );


//----- Selve filteret -----//

	Filter1 = Range of data(DataFilter_A) > AvgTrueRange(Filter1_N1 * 5) of data(DataFilter_A);


//----- Signal-registrering -----//

	// TÆNDER
	If Filter1 = True and Filter1_Forrige = False Then
		Begin
		StartTekst = FormatDate( "yyyy-MM-dd", ELDateToDateTime( Date of data(DataFilter_A) ) )
		           + " "
		           + FormatTime( "HH:mm", ELTimeToDateTime( Time of data(DataFilter_A) ) );
		SignalBars = 1;
		End;

	// FORTSÆTTER
	If Filter1 = True and Filter1_Forrige = True Then
		SignalBars = SignalBars + 1;

	// SLUKKER — linjen skrives her
	If Filter1 = False and Filter1_Forrige = True Then
		Begin
		// EasyLanguage kræver et fast filnavn i File() - en variabel kan ikke bruges her.
		// Kørsler adskilles i stedet via RunID, der skrives som første kolonne i hver linje.
		Print( File ("C:\Test\signals_test.csv"),
		       RunID, ",",
		       Filter1_N1:0:0, ",",
		       Filter1_N2:0:0, ",",
		       StartTekst, ",",
		       SignalBars:0:0 );
		SignalBars = 0;
		End;

	Filter1_Forrige = Filter1;
