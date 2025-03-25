from django import forms
from .models import JournalEntry

class JournalEntryCreateForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['entry']