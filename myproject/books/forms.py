# myapp/forms.py
from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from .models import BorrowRecord, Book


class BorrowRecordFilterForm(forms.Form):
    book = forms.ModelChoiceField(queryset=Book.objects.all(), required=False)
    borrower_name = forms.CharField(max_length=100, required=False)

    borrower_name = forms.ChoiceField(
        choices=[(n, n) for n in BorrowRecord.all_borrowers()],
        required=False,
    )
    borrowed_on_start = forms.DateTimeField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Borrow date (start range)",
    )
    borrowed_on_end = forms.DateTimeField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Borrow date (end range)",
    )
    returned_on_start = forms.DateTimeField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Return date (start range)",
    )
    returned_on_end = forms.DateTimeField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Return date (end range)",
    )

    # def _post_clean(self):
    #     cleaned_data = self.cleaned_data

    #     if cleaned_data["borrowed_on_start"] > cleaned_data["borrowed_on_end"]:
    #         raise ValidationError("Invalid borrow date range")

    #     if cleaned_data["returned_before"] > cleaned_data["returned_after"]:
    #         raise ValidationError("Invalid borrow date range")

    #     return super().clean()

    def apply_filter_on_model(self):
        borrow_records = BorrowRecord.objects.all()

        if self.is_valid():
            if book := self.cleaned_data.get("book"):
                borrow_records = borrow_records.filter(book=book)

            if borrower_name := self.cleaned_data.get("borrower_name"):
                borrow_records = borrow_records.filter(
                    borrower_name__icontains=borrower_name
                )
            if borrowed_on_start := self.cleaned_data.get("borrowed_on_start"):
                borrow_records = borrow_records.filter(
                    borrow_date__gte=borrowed_on_start
                )
            if borrowed_on_end := self.cleaned_data.get("borrowed_on_end"):
                borrow_records = borrow_records.filter(borrow_date__lte=borrowed_on_end)

            if returned_on_start := self.cleaned_data.get("returned_on_start"):
                borrow_records = borrow_records.filter(
                    return_date__gte=returned_on_start
                )
            if returned_on_end := self.cleaned_data.get("returned_on_end"):
                borrow_records = borrow_records.filter(return_date__lte=returned_on_end)

        return borrow_records
