from django.conf import settings
from django.db import models
from django.urls import reverse

User = settings.AUTH_USER_MODEL

class Category(models.Model):
    name = models.CharField(max_length=60, unique=True)
    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return self.name

class Post(models.Model):
    PENDING, APPROVED, DECLINED = "pending", "approved", "declined"
    STATUS = [(PENDING, "Pending"), (APPROVED, "Approved"), (DECLINED, "Declined")]
    NEWS, BLOG = "news", "blog"
    KINDS = [(NEWS, "News"), (BLOG, "Blog")]

    title = models.CharField(max_length=160)
    kind = models.CharField("Type", max_length=10, choices=KINDS, default=NEWS)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="posts")
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    status = models.CharField(max_length=10, choices=STATUS, default=PENDING)
    review_note = models.CharField(max_length=240, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("detail", args=[self.pk])
    @property
    def excerpt(self):
        return self.body[:180] + ("…" if len(self.body) > 180 else "")

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    body = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["created_at"]
    def __str__(self):
        return f"{self.user} on {self.post}"

class Bookmark(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="bookmarks")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "post"], name="one_bookmark_per_user_post")]  # composite key
