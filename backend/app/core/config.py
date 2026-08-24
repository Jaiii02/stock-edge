from pathlib import Path


# Resolve paths from this file instead of from the directory where the
# developer happened to start Uvicorn.
BACKEND_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BACKEND_DIR / "data" / "seed" / "nifty500nse.csv"

# Both addresses are useful during local development. Production origins
# should eventually come from environment-based configuration.
FRONTEND_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
