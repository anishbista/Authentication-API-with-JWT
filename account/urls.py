from django.urls import path
from .views import (
    UserPasswordResetView,
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    UserChangePasswordView,
    SendPasswordResetEmailView,
)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path("changepassword/", UserChangePasswordView.as_view(), name="change_password"),
    path(
        "send_reset_password/",
        SendPasswordResetEmailView.as_view(),
        name="send_reset_password",
    ),
    path(
        "reset_password/<uid>/<token>/",
        UserPasswordResetView.as_view(),
        name="reset_password",
    ),
]
