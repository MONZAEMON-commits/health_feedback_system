from django.urls import path
from .views import input_view
from . import views

urlpatterns = [
    path("", input_view, name="conditions_input"),
    path("complete/", views.complete_view, name="conditions_complete"),

]
