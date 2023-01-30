from django.urls import re_path, path, include
from .views import FacebookWebhook, get_lead


urlpatterns = [
    path("webhook-facebook/", FacebookWebhook.as_view(), name="facebook-webhook"),
    path("", get_lead, name="get-lead"),

]