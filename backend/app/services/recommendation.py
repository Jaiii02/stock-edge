# ---------------------------------------------------------
# Recommendation Thresholds
# ---------------------------------------------------------

HIGH_CONVICTION_THRESHOLD = 8.0
BUY_THRESHOLD = 6.5
WATCHLIST_THRESHOLD = 5.0
NEUTRAL_THRESHOLD = 3.5

# Minimum component scores required for stronger recommendations

MIN_HIGH_CONVICTION_BUSINESS = 8.0
MIN_HIGH_CONVICTION_VALUATION = 6.5

MIN_BUY_BUSINESS = 7.0
MIN_BUY_VALUATION = 5.0


def calculate_overall_score(
    business_quality_score: float,
    valuation_score: float,
):
    """
    Calculate the final investment score.

    Weighting:
        Business Quality : 70%
        Valuation        : 30%
    """

    overall_score = (
        business_quality_score * 0.70
        + valuation_score * 0.30
    )

    return round(overall_score, 2)


def get_recommendation(
    overall_score: float,
    business_score: float,
    valuation_score: float,
):
    """
    Generate the investment recommendation.

    A recommendation is based on both:
    - Overall score
    - Minimum Business & Valuation thresholds
    """

    if (
        overall_score >= HIGH_CONVICTION_THRESHOLD
        and business_score >= MIN_HIGH_CONVICTION_BUSINESS
        and valuation_score >= MIN_HIGH_CONVICTION_VALUATION
    ):
        return "High Conviction Buy"

    if (
        overall_score >= BUY_THRESHOLD
        and business_score >= MIN_BUY_BUSINESS
        and valuation_score >= MIN_BUY_VALUATION
    ):
        return "Buy"

    if overall_score >= WATCHLIST_THRESHOLD:
        return "Watchlist"

    if overall_score >= NEUTRAL_THRESHOLD:
        return "Neutral"

    return "Avoid"


def calculate_overall_confidence(
    business_quality: dict,
    valuation: dict,
):
    """
    Calculate confidence in the recommendation.
    """

    confidence = (
        business_quality["confidence"]
        + valuation["confidence"]
    ) / 2

    if confidence >= 90:
        confidence_level = "High"

    elif confidence >= 75:
        confidence_level = "Medium"

    elif confidence >= 50:
        confidence_level = "Low"

    else:
        confidence_level = "Insufficient Data"

    return {
        "score": round(confidence, 1),
        "level": confidence_level,
    }


def generate_summary(
    symbol: str,
    business_quality: dict,
    valuation: dict,
):
    """
    Generate the final StockEdge analysis.
    """

    business_score = business_quality["business_quality_score"]
    valuation_score = valuation["valuation_score"]

    overall_score = calculate_overall_score(
        business_score,
        valuation_score,
    )

    recommendation = get_recommendation(
        overall_score,
        business_score,
        valuation_score,
    )

    overall_confidence = calculate_overall_confidence(
        business_quality,
        valuation,
    )

    strengths = (
        business_quality["strengths"]
        + valuation["strengths"]
    )

    weaknesses = (
        business_quality["weaknesses"]
        + valuation["weaknesses"]
    )

    warnings = []
    if overall_confidence["level"] == "Insufficient Data":
        warnings.append("Recommendation confidence is limited by missing or insufficient comparison data.")

    return {
    "symbol": symbol,
    "scoring_model_version": SCORING_MODEL_VERSION,

    "overall_score": overall_score,

    "recommendation": recommendation,

    "overall_confidence": overall_confidence,

    "business_quality": {
        "score": business_score,
        "confidence": business_quality["confidence"],
        "confidence_level": business_quality["confidence_level"],
        "metrics": business_quality["metrics"],
    },

    "valuation": {
        "score": valuation_score,
        "confidence": valuation["confidence"],
        "confidence_level": valuation["confidence_level"],
        "metrics": valuation["metrics"],
    },

    "strengths": strengths,

    "weaknesses": weaknesses,
    "warnings": warnings,
    }
from app.services.scoring_config import SCORING_MODEL_VERSION
