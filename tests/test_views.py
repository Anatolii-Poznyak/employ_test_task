from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from employees_structure.models import Employee, Position
from employees_structure.views import index


class ViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.position = Position.objects.create(name="position1")
        self.employee1 = Employee.objects.create(
            username="employee1", position=self.position
        )
        self.employee2 = Employee.objects.create(
            username="employee2", position=self.position, manager=self.employee1
        )

    def test_index_view(self):
        request = self.factory.get(reverse("employees_structure:index"))
        request.user = AnonymousUser()

        response = index(request)

        self.assertEqual(response.status_code, 200)
