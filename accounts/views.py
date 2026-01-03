from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from accounts.models import CustomUser
from employee.models import Employee, Department

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Find user by email
        try:
            user = CustomUser.objects.get(emailid=email)
            # Authenticate using the found user's username
            user = authenticate(request, username=user.username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
                messages.error(request, 'Invalid email or password.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'auth/login.html')

def signup_view(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        emailid = request.POST.get('emailid')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')

        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/signup.html')

        try:
            validate_password(password)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return render(request, 'auth/signup.html')

        # Check if employee_id or emailid already exists
        if CustomUser.objects.filter(username=employee_id).exists():
            messages.error(request, 'Employee ID already exists.')
            return render(request, 'auth/signup.html')

        if emailid and CustomUser.objects.filter(emailid=emailid).exists():
            messages.error(request, 'Email ID already exists.')
            return render(request, 'auth/signup.html')

        try:
            # Create user
            user = CustomUser.objects.create_user(
                username=employee_id,
                email=emailid,  # Use emailid for the email field
                password=password,
                role=role,
                emailid=emailid
            )

            # Create employee profile
            Employee.objects.create(
                user=user,
                employee_id=employee_id,
                department=None,  # Will be assigned later by HR
                position='Employee',
                salary=0.00,
                hire_date=timezone.now().date()
            )

            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')

        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'auth/signup.html')

    return render(request, 'auth/signup.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    from employee.models import Employee, Department
    from hr.models import LeaveRequest, Attendance

    context = {'user': request.user}

    # Get current user's employee profile for employee dashboard
    try:
        current_employee = Employee.objects.get(user=request.user)
        context['current_employee'] = current_employee

        # Get employee's attendance stats
        employee_attendance = Attendance.objects.filter(employee=current_employee)
        total_days = employee_attendance.count()
        present_days = employee_attendance.filter(status='present').count()
        attendance_rate = round((present_days / total_days * 100), 1) if total_days > 0 else 0

        context.update({
            'attendance_total': total_days,
            'attendance_present': present_days,
            'attendance_rate': attendance_rate,
            'recent_attendance': employee_attendance.order_by('-date')[:5],
        })

        # Get employee's leave requests
        employee_leaves = LeaveRequest.objects.filter(employee=current_employee).order_by('-created_at')[:3]
        context['recent_leaves'] = employee_leaves

    except Employee.DoesNotExist:
        context['current_employee'] = None

    # Add HR-specific data if user is HR or admin
    if request.user.role == 'hr' or request.user.is_staff:
        context.update({
            'employees_count': Employee.objects.count(),
            'departments_count': Department.objects.count(),
            'pending_leaves': LeaveRequest.objects.filter(status='pending').count(),
            'attendance_rate': 96,  # This would be calculated from attendance data
            'recent_employees': Employee.objects.select_related('user').order_by('-hire_date')[:5],
            'recent_leaves': LeaveRequest.objects.select_related('employee__user').order_by('-created_at')[:3],
        })

    return render(request, 'auth/dashboard.html', context)

@login_required
def employee_profile(request):
    """View and edit employee profile"""
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found.')
        return redirect('dashboard')

    if request.method == 'POST':
        # Handle profile update
        employee.position = request.POST.get('position', employee.position)
        employee.department_id = request.POST.get('department')
        employee.phone = request.POST.get('phone', employee.phone)
        employee.address = request.POST.get('address', employee.address)

        # Update user information
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.emailid = request.POST.get('emailid', request.user.emailid)

        try:
            employee.save()
            request.user.save()
            messages.success(request, 'Profile updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')

        return redirect('employee_profile')

    from employee.models import Department
    departments = Department.objects.all()

    context = {
        'employee': employee,
        'departments': departments,
    }

    return render(request, 'accounts/employee_profile.html', context)
