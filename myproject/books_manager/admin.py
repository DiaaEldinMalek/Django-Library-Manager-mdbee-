from django.contrib import admin
from .models import Book, Visitor, BorrowRecord

admin.site.register(Book)

admin.site.register(Visitor)

admin.site.register(BorrowRecord)
