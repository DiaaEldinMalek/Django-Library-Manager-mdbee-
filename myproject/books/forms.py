# myapp/forms.py
from django import forms
from .models import BorrowRecord, Book


class BorrowRecordFilterForm(forms.Form):
    book = forms.ModelChoiceField(queryset=Book.objects.all(), required=False)
    borrower_name = forms.CharField(max_length=100, required=False)
    start_date = forms.DateTimeField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )
    end_date = forms.DateTimeField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )
