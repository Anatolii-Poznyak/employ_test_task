from django.test import TestCase

from employees_structure.models import Position, Employee


class PositionModelTest(TestCase):
    def setUp(self):
        self.test_position = Position.objects.create(name="TestPosition")

    def test_position_label(self):
        field_label = self.test_position._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "name")

    def test_position_name(self):
        expected_object_name = f"{self.test_position.name}"
        self.assertEquals(expected_object_name, str(self.test_position))


class EmployeeModelTest(TestCase):
    def setUp(self):
        self.test_position = Position.objects.create(name="TestPosition")
        self.first_employee = Employee.objects.create(middle_name="TestMiddle", position=self.test_position)
        self.manager = Employee.objects.create(
            username="manager", middle_name="TestManager", position=self.test_position
        )
        self.subordinate1 = Employee.objects.create(
            username="subordinate1",
            middle_name="TestSubordinate1",
            position=self.test_position,
            manager=self.manager,
        )
        self.subordinate2 = Employee.objects.create(
            username="subordinate2",
            middle_name="TestSubordinate2",
            position=self.test_position,
            manager=self.manager,
        )
        self.other_employee = Employee.objects.create(
            username="other", middle_name="TestOther", position=self.test_position
        )

    def test_employee_middle_name_label(self):
        field_label = self.first_employee._meta.get_field("middle_name").verbose_name
        self.assertEquals(field_label, "middle name")

    def test_employee_position_label(self):
        field_label = self.first_employee._meta.get_field("position").verbose_name
        self.assertEquals(field_label, "position")

    def test_get_subordinates(self):
        manager = Employee.objects.get(username="manager")
        subordinates = manager.get_subordinates()
        self.assertEqual(subordinates.count(), 2)
        self.assertTrue(Employee.objects.get(username="subordinate1") in subordinates)
        self.assertTrue(Employee.objects.get(username="subordinate2") in subordinates)

    def test_transfer_subordinates(self):
        manager1 = Employee.objects.get(username="manager")
        manager2 = Employee.objects.get(username="other")

        manager1.transfer_subordinates(manager2)

        self.assertEqual(manager1.get_subordinates().count(), 0)

        subordinates = manager2.get_subordinates()
        self.assertEqual(subordinates.count(), 2)
        self.assertTrue(Employee.objects.get(username="subordinate1") in subordinates)
        self.assertTrue(Employee.objects.get(username="subordinate2") in subordinates)
