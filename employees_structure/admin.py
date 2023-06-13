from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from employees_structure.models import Position, Employee

admin.site.register(Position)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = UserAdmin.list_display + (
        "middle_name",
        "hired",
        "position",
        "manager",
    )
    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional info",
            {"fields": ("middle_name", "hired", "position", "manager")},
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {"fields": ("middle_name", "hired", "position", "manager")},
        ),
    )
    list_filter = ["position", "manager", "hired"]
    search_fields = [
        "first_name",
        "last_name",
        "middle_name",
        "hired",
        "position__name",
    ]
