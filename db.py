import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Caminho absoluto da pasta onde está o db.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Carrega o .env exatamente dessa pasta
load_dotenv(os.path.join(BASE_DIR, ".env"))

def get_engine():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL não foi carregada. Verifique o arquivo .env")

    return create_engine(
        database_url,
        pool_pre_ping=True
    )
