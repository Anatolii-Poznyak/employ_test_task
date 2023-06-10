from django.views import generic
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Employee


def index(request):
    return render(request, "employees_structure/index.html")


class EmployeeListView(LoginRequiredMixin, generic.ListView):
    model = Employee
    queryset = Employee.objects.all().select_related("position")
    paginate_by = 30


class EmployeeDetailView(generic.DetailView):
    model = Employee
