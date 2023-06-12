from django.test import TestCase

from employees_structure.forms import BaseEmployeeForm
from employees_structure.models import Position


class BaseEmployeeFormTest(TestCase):
    def test_valid_data(self):
        position = Position.objects.create(name='position1')
        form = BaseEmployeeForm({
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
        })
        self.assertTrue(form.is_valid())
        employee = form.save()
        self.assertEqual(employee.username, "test_user")
        self.assertEqual(employee.email, "testuser@example.com")

