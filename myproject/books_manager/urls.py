from django.urls import path
from . import views

app_name = "books_manager"
urlpatterns = [
    path("", views.index, name="index"),
]
