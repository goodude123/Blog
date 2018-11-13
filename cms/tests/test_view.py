from test_plus.test import CBVTestCase
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from .. import views
from ..models import Post



class MainViewTest(CBVTestCase):
    def setUp(self):
        self.create_posts(5)

    def create_posts(self, amount):
        user = self.create_user()
        for i in range(amount):
            title = 'title' + str(i)
            post = Post.objects.create(
                title=title,
                content='content',
                author=user,
            )
            post.save()

    def create_user(self):
        user = User.objects.create(
            username='user',
            password='zaq1@WSX'
        )
        user.save()
        
        return user

    def test_valid_page_access(self):
        url = reverse('cms:main')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_list.html')

    def test_queryset_should_return_only_three_posts(self):
        my_view = self.get_instance(views.Main)
        queryset = my_view.get_queryset()
        self.assertEqual(len(queryset), 3)

    def test_rendered_posts_are_valid(self):
        '''Posts on main page are three last posts from database.'''
        url = self.reverse('cms:main')
        response = self.client.get(url)
        last_three_posts = Post.objects.order_by('-pub_date')[:3]
        self.assertEqual(str(response.context['posts']), str(last_three_posts))

    def test_template_render(self):
        url = self.reverse('cms:main')
        response = self.client.get(url)
        
    def test_is_url_achievable(self):
        url = self.reverse('cms:main')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestRegisterView(TestCase):
    def test_valid_page_access(self):
        url = reverse('cms:register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertContains(response,  'username')
        self.assertContains(response,  'password1')

    def test_valid_registration(self):
        '''Valid registration redirect to main page.'''
        url = reverse('cms:register')
        response = self.client.post(url, {
            'username': 'validusername',
            'password1': 'zaq1@WSX',
            'password2': 'zaq1@WSX',
        }, follow=True)
        self.assertRedirects(response, reverse('cms:main'))
        self.assertEqual(response.status_code, 200)

    def test_invalid_registration(self):
        '''Invalid registration redirects us again to registration page.'''
        url = reverse('cms:register')
        response = self.client.post(url, {
            'username': '',
            'password1': '',
            'password2': '',
        }, follow=True)
        self.assertRedirects(response, reverse('cms:register'))

