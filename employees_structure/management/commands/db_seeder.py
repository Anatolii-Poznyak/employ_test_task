"""
Script with 2 parameters. 
1 - Count of employees to create
2 - level of inheritance 
for example: python db_seeder.py 4200 4 -> will create 4200 employees. Each manager will have 4 employees. 

Important! First user without any position need to be created before using script, manually
"""
from django.core.management.base import BaseCommand

import json
import random
import sys

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


class Command(BaseCommand):
    help = "Create json file with fake employees for future load in DB"

    def add_arguments(self, parser):
        parser.add_argument("employees", type=int)
        parser.add_argument("subordinates", type=int)

    def print_success_message(self, number_of_employees):
        print(f"\033[92m  Creation of {number_of_employees} employees was successful!\033[0m")

    def create_positions(self, data):
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

    def write_to_json(self, data):
        with open("/app/employee_data.json", "w") as json_file:
            json.dump(data, json_file, indent=4, separators=(",", ": "))

    def create_employees(self, number_of_employees, number_of_subordinates, data):
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

    def handle(self, *args, **options):
        data = []

        if not options["employees"]:
            if len(sys.argv) != 3:
                print("\n  Usage: python db_seeder.py <number_of_employees> <number_of_subordinates>")
                sys.exit()
            number_of_employees = int(sys.argv[1])
            number_of_subordinates = int(sys.argv[2])

        else:
            number_of_employees = options["employees"]
            number_of_subordinates = options["subordinates"]
            print(
                f"\n\033[93m  Usage: python manage.py db_seeder {number_of_employees} {number_of_subordinates}\033[0m"
            )

        data = self.create_positions(data)
        data = self.create_employees(number_of_employees, number_of_subordinates, data)
        self.write_to_json(data)
        self.print_success_message(number_of_employees)
