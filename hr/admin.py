from django.contrib import admin
from .models import LeaveRequest, PerformanceReview

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'status', 'created_at')
    list_filter = ('status', 'leave_type', 'start_date')
    search_fields = ('employee__user__username', 'employee__employee_id')

@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ('employee', 'reviewer', 'review_date', 'rating')
    list_filter = ('rating', 'review_date')
    search_fields = ('employee__user__username', 'reviewer__username')
