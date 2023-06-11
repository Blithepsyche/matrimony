from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('login_validation/', views.login_validation, name="login-validation"),
    path('logout/', views.logout, name="logout"),
    path('sign-up/', views.signup, name="sign-up"),
    path('signup_validation/', views.signup_validation, name="sign-up-validation"),
    path('update_profile/', views.update_profile, name="update-profile"),
    path('update_validation/', views.update_validation, name="update-validation"),
    path('profiles/', views.profiles, name="profiles"),
]
