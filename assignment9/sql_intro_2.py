# --- Task 5 ---
# (incomplete)
import pandas as pd
import sqlite3

with sqlite3.connect("../db/magazines.db") as conn:
    sql_statement = """
    SELECT s.name, m.magazine_name, p.publisher_name
    FROM subscriptions sub
    JOIN subscribers s ON sub.subscriber_id = s.subscriber_id
    JOIN magazines m ON sub.magazine_id = m.magazine_id
    JOIN publishers p ON m.publisher_id = p.publisher_id
    """
    df = pd.read_sql_query(sql_statement, conn)
    print(df)