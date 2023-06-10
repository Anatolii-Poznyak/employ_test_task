from django.db import models
from django.contrib.auth.models import AbstractUser


class Position(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name


class Employee(AbstractUser):
    middle_name = models.CharField(max_length=63)
    hired = models.DateField()
    position = models.ForeignKey(
        to=Position,
        on_delete=models.SET_NULL,
        related_name="employees",
        null=True,
        blank=True
    )
    manager = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"
