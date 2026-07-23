import csv
import traceback
import os
import custom_module
from datetime import datetime

# --- Task 2: Read a CSV File ---
def read_employees():
    employees_data = {}
    rows = []

    try:
        with open('../csv/employees.csv') as file:
            reader = csv.reader(file)
            employees_data["fields"] = next(reader)

            for row in reader:
                rows.append(row)

            employees_data["rows"] = rows
        
        return employees_data
    except Exception as e:
        print("An exception occurred." + type(e).__name__)
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
        print(f"Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")

employees = read_employees()

print("--- Task 2 ---")
print(employees)

# --- Task 3: Find the Column Index ---
def column_index(header):
    return employees["fields"].index(header)

employee_id_column = column_index("employee_id")

print("--- Task 3 ---")
print(employee_id_column)

# --- Task 4: Find the Employee First Name ---
def first_name(row_num):
    index = employees["fields"].index("first_name")
    name = employees["rows"][row_num][index]

    return name

# --- Task 5: Find the Employee: a Function in a Function
def employee_find(employee_id):
    def employee_match(row):
        return int(row[employee_id_column]) == employee_id
    
    matches = list(filter(employee_match, employees["rows"]))
    return matches

# --- Task 6: Find the Employee with a Lambda ---
def employee_find_2(employee_id):
   matches = list(filter(lambda row : int(row[employee_id_column]) == employee_id , employees["rows"]))
   return matches

# --- Task 7: Sort the Rows by last_name Using a Lambda ---
def sort_by_last_name():
    index = column_index("last_name")
    
    employees["rows"].sort(key=(lambda row : row[index]))

    return employees["rows"]

# --- Task 8: Create a dict for an Employee ---
def employee_dict(row):
    employee_info = {}

    for index in range(len(employees["fields"])):
        field = employees["fields"][index]
        if field != "employee_id":
            employee_info[field] = row[index]
    
    return employee_info

print("--- Task 8 ---")
print(employee_dict(employees["rows"][0]))

# --- Task 9: A dict of dicts, for All Employees ---
def all_employees_dict():
    all_employees = {}
    employee_id_index = employees["fields"].index("employee_id")

    for employee in employees["rows"]:
        all_employees[employee[employee_id_index]] = employee_dict(employee)
    
    return all_employees

print(all_employees_dict())

# --- Task 10: Use the os Module ---
def get_this_value():
    return os.getenv("THISVALUE")

print("--- Task 10 ---")
print(get_this_value())

# --- Task 11: Creating Your Own Module ---
def set_that_secret(secret):
    custom_module.set_secret(secret)

set_that_secret("chicken")
print("--- Task 11 ---")
print(custom_module.secret)

# --- Task 12: Read minutes1.csv and minutes 2.csv ---
def read_minutes():
    minutes1_local = read_minutes_csv("../csv/minutes1.csv")
    minutes2_local = read_minutes_csv("../csv/minutes2.csv")
    
    return minutes1_local, minutes2_local

def read_minutes_csv(csv_file):
    minutes = {}
    rows = []

    with open(csv_file) as file:
        reader = csv.reader(file)
        minutes["fields"] = next(reader)

        for row in reader:
            row = tuple(row)
            rows.append(row)
        
        minutes["rows"] = rows
    return minutes

minutes1, minutes2 = read_minutes()
print("--- Task 12 ---")
print("Minutes1: " + str(minutes1))
print("Minutes2: " + str(minutes2))

# --- Task 13: Create minutes_set ---
def create_minutes_set():
    set1 = set(minutes1["rows"])
    set2 = set(minutes2["rows"])

    for row in set2:
        set1.add(row)

    return set1

minutes_set = create_minutes_set()
print("--- Task 13 ---")
print(minutes_set)

# --- Task 14: Convert to datetime ---
def create_minutes_list():
    minutes_list_local = map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")), minutes_set)

    return list(minutes_list_local)

minutes_list = create_minutes_list()
print("--- Task 14 ---")
print(minutes_list)

# --- Task 15: Write Out Sorted List ---
def write_sorted_list():
    minutes_list.sort(key=lambda x: x[1])
    converted_minutes_list = map(lambda x: (x[0], datetime.strftime(x[1], "%B %d, %Y")), minutes_list)
    converted_minutes_list2 = map(lambda x: (x[0], datetime.strftime(x[1], "%B %d, %Y")), minutes_list)

    with open("./minutes.csv", "w") as file:
        writer = csv.writer(file)
        
        writer.writerow(minutes1["fields"])

        for row in converted_minutes_list2:
            writer.writerow(row)

    return list(converted_minutes_list)

sorted_list = write_sorted_list()
print("--- Task 15 ---")
print(sorted_list)