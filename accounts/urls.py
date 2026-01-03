from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # Default to login page
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.employee_profile, name='employee_profile'),
]
