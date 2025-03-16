from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile

class UserFormsTests(TestCase):
    def setUp(self):
        # This sets up a user and profile for the User app tests
        self.user = User.objects.create_user(username='testuser', password='12345')
        Profile.objects.get_or_create(user=self.user, defaults={'image': 'default.png'})

    def test_register_view_get(self):
        # Test the register view with a GET request
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_view_post_valid(self):
        # Test the register view with valid POST data
        form_data = {
            'username': 'newuser',
            'email': 'newuser@fake.com',
            'password1': 'testing1234',
            'password2': 'testing1234'
        }
        response = self.client.post(reverse('register'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertRedirects(response, reverse('login'))
    
    def test_register_view_post_invalid(self):
        # Test the register view with invalid POST data
        form_data = {
            'username': '',
            'email': 'newuser@fake.com',
            'password1': 'testing1234',
            'password2': 'testing1234'
        }
        response = self.client.post(reverse('register'), data=form_data)
        self.assertEqual(response.status_code, 200)  # Re-render the form with errors
        self.assertTemplateUsed(response, 'users/register.html')
    
    def test_profile_view_get(self):
        # Test the profile view with a GET request
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
    
    def test_profile_view_post_invalid(self):
        # Test the profile view with invalid POST data
        self.client.login(username='testuser', password='12345')
        form_data = {
            'username': '',
            'email': 'updateuser@fake.com',
        }
        response = self.client.post(reverse('profile'), data=form_data)
        self.assertEqual(response.status_code, 200)  # Re-render the form with errors
        self.assertTemplateUsed(response, 'users/profile.html')
    
    def test_profile_update_with_invalid_image_format(self):
        # Test profile update with an invalid image format
        invalid_image_data = b'this is not real image data'
        invalid_image_file = SimpleUploadedFile('new_image.txt', invalid_image_data, content_type='text/plain')
        form = ProfileUpdateForm(files={'image': invalid_image_file}, instance=self.user.profile)
        self.assertFalse(form.is_valid())
    
    def test_profile_update_with_oversized_image(self):
        # Test profile update with an oversized image
        oversized_image_data = b'\x00' * 10485760 # 10MB which is my Cloudinary limit
        oversized_image_file = SimpleUploadedFile('new_image.jpg', oversized_image_data, content_type='image/jpeg')
        form = ProfileUpdateForm(files={'image': oversized_image_file}, instance=self.user.profile)
        self.assertFalse(form.is_valid())
    
    def test_profile_view_not_logged_in(self):
        # Test the profile view without being logged in
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile')}")

    def test_user_update_form(self):
        # Test user update form with valid data
        form_data = {
        'username': 'updateduser',
        'email': 'updateuser@fake.com',
        }
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
    

    
