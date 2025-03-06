import pytest
from openlibrary.client import OpenLibraryClient
from openlibrary.endpoints.authors import AuthorsEndpoint

@pytest.fixture
def client():
    return OpenLibraryClient()

@pytest.fixture
def authors_endpoint(client):
    return AuthorsEndpoint(client)

def test_get_author(authors_endpoint):
    author_key = "OL12345A"  # Example author key
    author = authors_endpoint.get_author(author_key)
    assert author is not None
    assert author['key'] == author_key

def test_get_authors_by_book(authors_endpoint):
    book_key = "OL1234567M"  # Example book key
    authors = authors_endpoint.get_authors_by_book(book_key)
    assert isinstance(authors, list)

def test_get_authors_by_subject(authors_endpoint):
    subject = "Science Fiction"  # Example subject
    authors = authors_endpoint.get_authors_by_subject(subject)
    assert isinstance(authors, list)

def test_get_author_not_found(authors_endpoint):
    author_key = "OL99999A"  # Non-existent author key
    author = authors_endpoint.get_author(author_key)
    assert author is None

def test_get_authors_by_book_not_found(authors_endpoint):
    book_key = "OL9999999M"  # Non-existent book key
    authors = authors_endpoint.get_authors_by_book(book_key)
    assert authors == []  # Expecting an empty list for non-existent book

def test_get_authors_by_subject_not_found(authors_endpoint):
    subject = "Non-Existent Subject"  # Non-existent subject
    authors = authors_endpoint.get_authors_by_subject(subject)
    assert authors == []  # Expecting an empty list for non-existent subject