from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Book, BorrowRecord
from django.urls import reverse
from .forms import BorrowRecordFilterForm


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


def borrow_record_list(request):

    form = BorrowRecordFilterForm(request.GET)
    borrow_records = BorrowRecord.objects.all()

    if form.is_valid():
        if form.cleaned_data.get("borrower_name"):
            borrow_records = borrow_records.filter(
                borrower_name__icontains=form.cleaned_data["borrower_name"]
            )
        if form.cleaned_data.get("start_date"):
            borrow_records = borrow_records.filter(
                borrow_date__gte=form.cleaned_data["start_date"]
            )
        if form.cleaned_data.get("end_date"):
            borrow_records = borrow_records.filter(
                borrow_date__lte=form.cleaned_data["end_date"]
            )
        if form.cleaned_data.get("book"):
            borrow_records = borrow_records.filter(book=form.cleaned_data["book"])

    context = {"form": form, "borrow_records": borrow_records}
    return render(request, "books/borrow_record_list.html", context)
