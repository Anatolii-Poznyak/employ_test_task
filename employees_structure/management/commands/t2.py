import json
import random
from faker import Faker

faker = Faker()

positions_list = [
    "Contractor",
    "Accountant",
    "Games developer",
    "Mechanical engineer",
    "Media planner",
    "Designer",
    "Backend Developer",
    "Frontend Developer",
    "QA",
    "Data processing manager"
]

data = []

# Create Position records first
for i, position_name in enumerate(positions_list):
    position_record = {
        "model": "employees_structure.position",
        "pk": i + 1,
        "fields": {
            "name": position_name,
        }
    }
    data.append(position_record)

# Create the root manager
root_manager_pk = 1

# Create Employees
for i in range(1, 1000):  # Start from 1 because root manager already exists
    # Track the manager for this employee
    if i % 10 == 0:
        root_manager_pk += 1
    record = {
        "model": "employees_structure.employee",
        "pk": i + 1,  # primary key starts from 1, increment because first employee already exists
        "fields": {
            "username": faker.simple_profile()["username"] + str(i),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "middle_name": faker.last_name(),
            "email": faker.email(),
            "hired": faker.date_between(start_date='-5y', end_date='today').strftime("%Y-%m-%d"),
            "position": random.randint(1, len(positions_list)),  # Assign a position pk
            "manager": root_manager_pk,  # Assign a manager with a lower pk
            "show_subordinates": True,
        }
    }
    data.append(record)

with open("../../../employee_data.json", "w") as json_file:
    json.dump(data, json_file)
