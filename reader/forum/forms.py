from django import forms
from .models import Thread, Post

# Form for creating a new forum thread
class ThreadCreateForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ('title', 'topic')

# Form for creating the first post in a forum thread
class FirstPostCreateForm(forms.ModelForm):
    class Meta:
        model = Post 
        fields = ['content']

# Form for adding a comment to an exiting forum thread
class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Post 
        fields = ['content']