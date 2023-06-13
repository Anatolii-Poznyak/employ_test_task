"""
Script with 2 parameters. 
1 - Count of employees to create
2 - level of inheritance 
for example: python db_seeder.py 4200 4 -> will create 4200 employees. Each manager will have 4 employees. 

Important! First user without any position need to be created before using script, manually
"""

import sys
import json
import random
from faker import Faker

faker = Faker()

positions_list = [
    "CEO",
    "Team Lead",
    "Employee",
    "Intern"
    "Data Analyst",
    "Mechanical engineer",
    "HR",
    "UI Developer",
    "UI/UX ",
    "Backend Architect",
    "Frontend Architect",
    "Software Tester",
    "QA",
]


def create_positions(data):
    for i, position_name in enumerate(positions_list):
        position_record = {
            "model": "employees_structure.position",
            "pk": i + 1,
            "fields": {
                "name": position_name,
            }
        }
        data.append(position_record)
    return data


def create_employees(number_of_employees, number_of_subordinates, data):
    root_manager_pk = 1
    for i in range(1, number_of_employees):
        if i % number_of_subordinates == 0:
            root_manager_pk += 1
        record = {
            "model": "employees_structure.employee",
            "pk": i + 1,
            "fields": {
                "username": faker.simple_profile()["username"] + str(i),
                "first_name": faker.first_name(),
                "last_name": faker.last_name(),
                "middle_name": faker.last_name(),
                "email": faker.email(),
                "hired": faker.date_between(start_date='-5y', end_date='today').strftime("%Y-%m-%d"),
                "position": random.randint(1, len(positions_list)),
                "manager": root_manager_pk,
                "show_subordinates": True,
            }
        }
        data.append(record)
    return data


def write_to_json(data):
    with open("employee_data.json", "w") as json_file:
        json.dump(data, json_file, indent=4, separators=(",", ": "))


def print_success_message(number_of_employees):
    print("\033[92mCreation of {} employees was successful!\033[0m".format(number_of_employees))


def main():
    data = []
    if len(sys.argv) != 3:
        print("Usage: python db_seeder.py <number_of_employees> <number_of_subordinates>")
        sys.exit()

    number_of_employees = int(sys.argv[1])
    number_of_subordinates = int(sys.argv[2])
    data = create_positions(data)
    data = create_employees(number_of_employees, number_of_subordinates, data)
    write_to_json(data)
    print_success_message(number_of_employees)


if __name__ == "__main__":
    main()
