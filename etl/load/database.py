import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def create_tables():
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                CREATE TABLE IF NOT EXISTS tracks (
                    track_id TEXT PRIMARY KEY,
                    track_name TEXT,
                    artist_name TEXT,
                    album_name TEXT
                );
                """)

                cur.execute("""
                CREATE TABLE IF NOT EXISTS listening_history (
                    id SERIAL PRIMARY KEY,
                    track_id TEXT REFERENCES tracks(track_id),
                    played_at TIMESTAMP,
                    UNIQUE(played_at) -- ESTO ES LO QUE SALVA TU PIPELINE
                );
                """)
    finally:
        conn.close()

def insert_tracks(tracks):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                for t in tracks:
                    cur.execute("""
                    INSERT INTO tracks (track_id, track_name, artist_name, album_name)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (track_id) DO NOTHING;
                    """, (
                        t["track_id"],
                        t["track_name"],
                        t["artist_name"],
                        t["album_name"]
                    ))
    finally:
        conn.close()

def insert_history(history):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                for h in history:
                    cur.execute("""
                    INSERT INTO listening_history (track_id, played_at)
                    VALUES (%s, %s)
                    ON CONFLICT (played_at) DO NOTHING; -- AHORA SI TIENE SENTIDO
                    """, (
                        h["track_id"],
                        h["played_at"]
                    ))
    finally:
        conn.close()