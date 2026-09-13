from dataclasses import dataclass

@dataclass
class EloState:
    ratings: dict

def win_probability(a,b):
    return 1/(1+10**((b-a)/400))

def update_elo(s,winner,loser,k=24):
    rw=s.ratings.setdefault(winner,1500.0)
    rl=s.ratings.setdefault(loser,1500.0)
    ew=win_probability(rw,rl)
    s.ratings[winner]=rw+k*(1-ew)
    s.ratings[loser]=rl+k*(0-(1-ew))
