from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    published_year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(timezone.now().year)]
    )

    def __str__(self) -> str:
        return self.title

    def is_borrowed(self) -> bool:
        # return False
        self.borrowrecord_set()  # type: ignore
        return False


class Visitor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class BorrowRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    borrower = models.ForeignKey(Visitor, on_delete=models.SET_NULL, null=True)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(default=None, null=True)
