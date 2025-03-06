class AuthorsEndpoint:
    def __init__(self, client):
        self.client = client

    def get_author(self, author_key):
        """Fetches details of a specific author by their key."""
        response = self.client.get(f"/authors/{author_key}")
        return response.json()

    def get_authors_by_book(self, book_key):
        """Fetches authors associated with a specific book."""
        response = self.client.get(f"/books/{book_key}/authors")
        return response.json()

    def get_authors_by_subject(self, subject):
        """Fetches authors related to a specific subject."""
        response = self.client.get(f"/subjects/{subject}/authors")
        return response.json()

    def search_authors(self, query):
        """Searches for authors based on a query string."""
        response = self.client.get(f"/search/authors.json?q={query}")
        return response.json()