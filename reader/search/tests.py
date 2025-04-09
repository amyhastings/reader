from django.test import TestCase, Client
from django.urls import reverse

class SearchViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.search_url = reverse('search')

    def test_search_with_valid_query(self):
        response = self.client.get(self.search_url, {'q': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Search')
        self.assertContains(response, 'test')

    def test_search_pagination(self):
        response = self.client.get(self.search_url, {'q': 'test', 'book_page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Search')
        self.assertContains(response, 'book_page=2')
