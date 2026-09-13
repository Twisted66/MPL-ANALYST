import math

def evaluate(rows):
    if not rows: return {"n":0,"accuracy":0,"brier":0,"log_loss":0}
    correct=brier=ll=0
    for p,y in rows:
        p=max(1e-12,min(1-1e-12,p))
        correct += int((p>=.5)==bool(y))
        brier += (p-y)**2
        ll += -(y*math.log(p)+(1-y)*math.log(1-p))
    n=len(rows)
    return {"n":n,"accuracy":correct/n,"brier":brier/n,"log_loss":ll/n}
