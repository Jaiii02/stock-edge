import pandas as pd

from app.core.config import DATA_PATH


_companies = pd.read_csv(DATA_PATH)


def get_symbols() -> list[str]:
    """Return the symbols currently in the local supported universe."""
    return _companies["Symbol"].tolist()
