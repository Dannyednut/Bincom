from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('register/record/', views.record, name='record'),
    path('download/', views.download, name='download'),
]