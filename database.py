
import sqlite3

DB_NAME = "bankpilot.db"


def initialize_database():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                receiver TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                timestamp TEXT NOT NULL,
                status TEXT NOT NULL,
                risk TEXT NOT NULL
            )
        """)


def save_transaction(transaction):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            INSERT INTO transactions
            (sender, receiver, amount, timestamp, status, risk)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            transaction["sender"],
            transaction["receiver"],
            transaction["amount"],
            transaction["timestamp"],
            transaction["status"],
            transaction["risk"]
        ))


def get_all_transactions():
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT * FROM transactions
            ORDER BY id DESC
        """).fetchall()

        return [dict(row) for row in rows]
