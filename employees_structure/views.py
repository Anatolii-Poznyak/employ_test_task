from django.views import generic
from django.shortcuts import render

from .models import Employee


def index(request):
    return render(request, "employees_structure/index.html")


class EmployeeListView(generic.ListView):
    model = Employee
