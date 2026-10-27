# Django admin module import kora hocche
from django.contrib import admin

# models.py theke Department ebong Profile model import kora hocche
from .models import Department, Profile

# Department model ke admin panel e register kora hocche
admin.site.register(Department)

# Profile model er jonno custom admin class toiri kora hocche decorator use kore
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    ProfileAdmin class ti admin panel e Profile model er view control kore.
    Ekhane list_display ebong list_filter use kora hoyeche.
    """
    
    # Admin panel-er list view te ei field gulo column hishebe dekhabe
    list_display = ["user", "department", "student_id"]
    
    # Right side e filter korar jonno department field ti add kora holo
    list_filter = ["department"]
