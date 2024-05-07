from django.urls import path
from . import views


app_name = "authsystem"

urlpatterns = [
    path("register/", views.Register.as_view(), name="register"),
    path("login/", views.Login.as_view(), name="login"),
    path("change-pass/", views.ChangePassword.as_view(), name="change-pass"),
    path("user-operation/", views.UserOperation.as_view(), name="user-operation"),
    path("sync-user/", views.SyncUser.as_view(), name="sync-user"),
    path("forget-password/", views.ForgetPassword.as_view(), name="forget-pass"),
    path("reset-password/", views.ResetPassword.as_view(), name="reset-pass"),
    path(
        "get-cellphone-verify-token/",
        views.GetCellphoneVerifyToken.as_view(),
        name="get-cellphone-verify-token",
    ),
]
