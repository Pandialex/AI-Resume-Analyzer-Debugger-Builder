from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("send-otp/", views.send_otp_ajax, name="send_otp_ajax"),
    path("forget-password/", views.forget_password_request, name="forget_password_request"),
    path("forget-password-verify/<int:user_id>/", views.forget_password_verify, name="forget_password_verify"),
    path("profile/", views.profile_view, name="profile"),
    # Optional direct result of verify (if you want separate)
    path("verify-otp/", views.register, name="verify_otp"),  # fallback: register handles OTP
]
