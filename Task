##RawSignal Creature process
Hent Filter_Case i TradingDB
   Køre .Skill der omskriver til RawSignal
      Verificer i TS   (fejler verificeringen, læs fejlen, tjek koden, notere fejlen/udfordringen, forsæt, vi samler alle fejl op senere ) 
         Opret i TradingDB journal. notere vis noget er off, udfordringer/fejl noget der kræver særlig opmærksomhed.

Lav Rå-Signal analyse

##EdgeFinder process ( Event Studiy, ikke helt udformet) 
Læs database journal, hviken Case der skal testes, hvilke parameter er gældende.
   Gå til TradeStation, load WorkSpace, sæt instillinger.
      Load RawSignal.
         Hent Backtest data i Folder, Læs og kontroler for fejl (ved fejl, stop process og meld fejl) gem i ny folder med nyt navn ( RawSignal(Number_WorkSpace_RunDate) )
            Analysere Event Studiy, Journalfør, (Passed/Failed)


##EdgeCruncher process (ikke helt udformet)
ikke helt 


Når hele processen er lavet og virker til Tradestation (TS) skal den også laves til Multicharts (MC)
