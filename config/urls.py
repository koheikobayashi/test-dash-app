# config/urls.py
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

urlpatterns = [
    path("", lambda request: HttpResponse("It works")),
    path("admin/", admin.site.urls),
]