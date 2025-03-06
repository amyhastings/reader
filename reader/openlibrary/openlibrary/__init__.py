# openlibrary/__init__.py

"""
This is the OpenLibrary API client package.

This package provides a client for interacting with the Open Library API,
including endpoints for books, authors, subjects, and search functionalities.
"""

from .client import OpenLibraryClient
from .endpoints.books import BooksEndpoint
from .endpoints.authors import AuthorsEndpoint
from .endpoints.subjects import SubjectsEndpoint
from .endpoints.search import SearchEndpoint

__all__ = [
    "OpenLibraryClient",
    "BooksEndpoint",
    "AuthorsEndpoint",
    "SubjectsEndpoint",
    "SearchEndpoint",
]