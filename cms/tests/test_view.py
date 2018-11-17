from test_plus.test import CBVTestCase
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from .. import views
from ..models import Article



class MainViewTest(CBVTestCase):
    def setUp(self):
        self.create_articles(5)

    def create_articles(self, amount):
        user = self.create_user()
        for i in range(amount):
            title = 'title' + str(i)
            article = Article.objects.create(
                title=title,
                content='content',
                author=user,
            )
            article.save()

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
        self.assertTemplateUsed(response, 'cms/articles_list.html')

    def test_queryset_should_return_only_three_articles(self):
        my_view = self.get_instance(views.Main)
        queryset = my_view.get_queryset()
        self.assertEqual(len(queryset), 3)

    def test_rendered_articles_are_valid(self):
        '''Articles on main page are three last Articles from database.'''
        url = self.reverse('cms:main')
        response = self.client.get(url)
        last_three_articles = Article.objects.order_by('-pub_date')[:3]
        self.assertEqual(str(response.context['articles']), str(last_three_articles))

    def test_template_render(self):
        url = self.reverse('cms:main')
        response = self.client.get(url)
        
    def test_is_url_achievable(self):
        url = self.reverse('cms:main')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestRegisterView(TestCase):
    def setUp(self):
        self.url = reverse('cms:register')

    def test_valid_page_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertContains(response,  'username')
        self.assertContains(response,  'password1')

    def test_valid_registration(self):
        '''Valid registration redirect to main page.'''
        response = self.client.post(self.url, {
            'username': 'validusername',
            'password1': 'zaq1@WSX',
            'password2': 'zaq1@WSX',
        }, follow=True)
        self.assertRedirects(response, reverse('cms:main'))
        self.assertEqual(response.status_code, 200)

    def test_invalid_registration(self):
        '''Invalid registration redirects us again to registration page.'''
        response = self.client.post(self.url, {
            'username': '',
            'password1': '',
            'password2': '',
        }, follow=True)
        self.assertRedirects(response, reverse('cms:register'))

    def test_prevent_logged_user_access(self):
        pass

