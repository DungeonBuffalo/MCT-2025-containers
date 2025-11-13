import psycopg2
import os
import time
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_ADMIN_USER = "postgres"
DB_ADMIN_PASSWORD = "postgres"
DB_NAME = os.getenv("DB_NAME", "app")

for _ in range(30):
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_ADMIN_USER,
            password=DB_ADMIN_PASSWORD,
            dbname="postgres"
        )
        conn.close()
        break
    except Exception:
        print("Waiting for database to be ready...")
        time.sleep(2)

conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_ADMIN_USER,
    password=DB_ADMIN_PASSWORD,
    dbname="postgres",
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

cur.execute("SELECT 1 FROM pg_roles WHERE rolname = 'user'")
if not cur.fetchone():
    cur.execute("CREATE ROLE user WITH LOGIN PASSWORD 'password';")
    print("Created role 'user'.")

cur.execute("SELECT 1 FROM pg_database WHERE datname = 'app'")
if not cur.fetchone():
    cur.execute("CREATE DATABASE app OWNER user;")
    print("Created database 'app'.")

cur.close()
conn.close()

conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    user="user",
    password="password",
    dbname=DB_NAME,
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