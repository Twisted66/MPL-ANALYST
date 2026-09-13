from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
ROOT = Path(__file__).resolve().parents[2]

@dataclass(frozen=True)
class Settings:
    db_path: Path
    host: str
    port: int
    token: str
    allowed_hosts: tuple[str, ...]
    allowed_origins: tuple[str, ...]
    timeout: int

def get_settings():
    hosts = tuple(x.strip() for x in os.getenv(
        "MPL_ALLOWED_HOSTS",
        "localhost,localhost:8000,127.0.0.1,127.0.0.1:8000"
    ).split(",") if x.strip())
    origins = tuple(x.strip() for x in os.getenv("MPL_ALLOWED_ORIGINS", "").split(",") if x.strip())
    return Settings(
        db_path=Path(os.getenv("MPL_DB_PATH", str(ROOT / "data" / "mpl_predictor.sqlite3"))),
        host=os.getenv("MPL_MCP_HOST", "0.0.0.0"),
        port=int(os.getenv("MPL_MCP_PORT", "8000")),
        token=os.getenv("MPL_MCP_TOKEN", "change-me"),
        allowed_hosts=hosts,
        allowed_origins=origins,
        timeout=int(os.getenv("MPL_REQUEST_TIMEOUT", "20")),
    )
