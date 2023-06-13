from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from django.urls import reverse

from employees_structure.models import Employee, Position
from employees_structure.views import (
    index,
    EmployeeCreateView,
    EmployeeUpdateView,
    EmployeeDeleteView,
    TransferSubordinatesView,
    toggle_subordinates,
)

EMPLOYEE_LIST_URL = reverse("employees_structure:employee-list")


class PublicTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.position = Position.objects.create(name="test_position")
        self.first_employee = Employee.objects.create(
            username="first_employee", position=self.position
        )
        self.second_employee = Employee.objects.create(
            username="second_employee", position=self.position, manager=self.first_employee
        )

    def test_index_view(self):
        request = self.factory.get(reverse("employees_structure:index"))
        request.user = AnonymousUser()

        response = index(request)

        self.assertEqual(response.status_code, 200)

    def test_login_required(self):
        res = self.client.get(EMPLOYEE_LIST_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateEmployeeViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("test", "password123")
        self.position = Position.objects.create(name="test_position")
        self.first_employee = Employee.objects.create(
            username="first_employee", position=self.position
        )
        self.second_employee = Employee.objects.create(
            username="second_employee", position=self.position, manager=self.first_employee
        )
        self.client.force_login(self.user)
        self.factory = RequestFactory()

    def test_employee_list_view(self):
        res = self.client.get(EMPLOYEE_LIST_URL)
        employees = Employee.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["employee_list"]), list(employees))
        self.assertTemplateUsed(res, "employees_structure/employee_list.html")

    def test_employee_detail_view(self):
        res = self.client.get(
            reverse("employees_structure:employee-detail", args=[self.first_employee.pk])
        )
        employee = Employee.objects.get(id=self.first_employee.pk)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "employees_structure/employee_detail.html")
        self.assertEqual(res.context["employee"], employee)

    def test_employee_create_view(self):
        request = self.factory.post(
            reverse("employees_structure:employee-create"),
            {"username": "third_employee", "position": self.position.pk},
        )
        request.user = AnonymousUser()

        response = EmployeeCreateView.as_view()(request)

        self.assertEqual(response.status_code, 302)

    def test_employee_update_view(self):
        request = self.factory.post(
            reverse("employees_structure:employee-update", args=[self.first_employee.pk]),
            {
                "username": "first_employee",
                "position": self.position.pk,
                "manager": self.second_employee.pk,
            },
        )
        request.user = AnonymousUser()

        response = EmployeeUpdateView.as_view()(request, pk=self.first_employee.pk)

        self.assertEqual(response.status_code, 302)

    def test_employee_delete_view(self):
        request = self.factory.post(
            reverse("employees_structure:employee-delete", args=[self.first_employee.pk])
        )
        request.user = AnonymousUser()

        response = EmployeeDeleteView.as_view()(request, pk=self.first_employee.pk)

        self.assertEqual(response.status_code, 302)

    def test_transfer_subordinates_view(self):
        request = self.factory.post(
            reverse(
                "employees_structure:transfer-subordinates", args=[self.first_employee.pk]
            ),
            {"new_manager": self.second_employee.pk},
        )
        request.user = AnonymousUser()

        response = TransferSubordinatesView.as_view()(request, pk=self.first_employee.pk)

        self.assertEqual(response.status_code, 302)

    def test_toggle_subordinates(self):
        request = self.factory.post(
            reverse("employees_structure:toggle_subordinates", args=[self.first_employee.pk])
        )
        request.user = AnonymousUser()

        response = toggle_subordinates(request, employee_id=self.first_employee.pk)

        self.assertEqual(response.status_code, 200)
