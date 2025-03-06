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

    def search_book(self, searchString):
        olResponse = self._get("/search.json", {'title': searchString, 'fields': 'key,title,author_name,isbn,publish_year'})
        return olResponse['docs']
    
    def search_author(self, searchString):
        olResponse = self._get("/search.json", {'author': searchString, 'fields': 'key,title,author_name,isbn,publish_year'})
        return olResponse['docs']
    
    def get_cover_by_id(self, coverId):
        return