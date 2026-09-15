import pytest


@pytest.fixture
def valuation_rows():
    return [
        {"pe": 10, "forward_pe": 12, "ev_ebitda": 8, "peg": 1, "price_to_book": 2, "fcf_yield": 0.10},
        {"pe": 20, "forward_pe": 18, "ev_ebitda": 12, "peg": 2, "price_to_book": 3, "fcf_yield": 0.05},
        {"pe": 30, "forward_pe": 25, "ev_ebitda": 15, "peg": 3, "price_to_book": 4, "fcf_yield": 0.02},
    ]
