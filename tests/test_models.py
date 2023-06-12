from django.test import TestCase
from employees_structure.models import Position


class PositionModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Position.objects.create(name='TestPosition')

    def test_position_label(self):
        position = Position.objects.get(id=1)
        field_label = position._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_position_name(self):
        position = Position.objects.get(id=1)
        expected_object_name = f'{position.name}'
        self.assertEquals(expected_object_name, str(position))
