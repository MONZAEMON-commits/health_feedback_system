from django.db import models
from django.contrib.auth.models import User

class EmployeeProfile(models.Model):
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE
    )
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    department = models.CharField(max_length=100)
    is_target = models.BooleanField(default=False)

class SystemSettings(models.Model):
    admin_timeout_minutes = models.IntegerField()

class UserRole(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    role_level = models.IntegerField(default=0)
