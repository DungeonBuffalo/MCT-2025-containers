from fastapi import FastAPI, Request
import psycopg2
from psycopg2.extras import RealDictCursor
import redis
import os

app = FastAPI()

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_NAME = os.getenv("DB_NAME", "visits_db")

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME,
        cursor_factory=RealDictCursor,
    )

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


@app.get("/ping")
def ping(request: Request):
    client_ip = request.client.host

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO visits (ip) VALUES (%s)", (client_ip,))
    conn.commit()
    cur.close()
    conn.close()

    redis_client.incr("ping_count")

    return {"response": "pong"}


@app.get("/visits")
def visits():
    cached_value = redis_client.get("ping_count")

    if cached_value is not None:
        return {"visits": int(cached_value), "source": "cache"}

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS cnt FROM visits")
    count = cur.fetchone()["cnt"]
    cur.close()
    conn.close()

    redis_client.set("ping_count", count)

    return {"visits": count, "source": "db"}