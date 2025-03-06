import unittest
from openlibrary.client import OpenLibraryClient
from openlibrary.endpoints.books import BooksEndpoint

class TestBooksEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = OpenLibraryClient()
        self.books_endpoint = BooksEndpoint(self.client)

    def test_get_book(self):
        book_id = "OL12345W"
        book = self.books_endpoint.get_book(book_id)
        self.assertIsNotNone(book)
        self.assertEqual(book['key'], f"/books/{book_id}")

    def test_get_books_by_author(self):
        author_id = "OL12345A"
        books = self.books_endpoint.get_books_by_author(author_id)
        self.assertIsInstance(books, list)
        for book in books:
            self.assertIn('author_key', book)

    def test_get_books_by_subject(self):
        subject = "Science"
        books = self.books_endpoint.get_books_by_subject(subject)
        self.assertIsInstance(books, list)
        for book in books:
            self.assertIn('subject', book)

    def test_get_books_invalid_author(self):
        author_id = "invalid_author_id"
        with self.assertRaises(ValueError):
            self.books_endpoint.get_books_by_author(author_id)

    def test_get_book_not_found(self):
        book_id = "invalid_book_id"
        book = self.books_endpoint.get_book(book_id)
        self.assertIsNone(book)

if __name__ == '__main__':
    unittest.main()