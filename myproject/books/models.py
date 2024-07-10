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
        """Return the last BorrowRecord if the book is currently borrowed. Otherwise, book is available and return None"""
        if self.is_available:
            return None

        try:
            last_borrow_record: BorrowRecord = self.borrowrecord_set.all().order_by("-borrow_date")[0]  # type: ignore
            if not last_borrow_record.is_returned():
                return last_borrow_record
        except IndexError:
            # realistically, the book can be unavailable for many other reasons (stolen, destroyed, etc.)
            # but for my application I will strictly assume that no such cases exist and that this is a database fault
            pass

        self.is_available = True
        self.save()
        return None

    def borrow(self, borrower_name: str):
        try:
            if self.is_available:
                self.borrowrecord_set.create(borrower_name=borrower_name)
                self.is_available = False
                self.save()
                return True, "Book borrowed successfuly"
            else:
                return False, "Book Unavailable for borrowing"
        except Exception as e:
            return False, str(e)

    def return_book(self):
        try:
            record: BorrowRecord = self.borrowrecord_set.all().order_by("-borrow_date")[
                0
            ]
            record.return_now()
            record.save()

            self.is_available = True
            self.save()

            return True, "Book returned successfuly"
        except IndexError:
            return False, "Book is not borrowed by anyone"
        except Exception as e:
            return False, str(e)


class BorrowRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    borrower_name = models.CharField(max_length=100)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(default=None, null=True)

    def __str__(self) -> str:
        return f"borrower:{self.borrower_name} | borrow_date:{self.borrow_date} | {f'return_date:{self.return_date}' if self.return_date else 'Not yet returned' }"

    def return_now(self):
        if self.return_date is None:
            self.return_date = timezone.now()
        else:
            raise Exception("BorrowRecord already closed")

    def is_returned(self):
        if self.return_date is None:
            # book has not been returned and return date is unset
            return False

        elif self.return_date > timezone.now():
            # return date is still in the future
            return False

        elif self.return_date < timezone.now():
            return True
        else:
            raise Exception(f"Invalid value for field {self.return_date}")

    @classmethod
    def all_borrowers(cls):
        all_borrowers = [record.borrower_name for record in BorrowRecord.objects.all()]
        return all_borrowers
