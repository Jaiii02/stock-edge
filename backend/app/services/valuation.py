import math

import pandas as pd
import yfinance as yf

from app.services.scoring_config import (
    VALUATION_HIGHER_IS_BETTER,
    VALUATION_LOWER_IS_BETTER,
    VALUATION_SCORE_COLUMNS,
    MIN_COMPARISON_PEERS,
    OUTLIER_LOWER_QUANTILE,
    OUTLIER_UPPER_QUANTILE,
)

STRENGTH_THRESHOLD = 0.80
WEAKNESS_THRESHOLD = 0.30

def get_valuation_metrics(info : dict) :
    """
    Fetch raw valuation metrics from Yahoo Finance.

    """

    return {
        "pe": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "ev_ebitda": info.get("enterpriseToEbitda"),
        "peg": info.get("pegRatio"),
        "price_to_book": info.get("priceToBook"),
        "market_cap": info.get("marketCap"),
        "free_cash_flow": info.get("freeCashflow"),
        "enterprise_value": info.get("enterpriseValue"),
    }

def calculate_derived_metrics(metrics: dict):

    metrics["fcf_yield"] = None

    if (metrics["enterprise_value"] not in (None, 0)) and (metrics["free_cash_flow"] is not None) :
        candidate = (metrics["free_cash_flow"])/(metrics["enterprise_value"])
        if math.isfinite(candidate):
            metrics["fcf_yield"] = candidate

    return metrics


def normalize_metrics(df: pd.DataFrame):
    """
    Convert raw metrics into percentile scores.

    """

    for metric in VALUATION_HIGHER_IS_BETTER:
        valid = df[metric].notna()
        if len(df) < MIN_COMPARISON_PEERS + 1:
            df[f"{metric}_score"] = pd.NA
            continue
        values = df.loc[valid, metric].clip(lower=df.loc[valid, metric].quantile(OUTLIER_LOWER_QUANTILE), upper=df.loc[valid, metric].quantile(OUTLIER_UPPER_QUANTILE))
        df.loc[valid, f"{metric}_score"] = (
            values.rank(pct=True)
        )

    for metric in VALUATION_LOWER_IS_BETTER:
        # Negative valuation multiples usually mean negative earnings or
        # another unsuitable denominator, so they are not comparable.
        valid = df[metric].notna() & (df[metric] > 0)
        if len(df) < MIN_COMPARISON_PEERS + 1:
            df[f"{metric}_score"] = pd.NA
            continue
        values = df.loc[valid, metric].clip(lower=df.loc[valid, metric].quantile(OUTLIER_LOWER_QUANTILE), upper=df.loc[valid, metric].quantile(OUTLIER_UPPER_QUANTILE))
        df.loc[valid, f"{metric}_score"] = (
            values.rank(pct=True, ascending=False)
        )

    return df


def calculate_valuation_score(df: pd.DataFrame):
    """
    Calculate Valuation Score and confidence.

    """

    score_columns = list(VALUATION_SCORE_COLUMNS)

    # Number of metrics available
    df["metrics_used"] = df[score_columns].count(axis=1)

    # Total metrics considered
    df["metrics_total"] = len(score_columns)

    # Confidence (0–1)
    df["confidence"] = (
        df["metrics_used"]
        / df["metrics_total"]
    )

    # Final Valuation Score (0–1)
    df["valuation_score"] = (
        df[score_columns]
        .mean(axis=1, skipna=True)
        .fillna(0)
    )

    return df


def explain_valuation(row):
    """
    Generate strengths, weaknesses and confidence
    for the Valuation Score.

    """

    strengths = []
    weaknesses = []
    explanations = []

    metric_descriptions = {
        "pe": ("Attractive P/E", "Expensive P/E"),
        "forward_pe": ("Low Forward P/E", "High Forward P/E"),
        "ev_ebitda": ("Low EV/EBITDA", "High EV/EBITDA"),
        "peg": ("Attractive PEG Ratio", "Expensive PEG Ratio"),
        "price_to_book": ("Attractive Price-to-Book", "Expensive Price-to-Book"),
        "fcf_yield": ("Strong FCF Yield", "Weak FCF Yield"),
    }

    # Evaluate every metric
    for metric, (good_msg, bad_msg) in metric_descriptions.items():

        score = row[f"{metric}_score"]

        if pd.isna(score):
            continue

        explanations.append({
            "metric": metric,
            "value": None if pd.isna(row[metric]) else round(float(row[metric]), 4),
            "peer_percentile": round(float(score) * 100, 1),
            "effect": "positive" if score >= 0.5 else "negative",
        })

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
            "pe": None if pd.isna(row["pe"]) or row["pe"] <= 0 else round(row["pe"], 2),
            "forward_pe": None if pd.isna(row["forward_pe"]) or row["forward_pe"] <= 0 else round(row["forward_pe"], 2),
            "ev_ebitda": None if pd.isna(row["ev_ebitda"]) or row["ev_ebitda"] <= 0 else round(row["ev_ebitda"], 2),
            "price_to_book": None if pd.isna(row["price_to_book"]) or row["price_to_book"] <= 0 else round(row["price_to_book"], 2),
            "fcf_yield": None if pd.isna(row["fcf_yield"]) else round(row["fcf_yield"] * 100, 2),
            "peg": None if pd.isna(row["peg"]) else round(row["peg"], 2),
        },
        "valuation_score": round(row["valuation_score"] * 10, 2),
        "confidence": round(confidence * 100, 1),
        "confidence_level": confidence_level,
        "metrics_used": int(row["metrics_used"]),
        "metrics_total": int(row["metrics_total"]),
        "strengths": strengths,
        "weaknesses": weaknesses,
        "explanations": explanations,
    }
