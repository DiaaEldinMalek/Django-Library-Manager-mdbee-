from django.urls import path
from . import views

app_name = "books"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:book_id>/", views.detail, name="detail"),
    path("<int:book_id>/borrow_book", views.borrow_book, name="borrow_book"),
    path("<int:book_id>/return_book", views.return_book, name="return_book"),
    path("borrow_records/", views.borrow_record_list, name="borrow_record_list"),
]
