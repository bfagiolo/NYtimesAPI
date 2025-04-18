
import sqlite3
import os
from datetime import datetime

def get_db_path():
    folder = os.path.join(os.path.expanduser("~"), "Documents", "NYTApp")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, "nyt_archive.db")

def connect():
    return sqlite3.connect(get_db_path())

def initialize_database():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS searches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        actual_date_searched TEXT UNIQUE,
        search_date TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        search_id INTEGER,
        title TEXT,
        section TEXT,
        summary TEXT,
        url TEXT,
        pub_date TEXT,
        FOREIGN KEY(search_id) REFERENCES searches(id)
    )
    ''')

    conn.commit()
    conn.close()

def has_already_searched(date_str):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM searches WHERE actual_date_searched = ?", (date_str,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def save_search_and_articles(actual_date, today_date, articles):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO searches (actual_date_searched, search_date) VALUES (?, ?)", (actual_date, today_date))
    search_id = cursor.lastrowid

    for a in articles:
        cursor.execute('''
            INSERT INTO articles (search_id, title, section, summary, url, pub_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (search_id, a.title, a.section, a.summary, a.url, a.pub_date))

    conn.commit()
    conn.close()
