from django.contrib.auth.forms import UserCreationForm
from .models import Employee
from django.forms.widgets import DateInput
from django import forms


class BaseEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = UserCreationForm.Meta.fields + (
            "last_name",
            "first_name",
            "middle_name",
            "hired",
            "email",
            "position",
            "manager",
        )
        widgets = {
            "hired": forms.DateInput(attrs={"type": "date"}),
        }


class EmployeeCreationForm(BaseEmployeeForm, UserCreationForm):
    pass


class EmployeeUpdateForm(BaseEmployeeForm):
    pass
