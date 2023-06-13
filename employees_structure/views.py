from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, CharField
from django.db.models.functions import Cast
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from .forms import (
    EmployeeCreationForm,
    EmployeeUpdateForm,
    EmployeeSearchForm,
    TransferSubordinatesForm,
)
from .models import Employee


def get_employee_with_depth(employee, depth=0):
    return {
        "employee": employee,
        "depth": depth,
        "show_subordinates": employee.show_subordinates,
        "subordinates": [
            get_employee_with_depth(e, depth + 1)
            for e in employee.employee_set.all()
            if employee.show_subordinates
        ],
    }


def index(request):
    top_level_employees = Employee.objects.filter(manager__isnull=True)
    employees = [get_employee_with_depth(e) for e in top_level_employees]
    return render(request, "employees_structure/index.html", {"employees": employees})


class EmployeeListView(LoginRequiredMixin, generic.ListView):
    model = Employee
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        employee = self.request.GET.get("employee", "")

        context["search_form"] = EmployeeSearchForm(initial={"employee": employee})

        return context

    def get_queryset(self):
        form = EmployeeSearchForm(self.request.GET)
        queryset = Employee.objects.select_related("position").annotate(
            hired_str=Cast("hired", CharField(max_length=63))
        )

        if form.is_valid() and form.cleaned_data["employee"]:
            query = form.cleaned_data["employee"]
            queryset = queryset.filter(
                Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(middle_name__icontains=query)
                | Q(email__icontains=query)
                | Q(position__name__icontains=query)
                | Q(manager__first_name__icontains=query)
                | Q(manager__last_name__icontains=query)
                | Q(manager__middle_name__icontains=query)
                | Q(hired_str__icontains=query)
            )

        sort_by = self.kwargs.get("sort_by", None)
        direction = self.kwargs.get("direction", None)
        sort_field = sort_by

        if sort_by:
            model = self.kwargs.get("model", None)
            if model:
                sort_field = f"{model}__{sort_by}"

            if direction == "desc":
                sort_field = f"-{sort_field}"

            queryset = queryset.order_by(sort_field)

        return queryset


class EmployeeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Employee

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["transfer_form"] = TransferSubordinatesForm(employee=self.object)
        return context


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


class TransferSubordinatesView(LoginRequiredMixin, generic.View):
    def post(self, request, *args, **kwargs):
        form = TransferSubordinatesForm(
            request.POST, employee=get_object_or_404(Employee, pk=self.kwargs.get("pk"))
        )
        if form.is_valid():
            new_manager = form.cleaned_data["new_manager"]
            employee = form.employee
            employee.transfer_subordinates(new_manager)
            messages.success(request, "Підлеглі були успішно передані.")
        return redirect("employees_structure:employee-detail", pk=employee.id)


@csrf_exempt
def toggle_subordinates(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    employee.show_subordinates = not employee.show_subordinates
    employee.save()
    return JsonResponse({"show_subordinates": employee.show_subordinates})
