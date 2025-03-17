from django.shortcuts import render
from openlibrary.openlibrary import *
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from journal.models import Book, BookToUser

def search(request):
    searchString = request.GET.get('q', False)
    book_page = request.GET.get('book_page', 1)
    author_page = request.GET.get('author_page', 1)
    results = '{}'
    author_results = None
    book_results = None
    if searchString:
        client = OpenLibraryClient()
        author_results = client.search_author(searchString, author_page)
        book_results = client.search_book(searchString, book_page)

    return render(request, 'search/search.html', {'q': searchString, 'book_page': book_page, 'book_results': book_results, 'author_page': author_page, 'author_results': author_results})

def book(request, *args, **kwargs):
    client = OpenLibraryClient()
    book = client.get_book_by_key(kwargs['book_id'])
    rating = client.get_book_ratings(kwargs['book_id'])
    pub_date_and_editions = client.get_pub_date_and_editions(kwargs['book_id'])

    if request.user.is_authenticated:
        db_book = Book.objects.get(olid=kwargs['book_id'])
        if db_book:
            try:
                book_to_user = BookToUser.objects.get(user=request.user, book=db_book)
                current_status = book_to_user.state
            except BookToUser.DoesNotExist:
                current_status = None
        else:
            current_status = None
    else:
        current_status = None

    return render(request, 'search/book_page.html', {'book': book, 'rating': rating, 'pub_date_and_editions': pub_date_and_editions, 'olid': kwargs['book_id'], 'current_status': current_status})

