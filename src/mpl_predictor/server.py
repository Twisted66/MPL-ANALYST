import hmac
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from mcp.server import MCPServer
from mcp.server.transport_security import TransportSecuritySettings

from .config import get_settings
from .db import init_db
from .data import list_matches,get_match
from .service import status,predict_match
from .backtest import run_backtest

s=get_settings(); init_db(s.db_path)
mcp=MCPServer("MPL-PH-Predictor",instructions="MLBB MPL Philippines prediction tools. Probabilities are estimates, never guarantees.")

@mcp.tool()
def get_system_status()->dict:
    """Return database and model status."""
    return status(s.db_path)

@mcp.tool()
def get_upcoming_matches(limit:int=10)->list[dict]:
    """Return scheduled matches."""
    return list_matches(s.db_path,"scheduled",limit)

@mcp.tool()
def get_match(match_id:int)->dict:
    """Return match, games and stored predictions."""
    x=get_match(s.db_path,match_id)
    if x is None: raise ValueError(f"Match {match_id} not found")
    return x

@mcp.tool()
def predict_match(match_id:int)->dict:
    """Predict the series using the current numerical baseline."""
    return predict_match(s.db_path,match_id)

@mcp.tool()
def predict_series(match_id:int)->dict:
    """Return series winner, probabilities and most likely score."""
    x=predict_match(s.db_path,match_id)
    return {"match_id":match_id,"series_winner":x["predicted_winner"],
            "team_a_probability":x["team_a_probability"],"team_b_probability":x["team_b_probability"],
            "most_likely_series_score":x["most_likely_series_score"],"model_version":x["model_version"]}

@mcp.tool()
def get_team_form(team:str,limit:int=10)->dict:
    """Return recent completed series for a team."""
    rows=[x for x in list_matches(s.db_path) if x["status"]=="completed" and team.lower() in (x["team_a"].lower(),x["team_b"].lower())]
    rows=sorted(rows,key=lambda x:x["match_date"],reverse=True)[:limit]
    wins=sum(x["winner"].lower()==team.lower() for x in rows)
    return {"team":team,"matches":rows,"wins":wins,"losses":len(rows)-wins,"win_rate":wins/len(rows) if rows else None}

@mcp.tool()
def get_player_hero_stats(player:str,hero:str)->dict:
    """Return player × hero availability status."""
    return {"player":player,"hero":hero,"available":False,"reason":"v0.2 ingestion layer not yet enabled"}

@mcp.tool()
def get_hero_team_stats(team:str,hero:str)->dict:
    """Return team × hero availability status."""
    return {"team":team,"hero":hero,"available":False,"reason":"v0.2 ingestion layer not yet enabled"}

@mcp.tool()
def get_model_performance()->dict:
    """Run the current chronological backtest."""
    return run_backtest(list_matches(s.db_path))["metrics"]

@mcp.tool()
def run_backtest_tool()->dict:
    """Run full walk-forward evaluation."""
    return run_backtest(list_matches(s.db_path))

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,request:Request,call_next):
        if request.url.path=="/health": return await call_next(request)
        if not s.token or s.token=="change-me":
            return JSONResponse({"error":"Configure MPL_MCP_TOKEN"},status_code=503)
        h=request.headers.get("authorization","")
        if not h.startswith("Bearer ") or not hmac.compare_digest(h[7:],s.token):
            return JSONResponse({"error":"Unauthorized"},status_code=401)
        return await call_next(request)

class HealthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,request,call_next):
        if request.url.path=="/health":
            return JSONResponse({"status":"ok","service":"mpl-ph-predictor","version":"0.1.0"})
        return await call_next(request)

security=TransportSecuritySettings(
    allowed_hosts=list(s.allowed_hosts),
    allowed_origins=list(s.allowed_origins)
)
app=mcp.streamable_http_app(
    streamable_http_path="/mcp",
    json_response=True,
    stateless_http=True,
    transport_security=security,
    host=s.host
)
app.add_middleware(AuthMiddleware)
app.add_middleware(HealthMiddleware)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host=s.host,port=s.port)
