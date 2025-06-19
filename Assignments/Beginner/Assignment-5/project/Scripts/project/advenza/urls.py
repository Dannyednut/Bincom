from django.urls import path
from . import views
from django.template import loader


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('register/record/', views.record, name='record'),
    path('download/', views.download, name='download'),
]