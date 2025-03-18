from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book, BookToUser, JournalEntry

class JournalAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.book = Book.objects.create(title='Test Book', authors='Test Author', olid='OL12345M')
        self.book_to_user = BookToUser.objects.create(user=self.user, book=self.book, state='WTR')
        self.journal_entry = JournalEntry.objects.create(user=self.user, book=self.book, entry='Test journal entry')

    def test_reading_list_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('my_lists'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/reading_list.html')
        self.assertContains(response, 'Test Book')
    
    def test_add_journal_entry_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('add_journal_entry', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/add_journal_entry.html')

    def test_view_journal_entry_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('view_journal_entry', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal/view_journal_entry.html')
        self.assertContains(response, 'Test journal entry')
    
    def test_view_journal_entry_view_no_entry(self):
        self.client.login(username='testuser', password='12345')
        JournalEntry.objects.filter(id=self.journal_entry.id).delete()
        response = self.client.get(reverse('view_journal_entry', args=[self.book.id]))
        self.assertEqual(response.status_code, 400)

    def test_reading_list_view_not_logged_in(self):
        response = self.client.get(reverse('my_lists'))
        self.assertEqual(response.status_code, 302)

    def test_add_journal_entry_view_not_logged_in(self):
        response = self.client.get(reverse('add_journal_entry', args=[self.book.id]))
        self.assertEqual(response.status_code, 302)

    def test_view_journal_entry_view_not_logged_in(self):
        response = self.client.get(reverse('view_journal_entry', args=[self.book.id]))
        self.assertEqual(response.status_code, 302)