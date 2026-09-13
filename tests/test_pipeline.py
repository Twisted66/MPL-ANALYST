from pathlib import Path
from tempfile import TemporaryDirectory
from mpl_predictor.db import init_db
from mpl_predictor.seed import seed_demo
from mpl_predictor.data import list_matches
from mpl_predictor.backtest import run_backtest

def test_pipeline():
    with TemporaryDirectory() as d:
        db=Path(d)/"test.sqlite3"
        init_db(db); seed_demo(db)
        r=run_backtest(list_matches(db))
        assert r["metrics"]["n"]>0
        assert 0<=r["metrics"]["accuracy"]<=1
        assert 0<=r["metrics"]["brier"]<=1
