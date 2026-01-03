from django.db import models
from django.contrib.auth import get_user_model
from employee.models import Employee

User = get_user_model()

class LeaveRequest(models.Model):
    LEAVE_TYPES = [
        ('annual', 'Annual Leave'),
        ('sick', 'Sick Leave'),
        ('personal', 'Personal Leave'),
        ('maternity', 'Maternity Leave'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee} - {self.leave_type} ({self.status})"

class PerformanceReview(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    review_date = models.DateField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 rating
    comments = models.TextField()
    goals = models.TextField(blank=True)

    def __str__(self):
        return f"Review for {self.employee} - {self.rating}/5"

class Attendance(models.Model):
    ATTENDANCE_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('half_day', 'Half Day'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=ATTENDANCE_CHOICES, default='present')
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    working_hours = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ['employee', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.employee.user.get_full_name()} - {self.date} ({self.status})"
