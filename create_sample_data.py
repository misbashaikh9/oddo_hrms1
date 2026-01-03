#!/usr/bin/env python
import os
import django
import sys
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from accounts.models import CustomUser
from employee.models import Employee, Department
from hr.models import LeaveRequest, PerformanceReview, Attendance
from django.utils import timezone
import random

def create_sample_data():
    print("Creating sample data...")

    # Create sample departments
    dept1, created = Department.objects.get_or_create(
        name='Development',
        defaults={'description': 'Software Development Team'}
    )
    dept2, created = Department.objects.get_or_create(
        name='Design',
        defaults={'description': 'UI/UX Design Team'}
    )
    dept3, created = Department.objects.get_or_create(
        name='HR',
        defaults={'description': 'Human Resources Team'}
    )

    # Create sample HR user
    hr_user, created = CustomUser.objects.get_or_create(
        username='hr_manager',
        defaults={
            'emailid': 'hr@company.com',
            'role': 'hr',
            'first_name': 'Sarah',
            'last_name': 'Johnson'
        }
    )
    if created:
        hr_user.set_password('hr123')
        hr_user.save()

    # Create sample employees
    employees_data = [
        {'username': 'john_doe', 'emailid': 'john@company.com', 'first_name': 'John', 'last_name': 'Doe', 'dept': dept1, 'position': 'Senior Developer'},
        {'username': 'jane_smith', 'emailid': 'jane@company.com', 'first_name': 'Jane', 'last_name': 'Smith', 'dept': dept2, 'position': 'UI Designer'},
        {'username': 'bob_johnson', 'emailid': 'bob@company.com', 'first_name': 'Bob', 'last_name': 'Johnson', 'dept': dept1, 'position': 'Project Manager'},
        {'username': 'alice_brown', 'emailid': 'alice@company.com', 'first_name': 'Alice', 'last_name': 'Brown', 'dept': dept3, 'position': 'HR Assistant'},
        {'username': 'mike_wilson', 'emailid': 'mike@company.com', 'first_name': 'Mike', 'last_name': 'Wilson', 'dept': dept1, 'position': 'Junior Developer'},
        {'username': 'lisa_davis', 'emailid': 'lisa@company.com', 'first_name': 'Lisa', 'last_name': 'Davis', 'dept': dept2, 'position': 'Graphic Designer'},
    ]

    for emp_data in employees_data:
        user, created = CustomUser.objects.get_or_create(
            username=emp_data['username'],
            defaults={
                'emailid': emp_data['emailid'],
                'role': 'employee',
                'first_name': emp_data['first_name'],
                'last_name': emp_data['last_name']
            }
        )
        if created:
            user.set_password('emp123')
            user.save()

            # Create employee profile
            Employee.objects.create(
                user=user,
                employee_id=f'EMP{random.randint(100,999)}',
                department=emp_data['dept'],
                position=emp_data['position'],
                salary=random.randint(50000, 80000),
                hire_date=timezone.now().date()
            )

    # Create sample leave requests
    employees = Employee.objects.all()
    leave_types = ['annual', 'sick', 'personal', 'maternity']
    statuses = ['pending', 'approved', 'rejected']

    for i, emp in enumerate(employees[:8]):  # Create leave requests for employees
        LeaveRequest.objects.get_or_create(
            employee=emp,
            leave_type=leave_types[i % 4],
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
            defaults={
                'reason': f'Sample {leave_types[i % 4]} leave request',
                'status': statuses[i % 3]
            }
        )

    # Create sample attendance data for the last 30 days
    from datetime import timedelta, time
    import random

    base_date = timezone.now().date()
    attendance_statuses = ['present', 'present', 'present', 'late', 'absent']  # Weighted towards present

    for emp in employees[:6]:  # Create attendance for first 6 employees
        for days_back in range(30):
            attendance_date = base_date - timedelta(days=days_back)

            # Skip weekends for some realism
            if attendance_date.weekday() >= 5:  # Saturday = 5, Sunday = 6
                continue

            status = random.choice(attendance_statuses)

            if status == 'present':
                check_in = time(hour=9, minute=random.randint(0, 30))
                check_out = time(hour=17, minute=random.randint(30, 59))
                working_hours = 8.0
            elif status == 'late':
                check_in = time(hour=10, minute=random.randint(0, 30))
                check_out = time(hour=18, minute=random.randint(0, 30))
                working_hours = 7.5
            elif status == 'absent':
                check_in = None
                check_out = None
                working_hours = 0.0
            else:  # half_day
                check_in = time(hour=9, minute=random.randint(0, 30))
                check_out = time(hour=13, minute=random.randint(0, 30))
                working_hours = 4.0

            Attendance.objects.get_or_create(
                employee=emp,
                date=attendance_date,
                defaults={
                    'status': status,
                    'check_in_time': check_in,
                    'check_out_time': check_out,
                    'working_hours': working_hours,
                    'recorded_by': hr_user,
                }
            )

    print('Sample data created successfully!')
    print(f'Departments: {Department.objects.count()}')
    print(f'Users: {CustomUser.objects.count()}')
    print(f'Employees: {Employee.objects.count()}')
    print(f'Leave Requests: {LeaveRequest.objects.count()}')

if __name__ == '__main__':
    create_sample_data()
