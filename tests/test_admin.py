from django.contrib.admin.sites import site
from django.test import TestCase

from employees_structure.models import Employee


class EmployeeAdminTest(TestCase):
    def setUp(self):
        self.admin_instance = site._registry[Employee]

    def test_list_display(self):
        expected = (
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "middle_name",
            "hired",
            "position",
            "manager",
        )
        self.assertEqual(self.admin_instance.list_display, expected)

    def test_add_fieldsets(self):
        expected = (
            (
                None,
                {
                    "classes": ("wide",),
                    "fields": ("username", "password1", "password2"),
                },
            ),
            (
                "Additional info",
                {"fields": ("middle_name", "hired", "position", "manager")},
            ),
        )
        self.assertEqual(self.admin_instance.add_fieldsets, expected)

    def test_list_filter(self):
        expected = ["position", "manager", "hired"]
        self.assertEqual(self.admin_instance.list_filter, expected)

    def test_search_fields(self):
        expected = ["first_name", "last_name", "middle_name", "hired", "position__name"]
        self.assertEqual(self.admin_instance.search_fields, expected)
