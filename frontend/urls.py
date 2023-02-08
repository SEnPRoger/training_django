from django.contrib import admin
from django.urls import path
from frontend import views

app_name = "frontend"

urlpatterns = [
    path('', views.showHome, name="home"),
    path('auth/', views.showAuth, name="auth"),
]