from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Visitor, BorrowRecord


def index(request):

    available_books = Book.objects.all()
    return render(request, "books/index.html", {"books_list": available_books})
