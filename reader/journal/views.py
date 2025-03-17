from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Book, BookToUser

@login_required
def want_to_read(request, olid):
    if request.method == 'POST':
        # Check if the book already exists in the Book table
        book, created = Book.objects.get_or_create(olid=olid, defaults={
            'title': request.POST.get('title'),
            'author': request.POST.get('author')
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
            'author': request.POST.get('author')
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
            'author': request.POST.get('author')
        })

        # Add the book to the BookToUser table with state HAVE_READ
        b2u, created = BookToUser.objects.get_or_create(user=request.user, book=book, defaults={'state': BookToUser.HAVE_READ})
        b2u.state = BookToUser.HAVE_READ
        b2u.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)