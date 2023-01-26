
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("adm/", admin.site.urls),
    path("api/lead/", include("lead.urls")),
]
