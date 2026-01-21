from django.contrib import admin
from .models import EmployeeProfile, SystemSettings,UserRole

admin.site.register(EmployeeProfile)
admin.site.register(SystemSettings)
admin.site.register(UserRole)
