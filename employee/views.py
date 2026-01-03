from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Employee, Department

@login_required
def employee_list(request):
    if not (request.user.role == 'hr' or request.user.is_staff):
        messages.error(request, 'You do not have permission to view employee list.')
        return redirect('dashboard')

    employees = Employee.objects.select_related('user', 'department').all()
    departments = Department.objects.all()
    return render(request, 'employee/employee_list.html', {
        'employees': employees,
        'departments': departments
    })

@login_required
def employee_detail(request, pk):
    # Handle employee switcher from dashboard
    employee_id = request.GET.get('employee_id')
    if employee_id:
        pk = employee_id

    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employee/employee_detail.html', {'employee': employee})

@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'employee/department_list.html', {'departments': departments})
