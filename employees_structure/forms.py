from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_select2.forms import (
    Select2Widget,
)

from .models import Employee


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
    def save(self, commit=True):
        employee = super().save(commit=commit)

        if commit:
            subordinates = Employee.objects.filter(manager=employee)
            subordinates.update(manager=employee.manager)

        return employee


class EmployeeSearchForm(forms.Form):
    employee = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search employees ..."}),
    )


class TransferSubordinatesForm(forms.Form):
    new_manager = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        label="Новий менеджер ",
        widget=Select2Widget(attrs={"data-minimum-input-length": 0}),
    )

    def __init__(self, *args, **kwargs):
        self.employee = kwargs.pop("employee", None)
        super().__init__(*args, **kwargs)
