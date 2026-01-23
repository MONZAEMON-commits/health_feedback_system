from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView

urlpatterns = [
    path(
        "logout/",
        LogoutView.as_view(next_page="/login/"),
        name="logout"
    ),
    path(
        "login/",
        CustomLoginView.as_view(),
        name="login"
    ),
]
