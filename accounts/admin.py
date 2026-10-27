from django.contrib import admin
from .models import Department, Profile
admin.site.register(Department)

@admin.register(Profile)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "department", "student_id"]
    list_filter = ["department"]
