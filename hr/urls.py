from django.urls import path
from . import views

urlpatterns = [
    path('leave-requests/', views.leave_requests, name='leave_requests'),
    path('leave-requests/<int:pk>/approve/', views.approve_leave, name='approve_leave'),
    path('performance-reviews/', views.performance_reviews, name='performance_reviews'),
    path('attendance/', views.attendance_records, name='attendance_records'),
    path('my-attendance/', views.employee_attendance, name='employee_attendance'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('submit-leave/', views.submit_leave_request, name='submit_leave_request'),
]
