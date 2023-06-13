from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Position(models.Model):
    name = models.CharField(max_length=63)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Employee(AbstractUser):
    middle_name = models.CharField(max_length=63)
    hired = models.DateField(null=True, blank=True)
    position = models.ForeignKey(
        to=Position,
        on_delete=models.SET_NULL,
        related_name="employees",
        null=True,
        blank=True,
    )
    manager = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employee_set",
    )
    show_subordinates = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("employees_structure:employee-detail", args=[str(self.id)])

    def transfer_subordinates(self, new_manager):
        subordinates = Employee.objects.filter(manager=self)
        subordinates.update(manager=new_manager)

    def get_subordinates(self):
        return Employee.objects.filter(manager=self)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    class Meta:
        ordering = ["id"]
