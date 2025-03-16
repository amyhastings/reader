from django.contrib import admin
from .models import Book, BookToUser, JournalEntry

admin.site.register(Book)
admin.site.register(BookToUser)
admin.site.register(JournalEntry)