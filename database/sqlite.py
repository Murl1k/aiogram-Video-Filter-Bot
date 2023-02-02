import sqlite3

db = sqlite3.connect('bot_database.db')
cursor = db.cursor()


async def db_start():
    cursor.execute("""CREATE TABLE IF NOT EXISTS videos (
    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    video_unique_id VARCHAR(50),
    video_id VARCHAR(150),
    filename TEXT,
    duration INT,
    size INT,
    added_user_id INT
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    telegram_id VARCHAR(150),
    videos TEXT,
    unique_videos NUMERIC
    )
    """)
    db.commit()
