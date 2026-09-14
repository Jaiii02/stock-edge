"""
Business Quality Engine

Purpose:
Evaluate the financial quality of a business.

Responsibilities:
- Fetch raw financial metrics
- Normalize metrics
- Calculate Business Quality Score

Not Responsible For:
- Valuation
- Recommendations
- Technical Analysis
"""

import yfinance as yf
import math

import pandas as pd

from app.services.scoring_config import (
    BUSINESS_HIGHER_IS_BETTER,
    BUSINESS_LOWER_IS_BETTER,
    BUSINESS_WEIGHTS,
    MIN_COMPARISON_PEERS,
    OUTLIER_LOWER_QUANTILE,
    OUTLIER_UPPER_QUANTILE,
)

def get_business_metrics(info : dict) :
    """
    Fetch raw business quality metrics from Yahoo Finance.

    """

    return {
    "roe": info.get("returnOnEquity"),
    "revenue_growth": info.get("revenueGrowth"),
    "earnings_growth": info.get("earningsGrowth"),
    "gross_margin": info.get("grossMargins"),
    "operating_margin": info.get("operatingMargins"),
    "free_cash_flow": info.get("freeCashflow"),
    "net_income": info.get("netIncomeToCommon"),
    "total_debt": info.get("totalDebt"),
    "total_cash": info.get("totalCash"),
    "ebitda": info.get("ebitda"),
}


def calculate_derived_metrics(metrics: dict):
    """
    Calculate business metrics that are not directly
    provided by Yahoo Finance.

    Returns:
        dict: Original metrics enriched with derived metrics.
    """

    fcf_conversion = None
    net_debt_ebitda = None

    # FCF Conversion = Free Cash Flow / Net Income
    if (
        metrics["free_cash_flow"] is not None
        and metrics["net_income"] not in (None, 0)
    ):
        candidate = (
            metrics["free_cash_flow"] / metrics["net_income"]
        )
        if math.isfinite(candidate):
            fcf_conversion = candidate

    # Net Debt / EBITDA = (Total Debt - Total Cash) / EBITDA
    if (
        metrics["total_debt"] is not None
        and metrics["total_cash"] is not None
        and metrics["ebitda"] not in (None, 0)
    ):
        candidate = (
            (metrics["total_debt"] - metrics["total_cash"])
            / metrics["ebitda"]
        )
        if math.isfinite(candidate):
            net_debt_ebitda = candidate

    metrics["fcf_conversion"] = fcf_conversion
    metrics["net_debt_ebitda"] = net_debt_ebitda

    return metrics


def normalize_metrics(df: pd.DataFrame):
    """
    Convert raw metrics into percentile scores.

    """

    for metric in BUSINESS_HIGHER_IS_BETTER:
        valid = df[metric].notna()
        if len(df) < MIN_COMPARISON_PEERS + 1:
            df[f"{metric}_score"] = pd.NA
            continue
        values = df.loc[valid, metric].clip(lower=df.loc[valid, metric].quantile(OUTLIER_LOWER_QUANTILE), upper=df.loc[valid, metric].quantile(OUTLIER_UPPER_QUANTILE))
        df.loc[valid, f"{metric}_score"] = (
            values.rank(pct=True)
        )

    for metric in BUSINESS_LOWER_IS_BETTER:
        valid = df[metric].notna()
        if len(df) < MIN_COMPARISON_PEERS + 1:
            df[f"{metric}_score"] = pd.NA
            continue
        values = df.loc[valid, metric].clip(lower=df.loc[valid, metric].quantile(OUTLIER_LOWER_QUANTILE), upper=df.loc[valid, metric].quantile(OUTLIER_UPPER_QUANTILE))
        df.loc[valid, f"{metric}_score"] = (
            values.rank(pct=True, ascending=False)
        )

    return df


def calculate_business_quality(df: pd.DataFrame):
    """
    Calculate weighted Business Quality Score and confidence.
    Missing metrics do not unfairly penalize the score.

    """

    # Metric weights
    weights = BUSINESS_WEIGHTS

    score_columns = weights.keys()

    # Number of metrics available
    df["metrics_used"] = df[score_columns].count(axis=1)

    # Total metrics considered
    df["metrics_total"] = len(score_columns)

    # Confidence (0–1)
    df["confidence"] = (
        df["metrics_used"] /
        df["metrics_total"]
    )

    # Weighted sum
    weighted_sum = pd.Series(0.0, index=df.index)
    available_weight = pd.Series(0.0, index=df.index)

    for column, weight in weights.items():
        values = df[column].fillna(0)

        weighted_sum += values * weight
        available_weight += df[column].notna() * weight

    # Final Business Quality Score (0–1)
    df["business_quality_score"] = (
    weighted_sum
    .div(available_weight)
    .fillna(0)
    )

    return df


STRENGTH_THRESHOLD = 0.80
WEAKNESS_THRESHOLD = 0.30

def explain_business_quality(row):
    """
    Generate strengths, weaknesses and confidence
    for the Business Quality score.
    
    """

    strengths = []
    weaknesses = []

    metric_descriptions = {
        "roe": ("Excellent ROE", "Weak ROE"),
        "revenue_growth": ("Strong Revenue Growth", "Weak Revenue Growth"),
        "earnings_growth": ("Strong Earnings Growth", "Weak Earnings Growth"),
        "gross_margin": ("Healthy Gross Margins", "Weak Gross Margins"),
        "operating_margin": ("Strong Operating Margins", "Weak Operating Margins"),
        "fcf_conversion": ("Excellent Cash Conversion", "Poor Cash Conversion"),
        "net_debt_ebitda": ("Healthy Debt Levels", "High Debt Burden"),
    }

    # Evaluate every metric
    for metric, (good_msg, bad_msg) in metric_descriptions.items():

        score = row[f"{metric}_score"]

        if pd.isna(score):
            continue

        if score >= STRENGTH_THRESHOLD:
            strengths.append(good_msg)

        elif score <= WEAKNESS_THRESHOLD:
            weaknesses.append(bad_msg)

    # Confidence Level
    confidence = row["confidence"]

    if confidence >= 0.90:
        confidence_level = "High"

    elif confidence >= 0.75:
        confidence_level = "Medium"

    elif confidence >= 0.50:
        confidence_level = "Low"

    else:
        confidence_level = "Insufficient Data"

    return {
        "metrics": {
            "roe": None if pd.isna(row["roe"]) else round(row["roe"] * 100, 2),
            "revenue_growth": None if pd.isna(row["revenue_growth"]) else round(row["revenue_growth"] * 100, 2),
            "earnings_growth": None if pd.isna(row["earnings_growth"]) else round(row["earnings_growth"] * 100, 2),
            "gross_margin": None if pd.isna(row["gross_margin"]) else round(row["gross_margin"] * 100, 2),
            "operating_margin": None if pd.isna(row["operating_margin"]) else round(row["operating_margin"] * 100, 2),
            "fcf_conversion": None if pd.isna(row["fcf_conversion"]) else round(row["fcf_conversion"] * 100, 2),
            "net_debt_ebitda": None if pd.isna(row["net_debt_ebitda"]) else round(row["net_debt_ebitda"], 2),
        },
        "business_quality_score": round(row["business_quality_score"] * 10, 2),
        "confidence": round(confidence * 100, 1),
        "confidence_level": confidence_level,
        "metrics_used": int(row["metrics_used"]),
        "metrics_total": int(row["metrics_total"]),
        "strengths": strengths,
        "weaknesses": weaknesses,
    }


