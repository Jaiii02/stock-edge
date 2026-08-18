import pandas as pd

from services.peer_engine import get_peers
from services.data_provider import get_stock_info

from services.business_quality import (
    get_business_metrics,
    calculate_derived_metrics as calculate_business_metrics,
    normalize_metrics as normalize_business_metrics,
    calculate_business_quality,
    explain_business_quality,
)

from services.valuation import (
    get_valuation_metrics,
    calculate_derived_metrics as calculate_valuation_metrics,
    normalize_metrics as normalize_valuation_metrics,
    calculate_valuation_score,
    explain_valuation,
)

from services.recommendation import generate_summary


def analyze_stock(symbol: str):
    """
    Complete StockEdge analysis pipeline.

    """

    # -----------------------------
    # Get Peer Universe
    # -----------------------------
    peer_info = get_peers(symbol)

    if peer_info is None:
        return {"error": "Stock not found"}

    peer_symbols = peer_info["peer_symbols"]

    # Include target stock
    all_symbols = [symbol] + peer_symbols

    business_data = []
    valuation_data = []

    # -----------------------------
    # Fetch data once per company
    # -----------------------------
    for stock in all_symbols:

        info = get_stock_info(stock)

        # Business
        business_metrics = get_business_metrics(info)
        business_metrics = calculate_business_metrics(business_metrics)
        business_metrics["symbol"] = stock
        business_data.append(business_metrics)

        # Valuation
        valuation_metrics = get_valuation_metrics(info)
        valuation_metrics = calculate_valuation_metrics(valuation_metrics)
        valuation_metrics["symbol"] = stock
        valuation_data.append(valuation_metrics)

    # -----------------------------
    # Business Quality
    # -----------------------------
    business_df = pd.DataFrame(business_data)
    business_df = normalize_business_metrics(business_df)
    business_df = calculate_business_quality(business_df)



    business_row = business_df[
        business_df["symbol"] == symbol
    ].iloc[0]

    business_result = explain_business_quality(business_row)

    # -----------------------------
    # Valuation
    # -----------------------------
    valuation_df = pd.DataFrame(valuation_data)
    valuation_df = normalize_valuation_metrics(valuation_df)
    valuation_df = calculate_valuation_score(valuation_df)
    

    valuation_row = valuation_df[
        valuation_df["symbol"] == symbol
    ].iloc[0]

    valuation_result = explain_valuation(valuation_row)

    # -----------------------------
    # Final Recommendation
    # -----------------------------
    return generate_summary(
        symbol=symbol,
        business_quality=business_result,
        valuation=valuation_result,
    )


