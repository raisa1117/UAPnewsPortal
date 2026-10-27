from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from content.models import Post
from .models import Notification, Report, ReviewLog

staff_only = user_passes_test(lambda u: u.is_staff, login_url="login")

@staff_only
def moderate(request):
    return render(request, "moderation/moderate.html", {
        "posts": Post.objects.filter(status=Post.PENDING).select_related("category", "author").order_by("created_at"),
        "reports": Report.objects.filter(resolved=False).select_related("post", "reporter"),
        "logs": ReviewLog.objects.select_related("post", "reviewer")[:5],
    })

@staff_only
@require_POST
def review(request, pk, action):
    if action not in ("approve", "decline"):
        raise Http404
    post = get_object_or_404(Post, pk=pk)
    note = request.POST.get("note", "")[:240]
    if action == "approve":
        post.status, post.published_at, post.review_note = Post.APPROVED, timezone.now(), ""
        msg = f'Your post "{post.title}" was approved and is now live.'
    else:
        post.status, post.review_note = Post.DECLINED, note
        msg = f'Your post "{post.title}" was declined.' + (f" Note: {note}" if note else "")
    post.save()
    ReviewLog.objects.create(post=post, reviewer=request.user, action=action, note=note)
    Notification.objects.create(recipient=post.author, post=post, message=msg)
    return JsonResponse({"ok": True, "pending": Post.objects.filter(status=Post.PENDING).count()})

@login_required
@require_POST
def report(request, pk):
    post = get_object_or_404(Post, pk=pk, status=Post.APPROVED)
    reason = request.POST.get("reason", "").strip()[:240] or "No reason given"
    _, created = Report.objects.get_or_create(post=post, reporter=request.user, defaults={"reason": reason})
    return JsonResponse({"ok": True, "created": created})

@staff_only
@require_POST
def dismiss_report(request, pk):
    Report.objects.filter(pk=pk).update(resolved=True)
    return JsonResponse({"ok": True})

@login_required
def notifications(request):
    items = list(request.user.notifications.select_related("post"))
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return render(request, "moderation/notifications.html", {"items": items})
