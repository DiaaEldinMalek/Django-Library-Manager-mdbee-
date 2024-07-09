from django.urls import path
from . import views

app_name = "books"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:book_id>/", views.detail, name="detail"),
    path("<int:book_id>/borrow_book", views.borrow_book, name="borrow_book"),
]
