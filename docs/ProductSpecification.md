# StockEdge MVP Product Specification

Status: Working draft

This document defines the first product version that StockEdge should deliver. It is intentionally narrower than the long-term vision so that the application can become reliable before more features are added.

## Product summary

StockEdge is a research assistant for long-term Indian-equity investors. A user enters a supported NSE stock symbol, and StockEdge compares the company with its industry peers using fundamental and valuation data.

The product explains how the score was produced. It is a starting point for research, not an automated trading system or a guarantee of investment returns.

## Target user

The first target user is a long-term investor who:

- researches Indian listed companies
- understands basic financial ratios
- wants to compare a company with similar businesses
- wants a structured explanation instead of a screen full of unrelated numbers
- is comfortable treating the result as research support rather than financial advice

The MVP is not designed for:

- intraday traders
- automated trading systems
- professional portfolio-management workflows
- users expecting guaranteed predictions

## The user problem

Investors often have to collect ratios from multiple places, decide which companies are comparable, and interpret conflicting signals manually.

StockEdge should answer three questions:

1. Does this appear to be a good business?
2. Does the current valuation look attractive compared with peers?
3. What evidence supports the result?

## MVP promise

> Given a supported NSE stock symbol, StockEdge will compare the company with its industry peers, calculate business-quality and valuation scores, and explain the main strengths, weaknesses, confidence level, and recommendation.

The MVP does not promise to predict the future price of a stock.

## Supported universe

The first release supports companies in the imported Nifty 500 universe.

- Symbols must exist in the `companies` data source.
- The user analyzes one stock at a time.
- Peer groups are initially based on industry.
- Market-cap-aware peer grouping is a future improvement.
- The company universe should show when it was last refreshed.

## User flow

```text
Open StockEdge
    ↓
Search for or select an NSE symbol
    ↓
Validate that the symbol is supported
    ↓
Show a loading state
    ↓
Load cached or freshly refreshed data
    ↓
Compare the company with its peer group
    ↓
Calculate business and valuation results
    ↓
Display scores, confidence, evidence, and recommendation
```

## MVP output

Every successful analysis should eventually include:

- symbol
- company name
- industry
- peer count
- peer-group description
- business-quality score out of 10
- valuation score out of 10
- overall score out of 10
- recommendation
- business-quality confidence
- valuation confidence
- overall confidence
- actual metric values
- peer percentiles
- strengths
- weaknesses
- data source
- data fetched timestamp
- financial-period or data-as-of information where available
- scoring-model version

## Recommendation meanings

These labels are decision-support categories, not instructions to buy or sell.

### High Conviction Buy

The company has a very strong overall result, strong business quality, and sufficiently attractive valuation according to the current scoring model.

This label still requires independent research. It does not mean the investment is risk-free.

### Buy

The company meets the current minimum business-quality, valuation, and overall-score thresholds.

It is a candidate for deeper research, not an automatic order instruction.

### Watchlist

The result is interesting but does not meet the stronger Buy requirements. The user may want to monitor price, business performance, or valuation.

### Neutral

The available evidence is mixed or insufficiently attractive for a stronger label.

### Avoid

The current peer-relative result is weak, or the score is below the Neutral threshold. This means “do not prioritize this stock for further research right now,” not “the stock can never perform well.”

## Provisional scoring rules

The first scoring model uses two components:

```text
Overall Score = Business Quality × 70%
              + Valuation × 30%
```

Business quality currently considers growth, profitability, cash conversion, and debt-related metrics.

Valuation currently considers P/E, forward P/E, EV/EBITDA, PEG, price-to-book, and free-cash-flow yield when data is available.

Scores are relative to the selected peer group. The scoring model must be versioned because weights and rules may change over time.

## Data freshness policy

The application must show when data was fetched instead of presenting values as timeless facts.

For the first database-backed version:

- Company and industry metadata may be refreshed when the universe changes.
- Fundamental and valuation snapshots should be considered fresh for 24 hours.
- Cached data older than 24 hours should be marked `stale`.
- A stale result may still be displayed, but the user must see the warning.
- The financial reporting period should be shown when the provider supplies it.
- Future price and technical data will need a shorter freshness window.

If the provider is unavailable:

- use a recent valid cache if one exists and clearly label it
- otherwise return an understandable unavailable-data error
- never silently replace missing values with invented values

## Missing-data policy

Missing data is expected in financial datasets.

- A missing metric is excluded from that component's score when possible.
- Confidence decreases as fewer metrics are available.
- If too little data exists, show `Insufficient Data` rather than a confident recommendation.
- The UI must show which metrics are unavailable.
- Derived metrics must handle zero and missing denominators safely.
- A company with no usable peer group must not automatically receive a perfect percentile score.

## Error behavior

The frontend should represent these states separately:

```text
idle
loading
success
empty
error
stale-success
```

Expected API behavior:

- Unknown symbol → `404`
- Invalid input → `400` or `422`
- External provider unavailable → `503`
- Unexpected server failure → `500`

The UI should provide a human-readable message and a retry action. It should never try to render an error object as though it were a successful analysis.

## User experience goals

The first reliable version should:

- show the interface immediately
- make the search field obvious
- provide autocomplete for supported symbols
- show progress while analysis is running
- never leave the user wondering whether the request worked
- display data freshness and confidence prominently
- explain every recommendation with evidence
- work on narrow screens
- support keyboard and screen-reader users

With cached data, the analysis page should feel close to instant. A provider refresh may take longer, but the UI must explain why.

## MVP scope

Included:

- Nifty 500 company universe
- Industry-based peer groups
- PostgreSQL-backed company metadata
- Cached fundamental and valuation snapshots
- Business-quality scoring
- Valuation scoring
- Overall recommendation
- Confidence and missing-data handling
- Explainable strengths and weaknesses
- React search and analysis screen
- Validated FastAPI API
- Automated tests for scoring and API behavior

Not included in the first reliable release:

- User accounts
- Watchlists
- Portfolio tracking
- Order execution
- Personalized recommendations
- Macro analysis
- Advanced charting
- Machine-learning predictions
- Intraday trading signals

## Success criteria

The MVP is successful when:

1. A user can search for a supported symbol.
2. The API returns a predictable validated response.
3. The backend can analyze using cached database data.
4. An unavailable provider produces a clear fallback or error.
5. Missing metrics reduce confidence rather than creating misleading certainty.
6. The UI has clear idle, loading, success, stale, empty, and error states.
7. The recommendation can be traced back to component scores and metrics.
8. Automated tests cover the important scoring rules.
9. A new developer can run the project using `docs/Development.md`.
10. The deployed application can be updated through database migrations and versioned code.

## Decisions to revisit later

These are deliberately provisional:

- whether industry alone is a sufficient peer definition
- whether business quality should remain 70% of the overall score
- how negative or unusual valuation ratios should be treated
- the exact freshness window for each metric
- whether technical and macro signals should affect the final recommendation
- how to communicate uncertainty to different types of users

Any change to these rules should be documented and assigned a new scoring-model version.
