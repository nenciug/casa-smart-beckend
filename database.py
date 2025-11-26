from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import psycopg2

# URL Supabase (modifici doar parola)
SUPABASE_URL = "postgresql://postgres:Dd152538@db.zyvcpzcoptknqszqztcj.supabase.co:5432/postgres"

def choose_database():
    try:
        conn = psycopg2.connect(SUPABASE_URL, connect_timeout=3)
        conn.close()
        print("✔ Folosesc SUPABASE")
        return SUPABASE_URL
    except:
        print("⚠ Supabase offline → trec pe SQLite local")
        return "sqlite:///./local.db"

DATABASE_URL = choose_database()

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
