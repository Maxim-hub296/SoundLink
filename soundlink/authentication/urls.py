from django.urls import path

from .views import RegistrationView, LoginView, LogoutView

app_name = "auth"
urlpatterns = [
    path("auth/register/", RegistrationView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
]
