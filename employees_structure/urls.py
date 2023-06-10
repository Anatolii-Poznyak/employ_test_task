from django.urls import path
from .views import index, EmployeeListView

urlpatterns = [
    path("", index, name="index"),
    path("employees/", EmployeeListView.as_view(), name="employee-list")
]

app_name = "employees_structure"
