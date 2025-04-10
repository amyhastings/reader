from django import forms
from .models import JournalEntry

# Form for adding a Journal Entry
class JournalEntryCreateForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['entry']