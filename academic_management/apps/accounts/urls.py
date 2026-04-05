from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView  # Use Django's built-in logout

# app_name = 'accounts' # Allows URL namespacing e.g., 'accounts:login'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('verify/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('resend-verification/', views.resend_verification, name='resend_verification'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('student-list/', views.student_list_view, name='student-list'),
    path('grading/', views.grading_view, name='grading'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    # path('logout/', views.register_view, name='logout'),
]