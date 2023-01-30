from django.urls import re_path, path, include
from .views import FacebookWebhook


urlpatterns = [
    path("webhook-facebook/", FacebookWebhook.as_view(), name="facebook-webhook"),
]