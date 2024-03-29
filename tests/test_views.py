import io

from django.contrib.auth.forms import AuthenticationForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from second_buy.web.models import Profile, Item, Category
from second_buy.web.views import ItemsList


class IndexViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')

    def test_index_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Make a GET request to the index view
        response = self.client.get(reverse('index'))

        # Check if the view is returning the correct template
        self.assertTemplateUsed(response, 'index.html')

        # Check if the user is authenticated in the context data
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEqual(response.context['user'], self.user)


class LoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertRedirects(response, reverse('index'))  # Change 'index' to the appropriate URL name for the homepage
        self.assertTrue(self.client.session['_auth_user_id'], self.user.pk)

    def test_login_failure(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
        print(response)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertIsInstance(form, AuthenticationForm)
        self.assertTrue(form.errors)


class LogoutTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_logout(self):
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('index'))  # Change 'index' to the appropriate URL name for the homepage
        self.assertFalse('_auth_user_id' in self.client.session)


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_success(self):
        # Ensure a successful registration
        response = self.client.post(reverse('register'), {'username': 'testuser', 'password1': 'testpassword123', 'password2': 'testpassword123'})
        self.assertEqual(response.status_code, 302)  # Redirect to login on successful registration

        # Check if the user and profile were created
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(Profile.objects.filter(user__username='testuser').exists())

    def test_register_failure(self):
        # Ensure registration with invalid data fails
        response = self.client.post(reverse('register'), {'username': 'testuser', 'password1': 'testpassword123', 'password2': 'mismatchedpassword'})
        self.assertEqual(response.status_code, 200)  # Stay on the registration page on failure

        # Check if the user and profile were not created due to the failed registration attempt
        self.assertFalse(User.objects.filter(username='testuser').exists())
        self.assertFalse(Profile.objects.filter(user__username='testuser').exists())

    def test_register_template(self):
        # Ensure the correct template is used
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'registration/register.html')


class ViewProfileViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a user and its associated profile
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.profile = Profile.objects.create(user=self.user, phone_number='1234567890', email='testuser@example.com')

    def test_view_profile_failure(self):
        # Ensure the view profile page is not accessible for anonymous users
        response = self.client.get(reverse('view profile', kwargs={'user_id': self.user.pk}))
        self.assertEqual(response.status_code, 403)




class EditProfileViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a user and its associated profile
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.profile = Profile.objects.create(user=self.user)

        # Set a test image for profile_photo
        image_content = b'f\x1f\x80\x00\x00\x00\x00IEND\xaeB`\x82'
        self.profile_photo = SimpleUploadedFile('test.png', image_content, content_type='image/png')

    def test_edit_profile_success(self):
        # Ensure the edit profile page is accessible for the logged-in user
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('edit profile', kwargs={'user_id': self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile/edit_profile.html')

    def test_edit_profile_failure(self):
        # Ensure the edit profile page is not accessible for anonymous users
        response = self.client.get(reverse('edit profile', kwargs={'user_id': self.user.pk}))
        self.assertEqual(response.status_code, 403)




