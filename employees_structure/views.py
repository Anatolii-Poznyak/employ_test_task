from django.views import generic
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.forms.widgets import DateInput, PasswordInput

from .forms import EmployeeCreationForm, EmployeeUpdateForm
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
    form_class = EmployeeCreationForm


class EmployeeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Employee
    form_class = EmployeeUpdateForm


class EmployeeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Employee
    fields = "__all__"
    success_url = reverse_lazy("employees_structure:employee-list")
    template_name = "employees_structure/employee_delete.html"

