from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from moderation.models import Notification
from .forms import CommentForm, PostForm
from .models import Bookmark, Category, Post, Tag

def _save_tags(post, raw):
    names = list(dict.fromkeys(t.strip().lower()[:30] for t in raw.split(",") if t.strip()))[:6]
    post.tags.set([Tag.objects.get_or_create(name=n)[0] for n in names])

def _public():
    return Post.objects.filter(status=Post.APPROVED).select_related("category", "author").prefetch_related("tags")

def home(request):
    return render(request, "content/home.html", {"posts": _public(), "categories": Category.objects.all()})

def detail(request, pk):
    post = get_object_or_404(Post.objects.select_related("category", "author__profile__department").prefetch_related("tags"), pk=pk)
    u = request.user
    if post.status != Post.APPROVED and not (u.is_authenticated and (u.is_staff or u == post.author)):
        raise Http404
    saved = u.is_authenticated and Bookmark.objects.filter(user=u, post=post).exists()
    return render(request, "content/detail.html", {"post": post, "saved": saved, "form": CommentForm(),
                  "comments": post.comments.select_related("user")})

@login_required
def create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        if request.user.is_staff:
            post.status, post.published_at = Post.APPROVED, timezone.now()
            messages.success(request, "Published. Staff posts go live immediately.")
        else:
            messages.success(request, "Submitted for review. An admin will approve or decline it.")
        post.save()
        _save_tags(post, form.cleaned_data["tags"])
        return redirect("mine")
    return render(request, "content/form.html", {"form": form, "title": "Write a post"})

@login_required
def edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    form = PostForm(request.POST or None, instance=post, initial={"tags": ", ".join(t.name for t in post.tags.all())})
    if form.is_valid():
        post = form.save(commit=False)
        if not request.user.is_staff:
            post.status, post.review_note, post.published_at = Post.PENDING, "", None
        post.save()
        _save_tags(post, form.cleaned_data["tags"])
        messages.success(request, "Changes saved." + ("" if request.user.is_staff else " Your post is back in the review queue."))
        return redirect("mine")
    return render(request, "content/form.html", {"form": form, "title": "Edit post"})

@login_required
def mine(request):
    return render(request, "content/mine.html", {"posts": request.user.posts.select_related("category")})

@login_required
def saved(request):
    ids = request.user.bookmarks.values_list("post_id", flat=True)
    return render(request, "content/saved.html", {"posts": _public().filter(pk__in=ids)})

@login_required
@require_POST
def comment(request, pk):
    post = get_object_or_404(Post, pk=pk, status=Post.APPROVED)
    form = CommentForm(request.POST)
    if form.is_valid():
        c = form.save(commit=False)
        c.post, c.user = post, request.user
        c.save()
        if post.author != request.user:
            Notification.objects.create(recipient=post.author, post=post,
                                        message=f'{request.user.username} commented on "{post.title}"')
    return redirect(post)

@login_required
@require_POST
def bookmark(request, pk):
    post = get_object_or_404(Post, pk=pk, status=Post.APPROVED)
    obj, created = Bookmark.objects.get_or_create(user=request.user, post=post)
    if not created:
        obj.delete()
    return JsonResponse({"saved": created})
