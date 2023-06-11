import random
from django.core.management.base import BaseCommand
from employees_structure.models import Employee, Position
from mimesis import Person, Datetime
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        positions = ['Manager', 'Employee', 'Team Lead', 'Intern', 'HR']
        Position.objects.bulk_create([Position(name=position) for position in positions])
        positions = Position.objects.all()
        all_employees = []
        for i in range(total):
            person = Person()
            hired_date = Datetime().date(start=2000, end=2023).isoformat()
            position = random.choice(positions)
            employee = Employee(
                username=person.username(),
                password=make_password('password123'),
                first_name=person.first_name(),
                last_name=person.last_name(),
                middle_name=person.last_name(),
                email=person.email(),
                hired=hired_date,
                position=position,
            )
            all_employees.append(employee)
        Employee.objects.bulk_create(all_employees)

        all_employees = list(Employee.objects.all())
        for i, employee in enumerate(all_employees[1:], 1):
            manager = random.choice(all_employees[:max(1, int(i * 0.07))])  # limit management level
            employee.manager = manager
        Employee.objects.bulk_update(all_employees, ['manager'])

        self.stdout.write(self.style.SUCCESS(f'{total} users were created successfully!'))
