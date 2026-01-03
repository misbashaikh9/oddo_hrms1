from django.contrib import admin
from .models import Department, Employee

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager')
    search_fields = ('name',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'department', 'position', 'hire_date')
    list_filter = ('department', 'hire_date')
    search_fields = ('user__username', 'employee_id', 'user__first_name', 'user__last_name')
