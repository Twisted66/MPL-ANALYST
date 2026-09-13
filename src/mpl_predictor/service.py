from .data import list_matches,get_match,insert_prediction
from .features import build_features
from .model import LogisticBaseline,FEATURES
from .backtest import run_backtest

def status(db):
    rows=list_matches(db)
    return {"database":str(db),"matches":len(rows),
            "completed_matches":sum(x["status"]=="completed" for x in rows),
            "scheduled_matches":sum(x["status"]=="scheduled" for x in rows),
            "model":"logistic-v1","mode":"CPU-first"}

def predict_match(db,match_id):
    rows=list_matches(db)
    target=next((x for x in rows if x["id"]==match_id),None)
    if not target: raise ValueError(f"Match {match_id} not found")
    prior=[x for x in rows if x["status"]=="completed" and x["match_date"]<target["match_date"] and x.get("winner")]
    model=LogisticBaseline(); X=[]; y=[]
    for m in prior:
        f=build_features(prior,m["team_a"],m["team_b"],m["match_date"])
        X.append([f[k] for k in FEATURES]); y.append(int(m["winner"]==m["team_a"]))
    if len(set(y))>=2: model.fit(X,y)
    f=build_features(prior,target["team_a"],target["team_b"],target["match_date"])
    p=max(.001,min(.999,model.probability(f)))
    winner=target["team_a"] if p>=.5 else target["team_b"]
    score="2-0" if max(p,1-p)>=.70 else "2-1"
    pid=insert_prediction(db,target["id"],model.version,"series_pre_match",p,1-p,winner,score,f,
      {"data_cutoff":target["match_date"],"note":"v0.1 baseline; no player/hero/draft/news layer yet"})
    return {"prediction_id":pid,"match":target,"model_version":model.version,
            "team_a_probability":p,"team_b_probability":1-p,"predicted_winner":winner,
            "most_likely_series_score":score,"features":f,
            "limitations":["No player/hero/draft features","No live post-draft updates","Estimate, not guarantee"]}
