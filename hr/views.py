from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from .models import LeaveRequest, PerformanceReview, Attendance
from employee.models import Employee

@login_required
def leave_requests(request):
    """Combined view for leave requests - employees can submit, HR can approve"""

    # Handle leave request submission (for employees)
    if request.method == 'POST' and request.POST.get('action') == 'submit':
        try:
            employee = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            messages.error(request, 'Employee profile not found.')
            return redirect('leave_requests')

        leave_type = request.POST.get('leave_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')

        # Validation
        from datetime import datetime
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            today = timezone.now().date()

            if start < today:
                messages.error(request, 'Start date cannot be in the past.')
                return redirect('leave_requests')

            if end < start:
                messages.error(request, 'End date cannot be before start date.')
                return redirect('leave_requests')

        except ValueError:
            messages.error(request, 'Invalid date format.')
            return redirect('leave_requests')

        # Create leave request
        LeaveRequest.objects.create(
            employee=employee,
            leave_type=leave_type,
            start_date=start,
            end_date=end,
            reason=reason,
            status='pending'
        )

        messages.success(request, 'Leave request submitted successfully!')
        return redirect('leave_requests')

    # Handle leave approval/rejection (for HR)
    if request.method == 'POST' and request.POST.get('action') == 'approve':
        if not (request.user.role == 'hr' or request.user.is_staff):
            messages.error(request, 'You do not have permission to approve leave requests.')
            return redirect('leave_requests')

        leave_id = request.POST.get('leave_id')
        action = request.POST.get('approve_action')

        try:
            leave_request = LeaveRequest.objects.get(id=leave_id)
            if action == 'approve':
                leave_request.status = 'approved'
                leave_request.approved_by = request.user
                messages.success(request, 'Leave request approved.')
            elif action == 'reject':
                leave_request.status = 'rejected'
                leave_request.approved_by = request.user
                messages.success(request, 'Leave request rejected.')

            leave_request.save()
        except LeaveRequest.DoesNotExist:
            messages.error(request, 'Leave request not found.')

        return redirect('leave_requests')

    # Get status filter from URL parameters
    status_filter = request.GET.get('status', 'all')

    # Filter leave requests based on user role and status
    if request.user.role == 'hr' or request.user.is_staff:
        # HR sees all requests
        if status_filter == 'pending':
            leave_requests = LeaveRequest.objects.select_related('employee__user', 'employee__department').filter(status='pending')
        elif status_filter == 'approved':
            leave_requests = LeaveRequest.objects.select_related('employee__user', 'employee__department').filter(status='approved')
        elif status_filter == 'rejected':
            leave_requests = LeaveRequest.objects.select_related('employee__user', 'employee__department').filter(status='rejected')
        else:
            leave_requests = LeaveRequest.objects.select_related('employee__user', 'employee__department').all()
    else:
        # Employees see only their own requests
        try:
            employee = Employee.objects.get(user=request.user)
            if status_filter == 'pending':
                leave_requests = LeaveRequest.objects.select_related('employee__user', 'employee__department').filter(employee=employee, status='pending')
            elif status_filter == 'approved':
                leave_requests = LeaveRequest.objects.select_related('employee__user', 'employee__department').filter(employee=employee, status='approved')
            elif status_filter == 'rejected':
                leave_requests = LeaveRequest.objects.select_related('employee__user', 'employee__department').filter(employee=employee, status='rejected')
            else:
                leave_requests = LeaveRequest.objects.select_related('employee__user', 'employee__department').filter(employee=employee)
        except Employee.DoesNotExist:
            leave_requests = LeaveRequest.objects.none()

    # Calculate statistics
    if request.user.role == 'hr' or request.user.is_staff:
        all_requests = LeaveRequest.objects.all()
    else:
        try:
            employee = Employee.objects.get(user=request.user)
            all_requests = LeaveRequest.objects.filter(employee=employee)
        except Employee.DoesNotExist:
            all_requests = LeaveRequest.objects.none()

    pending_count = all_requests.filter(status='pending').count()
    approved_count = all_requests.filter(status='approved').count()
    rejected_count = all_requests.filter(status='rejected').count()

    context = {
        'leave_requests': leave_requests,
        'status_filter': status_filter,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'is_hr': request.user.role == 'hr' or request.user.is_staff,
    }

    return render(request, 'hr/leave_requests.html', context)

@login_required
def approve_leave(request, pk):
    if request.user.role != 'hr' and not request.user.is_staff:
        messages.error(request, 'You do not have permission to approve leave requests.')
        return redirect('leave_requests')

    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    leave_request.status = 'approved'
    leave_request.approved_by = request.user
    leave_request.save()

    messages.success(request, 'Leave request approved.')
    return redirect('leave_requests')

@login_required
def performance_reviews(request):
    if request.user.role == 'hr' or request.user.is_staff:
        reviews = PerformanceReview.objects.select_related('employee__user', 'reviewer').all()
    else:
        # Employees can only see their own reviews
        employee = get_object_or_404(Employee, user=request.user)
        reviews = PerformanceReview.objects.filter(employee=employee)

    return render(request, 'hr/performance_reviews.html', {'reviews': reviews})

@login_required
def attendance_records(request):
    if not (request.user.role == 'hr' or request.user.is_staff):
        messages.error(request, 'You do not have permission to view attendance records.')
        return redirect('dashboard')

    employees = Employee.objects.select_related('user', 'department').all()

    # Get attendance statistics for each employee
    employee_stats = []
    for employee in employees:
        attendance_records = Attendance.objects.filter(employee=employee)
        total_days = attendance_records.count()
        present_days = attendance_records.filter(status='present').count()
        attendance_rate = round((present_days / total_days * 100), 1) if total_days > 0 else 0

        employee_stats.append({
            'employee': employee,
            'total_days': total_days,
            'present_days': present_days,
            'attendance_rate': attendance_rate,
            'recent_attendance': attendance_records.order_by('-date')[:31]  # Last 31 days for calendar view
        })

    context = {
        'employees': employees,
        'employee_stats': employee_stats,
        'today': timezone.now().date(),
    }

    return render(request, 'hr/attendance.html', context)

@login_required
def employee_attendance(request):
    """View for employees to see their own attendance"""
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found.')
        return redirect('dashboard')

    attendance_records = Attendance.objects.filter(employee=employee).order_by('-date')
    total_days = attendance_records.count()
    present_days = attendance_records.filter(status='present').count()
    attendance_rate = round((present_days / total_days * 100), 1) if total_days > 0 else 0

    # Monthly breakdown
    from django.db.models import Count, Q
    from django.db.models.functions import ExtractMonth, ExtractYear

    monthly_stats = attendance_records.annotate(
        month=ExtractMonth('date'),
        year=ExtractYear('date')
    ).values('month', 'year').annotate(
        present_count=Count('id', filter=Q(status='present')),
        total_count=Count('id')
    ).order_by('-year', '-month')[:6]

    context = {
        'employee': employee,
        'attendance_records': attendance_records[:30],  # Last 30 records
        'total_days': total_days,
        'present_days': present_days,
        'attendance_rate': attendance_rate,
        'monthly_stats': monthly_stats,
        'today': timezone.now().date(),
    }

    return render(request, 'hr/employee_attendance.html', context)

@login_required
def mark_attendance(request):
    """View for employees to mark their attendance"""
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found.')
        return redirect('dashboard')

    today = timezone.now().date()
    current_time = timezone.now().time()

    # Check if attendance already marked for today
    today_attendance = Attendance.objects.filter(employee=employee, date=today).first()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'check_in':
            if today_attendance:
                messages.warning(request, 'You have already checked in today.')
            else:
                Attendance.objects.create(
                    employee=employee,
                    date=today,
                    status='present',
                    check_in_time=current_time,
                    recorded_by=request.user
                )
                messages.success(request, f'Checked in successfully at {current_time.strftime("%I:%M %p")}')
                return redirect('mark_attendance')

        elif action == 'check_out':
            if not today_attendance:
                messages.error(request, 'You must check in first before checking out.')
            elif today_attendance.check_out_time:
                messages.warning(request, 'You have already checked out today.')
            else:
                today_attendance.check_out_time = current_time
                # Calculate working hours
                if today_attendance.check_in_time:
                    # Combine date with check-in time and make it timezone-aware
                    check_in_datetime = timezone.make_aware(
                        datetime.combine(today, today_attendance.check_in_time)
                    )
                    check_out_datetime = timezone.now()

                    time_diff = check_out_datetime - check_in_datetime
                    working_hours = time_diff.total_seconds() / 3600  # Convert to hours
                    today_attendance.working_hours = round(working_hours, 2)
                today_attendance.save()
                messages.success(request, f'Checked out successfully at {current_time.strftime("%I:%M %p")}')
                return redirect('mark_attendance')

    # Get today's attendance status
    attendance_status = None
    check_in_time = None
    check_out_time = None
    working_hours = None
    can_check_out = False

    if today_attendance:
        attendance_status = today_attendance.status
        check_in_time = today_attendance.check_in_time
        check_out_time = today_attendance.check_out_time
        working_hours = today_attendance.working_hours
        # Check if user can check out (has checked in but not checked out)
        can_check_out = check_in_time is not None and check_out_time is None

    context = {
        'employee': employee,
        'today': today,
        'current_time': current_time,
        'attendance_status': attendance_status,
        'check_in_time': check_in_time,
        'check_out_time': check_out_time,
        'working_hours': working_hours,
        'today_attendance': today_attendance,
        'can_check_out': can_check_out,
    }

    return render(request, 'hr/mark_attendance.html', context)

@login_required
def submit_leave_request(request):
    """View for employees to submit leave requests"""
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found.')
        return redirect('dashboard')

    if request.method == 'POST':
        leave_type = request.POST.get('leave_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')

        # Validation
        from datetime import datetime
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            today = timezone.now().date()

            if start < today:
                messages.error(request, 'Start date cannot be in the past.')
                return redirect('submit_leave_request')

            if end < start:
                messages.error(request, 'End date cannot be before start date.')
                return redirect('submit_leave_request')

        except ValueError:
            messages.error(request, 'Invalid date format.')
            return redirect('submit_leave_request')

        # Create leave request
        LeaveRequest.objects.create(
            employee=employee,
            leave_type=leave_type,
            start_date=start,
            end_date=end,
            reason=reason,
            status='pending'
        )

        messages.success(request, 'Leave request submitted successfully!')
        return redirect('dashboard')

    context = {
        'employee': employee,
    }

    return render(request, 'hr/submit_leave_request.html', context)
