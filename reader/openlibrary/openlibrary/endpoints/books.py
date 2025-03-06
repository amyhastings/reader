import requests

class BooksEndpoint:
    BASE_URL = "https://openlibrary.org/api/books"

    def get_book(self, bibkey):
        """Fetch a book by its BibKey."""
        response = requests.get(f"{self.BASE_URL}?bibkeys={bibkey}&format=json")
        return response.json()

    def get_books_by_author(self, author_key):
        """Fetch books by a specific author."""
        response = requests.get(f"{self.BASE_URL}/authors/{author_key}/works.json")
        return response.json()

    def get_books_by_subject(self, subject):
        """Fetch books related to a specific subject."""
        response = requests.get(f"{self.BASE_URL}/subjects/{subject}.json")
        return response.json()

    def get_book_details(self, book_id):
        """Fetch detailed information about a specific book."""
        response = requests.get(f"{self.BASE_URL}/{book_id}.json")
        return response.json()