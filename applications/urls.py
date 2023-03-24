from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.linked_jobs, name='linked_jobs')
]