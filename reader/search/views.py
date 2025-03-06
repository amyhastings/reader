from django.shortcuts import render
from openlibrary.openlibrary import *

def search(request):
    searchString = request.GET.get('q', False)
    results = '{}'
    if searchString:
        client = OpenLibraryClient()
        author_results = client.search_author(searchString)
        book_results = client.search_book(searchString)
    return render(request, 'search/search.html', {'author_results': author_results, 'book_results': book_results})
