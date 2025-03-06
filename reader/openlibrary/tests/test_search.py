import unittest
from openlibrary.client import OpenLibraryClient
from openlibrary.endpoints.search import SearchEndpoint

class TestSearchEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = OpenLibraryClient()
        self.search_endpoint = SearchEndpoint(self.client)

    def test_search_books(self):
        result = self.search_endpoint.search_books("Python")
        self.assertIsInstance(result, dict)
        self.assertIn('docs', result)

    def test_search_authors(self):
        result = self.search_endpoint.search_authors("Mark Twain")
        self.assertIsInstance(result, dict)
        self.assertIn('docs', result)

    def test_search_subjects(self):
        result = self.search_endpoint.search_subjects("Fiction")
        self.assertIsInstance(result, dict)
        self.assertIn('docs', result)

    def test_search_empty_query(self):
        result = self.search_endpoint.search_books("")
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('numFound'), 0)

if __name__ == '__main__':
    unittest.main()