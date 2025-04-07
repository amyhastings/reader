from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Book, Recommendation, RecommendationLike

User = get_user_model()

class RecommendationModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.book = Book.objects.create(title='Test Book', authors='Author Name')
        self.recommendation = Recommendation.objects.create(
            book=self.book,
            user=self.user,
            recommend_text='This is a test recommendation.'
        )

    def test_recommendation_creation(self):
        self.assertEqual(self.recommendation.book.title, 'Test Book')
        self.assertEqual(self.recommendation.user.username, 'testuser')
        self.assertEqual(self.recommendation.recommend_text, 'This is a test recommendation.')

    def test_recommendation_like(self):
        like = RecommendationLike.objects.create(user=self.user, recommendation=self.recommendation)
        self.assertEqual(self.recommendation.recommendation_likes.count(), 1)
        self.assertEqual(like.user.username, 'testuser')

class RecommendationViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.book = Book.objects.create(title='Test Book', authors='Author Name', olid='123456')
        self.recommendation = Recommendation.objects.create(
            book=self.book,
            user=self.user,
            recommend_text='This is a test recommendation.'
        )
        self.client.login(username='testuser', password='password')

    def test_recommendation_list_view(self):
        response = self.client.get(reverse('reader-home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Recommendations')
        self.assertContains(response, self.recommendation.recommend_text)

    def test_recommendation_detail_view(self):
        response = self.client.get(reverse('recommendation_detail', args=[self.recommendation.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.recommendation.recommend_text)

    def test_like_recommendation(self):
        response = self.client.post(reverse('like-recommendation', args=[self.recommendation.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.recommendation.recommendation_likes.count(), 1)

class RecommendationTemplateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.book = Book.objects.create(title='Test Book', authors='Author Name', olid='123456')
        self.recommendation = Recommendation.objects.create(
            book=self.book,
            user=self.user,
            recommend_text='This is a test recommendation.'
        )
        self.client.login(username='testuser', password='password')

    def test_home_template_used(self):
        response = self.client.get(reverse('reader-home'))
        self.assertTemplateUsed(response, 'recommendations/home.html')
    
    def test_detail_template_used(self):
        response = self.client.get(reverse('recommendation_detail', args=[self.recommendation.pk]))
        self.assertTemplateUsed(response, 'recommendations/recommendation_detail.html')