from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Book
from .forms import BorrowRecordFilterForm


@login_required()
def index(request):

    all_books = Book.objects.all()
    context = {"books_list": all_books}
    try:
        context.update({"redirect_context": request.session.pop("redirect_context")})
    except KeyError:
        pass

    return render(request, "books/index.html", context)


@login_required()
def detail(request: HttpRequest, book_id):
    book = get_object_or_404(Book, pk=book_id)
    username = request.user.username

    return render(
        request, "books/display_book.html", {"book": book, "username": username}
    )


@login_required()
def borrow_book(request: HttpRequest, book_id):
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

    form = BorrowRecordFilterForm(request.GET)
    if form.is_valid():
        borrow_records = form.apply_filter_on_model()

    context = {"form": form, "borrow_records": borrow_records}
    return render(request, "books/borrow_record_list.html", context)
