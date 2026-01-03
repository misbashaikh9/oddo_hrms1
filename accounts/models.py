from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('hr', 'HR'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    department = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    emailid = models.EmailField(blank=True, null=True, unique=True, help_text="Primary email address for the user")

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
