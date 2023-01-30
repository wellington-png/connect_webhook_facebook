
from django.contrib import admin
from django.urls import path, include
from lead.views import  get_lead

urlpatterns = [
    path("adm/", admin.site.urls),
    path("api/lead/", include("lead.urls")),
    path("", get_lead),
]
