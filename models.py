import sqlite3

DB_PATH = "students.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                roll TEXT UNIQUE NOT NULL,
                capacity REAL,
                sleep_start INTEGER,
                sleep_end INTEGER
            )
        """)

def add_student(name, roll, sleep_start, sleep_end, capacity):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO students VALUES (NULL, ?, ?, ?, ?, ?)", 
                    (name, roll, capacity, sleep_start, sleep_end))

def get_all_students():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT name, roll FROM students").fetchall()

def get_student_by_roll(roll):
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT * FROM students WHERE roll=?", (roll,)).fetchone()