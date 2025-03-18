from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

User = get_user_model()

class Book(models.Model):
    olid = models.CharField(max_length=100)
    authors = models.CharField(max_length=1000)
    title = models.CharField(max_length=1000)
    cover = models.CharField(max_length=100, default="")

    description = models.CharField(max_length=10000, default="")
    first_publish_year = models.IntegerField(default=0)
    rating = models.CharField(max_length=50, default="")
    subjects = models.CharField(max_length=10000, default="")
    edition_count = models.IntegerField(default=0)

    current_status = None
    
    def __str__(self):
        return self.title


class BookToUser(models.Model):
    WANT_TO_READ = "WTR"
    AM_READING = "AR"
    HAVE_READ = "HR"
    STATE_CHOICES = [
        (WANT_TO_READ, "Want to Read"),
        (AM_READING, "Am Reading"),
        (HAVE_READ, "Have Read"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booktouser')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='booktouser')
    state = models.CharField(max_length=3, choices=STATE_CHOICES, default=WANT_TO_READ)
    timestamp = models.DateTimeField(auto_now_add=True)
    has_journal_entry = False

    def check_for_journal_entry(self, user):
        self.has_journal_entry = JournalEntry.objects.filter(user=user, book=self.book).count() > 0

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journalentry')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='journalentry')
    entry = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

