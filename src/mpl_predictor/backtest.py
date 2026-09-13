from .features import build_features
from .model import LogisticBaseline, FEATURES
from .evaluation import evaluate

def run_backtest(matches):
    ordered=sorted([m for m in matches if m.get("status")=="completed" and m.get("winner")],key=lambda x:x["match_date"])
    rows=[]; details=[]
    for i,m in enumerate(ordered):
        prior=ordered[:i]
        if len(prior)<6: continue
        model=LogisticBaseline(); X=[]; y=[]
        for t in prior:
            f=build_features(prior,t["team_a"],t["team_b"],t["match_date"])
            X.append([f[k] for k in FEATURES]); y.append(int(t["winner"]==t["team_a"]))
        if len(set(y))<2: continue
        model.fit(X,y)
        f=build_features(prior,m["team_a"],m["team_b"],m["match_date"])
        p=model.probability(f); actual=int(m["winner"]==m["team_a"])
        rows.append((p,actual))
        details.append({"match_id":m["id"],"date":m["match_date"],"team_a":m["team_a"],"team_b":m["team_b"],
                        "predicted":m["team_a"] if p>=.5 else m["team_b"],"actual":m["winner"],"p_team_a":p})
    return {"metrics":evaluate(rows),"predictions":details,
            "methodology":"chronological walk-forward logistic baseline; features are computed only from pre-match data"}
