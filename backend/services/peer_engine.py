"""
Peer Engine

Purpose:
Construct the comparison universe for a given stock.

Responsibilities:
- Load Nifty 500 data
- Validate stock symbol
- Find company information
- Return peer companies
"""
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "nifty500nse.csv"
df = pd.read_csv(DATA_PATH)

def load_data() :
    #A function to load data.
    #It is a function due to seperation of responsibility (if we later store it in .sql or any api), readability and reusability.

    return df

def get_stock_info(symbol : str) :
    data = load_data()
    stock = data[data["Symbol"] == symbol]

    if stock.empty :
        return None
    
    row = stock.iloc[0]
    company_name = row["Company Name"]
    industry = row["Industry"] 

    return {
        "symbol": symbol,
        "company_name": company_name,
        "industry": industry,
    }


def get_peers(symbol : str) :
    stock_info = get_stock_info(symbol)
    data = load_data()
    if stock_info is None:
        return None

    industry = stock_info["industry"]
    peer_list = data[(data["Industry"] == industry) & (data["Symbol"] != symbol)]

    return {
    "company_name": stock_info["company_name"],
    "industry": industry,
    "peer_count": len(peer_list),
    "peer_symbols": peer_list["Symbol"].tolist(),
}












