# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("worldmap.urls")),  # ★トップを worldmap に
    path("admin/", admin.site.urls),
]
