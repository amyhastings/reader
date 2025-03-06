import unittest
from openlibrary.client import OpenLibraryClient
from openlibrary.endpoints.subjects import SubjectsEndpoint

class TestSubjectsEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = OpenLibraryClient()
        self.subjects_endpoint = SubjectsEndpoint(self.client)

    def test_get_subject(self):
        subject_key = "subject:science"
        response = self.subjects_endpoint.get_subject(subject_key)
        self.assertIn('key', response)
        self.assertEqual(response['key'], subject_key)

    def test_get_subjects(self):
        response = self.subjects_endpoint.get_subjects()
        self.assertIsInstance(response, list)
        self.assertGreater(len(response), 0)

    def test_get_books_by_subject(self):
        subject_key = "subject:science"
        response = self.subjects_endpoint.get_books_by_subject(subject_key)
        self.assertIsInstance(response, list)
        self.assertGreater(len(response), 0)

if __name__ == '__main__':
    unittest.main()