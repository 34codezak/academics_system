from django.urls import path
from . import views

# app_name = 'dashboard'

urlpatterns = [

    path('', views.dashboard_view, name='home'),
    path('courses/', views.courses_view, name='courses'),
    path('reports/', views.reports_view, name='reports'),
]