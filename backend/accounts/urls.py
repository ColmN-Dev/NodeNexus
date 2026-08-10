# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change_password/', views.change_password, name='change_password'),
    
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
        name='password_reset'
    ),
    
    path(
        'password_reset_done/',
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
        name='password_reset_done'
    ),
    
    path(
        'password_reset_confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    
    path(
        'password_reset_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'
    )
]
