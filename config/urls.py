# config/urls.py
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

urlpatterns = [
    path("", TemplateView.as_view(template_name="worldmap/templates/worldmap/index.html")),
    path("admin/", admin.site.urls),
]