from datetime import datetime,timedelta
from .data import upsert_match

def seed_demo(db):
    base=datetime(2026,1,1,12)
    rows=[
      ("TLPH","ONIC","ONIC"),("FLCN","RORA","FLCN"),("OMG","TNC","OMG"),("APBR","TWIS","APBR"),
      ("ONIC","FLCN","ONIC"),("TLPH","OMG","TLPH"),("RORA","APBR","RORA"),("TNC","TWIS","TNC"),
      ("ONIC","OMG","ONIC"),("FLCN","TNC","FLCN"),("TLPH","APBR","TLPH"),("RORA","TWIS","RORA"),
      ("ONIC","TLPH","ONIC"),("FLCN","OMG","OMG"),("RORA","TNC","RORA"),("APBR","TLPH","TLPH")
    ]
    for i,(a,b,w) in enumerate(rows,1):
        dt=base+timedelta(days=i)
        upsert_match(db,{"external_id":f"DEMO-{i:03}","season":"DEMO","stage":"synthetic",
          "match_date":dt.isoformat(),"team_a":a,"team_b":b,"best_of":3,
          "team_a_wins":2 if w==a else 1,"team_b_wins":2 if w==b else 1,
          "winner":w,"status":"completed","source_url":"internal://synthetic"})
    upsert_match(db,{"external_id":"DEMO-UPCOMING-001","season":"DEMO","stage":"synthetic",
      "match_date":(base+timedelta(days=30)).isoformat(),"team_a":"TLPH","team_b":"ONIC",
      "best_of":3,"status":"scheduled","source_url":"internal://synthetic"})
    return len(rows)+1
