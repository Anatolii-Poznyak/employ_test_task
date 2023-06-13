from django.test import TestCase

from employees_structure.forms import (
    BaseEmployeeForm,
    EmployeeCreationForm,
    EmployeeSearchForm,
    TransferSubordinatesForm,
)
from employees_structure.models import Position, Employee


class BaseEmployeeFormTest(TestCase):
    def test_valid_data(self):
        position = Position.objects.create(name="position1")
        form = BaseEmployeeForm(
            {
                "username": "test_user",
                "password1": "abcdef123456",
                "password2": "abcdef123456",
                "last_name": "Test",
                "first_name": "User",
                "middle_name": "Tester",
                "hired": "2023-05-31",
                "email": "testuser@example.com",
                "position": position.id,
                "manager": None,
            }
        )
        self.assertTrue(form.is_valid())
        employee = form.save()
        self.assertEqual(employee.username, "test_user")
        self.assertEqual(employee.email, "testuser@example.com")


class EmployeeCreationFormTest(TestCase):
    def test_valid_data(self):
        position = Position.objects.create(name="position1")
        form = EmployeeCreationForm(
            {
                "username": "test_user",
                "password1": "abcdef123456",
                "password2": "abcdef123456",
                "last_name": "Test",
                "first_name": "User",
                "middle_name": "Tester",
                "hired": "2023-05-31",
                "email": "testuser@example.com",
                "position": position.id,
                "manager": None,
            }
        )
        self.assertTrue(form.is_valid())
        employee = form.save()
        self.assertEqual(employee.username, "test_user")
        self.assertEqual(employee.email, "testuser@example.com")


class EmployeeSearchFormTest(TestCase):
    def test_valid_data(self):
        form = EmployeeSearchForm(
            {
                "employee": "test_user",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["employee"], "test_user")


class TransferSubordinatesFormTest(TestCase):
    def test_valid_data(self):
        position = Position.objects.create(name="position1")
        first_employee = Employee.objects.create(username="employee1", position=position)
        form = TransferSubordinatesForm(
            {
                "new_manager": first_employee.id,
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["new_manager"], first_employee)
