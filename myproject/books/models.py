from typing import Optional
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    published_year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(timezone.now().year)]
    )
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title

    def current_borrower(self):
        if self.is_available:
            return None

        try:
            last_borrow_record: BorrowRecord = self.borrowrecord_set.all()[0]  # type: ignore
        except IndexError:
            self.is_available = True
            return None

        if last_borrow_record.return_date is None:
            # book has not been returned and return date is not specified
            return last_borrow_record

        elif last_borrow_record.return_date > timezone.now():
            # return date is still in the future
            return last_borrow_record

        elif last_borrow_record.return_date < timezone.now():
            # realistically, the book can be unavailable for many other reasons (stolen, destroyed, etc.)
            # but for my application I will strictly assume that no such cases exist and that this is a database fault
            self.is_available = True
            return None


class Visitor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class BorrowRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    borrower_name = models.CharField(max_length=100)
    # borrower = models.ForeignKey(Visitor, on_delete=models.SET_NULL, null=True)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(default=None, null=True)
