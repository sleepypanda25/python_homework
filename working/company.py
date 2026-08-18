import sqlite3
import os

# Note, you need to create a 'db' directory if it isn't already in your workspace
DB_PATH = "../db/company.db"

# Start fresh so results are predictable when re-running this script
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

# --- Schema ---
cursor.executescript("""
CREATE TABLE Departments (
  department_id   INTEGER PRIMARY KEY,
  department_name TEXT NOT NULL UNIQUE,
  manager_id      INTEGER  -- (left without FK to avoid circular reference)
);
CREATE TABLE Employees (
  employee_id   INTEGER PRIMARY KEY,
  first_name    TEXT NOT NULL,
  last_name     TEXT NOT NULL,
  department_id INTEGER NOT NULL,
  title         TEXT NOT NULL,
  salary        INTEGER NOT NULL,
  hire_date     TEXT DEFAULT (date('now')),
  FOREIGN KEY (department_id) REFERENCES Departments(department_id)
);
""")

# --- Seed data ---
cursor.executemany(
    "INSERT INTO Departments(department_id, department_name) VALUES (?, ?);",
    [
        (10, "Engineering"),
        (20, "Sales"),
        (30, "HR"),
        (40, "Finance"),
        (50, "R&D"),
    ],
)

employees = [
    # Engineering (dept 10)
    (1, "Alice", "Nguyen", 10, "Software Engineer",        120000, "2019-05-01"),
    (2, "Bob",   "Smith",  10, "Senior Software Engineer", 135000, "2018-07-15"),
    (3, "Carol", "Zhang",  10, "Staff Engineer",           135000, "2017-03-20"),  # tie
    (4, "David", "Lee",    10, "QA Engineer",               95000, "2021-11-02"),

    # Sales (dept 20)
    (5, "Eve",   "Martinez", 20, "Sales Associate",         90000, "2020-01-10"),
    (6, "Frank", "O'Connor", 20, "Account Executive",      110000, "2016-09-29"),
    (7, "Grace", "Kim",      20, "Sales Manager",          105000, "2015-04-12"),

    # HR (dept 30) -> avg ~68.5k (so it will be filtered out by HAVING > 70000)
    (8, "Heidi", "Brown", 30, "HR Generalist",              65000, "2022-06-03"),
    (9, "Ivan",  "Garcia", 30, "HR Manager",                72000, "2019-08-21"),

    # Finance (dept 40)
    (10, "Judy", "Wilson", 40, "Financial Analyst",        125000, "2017-02-17"),
    (11, "Karl", "Davis",  40, "Finance Director",         130000, "2014-12-09"),

    # R&D (dept 50)
    (12, "Liam", "Patel",  50, "Research Scientist",       150000, "2018-10-31"),
    (13, "Mia",  "Chen",   50, "Principal Scientist",      150000, "2013-05-07"),   # tie
]

cursor.executemany(
    """INSERT INTO Employees
       (employee_id, first_name, last_name, department_id, title, salary, hire_date)
       VALUES (?, ?, ?, ?, ?, ?, ?);""",
    employees,
)

# Assign managers by employee_id for each department
cursor.executemany(
    "UPDATE Departments SET manager_id = ? WHERE department_id = ?;",
    [
        (2, 10),   # Engineering -> Bob Smith
        (7, 20),   # Sales -> Grace Kim
        (9, 30),   # HR -> Ivan Garcia
        (11, 40),  # Finance -> Karl Davis
        (13, 50),  # R&D -> Mia Chen
    ],
)

conn.commit()

print("company.db created with Departments(department_name, manager_id) and Employees.")

# Execute the query
query = """
SELECT department_id, employee_id, salary
FROM Employees AS e
WHERE salary = (
    SELECT MAX(salary)
    FROM Employees
    WHERE department_id = e.department_id
);
"""
cursor.execute(query)
print(cursor.fetchall())

# Lesson 10.2 Complex JOINs
creation = """
CREATE TABLE IF NOT EXISTS Projects(
  id   INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  department_id INTEGER NOT NULL,
  FOREIGN KEY (department_id) REFERENCES Departments(department_id)
);
"""

cursor.execute(creation)

insertion = """
INSERT INTO Projects (name, department_id) VALUES
    ('Project A', (SELECT department_id FROM Departments WHERE department_name = 'HR')),
    ('Project B', (SELECT department_id FROM Departments WHERE department_name = 'Engineering')),
('Project C', (SELECT department_id FROM Departments WHERE department_name = 'Finance'));
"""

cursor.execute(insertion)

join = """
SELECT (e.first_name || ' ' || e.last_name) AS employee_name, p.name as project_name 
FROM Employees e 
JOIN Projects p ON e.department_id = p.department_id
WHERE p.name = 'Project A';
"""

cursor.execute(join)

conn.commit()
conn.close()

# Lesson 10.3 Aggregation
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

query = """
SELECT department_id,
    MIN(e.salary) AS min_salary,
    MAX(e.salary) AS max_salary
FROM Employees e
GROUP BY department_id;
"""

cursor.execute(query)
print(cursor.fetchall())

# Lesson 10.4 Aggregation with HAVING
query = """
SELECT d.department_id,
    d.department_name,
    d.manager_id,
    AVG(e.salary) AS avg_salary
FROM Departments d
JOIN Employees e ON d.department_id = e.department_id
GROUP BY d.department_id
HAVING avg_salary > 70000;
"""

cursor.execute(query)
print(cursor.fetchall())

query = """
WITH dept_avg AS (
    SELECT e.department_id, AVG(e.salary) AS avg_salary
    FROM Employees e
    GROUP BY e.department_id
)
SELECT d.department_name,
    (m.first_name || ' ' || m.last_name) AS manager_name,
    da.avg_salary
FROM dept_avg da
JOIN Departments d ON d.department_id = da.department_id
LEFT JOIN Employees AS m ON m.employee_id = d.manager_id
WHERE da.avg_salary > 70000;
"""

cursor.execute(query)
print(cursor.fetchall())

# Lesson 10.5 Performance Optimization: Indexing
cursor.execute("CREATE INDEX idx_department ON Employees(department_id);")

# Lesson 10.6 Transactions and Rollbacks
try:
    cursor.execute("INSERT INTO Employees (name, department_id) VALUES ('Mario Rossi', 2)")
    cursor.execute("INSERT INTO Employees (name, department_id) VALUES ('Yamada Hanako', 3)")
    conn.commit()  # Commit transaction
except Exception as e:
    conn.rollback()  # Rollback transaction if there's an error
    print("Error:", e)

# Lesson 10.7: Parameterized Queries to Prevent SQL Injection

# DO NOT DO THIS (vulnerable to SQL injection)
# - user input is treated as SQL code, not data --> vulnerable to SQL injections
# cursor.execute(f"SELECT * FROM Employees WHERE department_id = {department_id};")
# OR
# cursor.execute("SELECT * FROM Employees WHERE department_id = " + department_id + ";")

# Potential SQL injection example:
# SELECT * FROM Employees WHERE department_id = 1 OR 1=1;

# INSTEAD:
# - user input is treated as data, not SQL code
# cursor.execute("SELECT * FROM Employees WHERE department_id = ?;", (department_id,))

# Lesson 10.8: Window Functions
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

query = """
SELECT (e.first_name || ' ' || e.last_name) AS employee_name,
    e.salary,
    e.department_id,
    RANK() OVER (PARTITION by e.department_id ORDER BY e.salary DESC) AS rank
    FROM Employees e;
"""

cursor.execute(query)
print(cursor.fetchall())

conn.commit()
conn.close()

# Lesson 10.9 Date and Time Functions
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

query = """
SELECT (e.first_name || ' ' || e.last_name) AS employee_name,
    e.hire_date,
    ROUND(JULIANDAY('now') - JULIANDAY(e.hire_date), 2) AS tenure_in_days
FROM Employees e;
"""

cursor.execute(query)

conn.commit()
conn.close()