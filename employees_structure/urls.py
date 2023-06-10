from django.urls import path
from .views import index, EmployeeListView, EmployeeDetailView, EmployeeCreateView

urlpatterns = [
    path("", index, name="index"),
    path("employees/", EmployeeListView.as_view(), name="employee-list"),
    path("employees/<int:pk>/", EmployeeDetailView.as_view(), name="employee-detail"),
    path("employees/create/",  EmployeeCreateView.as_view(), name="employee-create"),

]

app_name = "employees_structure"
