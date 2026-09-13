import argparse,json
from .config import get_settings
from .db import init_db
from .seed import seed_demo
from .data import list_matches
from .backtest import run_backtest
from .service import status,predict_match
from .ingest import inspect_schedule

def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="cmd",required=True)
    for x in ["init-db","seed-demo","import-schedule","backtest","status","predict-demo"]: sub.add_parser(x)
    a=p.parse_args(); s=get_settings(); init_db(s.db_path)
    if a.cmd=="init-db": print(s.db_path)
    elif a.cmd=="seed-demo": print(seed_demo(s.db_path))
    elif a.cmd=="import-schedule": print(json.dumps(inspect_schedule(s.timeout),indent=2))
    elif a.cmd=="backtest": print(json.dumps(run_backtest(list_matches(s.db_path))["metrics"],indent=2))
    elif a.cmd=="status": print(json.dumps(status(s.db_path),indent=2))
    elif a.cmd=="predict-demo":
        scheduled=[m for m in list_matches(s.db_path) if m["status"]=="scheduled"]
        if not scheduled: raise SystemExit("No scheduled match; run seed-demo.")
        print(json.dumps(predict_match(s.db_path,scheduled[-1]["id"]),indent=2))
if __name__=="__main__": main()
