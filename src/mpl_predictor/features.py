from .ratings import win_probability, EloState, update_elo

def build_elo_before(matches, before_date, k=24):
    s=EloState({})
    for m in sorted(matches,key=lambda x:x["match_date"]):
        if m["match_date"] >= before_date: break
        if m.get("status")=="completed" and m.get("winner"):
            loser=m["team_b"] if m["winner"]==m["team_a"] else m["team_a"]
            update_elo(s,m["winner"],loser,k)
    return s

def recent_form(matches, team, before_date, window=5):
    rows=[m for m in matches if m.get("status")=="completed" and m.get("winner")
          and m["match_date"]<before_date and team in (m["team_a"],m["team_b"])]
    rows=sorted(rows,key=lambda x:x["match_date"],reverse=True)[:window]
    return sum(m["winner"]==team for m in rows)/len(rows) if rows else .5

def game_rate(matches, team, before_date, window=10):
    rows=[]
    for m in matches:
        if m.get("status")!="completed" or m["match_date"]>=before_date or team not in (m["team_a"],m["team_b"]):
            continue
        a,b=m.get("team_a_wins"),m.get("team_b_wins")
        if a is None or b is None: continue
        rows.append((a,b) if m["team_a"]==team else (b,a))
    rows=rows[-window:]
    total=sum(a+b for a,b in rows)
    return sum(a for a,b in rows)/total if total else .5

def build_features(matches, team_a, team_b, before_date):
    s=build_elo_before(matches,before_date)
    ra=s.ratings.get(team_a,1500); rb=s.ratings.get(team_b,1500)
    return {
        "elo_a":ra,"elo_b":rb,
        "elo_probability_a":win_probability(ra,rb),
        "recent_form_a":recent_form(matches,team_a,before_date),
        "recent_form_b":recent_form(matches,team_b,before_date),
        "game_rate_a":game_rate(matches,team_a,before_date),
        "game_rate_b":game_rate(matches,team_b,before_date),
    }
