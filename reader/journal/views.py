from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Book, BookToUser, JournalEntry

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

@login_required
def add_journal_entry(request, *args, **kwargs):
    return render(request, 'journal/add_journal_entry.html')

@login_required
def view_journal_entry(request, *args, **kwargs):
    journal_entries = JournalEntry.objects.filter(user=request.user, book=kwargs['book_id'])
    if journal_entries.count() < 1:
        return HttpResponseBadRequest()
    journal_entry = journal_entries[0]
    return render(request, 'journal/view_journal_entry.html', {'journal_entry': journal_entry})