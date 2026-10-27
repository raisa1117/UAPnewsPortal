from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("post/<int:pk>/", views.detail, name="detail"),
    path("write/", views.create, name="create"),
    path("post/<int:pk>/edit/", views.edit, name="edit"),
    path("mine/", views.mine, name="mine"),
    path("saved/", views.saved, name="saved"),
    path("post/<int:pk>/comment/", views.comment, name="comment"),
    path("post/<int:pk>/bookmark/", views.bookmark, name="bookmark"),
]
