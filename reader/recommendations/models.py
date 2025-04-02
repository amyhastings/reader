from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from journal.models import Book

User = get_user_model()

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendation')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='recommendation')
    recommend_text = models.TextField()
    recommend_who = models.TextField(blank=True)
    recommend_favourite_part = models.TextField(blank=True)
    recommend_why = models.TextField(blank=True)
    upvotes = models.CharField(max_length=100)
    downvotes = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

