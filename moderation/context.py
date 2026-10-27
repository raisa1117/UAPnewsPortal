from content.models import Post
def counters(request):
    u, out = request.user, {}
    if u.is_authenticated:
        out["unread_count"] = u.notifications.filter(is_read=False).count()
        if u.is_staff:
            out["pending_count"] = Post.objects.filter(status=Post.PENDING).count()
    return out
