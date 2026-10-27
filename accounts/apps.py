from django.apps import AppConfig
from django.db.models.signals import post_migrate, post_save

DEPARTMENTS = ["Computer Science & Engineering", "Electrical & Electronic Engineering", "Civil Engineering",
               "Architecture", "Pharmacy", "Law", "English", "Business Administration"]

def seed_departments(sender, **kw):
    from .models import Department
    if not Department.objects.exists():
        Department.objects.bulk_create([Department(name=n) for n in DEPARTMENTS])

def create_profile(sender, instance, created, **kw):
    from .models import Profile
    if created:
        Profile.objects.create(user=instance)

class AccountsConfig(AppConfig):
    name = "accounts"
    def ready(self):
        from django.contrib.auth import get_user_model
        post_save.connect(create_profile, sender=get_user_model())
        post_migrate.connect(seed_departments, sender=self)
