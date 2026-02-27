import sqlite3
import aiosqlite
from pathlib import Path

DB_PATH = Path(__file__).parent / "prism.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                tier TEXT DEFAULT 'free',
                is_active INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_login TEXT
            )
        ''')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS usage_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                endpoint TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        await db.commit()

async def get_db():
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    try:
        yield db
    finally:
        await db.close()

# Helper queries
async def get_user_by_email(email: str):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE email = ?", (email,)) as cursor:
            return await cursor.fetchone()

async def get_user_by_id(user_id: str):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE id = ?", (user_id,)) as cursor:
            return await cursor.fetchone()

async def log_usage(user_id: str, endpoint: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO usage_logs (user_id, endpoint) VALUES (?, ?)",
            (user_id, endpoint)
        )
        await db.commit()

async def get_today_usage(user_id: str, endpoint: str) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('''
            SELECT COUNT(*) 
            FROM usage_logs 
            WHERE user_id = ? 
              AND endpoint = ? 
              AND date(created_at) = date('now')
        ''', (user_id, endpoint)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0
