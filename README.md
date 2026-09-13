# MPL PH Predictor v0.1

CPU-first MLBB MPL Philippines prediction engine + MCP server.

## What is included

- SQLite data store
- chronological/walk-forward backtesting
- Elo-derived features
- logistic-regression baseline
- recent form and game-rate features
- immutable prediction records
- experiment-ready structure
- official MPL PH schedule fetch adapter
- MCP server using the current MCP Python SDK v2
- Streamable HTTP endpoint at `/mcp`
- bearer-token protection
- `/health` endpoint
- demo dataset so the complete pipeline can be tested immediately

## Run locally

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
python -m mpl_predictor.cli init-db
python -m mpl_predictor.cli seed-demo
python -m mpl_predictor.cli backtest
python -m mpl_predictor.cli predict-demo
python -m mpl_predictor.server
```

Local endpoint:

`http://127.0.0.1:8000/mcp`

Health:

`http://127.0.0.1:8000/health`

## Cloud

Set a strong `MPL_MCP_TOKEN` and the real hostname in `MPL_ALLOWED_HOSTS`.

Example:

```env
MPL_MCP_TOKEN=LONG_RANDOM_SECRET
MPL_ALLOWED_HOSTS=mcp.example.com,mcp.example.com:*
```

Then run the ASGI app behind HTTPS.

The intended public shape is:

`https://mcp.example.com/mcp`

not `/mcp/sse`.

## MCP tools

- `get_system_status`
- `get_upcoming_matches`
- `get_match`
- `predict_match`
- `predict_series`
- `get_team_form`
- `get_player_hero_stats`
- `get_hero_team_stats`
- `get_model_performance`
- `run_backtest_tool`

## Architecture

```text
MPL PH web/data
      |
      v
 ingestion -> SQLite -> feature engine
                         |
                         v
                  Elo + Logistic
                         |
                         v
                   Prediction
                         |
                         v
                    Evaluation
                         |
                         v
                 Experiment loop

LLMs are added later for web research, roster/news context,
patch interpretation, draft reasoning and challenger analysis.
```

## Important

The demo data is synthetic and exists only to prove the software works. It must never be used for real MPL claims.

The official schedule adapter intentionally fails closed: if the website DOM changes, it reports diagnostics instead of inventing matches.

Detailed player/hero/draft ingestion is the next implementation phase.
