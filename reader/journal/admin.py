from django.contrib import admin
from .models import Book, BookToUser, JournalEntry

# Show Book, BootToUser, and JournalEntry in the Django admin
admin.site.register(Book)
admin.site.register(BookToUser)
admin.site.register(JournalEntry)