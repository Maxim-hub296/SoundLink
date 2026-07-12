from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegistrationView, LoginView, LogoutView

app_name = "authentication"
urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
