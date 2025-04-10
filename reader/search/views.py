from django.shortcuts import render
from django.http import HttpResponse
from openlibrary.openlibrary import *
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from journal.models import Book, BookToUser
from recommendations.models import Recommendation, RecommendationLike

# Search for book/author
def search(request):
    searchString = request.GET.get('q', False)
    book_page = int(request.GET.get('book_page', 1))
    author_page = int(request.GET.get('author_page', 1))
    results = '{}'
    author_results = None
    book_results = None
    if searchString:
        client = OpenLibraryClient()
        author_results = client.search_author(searchString, author_page)
        book_results = client.search_book(searchString, book_page)
        if not author_results or not book_results:
            return HttpResponse(status=500)

    return render(request, 'search/search.html', {'q': searchString, 'book_page': book_page, 'book_results': book_results, 'author_page': author_page, 'author_results': author_results})

# Show a single Book
def book(request, *args, **kwargs):
    
    # See if book already exists in DB
    book = None
    db_books = Book.objects.filter(olid=kwargs['book_id'])
    if db_books.count() > 0:
        # Book is already in DB, serve page from that.
        book = db_books[0]
    else:
        # Book is not in DB, go fetch it from OpenLibrary
        client = OpenLibraryClient()
        book = client.get_book_by_key(kwargs['book_id'])
        rating = client.get_book_ratings(kwargs['book_id'])
        pub_date_and_editions = client.get_pub_date_and_editions(kwargs['book_id'])
        # We got a bad response from OpenLibrary, fail
        if not book or not rating or not pub_date_and_editions:
            return HttpResponse(status=500)
        print(book)
        # Do some error handling. Not all of these fields are populated.
        if not 'subjects' in book.keys():
            subjects = ""
        else:
            subjects = ', '.join(book['subjects'])
        if not 'covers' in book.keys():
            cover = ""
        else:
            cover = book['covers'][0]
        # Create Book in DB for use next time
        new_book = Book(olid=book['olid'], authors=', '.join(book['authors']), 
                        title=book['title'], cover=cover, description=book['description'],
                        first_publish_year=pub_date_and_editions['first_publish_year'], rating=rating,
                        subjects=subjects, edition_count=pub_date_and_editions['edition_count'])
        new_book.save()
        book = new_book

    if request.user.is_authenticated:
        try:
            # Get reading list entries for this book
            book_to_user = BookToUser.objects.get(user=request.user, book=book)
            book.current_status = book_to_user.state
        except BookToUser.DoesNotExist:
            book.current_status = None
    else:
        book.current_status = None

    # Get the recommendations for this book
    recommendations = Recommendation.objects.filter(book=book)
    # Get all RecommendationLikes for this user so we can mark them properly in the UI
    user_likes = RecommendationLike.objects.filter(user=request.user).values_list('recommendation_id', flat=True)

    return render(request, 'search/book_page.html', {'book': book, 'recommendations': recommendations, 'user_likes': user_likes})

