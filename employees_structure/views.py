from django.views import generic
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.forms.widgets import DateInput, PasswordInput

from .models import Employee


def index(request):
    return render(request, "employees_structure/index.html")


class EmployeeListView(LoginRequiredMixin, generic.ListView):
    model = Employee
    queryset = Employee.objects.all().select_related("position")
    paginate_by = 30


class EmployeeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Employee


class EmployeeCreateView(LoginRequiredMixin, generic.CreateView):
    model = Employee
    success_url = reverse_lazy("employees_structure:employee-list")
    template_name = "employees_structure/employee_form.html"
    fields = [
        "username",
        "password",
        "last_name",
        "first_name",
        "middle_name",
        "hired",
        "email",
        "position",
        "manager",
    ]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["hired"].widget = DateInput(attrs={"type": "date"})
        form.fields["password"].widget = PasswordInput()
        return form


class EmployeeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Employee
    fields = "__all__"
    success_url = reverse_lazy("employees_structure:employee-list")
    template_name = "employees_structure/employee_form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["hired"].widget = DateInput(attrs={"type": "date"})
        form.fields["password"].widget = PasswordInput()
        return form


class EmployeeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Employee
    fields = "__all__"
    success_url = reverse_lazy("employees_structure:employee-list")
    template_name = "employees_structure/employee_delete.html"

