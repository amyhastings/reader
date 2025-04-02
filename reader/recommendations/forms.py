from django import forms
from .models import Recommendation

class RecommendationCreateForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = ['recommend_text', 'recommend_who', 'recommend_favourite_part', 'recommend_why']
        labels = {
            'recommend_text': 'Why did you love this book? (Required)',
            'recommend_who': 'Who do you think should read this book?',
            'recommend_favourite_part': 'Did you have a favourite part of the book or is there a memorable quote that you loved?',
            'recommend_why': 'What makes this recommendation personal? Tell us about your own experience with the book—maybe it changed your perspective or helped you through a tough time.',
        }