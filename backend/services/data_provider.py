import yfinance as yf

def get_stock_info(symbol: str):
    """
    Fetch raw Yahoo Finance info.
    """

    stock = yf.Ticker(f"{symbol}.NS")

    return stock.info