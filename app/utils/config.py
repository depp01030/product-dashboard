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