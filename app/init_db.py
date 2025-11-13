import psycopg2
import os
import time
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_ADMIN_USER = "postgres"
DB_ADMIN_PASSWORD = "postgres"
DB_NAME = os.getenv("DB_NAME", "app")

for attempt in range(60):
    try:
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT,
            user=DB_ADMIN_USER, password=DB_ADMIN_PASSWORD,
            dbname="postgres"
        )
        conn.close()
        print("PostgreSQL is reachable.")
        break
    except Exception as e:
        print(f"[{attempt+1}/60] Waiting for DB... ({e})")
        time.sleep(2)
else:
    print("PostgreSQL not reachable in time.")
    exit(1)

conn = psycopg2.connect(
    host=DB_HOST, port=DB_PORT,
    user=DB_ADMIN_USER, password=DB_ADMIN_PASSWORD,
    dbname="postgres"
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

cur.close()
conn.close()

conn = psycopg2.connect(
    host=DB_HOST, port=DB_PORT,
    user="user", password="password", dbname=DB_NAME
)
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS visits (
        id SERIAL PRIMARY KEY,
        ip VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")
conn.commit()
cur.close()
conn.close()

print("Database initialization complete.")