import os

from django.core.management.base import BaseCommand
from employees_structure.models import Employee


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not Employee.objects.filter(username=os.environ["ADMIN_USERNAME"]).exists():
            Employee.objects.create_superuser(
                os.environ["ADMIN_USERNAME"],
                os.environ["ADMIN_PASSWORD"],
                os.environ["ADMIN_EMAIL"],
                os.environ["ADMIN_FIRST_NAME"],
                os.environ["ADMIN_LAST_NAME"],
                os.environ["ADMIN_MIDDLE_NAME"],
            )