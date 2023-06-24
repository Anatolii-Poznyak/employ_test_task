import os

from django.core.management.base import BaseCommand
from employees_structure.models import Employee


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not Employee.objects.filter(username=os.environ["ADMIN_USERNAME"]).exists():
            employee = Employee.objects.create_superuser(
                username=os.environ["ADMIN_USERNAME"],
                password=os.environ["ADMIN_PASSWORD"],
                email=os.environ["ADMIN_EMAIL"],
                first_name=os.environ["ADMIN_FIRST_NAME"],
                last_name=os.environ["ADMIN_LAST_NAME"],
                middle_name=os.environ["ADMIN_MIDDLE_NAME"],
            )
            print(f"\033[92m  Superuser {employee.username} was created successfully!\033[0m")
