# --- Tasks 1 & 2 ---
import sqlite3
import os

DB_PATH = '../db/magazines.db'
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

def fill_publishers(cursor, publisher_id, publisher_name):
    try:
        cursor.execute(
            "SELECT publisher_id FROM publishers WHERE publisher_name=?",
            (publisher_name,)
        )
        exists = cursor.fetchone()
        
        if exists:
            print(f"Publisher {publisher_name} with the id {publisher_id} already exists.")
        else:
            cursor.execute("INSERT INTO publishers (publisher_id, publisher_name) VALUES(?, ?)", (publisher_id, publisher_name))
    except Exception as e:
        print(f"Error filling publishers: {e}")
        conn.rollback()

def fill_magazines(cursor, magazine_id, magazine_name, publisher_id):
    try:
        cursor.execute(
            "SELECT magazine_id FROM magazines WHERE magazine_name=? AND publisher_id=?",
            (magazine_name, publisher_id)
        )
        exists = cursor.fetchone()
        
        if exists:
            print(f"Magazine {magazine_name} with the id {magazine_id} and publisher {publisher_id} already exists.")
        else:
            cursor.execute("INSERT INTO magazines (magazine_id, publisher_id, magazine_name) VALUES(?, ?, ?)", (magazine_id, publisher_id, magazine_name))
    except Exception as e:
        print(f"Error filling magazines: {e}")
        conn.rollback()

def fill_subscribers(cursor, subscriber_id, name, address):
    try:
        cursor.execute(
            "SELECT subscriber_id FROM subscribers WHERE name = ? AND address = ?",
            (name, address)
        )
        exists = cursor.fetchone()
        
        if exists:
            print(f"Subscriber {name} with the id {subscriber_id} and address {address} already exists.")
        else:
            cursor.execute("INSERT INTO subscribers (subscriber_id, name, address) VALUES(?, ?, ?)", (subscriber_id, name, address))
    except Exception as e:
        print(f"Error filling subscribers: {e}")
        conn.rollback()

def fill_subscriptions(cursor, subscription_id, subscriber_id, magazine_id):
    try:
        cursor.execute(
            "SELECT subscriber_id, magazine_id FROM subscriptions WHERE subscriber_id=? AND magazine_id=?",
            (subscriber_id, magazine_id)
        )
        exists = cursor.fetchone()

        if exists:
            print(f"Subscriber {subscriber_id} has already subscribed to Magazine {magazine_id}")
        else:
            cursor.execute("INSERT INTO subscriptions (subscription_id, subscriber_id, magazine_id) VALUES(?, ?, ?)", (subscription_id, subscriber_id, magazine_id))
    except Exception as e:
        print(f"Error filling subscriptions: {e}")
        conn.rollback()

conn = sqlite3.connect(DB_PATH)

conn.execute("PRAGMA foreign_keys = 1")
cursor = conn.cursor()

try:
    publishers = """
    CREATE TABLE IF NOT EXISTS publishers(
        publisher_id INTEGER PRIMARY KEY,
        publisher_name TEXT NOT NULL UNIQUE
    )"""
    
    cursor.execute(publishers)
    
    magazines = """
    CREATE TABLE IF NOT EXISTS magazines(
        magazine_id INTEGER PRIMARY KEY,
        magazine_name TEXT NOT NULL UNIQUE,
        publisher_id INTEGER NOT NULL,
        FOREIGN KEY(publisher_id) REFERENCES publishers(publisher_id)
    )"""

    cursor.execute(magazines)

    subscribers = """
    CREATE TABLE IF NOT EXISTS subscribers(
        subscriber_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        address TEXT NOT NULL,
        UNIQUE(name, address)
    )"""

    cursor.execute(subscribers)

    subscriptions = """
    CREATE TABLE IF NOT EXISTS subscriptions(
        subscription_id INTEGER PRIMARY KEY,
        subscriber_id INTEGER NOT NULL,
        magazine_id INTEGER NOT NULL,
        UNIQUE (subscriber_id, magazine_id),
        FOREIGN KEY(subscriber_id) REFERENCES subscribers(subscriber_id),
        FOREIGN KEY(magazine_id) REFERENCES magazines(magazine_id)
    )"""

    cursor.execute(subscriptions)

    # --- Task 3 ---
    fill_publishers(cursor, 1, "Publisher A")
    fill_publishers(cursor, 2, "Publisher B")
    fill_publishers(cursor, 1, "Publisher A")
    fill_publishers(cursor, 3, "Publisher C")

    fill_magazines(cursor, 1, "Magazine X", 1)
    fill_magazines(cursor, 2, "Magazine Y", 1)
    fill_magazines(cursor, 3, "Magazine Z", 2)

    fill_subscribers(cursor, 1, "John Doe", "123 Main St")
    fill_subscribers(cursor, 2, "Jane Smith", "456 Elm St")
    fill_subscribers(cursor, 3, "Alice Johnson", "789 Oak St")
    fill_subscribers(cursor, 4, "Bob Brown", "321 Pine St")

    fill_subscriptions(cursor, 1, 1, 1)
    fill_subscriptions(cursor, 2, 1, 2)
    fill_subscriptions(cursor, 3, 2, 1)
    fill_subscriptions(cursor, 4, 3, 3)

    conn.commit()

    # --- Task 4 ---
    query = """
    SELECT * FROM subscribers;
    """

    cursor.execute(query)
    print(cursor.fetchall())

    query = """
    SELECT * FROM magazines ORDER BY magazine_name ASC;
    """
    cursor.execute(query)
    print(cursor.fetchall())

    query = """
    SELECT m.magazine_name, p.publisher_name
    FROM publishers p JOIN magazines m ON p.publisher_id = m.publisher_id
    WHERE p.publisher_name='Publisher A';
    """
    cursor.execute(query)
    print(cursor.fetchall())

    conn.commit()
except Exception as e:
    print(f"Error: {e}")
    conn.rollback()

conn.close()