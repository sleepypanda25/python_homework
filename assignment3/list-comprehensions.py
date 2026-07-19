import csv

employees_content = []
first_name = -1
last_name = -1

with open('../csv/employees.csv') as file:
    reader = csv.reader(file)
    headers = next(reader)
    first_name = headers.index("first_name")
    last_name = headers.index("last_name")

    for row in reader:
        employees_content.append(row)

employee_names = [x[first_name] + " " + x[last_name] for x in employees_content]
e_employees = [x for x in employee_names if "e" in x]

print("--- Task 3 ---")
print(employee_names)
print(e_employees)