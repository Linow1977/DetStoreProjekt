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
// FILNAVNET BYGGES AF STRATEGIEN SELV
//
// Samme filter køres på flere workspaces med hver sin opsætning af
// tidsrammer (5,10,60 - 10,20,60 - 5,30,120 - 5,10,120). Skrev de alle til
// samme filnavn, ville hver kørsel slette den forrige, uden varsel.
//
// Strategien aflæser derfor selv tidsrammerne med BarInterval og sætter dem
// ind i filnavnet sammen med kørselsmåneden:
//
//   RawSignalTest_2__5_10_60__2026_09.csv
//
// Alle tre tidsrammer skal med. To af opsætningerne (5,10,60 og 5,10,120)
// bruger samme tidsramme som filter-data, så kun filterets eget tal ville
// ikke kunne skelne dem fra hinanden.
//
// Datoen kommer fra computerens ur på kørselstidspunktet - altså hvornår
// backtesten blev kørt, ikke hvornår koden blev skrevet.
//
// Derfor bruges FileAppend i stedet for Print(File(...)): Print kræver et
// fast filnavn i anførselstegn og kan ikke bruge en variabel.
//
//
// VIGTIGT: Kør som almindelig backtest - IKKE via Optimize.
// VIGTIGT: CSV-filen skal være lukket i Excel, mens der køres.
// VIGTIGT: Chartet skal have mindst tre data-strømme, da data(3) aflæses.
}

Input:
	int    DataFilter_A( 2 ),
	string Mappe( "C:\Test\" ),
	string RawSignalNavn( "RawSignalTest_2" );

Var:
	int    Filter1( 0 ),
	int    Filter1_Forrige( 0 ),
	int    SignalBars( 0 ),
	string StartTekst( "" ),
	string KoerselsID( "" ),
	string FilNavn( "" );


//----- Engangsopsætning: byg kørsels-ID og filnavn, og start filen forfra -----//

	Once
		Begin

		// Kørsels-ID og filnavn er det samme, så data og filnavn altid passer sammen
		KoerselsID = RawSignalNavn
		           + "__"
		           + NumToStr( BarInterval of data(1), 0 ) + "_"
		           + NumToStr( BarInterval of data(2), 0 ) + "_"
		           + NumToStr( BarInterval of data(3), 0 )
		           + "__"
		           + FormatDate( "yyyy_MM", ComputerDateTime );

		FilNavn = Mappe + KoerselsID + ".csv";

		FileDelete( FilNavn );
		FileAppend( FilNavn, "RunID,N1,Starttid,AntalBars" + NewLine );

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
		FileAppend( FilNavn,
		            KoerselsID + ","
		          + "1" + ","
		          + StartTekst + ","
		          + NumToStr( SignalBars, 0 )
		          + NewLine );
		SignalBars = 0;
		End;

	Filter1_Forrige = Filter1;
