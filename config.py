"""Configuration: env vars and paths. Uses local CSV if Sheets not configured."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# Google Sheets (optional)
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON", "credentials.json")
# Inline JSON string (e.g. from Streamlit Secrets) — use key GOOGLE_CREDENTIALS_JSON_CONTENT
GOOGLE_CREDENTIALS_JSON_CONTENT = (os.getenv("GOOGLE_CREDENTIALS_JSON_CONTENT") or "").strip()
PILOT_SHEET_ID = os.getenv("PILOT_SHEET_ID", "")
DRONE_SHEET_ID = os.getenv("DRONE_SHEET_ID", "")
MISSIONS_SHEET_ID = os.getenv("MISSIONS_SHEET_ID", "")

# Resolve credentials path (used when no inline content)
CREDENTIALS_PATH = BASE_DIR / GOOGLE_CREDENTIALS_JSON if not os.path.isabs(GOOGLE_CREDENTIALS_JSON) else Path(GOOGLE_CREDENTIALS_JSON)

def use_google_sheets() -> bool:
    """True if we have sheet IDs and valid credentials (file or inline JSON)."""
    has_sheets = bool(PILOT_SHEET_ID and DRONE_SHEET_ID and MISSIONS_SHEET_ID)
    has_creds = CREDENTIALS_PATH.exists() or bool(GOOGLE_CREDENTIALS_JSON_CONTENT)
    return has_sheets and has_creds

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
