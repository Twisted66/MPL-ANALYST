import json
from pathlib import Path
from typing import Any
from .db import connect

def upsert_match(db_path: Path, m: dict[str, Any]) -> int:
    with connect(db_path) as c:
        c.execute("""
        INSERT INTO matches(external_id,season,stage,match_date,team_a,team_b,best_of,
          team_a_wins,team_b_wins,winner,status,source_url)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(external_id) DO UPDATE SET
          season=excluded.season,stage=excluded.stage,match_date=excluded.match_date,
          team_a=excluded.team_a,team_b=excluded.team_b,best_of=excluded.best_of,
          team_a_wins=excluded.team_a_wins,team_b_wins=excluded.team_b_wins,
          winner=excluded.winner,status=excluded.status,source_url=excluded.source_url
        """, (
            m.get("external_id"),m["season"],m.get("stage"),m["match_date"],
            m["team_a"],m["team_b"],m.get("best_of",3),m.get("team_a_wins"),
            m.get("team_b_wins"),m.get("winner"),m.get("status","scheduled"),m.get("source_url")
        ))
        return c.execute("SELECT id FROM matches WHERE external_id=?", (m.get("external_id"),)).fetchone()["id"]

def list_matches(db_path: Path, status=None, limit=10000):
    with connect(db_path) as c:
        if status:
            rows=c.execute("SELECT * FROM matches WHERE status=? ORDER BY match_date", (status,)).fetchall()
        else:
            rows=c.execute("SELECT * FROM matches ORDER BY match_date",()).fetchall()
        return [dict(x) for x in rows[-limit:]]

def get_match(db_path: Path, match_id: int):
    with connect(db_path) as c:
        m=c.execute("SELECT * FROM matches WHERE id=?", (match_id,)).fetchone()
        if not m: return None
        result=dict(m)
        result["games"]=[dict(x) for x in c.execute("SELECT * FROM games WHERE match_id=? ORDER BY game_number",(match_id,)).fetchall()]
        result["predictions"]=[dict(x) for x in c.execute("SELECT * FROM predictions WHERE match_id=? ORDER BY created_at DESC",(match_id,)).fetchall()]
        return result

def insert_prediction(db_path, match_id, version, kind, a, b, winner, score, features, rationale):
    with connect(db_path) as c:
        cur=c.execute("""
        INSERT INTO predictions(match_id,model_version,prediction_type,team_a_probability,
        team_b_probability,predicted_winner,predicted_score,features_json,rationale_json)
        VALUES(?,?,?,?,?,?,?,?,?)
        """,(match_id,version,kind,a,b,winner,score,json.dumps(features),json.dumps(rationale)))
        c.commit()
        return cur.lastrowid
