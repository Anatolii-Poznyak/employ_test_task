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


class PublicTest(TestCase):
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

    def test_login_required(self):
        res = self.client.get(reverse("employees_structure:employee-list"))

        self.assertNotEqual(res.status_code, 200)


class PrivateEmployeeViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("test", "password123")
        self.position = Position.objects.create(name="position1")
        self.employee1 = Employee.objects.create(
            username="employee1", position=self.position
        )
        self.employee2 = Employee.objects.create(
            username="employee2", position=self.position, manager=self.employee1
        )
        self.client.force_login(self.user)
        self.factory = RequestFactory()

    def test_EmployeeListView(self):
        res = self.client.get(reverse("employees_structure:employee-list"))
        employees = Employee.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["employee_list"]), list(employees))
        self.assertTemplateUsed(res, "employees_structure/employee_list.html")

    def test_EmployeeDetailView(self):
        res = self.client.get(
            reverse("employees_structure:employee-detail", args=[self.employee1.pk])
        )
        employee = Employee.objects.get(id=self.employee1.pk)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "employees_structure/employee_detail.html")
        self.assertEqual(res.context["employee"], employee)

    def test_EmployeeCreateView(self):
        request = self.factory.post(
            reverse("employees_structure:employee-create"),
            {"username": "employee3", "position": self.position.pk},
        )
        request.user = AnonymousUser()

        response = EmployeeCreateView.as_view()(request)

        self.assertEqual(response.status_code, 302)

    def test_EmployeeUpdateView(self):
        request = self.factory.post(
            reverse("employees_structure:employee-update", args=[self.employee1.pk]),
            {
                "username": "employee1",
                "position": self.position.pk,
                "manager": self.employee2.pk,
            },
        )
        request.user = AnonymousUser()

        response = EmployeeUpdateView.as_view()(request, pk=self.employee1.pk)

        self.assertEqual(response.status_code, 302)

    def test_EmployeeDeleteView(self):
        request = self.factory.post(
            reverse("employees_structure:employee-delete", args=[self.employee1.pk])
        )
        request.user = AnonymousUser()

        response = EmployeeDeleteView.as_view()(request, pk=self.employee1.pk)

        self.assertEqual(response.status_code, 302)

    def test_TransferSubordinatesView(self):
        request = self.factory.post(
            reverse(
                "employees_structure:transfer-subordinates", args=[self.employee1.pk]
            ),
            {"new_manager": self.employee2.pk},
        )
        request.user = AnonymousUser()

        response = TransferSubordinatesView.as_view()(request, pk=self.employee1.pk)

        self.assertEqual(response.status_code, 302)

    def test_toggle_subordinates(self):
        request = self.factory.post(
            reverse("employees_structure:toggle_subordinates", args=[self.employee1.pk])
        )
        request.user = AnonymousUser()

        response = toggle_subordinates(request, employee_id=self.employee1.pk)

        self.assertEqual(response.status_code, 200)
