import sqlite3
import pandas as pd
from datetime import date

with sqlite3.connect("../db/lesson.db") as conn:
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()

    # --- Task 1 ---
    task_1 = """
    SELECT o.order_id, SUM(p.price * li.quantity) as total_price
    FROM line_items li
    JOIN orders o ON o.order_id = li.order_id
    JOIN products p ON p.product_id = li.product_id
    GROUP BY o.order_id
    ORDER BY o.order_id
    LIMIT 5
    """

    print("\n--- Task 1 ---")
    cursor.execute(task_1)
    print(cursor.fetchall())

    # --- Task 2 ---
    task_2 = """
    SELECT c.customer_name, AVG(total.total_price) AS average_price
    FROM customers c
    LEFT JOIN (
        SELECT o.customer_id AS customer_id_b, SUM(p.price * li.quantity) AS total_price
        FROM line_items li
        JOIN orders o ON li.order_id = o.order_id
        JOIN products p ON p.product_id = li.product_id
        GROUP BY o.order_id
    ) total ON c.customer_id = customer_id_b
    GROUP BY c.customer_id
    """

    print("\n--- Task 2 ---")
    cursor.execute(task_2)
    print(cursor.fetchall())

    # --- Task 3 ---
    customer_name = "Perez and Sons"
    employee_first_name = "Miranda"
    employee_last_name = "Harris"

    cursor.execute("SELECT c.customer_id FROM customers c WHERE c.customer_name = ?", (customer_name,))
    customer_id = cursor.fetchone()[0]

    task_5_products = """
    SELECT p.product_id
    FROM products p
    ORDER BY p.price
    LIMIT 5
    """

    cursor.execute(task_5_products)
    products = cursor.fetchall()

    cursor.execute("SELECT e.employee_id FROM employees e WHERE e.first_name = ? AND e.last_name = ?", (employee_first_name, employee_last_name))
    employee_id = cursor.fetchone()[0]

    try:
        today = date.today().strftime('%Y-%m-%d')

        cursor.execute("INSERT INTO orders (customer_id, employee_id, date) VALUES(?, ?, ?) RETURNING order_id", (customer_id, employee_id, today))
        
        order_id = cursor.fetchone()[0]

        for product_id_tuple in products:
            product_id = product_id_tuple[0]
            cursor.execute("INSERT INTO line_items (order_id, product_id, quantity) VALUES(?, ?, ?)", (order_id, product_id, 10))
            
        conn.commit()

        query = """
        SELECT li.line_item_id, p.product_name, li.quantity
        FROM line_items li
        JOIN products p ON li.product_id = p.product_id
        WHERE li.order_id = ?
        """

        print("\n--- Task 3 ---")
        cursor.execute(query, (order_id,))
        print(cursor.fetchall())
    except Exception as e:
        conn.rollback()
        print(e)

    # --- Task 4 ---
    task_4 = """
    SELECT e.first_name, e.last_name, COUNT(o.order_id)
    FROM employees e
    JOIN orders o ON o.employee_id = e.employee_id
    GROUP BY e.employee_id
    HAVING COUNT(o.order_id) > 5
    """

    print("\n--- Task 4 ---")
    cursor.execute(task_4)
    print(cursor.fetchall())
