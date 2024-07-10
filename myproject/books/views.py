from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Book
from .forms import BorrowRecordFilterForm


@login_required()
def index(request):
    """Index view that retrieves and lists all books. Front page of the `books` application"""
    all_books = Book.objects.all()
    context = {"books_list": all_books}
    try:
        context.update({"redirect_context": request.session.pop("redirect_context")})
    except KeyError:
        pass

    return render(request, "books/index.html", context)


@login_required()
def detail(request: HttpRequest, book_id):
    """Retrieves and presents details about the book and potential borrower"""
    book = get_object_or_404(Book, pk=book_id)
    username = request.user.username

    return render(
        request, "books/display_book.html", {"book": book, "username": username}
    )


@login_required()
def borrow_book(request: HttpRequest, book_id):
    """Borrows a book under the current user name and writes to database"""
    username = request.user.username

    book = Book.objects.get(pk=book_id)
    status, message = book.borrow(username)
    if status is True:
        request.session["redirect_context"] = message
        return HttpResponseRedirect(reverse("books:index"))
    else:
        return render(
            request,
            "books/display_book.html",
            {"book": book, "error_message": message},
        )


@login_required()
def return_book(request: HttpRequest, book_id):
    """Returns the book borrowed by the current user and updates the book on the database"""
    book = Book.objects.get(pk=book_id)
    username = request.user.username

    status, message = book.return_book(username)

    if status is True:
        request.session["redirect_context"] = message
        return HttpResponseRedirect(reverse("books:index"))
    else:
        return render(
            request,
            "books/display_book.html",
            {"book": book, "error_message": message},
        )


@login_required()
def borrow_record_list(request):
    """Retrieves all BorrowRecords from database and displays them (after applying filter)"""
    form = BorrowRecordFilterForm(request.GET)
    if form.is_valid():
        borrow_records = form.apply_filter_on_model()

    context = {"form": form, "borrow_records": borrow_records}
    return render(request, "books/borrow_record_list.html", context)
