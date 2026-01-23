from django.urls import path
from .views import dashboard_home,index

urlpatterns = [
    path("", dashboard_home),
    path("", index, name="dashboard_index"),
]
