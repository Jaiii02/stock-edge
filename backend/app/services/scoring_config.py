"""Central configuration for the current scoring model."""

BUSINESS_HIGHER_IS_BETTER = (
    "roe",
    "revenue_growth",
    "earnings_growth",
    "gross_margin",
    "operating_margin",
    "fcf_conversion",
)

BUSINESS_LOWER_IS_BETTER = ("net_debt_ebitda",)

BUSINESS_WEIGHTS = {
    "roe_score": 0.20,
    "revenue_growth_score": 0.20,
    "earnings_growth_score": 0.20,
    "operating_margin_score": 0.15,
    "gross_margin_score": 0.10,
    "fcf_conversion_score": 0.10,
    "net_debt_ebitda_score": 0.05,
}

VALUATION_HIGHER_IS_BETTER = ("fcf_yield",)

VALUATION_LOWER_IS_BETTER = (
    "pe",
    "forward_pe",
    "ev_ebitda",
    "peg",
    "price_to_book",
)

VALUATION_SCORE_COLUMNS = (
    "pe_score",
    "forward_pe_score",
    "ev_ebitda_score",
    "peg_score",
    "price_to_book_score",
    "fcf_yield_score",
)

SCORING_MODEL_VERSION = "business-quality-v1"
MIN_COMPARISON_PEERS = 2
OUTLIER_LOWER_QUANTILE = 0.05
OUTLIER_UPPER_QUANTILE = 0.95
