from app.services.peer_engine import get_peers, get_stock_info


def test_unknown_stock_has_no_info():
    assert get_stock_info("NOT_A_REAL_SYMBOL") is None


def test_unknown_stock_has_no_peers():
    assert get_peers("NOT_A_REAL_SYMBOL") is None
