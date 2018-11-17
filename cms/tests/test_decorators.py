from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..decorators import prevent_logged


class PreventLoggedTestCase(TestCase):
    '''Logged user has prevented view'''
    def setUp(self):
        user = User.objects.create_user(
            username='username',
            password='password'
        )
        user.save()

    def test_access_logged_user_to_forbidden_logged_users_view(self):
        '''User is logged, redirect to main view'''
        self.client.login(
            username='username',
            password='password'
        )        
        response = self.client.get(reverse('cms:register'), follow=True)
        self.assertRedirects(response, reverse('cms:main'))

    def test_access_unlogged_to_forbidden_logged_users_view(self):
        response = self.client.get(reverse('cms:register'), follow=True)
        self.assertEqual(response.status_code, 200)