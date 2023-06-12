from django.test import TestCase

from employees_structure.models import Position, Employee


class PositionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Position.objects.create(name="TestPosition")

    def test_position_label(self):
        position = Position.objects.get(id=1)
        field_label = position._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "name")

    def test_position_name(self):
        position = Position.objects.get(id=1)
        expected_object_name = f"{position.name}"
        self.assertEquals(expected_object_name, str(position))


class EmployeeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_position = Position.objects.create(name="TestPosition")
        Employee.objects.create(middle_name="TestMiddle", position=test_position)
        manager = Employee.objects.create(
            username="manager", middle_name="TestManager", position=test_position
        )
        Employee.objects.create(
            username="subordinate1",
            middle_name="TestSubordinate1",
            position=test_position,
            manager=manager,
        )
        Employee.objects.create(
            username="subordinate2",
            middle_name="TestSubordinate2",
            position=test_position,
            manager=manager,
        )
        Employee.objects.create(
            username="other", middle_name="TestOther", position=test_position
        )

    def test_employee_middle_name_label(self):
        employee = Employee.objects.get(id=1)
        field_label = employee._meta.get_field("middle_name").verbose_name
        self.assertEquals(field_label, "middle name")

    def test_employee_position_label(self):
        employee = Employee.objects.get(id=1)
        field_label = employee._meta.get_field("position").verbose_name
        self.assertEquals(field_label, "position")

    def test_position_id(self):
        employee = Employee.objects.get(id=1)
        position = Position.objects.get(id=1)
        self.assertEquals(employee.position.id, position.id)

    def test_get_absolute_url(self):
        employee = Employee.objects.get(id=1)
        self.assertEquals(employee.get_absolute_url(), "/employees/1/")

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
