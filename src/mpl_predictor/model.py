import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

FEATURES=["elo_probability_a","recent_form_a","recent_form_b","game_rate_a","game_rate_b"]

class LogisticBaseline:
    version="logistic-v1"
    def __init__(self):
        self.pipe=Pipeline([("scale",StandardScaler()),("clf",LogisticRegression(max_iter=1000))])
        self.fitted=False
    def fit(self,X,y):
        if len(set(y))<2: return
        self.pipe.fit(np.asarray(X),np.asarray(y)); self.fitted=True
    def probability(self,f):
        if not self.fitted:
            return .55*f["elo_probability_a"]+.25*f["recent_form_a"]+.20*(1-f["recent_form_b"])
        return float(self.pipe.predict_proba([[f[k] for k in FEATURES]])[0][1])
