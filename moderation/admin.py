from django.contrib import admin
from .models import Notification, Report, ReviewLog

@admin.register(ReviewLog)
class ReviewLogAdmin(admin.ModelAdmin):
    list_display = ["post", "reviewer", "action", "created_at"]
    list_filter = ["action"]

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["post", "reporter", "reason", "resolved"]
    list_filter = ["resolved"]

admin.site.register(Notification)
