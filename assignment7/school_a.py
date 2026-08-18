import sqlite3

# Pass cursor to function so it can execute SQL commands
def add_student(cursor, name, age, major):
    try:
        cursor.execute("INSERT INTO Students (name, age, major) VALUES(?,?,?)", (name, age, major))
    except sqlite3.IntegrityError:
        print(f"Error: Student with name {name} already exists.")

def add_course(cursor, course_name, instructor_name):
    try:
        cursor.execute("INSERT INTO Courses (course_name, instructor_name) VALUES(?,?)", (course_name, instructor_name))
    except sqlite3.IntegrityError:
        print(f"Error: Course with name {course_name} already exists.")

def enroll_student(cursor, student, course):
    # Tuple with one element needs comma
    cursor.execute("SELECT * FROM Students WHERE name = ?", (student,))
    results = cursor.fetchall()
    if len(results) > 0:
        student_id = results[0][0]
    else:
        print(f"There was no student named {student}.")
        return
    cursor.execute("SELECT * FROM Courses WHERE course_name = ?", (course,))
    results = cursor.fetchall()
    if len(results) > 0:
        course_id = results[0][0]
    else:
        print(f"There was no course named {course}.")
        return
    cursor.execute("INSERT INTO Enrollments (student_id, course_id) VALUES (?, ?)", (student_id, course_id))

with  sqlite3.connect("../db/school.db") as conn:
    print("Database created and connected successfully.")

    cursor = conn.cursor()

    # Creates table named Students if it doesn't already exist
    # Text after column names (e.g. student_id) specifies constraints
    #   - e.g. 
    #       - student_id is an integer column that also serves as the primary key
    #       - name is a text column that can't be null and must be unique
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Students (
        student_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        age INTEGER,
        major TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Courses (
        course_id INTEGER PRIMARY KEY,
        course_name TEXT NOT NULL UNIQUE,
        instructor_name TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Enrollments (
        enrollment_id INTEGER PRIMARY KEY,
        student_id INTEGER,
        course_id INTEGER,
        FOREIGN KEY (student_id) REFERENCES Students(student_id),
        FOREIGN KEY (course_id) REFERENCES Courses(course_id)
    )
    """)

    print("Tables created successfully.")

    add_student(cursor, 'Jasmine', 20, 'Computer Science')
    add_student(cursor, 'Pratik', 22, 'History')
    add_student(cursor, 'Carlos', 19, 'Biology')
    add_course(cursor, 'Math 101', 'Dr. Sanchez')
    add_course(cursor, 'English 101', 'Ms. Jones')
    add_course(cursor, 'Chemistry 101', 'Dr. Lee')

    # cursor.execute("INSERT INTO Students (name, age, major) VALUES('Jasmine', 20, 'Computer Science')")
    # cursor.execute("Insert INTO Students (name, age, major) VALUES('Pratik', 22, 'History')")
    # cursor.execute("INSERT INTO Students (name, age, major) VALUES ('Carlos', 19, 'Biology')") 
    # cursor.execute("INSERT INTO Courses (course_name, instructor_name) VALUES ('Math 101', 'Dr. Sanchez')")
    # cursor.execute("INSERT INTO Courses (course_name, instructor_name) VALUES ('English 101', 'Ms. Jones')") 
    # cursor.execute("INSERT INTO Courses (course_name, instructor_name) VALUES ('Chemistry 101', 'Dr. Lee')") 

    conn.commit()
    print("Sample data inserted successfully.")

    cursor.execute("SELECT * FROM Students WHERE name = 'Jasmine'")
    result = cursor.fetchall()
    for row in result:
        print(row)

    enroll_student(cursor, 'Jasmine', 'Math 101')
    enroll_student(cursor, "Jasmine", "Chemistry 101")
    enroll_student(cursor, "Pratik", "Math 101")
    enroll_student(cursor, "Pratik", "English 101")
    enroll_student(cursor, "Carlos", "English 101")

    conn.commit()