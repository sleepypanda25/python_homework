import pandas as pd

# --- Task 1: Introduction to Pandas - Creating and Manipulating DataFrames ---
people = {
    'Name':['Alice', 'Bob', 'Charlie'],
    'Age':[25, 30, 35],
    'City':['New York', 'Los Angeles', 'Chicago']
}

print("--- Task 1 ---")

# --- Task 1: Part 1 ---
task1_data_frame = pd.DataFrame(people)
print(task1_data_frame)

# --- Task 1: Part 2 ---
task1_with_salary = task1_data_frame.copy()
task1_with_salary['Salary'] = [70000, 80000, 90000]

print(task1_with_salary)

# --- Task 1: Part 3 ---
age_column = task1_with_salary['Age'].copy()

for i in range(len(age_column)):
    age_column[i] += 1

task1_older = task1_with_salary.copy()
task1_older['Age'] = age_column

print(task1_older)

# --- Task 1: Part 4 ---
task1_older.to_csv("employees.csv", index=False)


# --- Task 2: Loading Data from CSV and JSON ---
task2_employees = pd.read_csv("employees.csv")

print("\n--- Task 2 ---")

# --- Task 2: Part 1 ---
print(task2_employees)

# --- Task 2: Part 2 ---
json_employees = pd.read_json("additional_employees.json")

print(json_employees)

# --- Task 2: Part 3 ---
more_employees = pd.concat([task2_employees, json_employees], ignore_index=True)

print(more_employees)


# --- Task 3: Data Inspection - Using Head, Tail, and Info Methods ---
print("\n--- Task 3 ---")

# --- Task 3: Part 1 ---
first_three = more_employees.head(3)

print(first_three)

# --- Task 3: Part 2 ---
last_two = more_employees.tail(2)

print(last_two)

# --- Task 3: Part 3 ---
employee_shape = more_employees.shape

print(employee_shape)

# --- Task 3: Part 4 ---
print(more_employees.info())


# --- Task 4: Data Cleaning ---
print("\n--- Task 4 ---")

# --- Task 4: Part 1 ---
dirty_data = pd.read_csv("dirty_data.csv")

print(dirty_data)

clean_data = dirty_data.copy()

# --- Task 4: Part 2 ---
clean_data = clean_data.drop_duplicates()

print(clean_data)

# --- Task 4: Part 3 ---
clean_data["Age"] = pd.to_numeric(clean_data["Age"], errors="coerce")

print(clean_data)

# --- Task 4: Part 4 ---
clean_data["Salary"] = pd.to_numeric(clean_data["Salary"], errors="coerce")
clean_data["Salary"] = clean_data["Salary"].replace("unknown", pd.NA)
clean_data["Salary"] = clean_data["Salary"].replace("n/a", pd.NA)

print(clean_data)

# --- Task 4: Part 5 ---
age_mean = clean_data["Age"].mean()
clean_data["Age"] = clean_data["Age"].fillna(age_mean)

salary_median = clean_data["Salary"].median()
clean_data["Salary"] = clean_data["Salary"].fillna(salary_median)

# --- Task 4: Part 6 ---
clean_data["Hire Date"] = pd.to_datetime(clean_data["Hire Date"], format="mixed", errors="coerce")

print(clean_data)

# --- Task 4: Part 7 ---
clean_data["Name"] = clean_data["Name"].str.strip()
clean_data["Name"] = clean_data["Name"].str.upper()

clean_data["Department"] = clean_data["Department"].str.strip()
clean_data["Department"] = clean_data["Department"].str.upper()

print(clean_data)