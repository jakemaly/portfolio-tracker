"""
Configuration settings for the application.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIR / "portfolio.db"

CACHE_DURATION_SECONDS = 3600  # 1 hour
DEFAULT_START_DATE = "2020-01-01"

DATA_DIR.mkdir(exist_ok=True)