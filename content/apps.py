from django.apps import AppConfig
from django.db.models.signals import post_migrate

CATEGORIES = ["Campus News", "Academics", "Research", "Events", "Sports", "Student Life", "Opinion"]

def seed_categories(sender, **kw):
    from .models import Category
    if not Category.objects.exists():
        Category.objects.bulk_create([Category(name=n) for n in CATEGORIES])

class ContentConfig(AppConfig):
    name = "content"
    def ready(self):
        post_migrate.connect(seed_categories, sender=self)
