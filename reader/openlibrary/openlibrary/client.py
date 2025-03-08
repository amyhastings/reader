import math

class searchResult:
    def __init__(self, _count, _results):
        self.count = _count
        self.results = _results
        self.pages = range(1, (math.ceil(self.count / 100)+1))

class OpenLibraryClient:
    BASE_URL = "https://openlibrary.org"

    def __init__(self):
        pass

    def _get(self, endpoint, params=None):
        import requests

        url = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        print(response)
        return response.json()

    def get_books(self, params=None):
        return self._get("/books", params)

    def get_authors(self, params=None):
        return self._get("/authors", params)

    def get_subjects(self, params=None):
        return self._get("/subjects", params)

    def search_book(self, searchString, page):
        olResponse = self._get("/search.json", {'title': searchString, 'fields': 'key,title,author_name,isbn,first_publish_year,edition_count,cover_i', 'page': page})
        result = searchResult(olResponse['num_found'], olResponse['docs'])
        return result
    
    def search_author(self, searchString):
        olResponse = self._get("/search.json", {'author': searchString, 'fields': 'key,title,author_name,isbn,first_publish_year,edition_count,cover_i'})
        return olResponse['docs']
    
    def get_cover_by_id(self, coverId):
        return