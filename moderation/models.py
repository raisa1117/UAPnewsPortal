from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class ReviewLog(models.Model):
    """Audit trail: who approved or declined which post."""
    ACTIONS = [("approve", "Approved"), ("decline", "Declined")]
    post = models.ForeignKey("content.Post", on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reviews_done")
    action = models.CharField(max_length=10, choices=ACTIONS)
    note = models.CharField(max_length=240, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]

class Report(models.Model):
    post = models.ForeignKey("content.Post", on_delete=models.CASCADE, related_name="reports")
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports_made")
    reason = models.CharField(max_length=240)
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]
        constraints = [models.UniqueConstraint(fields=["post", "reporter"], name="one_report_per_user_post")]

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    post = models.ForeignKey("content.Post", on_delete=models.CASCADE, null=True, blank=True, related_name="notifications")
    message = models.CharField(max_length=240)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]
