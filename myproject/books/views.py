from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Book, Visitor, BorrowRecord
from django.views import generic


# class IndexView(generic.ListView):
#     template_name = "books/index.html"
#     context_object_name = "books_list"

#     def get_queryset(self):
#         """Return the last five published questions."""
#         return Book.objects.all()


def index(request):

    all_books = Book.objects.all()
    return render(request, "books/index.html", {"books_list": all_books})


def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    return render(request, "books/display_book.html", {"book": book})


def borrow_book(request, book_id):
    return HttpResponse()


# def return_book(request, book_id):
#     return render(request, "")
