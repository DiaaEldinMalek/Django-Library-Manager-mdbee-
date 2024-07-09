from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from .models import Book, BorrowRecord
from django.urls import reverse
from django.contrib.sessions.backends.db import SessionStore


def index(request):

    all_books = Book.objects.all()
    context = {"books_list": all_books}
    try:
        context.update({"redirect_context": request.session.pop("redirect_context")})
    except KeyError:
        pass

    return render(request, "books/index.html", context)


def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, "books/display_book.html", {"book": book})


def borrow_book(request, book_id):
    borrower_name = request.POST["borrower_name"]

    book = Book.objects.get(pk=book_id)
    status, message = book.borrow(borrower_name)
    print(book)
    if status is True:
        request.session["redirect_context"] = message
        return HttpResponseRedirect(reverse("books:index"))
    else:
        return render(
            request,
            "books/display_book.html",
            {"book": book, "error_message": message},
        )


def return_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    status, message = book.return_book()

    if status is True:
        request.session["redirect_context"] = message
        return HttpResponseRedirect(reverse("books:index"))
    else:
        return render(
            request,
            "books/display_book.html",
            {"book": book, "error_message": message},
        )
