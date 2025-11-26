import psycopg2

# Înlocuiește PAROLA_TA cu parola ta din Supabase
DATABASE_URL = "postgresql://postgres:Dd152538@db.zyvcpzcoptknqszqztcj.supabase.co:5432/postgres"

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT version();")
    print("Conexiune reușită!")
    print("PostgreSQL version:", cur.fetchone())
    conn.close()
except Exception as e:
    print("Eroare la conectare:", e)
