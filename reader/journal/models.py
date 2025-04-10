from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

User = get_user_model()

# Stores data about one paritcular book. When a user views a particular book,
# we store it in the DB for quick access later.
class Book(models.Model):
    # OpenLibrary book identifier
    olid = models.CharField(max_length=100)
    # Comma separated list of authors
    authors = models.CharField(max_length=1000)
    # Title of the book
    title = models.CharField(max_length=1000)
    # OpenLibrary reference to the book cover
    cover = models.CharField(max_length=100, default="")
    # Book description, from OpenLibrary
    description = models.CharField(max_length=10000, default="")
    # First year the book was published, from OpenLibrary
    first_publish_year = models.IntegerField(default=0)
    # Book rating, from OpenLibrary
    rating = models.CharField(max_length=50, default="")
    # Book 'subjecs', from OpenLibrary. Sort of like genre, but many more options.
    subjects = models.CharField(max_length=10000, default="")
    # How many editions of the book there are in OpenLibrary
    edition_count = models.IntegerField(default=0)
    # Temp variable
    current_status = None
    
    def __str__(self):
        return self.title

# Relationship between a Book and a User.
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
    # What relationship does the user have to the book. E.g. the user wants to read the book.
    state = models.CharField(max_length=3, choices=STATE_CHOICES, default=WANT_TO_READ)
    timestamp = models.DateTimeField(auto_now_add=True)
    # Temp variable to store wether there is a JournalEntry for this book/user combo or not.
    has_journal_entry = False

    def check_for_journal_entry(self, user):
        self.has_journal_entry = JournalEntry.objects.filter(user=user, book=self.book).count() > 0

# Journal Entry written by a User about a Book
class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journalentry')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='journalentry')
    # The actual Journal Entry text
    entry = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

