from django.urls import path
from . import views
urlpatterns = [
    path("moderate/", views.moderate, name="moderate"),
    path("moderate/<int:pk>/<str:action>/", views.review, name="review"),
    path("post/<int:pk>/report/", views.report, name="report"),
    path("reports/<int:pk>/dismiss/", views.dismiss_report, name="dismiss_report"),
    path("notifications/", views.notifications, name="notifications"),
]
