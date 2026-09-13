import re
import requests
from bs4 import BeautifulSoup

OFFICIAL_SCHEDULE="https://ph-mpl.com/schedule"

def fetch_schedule(timeout=20):
    r=requests.get(OFFICIAL_SCHEDULE,timeout=timeout,headers={"User-Agent":"MPL-PH-Predictor/0.1 research"})
    r.raise_for_status()
    return r.text

def inspect_schedule(timeout=20):
    html=fetch_schedule(timeout)
    text=re.sub(r"\s+"," ",BeautifulSoup(html,"html.parser").get_text(" ",strip=True))
    scores=re.findall(r"\b[0-2]\s*:\s*[0-2]\b",text)
    return {"source":OFFICIAL_SCHEDULE,"fetched":True,"recognized_score_strings":len(scores),
            "note":"DOM extraction is intentionally conservative; update this adapter after inspecting markup changes."}
