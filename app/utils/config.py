import os
from dotenv import load_dotenv

def load_env():
    load_dotenv()

def get_database_uri():
    return (
        f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    )

def get_candidates_root() -> str:
    return os.getenv("CANDIDATES_ROOT", "./Candidates_root")
def get_products_root() -> str:
    return os.getenv("PRODUCTS_ROOT", "./products_root")

PRODUCTS_ROOT = get_products_root()
CANDIDATES_ROOT = get_candidates_root()
DATABASE_URL = get_database_uri()