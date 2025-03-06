# Open Library API Client

This project is a Python library that provides a simple interface for interacting with the Open Library API. It allows users to access various endpoints related to books, authors, subjects, and search functionalities.

## Features

- Access to books-related endpoints:
  - Get details of a specific book
  - Retrieve books by author
  - Retrieve books by subject

- Access to authors-related endpoints:
  - Get details of a specific author
  - Retrieve authors by book
  - Retrieve authors by subject

- Access to subjects-related endpoints:
  - Get details of a specific subject
  - Retrieve all subjects
  - Retrieve books by subject

- Search functionality:
  - Search for books
  - Search for authors
  - Search for subjects

## Installation

To install the library, clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/openlibrary-api.git
cd openlibrary-api
pip install -r requirements.txt
```

## Usage

Here is a basic example of how to use the library:

```python
from openlibrary.client import OpenLibraryClient

client = OpenLibraryClient()

# Get a book by its ID
book = client.books.get_book('OL12345W')
print(book)

# Search for books by a specific author
books_by_author = client.books.get_books_by_author('OL12345A')
print(books_by_author)
```

## Running Tests

To run the tests for the library, use the following command:

```bash
pytest tests/
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.