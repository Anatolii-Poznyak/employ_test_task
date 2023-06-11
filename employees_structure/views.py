from django.views import generic
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.forms.widgets import DateInput, PasswordInput

from .forms import EmployeeCreationForm, EmployeeUpdateForm, EmployeeSearchForm
from .models import Employee


def index(request):
    return render(request, "employees_structure/index.html")


class EmployeeListView(LoginRequiredMixin, generic.ListView):
    model = Employee
    queryset = Employee.objects.all().select_related("position")
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        employee = self.request.GET.get("employee", "")

        context["search_form"] = EmployeeSearchForm(initial={
            "employee": employee
        })

        return context

    def get_queryset(self):
        form = EmployeeSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(first_name__icontains=form.cleaned_data["employee"])

        return self.queryset


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

