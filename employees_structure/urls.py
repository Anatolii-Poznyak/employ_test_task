from django.urls import path

from .views import (
    index,
    EmployeeListView,
    EmployeeDetailView,
    EmployeeCreateView,
    EmployeeUpdateView,
    EmployeeDeleteView,
    TransferSubordinatesView,
    toggle_subordinates,
)

urlpatterns = [
    path("", index, name="index"),
    path("employees/", EmployeeListView.as_view(), name="employee-list"),
    path("employees/create/", EmployeeCreateView.as_view(), name="employee-create"),
    path("employees/<int:pk>/", EmployeeDetailView.as_view(), name="employee-detail"),
    path(
        "employees/<int:pk>/update/",
        EmployeeUpdateView.as_view(),
        name="employee-update",
    ),
    path(
        "employees/<int:pk>/delete/",
        EmployeeDeleteView.as_view(),
        name="employee-delete",
    ),
    path(
        "employees/<int:pk>/transfer-subordinates/",
        TransferSubordinatesView.as_view(),
        name="transfer-subordinates",
    ),
    path(
        "toggle_subordinates/<int:employee_id>/",
        toggle_subordinates,
        name="toggle_subordinates",
    ),
    path(
        "employees/<str:sort_by>/<str:direction>/",
        EmployeeListView.as_view(),
        name="employee-list-sort",
    ),
    path(
        "employees/<str:model>/<str:sort_by>/<str:direction>/",
        EmployeeListView.as_view(),
        name="manager-list-sort",
    ),
]

app_name = "employees_structure"
