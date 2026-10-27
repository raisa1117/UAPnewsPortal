from django.contrib import admin
from django.utils import timezone
from .models import Bookmark, Category, Comment, Post, Tag

admin.site.register([Category, Tag, Bookmark])

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "post", "created_at"]

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "kind", "category", "author", "status", "created_at"]
    list_filter = ["status", "kind", "category"]
    search_fields = ["title", "body"]
    actions = ["approve", "decline"]

    @admin.action(description="Approve selected posts")
    def approve(self, request, qs):
        qs.update(status=Post.APPROVED, published_at=timezone.now(), review_note="")

    @admin.action(description="Decline selected posts")
    def decline(self, request, qs):
        qs.update(status=Post.DECLINED)
