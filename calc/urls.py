from django.conf.urls import url, include
from django.contrib import admin
from . import views

app_name="calc"
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'add/', views.AddView.as_view(), name="add"),
    url(r'calc/', views.CalcView.as_view(), name="calc"),
]