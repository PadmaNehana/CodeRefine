import sqlite3
import json

DB_NAME = "coderefine.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            repo TEXT,
            pr_number INTEGER,
            review TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_review(repo: str, pr_number: int, review: dict):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO reviews (repo, pr_number, review) VALUES (?, ?, ?)",
        (repo, pr_number, json.dumps(review)),
    )

    conn.commit()
    conn.close()
def get_latest_review():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT review FROM reviews ORDER BY id DESC LIMIT 1"
    )
    row = cursor.fetchone()

    conn.close()

    if row:
        return json.loads(row[0])

    return {"message": "No PR reviewed yet"}