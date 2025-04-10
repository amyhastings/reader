from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from .models import Book, BookToUser, JournalEntry

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django import forms
from .forms import JournalEntryCreateForm

User = get_user_model()

# Mark this book as 'want to read' (called by js)
@login_required
def want_to_read(request, olid):
    if request.method == 'POST':
        # Check if the book already exists in the Book table
        book, created = Book.objects.get_or_create(olid=olid, defaults={
            'title': request.POST.get('title'),
            'author': request.POST.get('author'),
            'cover': request.POST.get('cover'),
        })

        # Add the book to the BookToUser table with state WANT_TO_READ
        b2u, created = BookToUser.objects.get_or_create(user=request.user, book=book, defaults={'state': BookToUser.WANT_TO_READ})
        b2u.state = BookToUser.WANT_TO_READ
        b2u.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

# Mark this book as 'am reading' (called by js)
@login_required
def am_reading(request, olid):
    if request.method == 'POST':
        # Check if the book already exists in the Book table
        book, created = Book.objects.get_or_create(olid=olid, defaults={
            'title': request.POST.get('title'),
            'author': request.POST.get('author'),
            'cover': request.POST.get('cover'),
        })

        # Add the book to the BookToUser table with state AM_READING
        b2u, created = BookToUser.objects.get_or_create(user=request.user, book=book, defaults={'state': BookToUser.AM_READING})
        b2u.state = BookToUser.AM_READING
        b2u.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

# Mark this book as 'have read' (called by js)
@login_required
def have_read(request, olid):
    if request.method == 'POST':
        # Check if the book already exists in the Book table
        book, created = Book.objects.get_or_create(olid=olid, defaults={
            'title': request.POST.get('title'),
            'author': request.POST.get('author'),
            'cover': request.POST.get('cover'),
        })

        # Add the book to the BookToUser table with state HAVE_READ
        b2u, created = BookToUser.objects.get_or_create(user=request.user, book=book, defaults={'state': BookToUser.HAVE_READ})
        b2u.state = BookToUser.HAVE_READ
        b2u.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

# Remove relationship between Book and User
@login_required
def delete_book_to_user(request, book_id):
    book_to_user = get_object_or_404(BookToUser, user=request.user, book_id=book_id)
    book_to_user.delete()
    return redirect('my_lists')

# Show all Book to User relationships
@login_required
def reading_list(request):
    user_books = BookToUser.objects.filter(user=request.user)
    journal_entry = JournalEntry.objects.filter(user=request.user)
    user_books_wtr = []
    user_books_ar = []
    user_books_hr = []
    for user_book in user_books:
        if user_book.state == 'WTR':
            user_books_wtr.append(user_book)
        elif user_book.state == 'AR':
            user_books_ar.append(user_book)
        elif user_book.state == 'HR':
            user_books_hr.append(user_book)
        user_book.check_for_journal_entry(request.user)
    return render(request, 'journal/reading_list.html', {'user_books_wtr': user_books_wtr, 'user_books_ar': user_books_ar, 'user_books_hr': user_books_hr, 'journal_entry': journal_entry})

# Add a Journal Entry for this Book
@login_required
def add_journal_entry(request, *args, **kwargs):
    return render(request, 'journal/add_journal_entry.html')

# Show a Journal Entry
@login_required
def view_journal_entry(request, *args, **kwargs):
    journal_entries = JournalEntry.objects.filter(user=request.user, book=kwargs['book_id'])
    # Error handling
    if journal_entries.count() < 1:
        return HttpResponseBadRequest()
    journal_entry = journal_entries[0]
    return render(request, 'journal/view_journal_entry.html', {'journal_entry': journal_entry})

# Show all Journal Entries
class UserJournalEntryListView(ListView):
    model = JournalEntry
    template_name = 'journal/my_journal.html'
    context_object_name = 'user_journal_entries'
    paginate_by = 5

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user).order_by('timestamp')

# Create a new Journal Entry
@login_required
def create_journal_entry(request, *args, **kwargs):
    book = get_object_or_404(Book, id=kwargs['book_id'])

    if request.method == 'POST':
        form = JournalEntryCreateForm(request.POST)

        if form.is_valid():
            journal_entry = form.save(commit=False)
            journal_entry.book = book
            journal_entry.user = request.user
            journal_entry.save()
            return redirect(reverse('view_journal_entry', kwargs={'book_id': journal_entry.book.id}))

    else:
        form = JournalEntryCreateForm()
    return render(request, 'journal/journal_entry_form.html', {'form': form, 'book': book})

# Change relationship between Book and User
@login_required
def change_book_status(request, book_id, status):
    book_to_user = get_object_or_404(BookToUser, user=request.user, book_id=book_id)
    book_to_user.state = status
    book_to_user.save()
    return redirect('my_lists')

# Show form to modify a Journal Entry
class JournalEntryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): 
    model = JournalEntry
    template_name = 'journal/update_journal_entry_form.html'
    fields = ['entry']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        journal_entry = get_object_or_404(JournalEntry, id=self.kwargs['pk'])
        return reverse_lazy('view_journal_entry', kwargs={'book_id': journal_entry.book.id})
    
    def test_func(self):
        journal_entry = self.get_object()
        return self.request.user == journal_entry.user

# Delete a Journal Entry
class JournalEntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = JournalEntry
    template_name = 'journal/journal_entry_confirm_delete.html'

    def test_func(self):
        journal_entry = self.get_object()
        return self.request.user == journal_entry.user
    
    def get_success_url(self):
        return reverse_lazy('all_journal_entries')