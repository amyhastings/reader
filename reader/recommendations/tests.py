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
    
    def test_recommendation_list_view_content(self):
        response = self.client.get(reverse('reader-home'))
        self.assertContains(response, self.recommendation.recommend_text)
        self.assertContains(response, self.book.title)

    def test_recommendation_detail_view(self):
        response = self.client.get(reverse('recommendation_detail', args=[self.recommendation.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.recommendation.recommend_text)
    
    def test_recommendation_detail_view_content(self):
        response = self.client.get(reverse('recommendation_detail', args=[self.recommendation.pk]))
        self.assertContains(response, self.recommendation.recommend_text)
        self.assertContains(response, self.book.title)

    def test_like_recommendation(self):
        response = self.client.post(reverse('like-recommendation', args=[self.recommendation.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.recommendation.recommendation_likes.count(), 1)
    
    def test_create_recommendation_view(self):
        response = self.client.post(reverse('create_recommendation', args=[self.book.pk]), {
            'recommend_text': 'A new recommendation.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Recommendation.objects.filter(recommend_text='A new recommendation.').exists())

    def test_update_recommendation_view(self):
        response = self.client.get(reverse('update_recommendation', args=[self.recommendation.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Update Recommendation')
        response = self.client.post(reverse('update_recommendation', args=[self.recommendation.pk]), {
            'recommend_text': 'Updated recommendation text.',
        })
        self.assertEqual(response.status_code, 302)
        self.recommendation.refresh_from_db()
        self.assertEqual(self.recommendation.recommend_text, 'Updated recommendation text.')

    def test_update_recommendation_permission_denied(self):
        self.client.logout()
        other_user = User.objects.create_user(username='otheruser', password='password')
        self.client.login(username='otheruser', password='password')
        response = self.client.get(reverse('update_recommendation', args=[self.recommendation.pk]))
        self.assertEqual(response.status_code, 403)
    
    def test_delete_recommendation_view(self):
        response = self.client.get(reverse('delete_recommendation', args=[self.recommendation.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Are you sure you want to delete your recommendation')
        response = self.client.post(reverse('delete_recommendation', args=[self.recommendation.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Recommendation.objects.filter(pk=self.recommendation.pk).exists())

    def test_delete_recommendation_permission_denied(self):
        self.client.logout()
        other_user = User.objects.create_user(username='otheruser', password='password')
        self.client.login(username='otheruser', password='password')
        response = self.client.get(reverse('delete_recommendation', args=[self.recommendation.pk]))
        self.assertEqual(response.status_code, 403)
    
    def test_like_recommendation(self):
        # Like the recommendation
        response = self.client.post(reverse('like-recommendation', args=[self.recommendation.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.recommendation.recommendation_likes.count(), 1)

        # Unlike the recommendation
        response = self.client.post(reverse('like-recommendation', args=[self.recommendation.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.recommendation.recommendation_likes.count(), 0)
    
    def test_update_recommendation_invalid_data(self):
        response = self.client.post(reverse('update_recommendation', args=[self.recommendation.pk]), {
            'recommend_text': '',  # Empty text
        })
        self.assertEqual(response.status_code, 200)  # Form re-renders with errors
        self.assertFormError(response, 'form', 'recommend_text', 'This field is required.')
    
    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get(reverse('update_recommendation', args=[self.recommendation.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        # Attempt to access the delete view
        response = self.client.get(reverse('delete_recommendation', args=[self.recommendation.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect to login

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
    
    def test_update_template_used(self):
        response = self.client.get(reverse('update_recommendation', args=[self.recommendation.pk]))
        self.assertTemplateUsed(response, 'recommendations/update_recommendation_form.html')
    
    def test_delete_template_used(self):
        response = self.client.get(reverse('delete_recommendation', args=[self.recommendation.pk]))
        self.assertTemplateUsed(response, 'recommendations/recommendation_confirm_delete.html')