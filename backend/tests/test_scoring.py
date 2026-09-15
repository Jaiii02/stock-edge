import pandas as pd

from app.services.business_quality import calculate_derived_metrics
from app.services.recommendation import calculate_overall_score, get_recommendation
from app.services.valuation import calculate_derived_metrics as calculate_valuation_metrics
from app.services.valuation import calculate_valuation_score, normalize_metrics


def test_business_derived_metrics_handle_zero_denominators():
    result = calculate_derived_metrics(
        {
            "free_cash_flow": 100,
            "net_income": 0,
            "total_debt": 100,
            "total_cash": 50,
            "ebitda": 0,
        }
    )

    assert result["fcf_conversion"] is None
    assert result["net_debt_ebitda"] is None


def test_valuation_derived_metrics_handle_zero_denominator():
    result = calculate_valuation_metrics(
        {
            "free_cash_flow": 100,
            "enterprise_value": 0,
        }
    )

    assert result["fcf_yield"] is None


def test_negative_pe_is_excluded_from_valuation_score(valuation_rows):
    valuation_rows[0]["pe"] = -5
    frame = pd.DataFrame(valuation_rows)

    scored = calculate_valuation_score(normalize_metrics(frame))

    assert pd.isna(scored.loc[0, "pe_score"])
    assert scored.loc[0, "metrics_used"] == 5


def test_recommendation_uses_weighted_score():
    assert calculate_overall_score(8.0, 6.0) == 7.4
    assert get_recommendation(8.0, 8.0, 6.5) == "High Conviction Buy"
