class SearchEndpoint:
    BASE_URL = "https://openlibrary.org/search.json"

    def search_books(self, query, **kwargs):
        """Search for books by a query string."""
        params = {'q': query}
        params.update(kwargs)
        response = self._make_request(params)
        return response

    def search_authors(self, query, **kwargs):
        """Search for authors by a query string."""
        params = {'author': query}
        params.update(kwargs)
        response = self._make_request(params)
        return response

    def search_subjects(self, query, **kwargs):
        """Search for subjects by a query string."""
        params = {'subject': query}
        params.update(kwargs)
        response = self._make_request(params)
        return response

    def _make_request(self, params):
        """Make a GET request to the Open Library API."""
        import requests
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        return response.json()