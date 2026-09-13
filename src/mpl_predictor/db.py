import sqlite3
from pathlib import Path
from contextlib import contextmanager

SCHEMA = """
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS teams(
 id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, short_name TEXT, active INTEGER DEFAULT 1
);
CREATE TABLE IF NOT EXISTS players(
 id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, team_id INTEGER, role TEXT, active INTEGER DEFAULT 1,
 FOREIGN KEY(team_id) REFERENCES teams(id)
);
CREATE TABLE IF NOT EXISTS heroes(
 id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, role TEXT, active INTEGER DEFAULT 1
);
CREATE TABLE IF NOT EXISTS patches(
 id INTEGER PRIMARY KEY, version TEXT UNIQUE NOT NULL, released_at TEXT
);
CREATE TABLE IF NOT EXISTS matches(
 id INTEGER PRIMARY KEY,
 external_id TEXT UNIQUE,
 season TEXT NOT NULL,
 stage TEXT,
 match_date TEXT NOT NULL,
 team_a TEXT NOT NULL,
 team_b TEXT NOT NULL,
 best_of INTEGER DEFAULT 3,
 team_a_wins INTEGER,
 team_b_wins INTEGER,
 winner TEXT,
 status TEXT DEFAULT 'scheduled',
 source_url TEXT
);
CREATE TABLE IF NOT EXISTS games(
 id INTEGER PRIMARY KEY,
 match_id INTEGER NOT NULL,
 game_number INTEGER NOT NULL,
 winner TEXT,
 patch TEXT,
 duration_seconds INTEGER,
 team_a_players TEXT,
 team_b_players TEXT,
 team_a_picks TEXT,
 team_b_picks TEXT,
 team_a_bans TEXT,
 team_b_bans TEXT,
 FOREIGN KEY(match_id) REFERENCES matches(id),
 UNIQUE(match_id, game_number)
);
CREATE TABLE IF NOT EXISTS predictions(
 id INTEGER PRIMARY KEY,
 match_id INTEGER NOT NULL,
 created_at TEXT DEFAULT CURRENT_TIMESTAMP,
 model_version TEXT NOT NULL,
 prediction_type TEXT NOT NULL,
 team_a_probability REAL NOT NULL,
 team_b_probability REAL NOT NULL,
 predicted_winner TEXT NOT NULL,
 predicted_score TEXT,
 features_json TEXT,
 rationale_json TEXT,
 FOREIGN KEY(match_id) REFERENCES matches(id)
);
CREATE TABLE IF NOT EXISTS experiments(
 id INTEGER PRIMARY KEY,
 experiment_key TEXT UNIQUE NOT NULL,
 created_at TEXT DEFAULT CURRENT_TIMESTAMP,
 model_version TEXT NOT NULL,
 hypothesis TEXT NOT NULL,
 metrics_json TEXT NOT NULL,
 decision TEXT NOT NULL,
 notes TEXT
);
CREATE INDEX IF NOT EXISTS idx_match_date ON matches(match_date);
"""

def connect(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(path)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys=ON")
    return c

def init_db(path: Path):
    with connect(path) as c:
        c.executescript(SCHEMA)
        c.commit()

@contextmanager
def tx(path: Path):
    c = connect(path)
    try:
        yield c
        c.commit()
    except:
        c.rollback()
        raise
    finally:
        c.close()
