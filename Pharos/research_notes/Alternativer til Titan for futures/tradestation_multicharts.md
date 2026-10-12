# TradeStation / MultiCharts ecosystem: tools for strategy monitoring, incubation and strategy-portfolio management (futures)

> **Source access warning (read first).** Research date 2026-10-12. The network proxy refused connections (HTTP 403 on CONNECT) to every vendor and forum site that was tried: tradestation.com, help.tradestation.com, multicharts.com, multiwalk.net, adaptrade.com, trademaid.info, kjtradingsystems.com, strategyquant.com, buildalpha.com, nexusfi.com, elitetrader.com, bettersystemtrader.com, unger.academy, ungeracademy.com and algoadvantage.substack.com. **No vendor page could be opened directly.** Every finding below comes from search-engine excerpts of those pages. The URLs are the pages the excerpts came from. Treat prices and "current" status as "per the search excerpt, page date often unknown" unless stated otherwise. Where an excerpt is vendor marketing, this is marked **[vendor claim]**.

## Q1: Which add-ons, apps or standalone tools in the TradeStation/MultiCharts ecosystem cover monitoring live vs. backtest, incubation/paper tracking, strategy rotation on/off, or strategy-portfolio management?

### Takeaway
No single TS/MC-ecosystem product does what Titan does: daily P&L for every strategy (live and incubating), then a monthly live/incubation decision, sizing from worst day or drawdown, and correlation caps. The pieces exist in separate tools:
- **MultiWalk/MultiWalk Trader:** walk-forward, hidden-OOS incubation pass/fail, live-strategy and reoptimization tracking, rollover alerts.
- **MultiCharts Portfolio Trader:** portfolio backtest and auto-trading with a programmable portfolio money-management signal that can rotate instruments.
- **TradeStation Portfolio Maestro:** portfolio backtest only.
- **Analyzers fed by trade lists:** Portfolio Analyst, QuantAnalyzer, Adaptrade MSA and Build Alpha cover correlation, live vs. backtest, Monte Carlo and position sizing.
- **TITAN X:** no strategy-portfolio features at all.

### Cited Findings

**A. TradeStation-native**

- **Portfolio Maestro (TradeStation)**
  - TradeStation help: "a back-testing tool that lets you evaluate the performance of a group of strategies applied to a basket of symbols." — [TS help 9.1](https://help.tradestation.com/09_01/tsportfolio/portfolios/about_portfolios.htm)
  - It "is installed and runs separately from the TradeStation platform." — [TradeStation Lesson 6 PDF](https://cdn.tradestation.com/wp-content/uploads/2016/09/04150222/Lesson-6-Strategy-Testing-Optimization-and-Automation.pdf)
  - TS 10 help calls it an "optional platform feature (for an additional monthly subscription fee) that runs outside of the TradeStation platform." — [TS 10 help, Portfolio Maestro](https://help.tradestation.com/10_00/eng/TradeStationHelp/default/portfolio_maestro.htm)
  - No source found says it trades live, monitors live strategies, or tracks incubation. All descriptions call it backtesting. (Help page not openable. This rests on search excerpts.)

- **TradeStation Strategy Performance Report / Strategy Equity indicator.** These are built in.
  - The Performance Report covers a strategy's backtest results. — [TS help: Review the Strategy's Performance](https://help.tradestation.com/10_00/eng/tradestationhelp/st_testing/review_strategy%20performance.htm)
  - The Strategy Equity indicator "only returns results when applied to a chart containing a strategy." — [TS help: Strategy Equity indicator](https://help.tradestation.com/10_00/eng/tradestationhelp/elanalysis/indicator/strategy_equity_indicator_.htm)
  - Neither is a cross-strategy monitor.

- **TITAN X (TradeStation, 2026).** Unrelated to Unger's Titan.
  - Marketed as a next-generation desktop platform for Windows/Mac for active options and futures traders.
  - Features listed: "group positions by strategy", "monitor exposure with real-time alerts", margin/risk review before order entry, multi-leg options tickets and a redesigned Matrix ladder. **[vendor claim]** — [TradeStation TITAN X page](https://www.tradestation.com/platforms-and-tools/titanx/); [TradeStation Insights, 2026-04-10](https://www.tradestation.com/insights/2026/04/10/titan-x-options-trading-platform-bull-call-spread-guide/); [BusinessWire, 2026-01-05](https://www.businesswire.com/news/home/20260105805579/en)
  - In TITAN X, "group by strategy" refers to options position grouping (multi-leg spreads), not automated-strategy portfolios. This is an inference from the context of the excerpts.
  - TradeStation's own TITAN X page says "TradeStation Desktop continues to support automation and EasyLanguage-based strategies." — [TradeStation TITAN X page](https://www.tradestation.com/platforms-and-tools/titanx/)
  - A third-party review says TITAN X "does not run EasyLanguage strategy automation; that still lives on the older Desktop app." — [PickMyTrade review 2026](https://blog.pickmytrade.io/tradestation-review-2026-best-broker-for-automated-traders/)
  - StockBrokers.com says backtesting and Portfolio Maestro "still live in legacy tools", so users must switch windows out of TITAN X. — [StockBrokers TITAN X review](https://www.stockbrokers.com/review/tradestation/titan-x)
  - TradeStation's roadmap mentions future "analytics, grouping … automation". This is forward-looking marketing only. — [search summary of TradeStation TITAN X pages](https://www.tradestation.com/titan-x/)

**B. MultiCharts-native**

- **MultiCharts Portfolio Trader**
  - Runs a portfolio backtest, then forward testing on real-time data, then auto trading. A separate broker profile can be chosen per strategy. — [MC wiki: Understanding Portfolio Trader](https://www.multicharts.com/trading-software/index.php?title=Understanding_Portfolio_Trader); [MC features: Portfolio trading](https://www.multicharts.com/features/portfolio-trading/)
  - The **Forward Performance Testing** tab "contains the main information on strategy performance for every instrument", with a Close Position button per instrument. — [MC wiki](https://www.multicharts.com/trading-software/index.php?title=Understanding_Portfolio_Trader)
  - The Portfolio Performance Report "is recalculated automatically in the Forward Testing and Auto Trading modes". It includes a Breakdown by Symbols section. — [MC wiki: Portfolio Performance Report](https://www.multicharts.com/trading-software/index.php?title=Portfolio_Performance_Report)
  - Symbols can be grouped, and each group can have its own strategy. Per-strategy results come from that grouping. — [same MC wiki pages, via search excerpt](https://www.multicharts.com/trading-software/index.php?title=Understanding_Portfolio_Trader)
  - The **Portfolio Money Management Signal (PMMS)** is calculated on every calculation step after all signals. It can select instruments, size positions, force exits and allocate equity.
  - Wiki examples include **rotation** ("trading the N best instruments at once"), index-based selection and pair trading. — [MC wiki: Portfolio Trader](https://Multicharts.com/trading-software/index.php/Portfolio_Trader)
  - Futures margin: "Absolute Margin value is taken from the symbol settings (only for futures)". The number of contracts is corrected according to Money Management and margin. — [MC forum](https://www.multicharts.com/discussion/viewtopic.php?p=140645)
  - Limitation (2014 thread, staff): passing per-instrument performance into the money-management signal "is not a trivial task and it requires significant changes to the components." No newer confirmation either way was found. — [MC forum: Tracking strategy performance in Portfolio Trader](https://www.multicharts.com/discussion/viewtopic.php?t=47452)
  - The Portfolio Trader manual found is dated 2014-04-30. — [Portfolio Trader Manual PDF](https://www.Multicharts.com/trading-software/images/1/16/Portfolio_Trader_Manual.pdf)

**C. Third-party tools tied to TradeStation/MultiCharts**

- **MultiWalk / MultiWalk Pro / MultiWalk Trader (multiwalk.net)**
  - A TradeStation-based application for testing ideas across many markets and bar intervals with optimization and walk-forward. — [multiwalk.net](https://multiwalk.net/)
  - It was "exclusively designed for Kevin Davey's Strategy Factory community". — [multiwalk.net](https://multiwalk.net/)
  - The **Trader** module manages multiple strategies as a portfolio and runs analysis projects as a batch or as a whole portfolio "to track performance and reoptimization dates". **[vendor claim]** — [multiwalk.net](https://multiwalk.net/)
  - Its consolidated reports "show which strategies are due for reoptimization", with columns Reopt Date and Days To Reopt.
  - The knowledge base describes "a single weekly-run Trader project used to monitor live strategies and their performance". — [MultiWalk KB: Monitoring and Re-optimizing Walkforward Strategies](https://multiwalk.net/knowledge-base/monitoring-reoptimizing-walkforward-strategies/)
  - A MultiWalk Trader Quick Start Guide exists. Its contents were not readable. — [MWT Quick Start](https://multiwalk.net/knowledge-base/mwt-quick-start-guide/)
  - **Incubation:** an OOS period "must be hidden from all reports until you are ready run the trading strategy on the unseen OOS data". Once it is unhidden, "There is no going back … It either passed or failed incubation". Re-editing after poor results "burns" that OOS period. — [MultiWalk KB: Incubation period in MultiWalk](https://multiwalk.net/knowledge-base/incubation-period-in-multiwalk/)
  - This is **back-incubation on historical data**, not live paper tracking. That is an inference from the wording quoted above.
  - **MultiWalk Rollover Monitor:** a separate app that sends pop-up, external-program or email notifications.
    - Triggers: a TradeStation rollover, or N days before rollover, first notice or expiration.
    - Contract dates update automatically from TradeStation servers, checked every 2 h by default.
    - Caveat: alerts wait until TradeStation's continuous-contract data changes.
    - — [MultiWalk KB: Rollover Monitor](https://multiwalk.net/knowledge-base/multiwalk-rollover-monitor/)
  - **MultiCharts / IB:** a KB article covers "Using MultiWalk with TradeStation, MultiCharts and Interactive Brokers". Pro has "cross-platform functions for TradeStation and MultiCharts". — [MultiWalk KB](https://multiwalk.net/knowledge-base/using-multiwalk-and-multicharts/)
  - **Contracts:** a KB page covers "Specifying Multiple Contracts or Shares". — [MultiWalk KB](https://multiwalk.net/knowledge-base/specifiying-multiple-contracts-or-shares/)

- **Kevin Davey / KJ Trading Systems: Strategy Factory**
  - The workshop includes "Strategy Factory Step 6 – Incubation" (with "Basics of Incubation", 38:08) and "Step 8 – Live Trading", with a lecture "Monitoring Live Strategies". — [Teachable course outline](https://ultimate-algo-trading.teachable.com/courses/1066921/lectures/22714843); [Strategy Factory Workshop](https://ultimate-algo-trading.teachable.com/p/strategy-factory-workshop)
  - The **Strategy Factory Professional Kit** includes "a monthly reoptimization workbook and spreadsheets for tracking walkforward reoptimizations". These are spreadsheets, not software. — [kjtradingsystems.com Professional Trader Kit](https://kjtradingsystems.com/professional-trader-kit.html)
  - Davey's BST Live episode on detecting failing strategies covers probability cones, statistical process control and ranges of future performance, plus what to do when a strategy over-performs. — [Better System Trader ep. 170 (libsyn)](https://sites.libsyn.com/66295/170-how-to-detect-when-a-trading-strategy-is-failing-kevin-davey)
  - Davey has a page "Equity Curve Trading Myths Analyzed". Its conclusion could not be read (blocked). — [kjtradingsystems.com](https://kjtradingsystems.com/equity-curve-trading.html)
  - His "Algo Trader Toolkit" contains chapters "Myths and Facts of Equity Curve Trading" and "Equity Curve Analysis: A Fool's Path?". — [Scribd ToC](https://www.scribd.com/document/352693109/Algo-Trader-Toolkit)

- **Portfolio Analyst / Portfolio Analyst Professional (Trademaid)**
  - Input is "standard Tradestation/Multicharts XML format, or with a Strategy inserted on your chart". Output is PDF, HTML and CSV/Excel trade lists. — [trademaid.info/pa.html](https://trademaid.info/pa.html)
  - "PA also has correlation of bad days, weeks, months & contribution of all systems to total max draw down. Portfolio Intra day draw down also shown." **[vendor claim]** — [trademaid.info](https://trademaid.info/pa.html)
  - The Pro version adds automatic portfolio selection, Monte Carlo, criteria-based system selection and "very basic money management". — [trademaid.info](https://trademaid.info/pa.html)
  - One substack author building a small-account futures portfolio uses Portfolio Analyst to test combinations and says it "works well with TradeStation exports". — [algorithmicguys substack, 2026](https://algorithmicguys.substack.com/p/how-i-created-a-small-futures-portfolio)

- **Adaptrade Market System Analyzer (MSA)**
  - Imports a strategy's trade history, rebuilds the equity curve under a chosen position-sizing method, and expresses statistics as percent of account equity. — [Adaptrade MSA](https://www.adaptrade.com/MSA/index.htm); [MSA perf stats](https://adaptrade.com/MSA/perfstats.htm)
  - Offers "15 different position sizing methods" on one page and 12 on another, so the count likely depends on version. — [MSA possizing](https://www.adaptrade.com/MSA/possizing.htm); [MSA optim](https://www.adaptrade.com/MSA/optim.htm)
  - Methods include fixed fractional and fixed ratio. — [fixfrac](https://www.adaptrade.com/MSA/fixfrac.htm); [fixratio](https://www.adaptrade.com/MSA/fixratio.htm)
  - Position-sizing optimization maximizes a chosen metric under an optional drawdown constraint, on the actual trade sequence or by Monte Carlo. — [MSA optim](https://www.adaptrade.com/MSA/optim.htm)
  - A "RealTime PS" video exists, suggesting a real-time position-sizing feature. Its details could not be read. — [Adaptrade video](https://www.adaptrade.com/videos/RealTime-PS-video.htm)

- **StrategyQuant QuantAnalyzer** (not TS-specific, but imports TS reports)
  - The "Compare results" module bulk-compares live or platform results ("TradeStation, MetaTrader, MyFxbook…") in folder 1 against StrategyQuant backtests (.sqx/.str) in folder 2. Files are matched by filename. — [QA docs: comparing results](https://strategyquant.com/doc/quantanalyzer/comparing-results/); [SQ blog](https://strategyquant.com/blog/how-to-compare-live-results-with-backtests-with-quant-analyzer/)
  - **Limitation:** the backtest side must be a StrategyQuant/AlgoWizard file. There is no evidence it compares a TS live report with a TS backtest report directly. That is an inference from the folder description.
  - **Portfolio Master** computes strategy correlation by daily, weekly or monthly P&L (daily P&L is the default) and can filter portfolios by correlation threshold. — [QA: portfolio correlation explained](https://strategyquant.com/doc/quantanalyzer/portfolio-correlation-explained/); [QA advanced metrics](https://strategyquant.com/quantanalyzer/extensive-reports/)
  - It also has "Money Management and Equity control" (equity-curve control). The free version shows these for only 30% of trades. — [QA pricing](https://strategyquant.com/quantanalyzer/pricing/)

- **Build Alpha** (strategy generator; exports EasyLanguage and PowerLanguage)
  - The homepage frames a "portfolio governance" layer for "deciding when to size down, replace, or retire strategies". Strategies are "evaluated against historical limits, regime behavior, and portfolio-level risk impact". **[vendor claim]** — [buildalpha.com](https://www.buildalpha.com/)
  - Portfolio mode can "combine them, analyze asset allocation methods, optimize rebalancing frequencies". — [Build Alpha portfolio backtest](https://www.buildalpha.com/portfolio-backtest-trading/)
  - Generates EasyLanguage and PowerLanguage code. — [softwaresuggest listing](https://www.softwaresuggest.com/us/buildalpha)
  - No source describes Build Alpha ingesting live TS/MC fills.

- **Equity-curve trading (DIY in EasyLanguage/PowerLanguage)**
  - The standard approach turns a strategy off when its own equity curve falls below a moving average.
  - Overfitting warning: the lookback length "could be overoptimized by varying the value of N". — [EasyLanguage Mastery: Equity Curve Trading](https://easylanguagemastery.com/equity-curve-trading/); [EL Mastery: Equity Curve Indicators](https://easylanguagemastery.com/indicators/equity-curve-indicators/)
  - TradeStation's own guide: NetProfit gives closed-trade equity per bar. A `TradeOK` gating variable controls entries. — [Learning EasyLanguage Strategies PDF](https://cdn.tradestation.com/uploads/Learning-EasyLanguage-Strategies.pdf)
  - Note: in a single TS chart, once the strategy stops trading, its own equity curve stops updating. A "shadow" (simulated) equity is needed to switch back on. This is an inference. No verified ready-made TS script was found.

- **Journals (not strategy-level)**
  - TradesViz imports TradeStation trades via CSV (Trade Blotter) or API sync. It is a trade journal, not a strategy incubation tool. — [TradesViz TradeStation](https://www.tradesviz.com/brokers/TradeStation)

### Inferences
- Tools split into two groups:
  - **Connected to the platform:** MultiWalk (drives TradeStation), MC Portfolio Trader (runs inside MultiCharts) and Portfolio Maestro (TS, separate app).
  - **Trade-list importers:** Portfolio Analyst, MSA, QuantAnalyzer and Build Alpha.
- None of the importers pulls live fills automatically from TS/MC on a schedule, based on the excerpts.
- Incubating/paper strategies only appear in any of these tools if the user runs them somewhere (a TS sim account, MC forward testing, or a chart with orders off) and exports the trade lists.

### Gaps
- No vendor page could be opened directly (proxy 403). TITAN X's current automation status, MSA's current version and the exact contents of the MultiWalk Trader module are therefore unverified beyond excerpts.
- No product was found in the TradeStation TradingApp Store that monitors strategy portfolios. The search found nothing, which is weak evidence of absence.
- ungeracademy.com / unger.academy were blocked. Whether Titan itself is sold or licensable to outsiders was not checked in this file.

## Q2: For each tool: what it does exactly, how data gets in, futures handling, price, maintained as of 2026, user feedback

### Takeaway
- **Most actively maintained, futures-native and cheapest:** MultiWalk (lifetime license, but only for Strategy Factory alumni) and Portfolio Maestro (TradeStation, monthly or free with an account).
- **Most flexible for rule-based rotation:** MultiCharts Portfolio Trader via PMMS, but it requires coding, and users complain that chart and portfolio trades differ.
- **Trade-list analyzers:** Portfolio Analyst, MSA and QuantAnalyzer are cheap. Maintenance status ranges from active (PA build 2025-11, QA 4.9.4) to possibly stagnant (MSA).

### Cited Findings

**Portfolio Maestro (TradeStation)**

| Item | Finding |
|---|---|
| Function | Portfolio backtest only. No live monitoring or incubation found. |
| Data in | Runs separately and uses TradeStation data (see Q1). |
| Futures | Not specified in the excerpts. |
| Price | $59.95/month on the TS pricing page — [TradeStation pricing](https://www.tradestation.com/pricing/). A service-fee table (~1 year old) lists it **FREE** with an active brokerage account and $59.95/month without — [TS service fees](https://www.tradestation.com/pricing/service-fees/). **Conflict between the two TS pages. Verify.** |
| Status | Help pages exist for 9.1, 9.5 and 10.0 — [TS help 9.5](https://help.tradestation.com/09_05/eng/tsportfolio/portfolios/about_portfolios.htm). StockBrokers 2026 says it is still in "legacy tools" alongside TITAN X — [StockBrokers](https://www.stockbrokers.com/review/tradestation/titan-x). No discontinuation notice found. |

User feedback on Portfolio Maestro:
- "misses certain trades for some unknown reason" while the same strategy showed none missing in MultiCharts. — [NexusFi](https://nexusfi.com/showthread.php?p=815439)
- On a ~400-stock universe "only about 200 of them are generating trades". — [NexusFi](https://nexusfi.com/showthread.php?p=816185)
- 2020: "conflicts and not all transactions appear". — [futures.io](https://futures.io/trading_member/42990-eiwoh.html)
- Unverified forum claim that it was a third-party product TradeStation purchased. — [NexusFi](https://nexusfi.com/showthread.php?p=815439)

**MultiCharts Portfolio Trader**

| Item | Finding |
|---|---|
| Function | Portfolio backtest, forward test and live auto-trading. Programmable PMMS for selection, rotation and sizing. Per-instrument forward-performance tab (see Q1). |
| Data in | Native to MultiCharts. |
| Futures | Uses futures margin from symbol settings. Contracts are adjusted to money management and margin — [MC forum](https://www.multicharts.com/discussion/viewtopic.php?p=140645). Differences can appear around rollover because continuous contracts are stitched — [MC wiki: Chart vs Portfolio backtesting](https://www.multicharts.com/trading-software/index.php/Chart_Backtesting_VS_Portfolio_Backtesting). |
| Price | **Unresolved.** See the price bullets below the table. The "~$499 add-on" figure was not confirmed by any source. |
| Status | MC wiki and forum active. The manual is 2014. |

Portfolio Trader price, as found:
- QuantVPS places Portfolio Trader in the **Advanced Edition**: $1,440/yr, "currently discounted to $999". Advanced Lifetime is only available in an "Ultimate Bundle" (2 licenses, $3,998, discounted to $1,999). Standard Lifetime is $1,497. — [QuantVPS: MultiCharts explained](https://www.quantvps.com/blog/multicharts-explained); [Warrior Trading](https://www.warriortrading.com/multicharts-review/)
- **Contradicted by** a reseller page (~412 days old): "you don't have to buy or lease additional functionality like the Portfolio Trader". — [ABC Trading Group](https://www.abctradinggroup.com/multicharts/)
- The official MC pricing page was blocked.

User feedback on Portfolio Trader:
- 2023 thread "So Frustrated. Portfolio Trader, Different Trades": identical code gives different trades in the portfolio, and staff attributed it to money-management filtering. — [MC forum](https://www.multicharts.com/discussion/viewtopic.php?p=140645)
- Official wiki: chart and portfolio backtests are "not supposed to match". Intra-bar order generation, Bar Magnifier and extended backtesting are unavailable in Portfolio. — [MC wiki](https://www.multicharts.com/trading-software/index.php/Chart_Backtesting_VS_Portfolio_Backtesting)
- The "optimize by Sharpe ratio" option is poorly documented, per a user. — [MC forum](https://www.multicharts.com/discussion/viewtopic.php?p=139605)

**MultiWalk / MultiWalk Pro / MultiWalk Trader / Rollover Monitor**

| Item | Finding |
|---|---|
| Function | Walk-forward across many markets, hidden-OOS incubation pass/fail, Trader portfolio projects tracking performance and reoptimization dates (see Q1). |
| Data in | Drives TradeStation directly. Pro adds TS/MC cross-platform functions. |
| Futures | Multi-contract support (KB). Rollover Monitor reads contract dates from TradeStation servers. |
| Price | MultiWalk $1,295; MultiWalk Pro $1,895; upgrade $600; lifetime license and updates, no subscription. Rollover Monitor $249 (requires a MultiWalk license). — [MultiWalk Purchasing and Pricing](https://multiwalk.net/purchasing-and-pricing/) |
| Availability | "currently only available to those who have taken" Davey's Strategy Factory Workshop — [multiwalk.net](https://multiwalk.net/). A two-week trial of the non-Strategy-Factory Pro features is offered — [Downloads](https://multiwalk.net/downloads/). |
| Status | A change log exists — [change log](https://multiwalk.net/multiwalk-change-log/). The latest version and date could not be read (blocked). |
| Feedback | A testimonials page exists (vendor-curated) — [testimonials](https://multiwalk.net/testimonials/). No independent reviews found. |

**Kevin Davey materials**
- Spreadsheets and a monthly reoptimization workbook come in the Professional Kit (see Q1). Price was not readable. — [kjtradingsystems.com](https://kjtradingsystems.com/professional-trader-kit.html)
- Davey's approach per an Interactive Brokers Campus summary: "walk-forward and Monte Carlo methods, live incubation, and proactive portfolio management". — [IBKR Campus](https://www.interactivebrokers.com/campus/?p=249402)
- A Strategy Factory description on NexusFi: incubation means "you watch the system for a period of time to verify that it's performance is what you expect". A large gap from backtest "is probably the best warning you could get". — [NexusFi](https://nexusfi.com/showthread.php?p=163768)

**Portfolio Analyst (Trademaid)**
- Data in: TS/MC XML or a strategy on a chart (see Q1).
- Futures: aimed at futures systems, per the search summary.
- Price: Portfolio Analyst Professional $400 (page date unknown).
- Latest build: 2025-11-28. **Maintained into late 2025.**
- — [trademaid.info](https://trademaid.info/pa.html)
- Feedback: a positive mention in a 2026 substack. — [algorithmicguys](https://algorithmicguys.substack.com/p/how-i-created-a-small-futures-portfolio)

**Adaptrade MSA**
- Price: a NexusFi listing says "$349 lifetime license". — [NexusFi Adaptrade listing](https://nexusfi.com/d/platforms/adaptrade-software)
- Versions: user guides exist for v3 and v4 — [Adaptrade support](https://www.adaptrade.com/support.htm). Videos are based on v3.2.0 — [Adaptrade videos](https://www.adaptrade.com/videos/index.htm).
- A 30-day trial is available.
- The S&C vendor listing was "not updated by the vendor since 09/20/21". — [S&C vendor listing](https://technical.traders.com/Products/company.asp?act=100923)
- **Maintenance as of 2026: unclear, possibly low.**

**QuantAnalyzer (StrategyQuant)**
- Latest build: 4.9.4. — [QA download](https://strategyquant.com/de/quantanalyzer/herunterladen-2/)
- Free-version limits: money management and equity control on 30% of trades; Portfolio Master max 4 strategies; Compare results only the first 50 trades. — [QA pricing](https://strategyquant.com/quantanalyzer/pricing/)
- Pro price: the excerpt rendered it as "$2900 monthly subscription". That figure is probably a formatting artifact of "$29.00/month". **Unverified. Check the page.**
- Symbol mapping: imported broker symbols may need defining in PredefinedSymbols.csv. — [SQ blog](https://strategyquant.com/blog/real-trading-compare-live-strategy-results-backtest/)
- In a worked example, a TS backtest vs. an SQ backtest of the same strategy showed some trade differences but close equity curves. — [SQ blog](https://strategyquant.com/blog/real-trading-compare-live-strategy-results-backtest/)

**Build Alpha**
- Price was not found (site blocked).
- Forum users who trade on TradeStation praise the generated code as a learning aid. — [NexusFi](https://nexusfi.com/showthread.php?p=911156)
- No live-monitoring feature is documented.

**General live-vs-sim practice on TradeStation (forums)**
- One NexusFi member says SIM is "good for order testing, etc., but not for P/L evaluation".
- Another suggests forward-testing in the live account with order generation off, so orders only display in TradeManager. — [futures.io](https://futures.io/tradestation/46604-sim-live-trading-tradestation.html)
- Limit-order fill settings ("fill only when price exceeded" vs. "touched") cause backtest-vs-live mismatches. — [NexusFi](https://nexusfi.com/showthread.php?p=441755)

### Inferences
- Futures specifics differ by tool:
  - **MultiWalk is the most futures-aware**, with rollover alerts and contract dates taken from TS servers.
  - **MC Portfolio Trader** handles margin and contract counts.
  - Trade-list tools only see whatever P&L the export contains. Tick values and micro contracts are only as correct as the TS/MC symbol settings that produced the export.
- No explicit micro-contract handling is documented in any tool found.
- On the TS side, the community advice "SIM is not for P/L evaluation" matters for Pharos. Paper P&L for incubating strategies from a TS sim account may be biased, especially for limit orders.

### Gaps
- Whether TradeStation sim/paper accounts are reliable for incubation P&L in 2026 was not verified.
- MC Portfolio Trader's official price and licensing on MultiCharts 15 were not verified (pricing page blocked; sources conflict).
- Current MultiWalk version/date, current MSA version and price, Build Alpha price, and the Kevin Davey kit price were not found.
- No independent (non-vendor) reviews of MultiWalk Trader or Portfolio Analyst were found.
- Explicit handling of micro contracts (MES/MNQ) is not documented for any tool found.

## Q3: Which come closest to Titan's monthly "live vs. incubation" selection?

### Takeaway
**MultiWalk Trader** comes closest in spirit, with walk-forward reoptimization dates, weekly portfolio monitoring and a formal incubation pass/fail. But its incubation is a one-time hidden-OOS test, not an ongoing monthly live/incubation status per strategy. It is also restricted to Strategy Factory alumni and TradeStation-centred.

**MultiCharts Portfolio Trader with a custom PMMS** is the only platform-native component that could switch strategies on and off by rule during live trading. MC staff indicated in 2014 that feeding per-strategy performance into the PMMS was hard. Nothing found does Titan's monthly selection for a mixed live/paper book.

### Cited Findings
- MultiWalk Trader tracks "performance and reoptimization dates". A weekly-run Trader project monitors live strategies. — [multiwalk.net](https://multiwalk.net/); [MultiWalk KB](https://multiwalk.net/knowledge-base/monitoring-reoptimizing-walkforward-strategies/)
- MultiWalk incubation is one-shot: "It either passed or failed incubation." — [MultiWalk KB](https://multiwalk.net/knowledge-base/incubation-period-in-multiwalk/)
- MC PMMS supports rotation ("trading the N best instruments at once"), sizing and forced exits. — [MC wiki](https://Multicharts.com/trading-software/index.php/Portfolio_Trader)
- MC staff, 2014: per-instrument performance in the PMMS "is not a trivial task". — [MC forum](https://www.multicharts.com/discussion/viewtopic.php?t=47452)
- Portfolio Analyst Pro has "automatic portfolio selection" plus correlation of bad days, weeks and months. This is offline, on exported trade lists. — [trademaid.info](https://trademaid.info/pa.html)
- QuantAnalyzer correlates strategies by daily P&L, filters portfolios by correlation threshold, and compares live vs. backtest in bulk. — [QA docs](https://strategyquant.com/doc/quantanalyzer/portfolio-correlation-explained/); [QA compare](https://strategyquant.com/doc/quantanalyzer/comparing-results/)
- Build Alpha markets "portfolio governance" for deciding when to "size down, replace, or retire strategies". **[vendor claim, no independent verification]** — [buildalpha.com](https://www.buildalpha.com/)
- MSA covers position sizing with a drawdown constraint and Monte Carlo, for single trade histories. — [MSA optim](https://www.adaptrade.com/MSA/optim.htm)
- A general search for "strategy incubation tracker" software found no dedicated product with a live-sim-to-live rotation workflow or a monthly review cadence. — [search results incl. StrategyQuant, QuantConnect, Build Alpha](https://www.buildalpha.com/algorithmic-futures-trading-software/)

### Inferences
- **Coverage of Titan's components across the ecosystem:**

| Titan component | Who covers it (partly) | Gap |
|---|---|---|
| Daily P&L for all strategies incl. incubating | MC Portfolio Trader forward test (MC only); manual export into PA or QA | No automatic DB feed; TS sim P&L reliability questioned |
| Monthly live/incubation selection | None directly; PA Pro "automatic portfolio selection" (offline); MC PMMS (custom code) | Nothing implements state-per-strategy with monthly re-evaluation |
| Sizing from worst day / drawdown | MSA (single strategy, drawdown constraint); MC PMMS (custom) | Not portfolio-wide with worst-day logic out of the box |
| Correlation caps | QuantAnalyzer (daily P&L correlation, threshold filter); Portfolio Analyst (bad-day correlation) | Offline analysis, not enforced live |
| Alerts | MultiWalk Rollover Monitor (rollovers only); TITAN X exposure alerts (account-level) | No strategy-degradation alerts found |

- For Pharos, this supports building the Titan-like selection layer in-house on PostgreSQL. The candidate inputs are:
  - TS/MC trade-list or XML exports, which are what PA, MSA and QA all consume. The XML is the de facto interchange format.
  - Optionally, MultiWalk for walk-forward and rollover handling on the TS side.
  - Optionally, MC Portfolio Trader as the later execution layer for prop-firm accounts.
- TITAN X is not relevant to strategy-portfolio monitoring as of Oct 2026. It is a discretionary/options-oriented front end, and EasyLanguage automation stays on TradeStation Desktop (per reviews).

### Gaps
- Whether MultiWalk Trader can mark strategies as "live" vs. "incubating" and track forward paper P&L. Its Quick Start Guide could not be read.
- Whether Portfolio Analyst's "automatic portfolio selection" can run on a rolling monthly basis.
- Whether any TradeStation TradingApp Store app offers strategy-level monitoring. None was found, but the store was not directly searchable.
- Kevin Davey's actual monthly go-live/turn-off rules. The podcast page and his site were blocked, and the libsyn episode summary gives topics only.
