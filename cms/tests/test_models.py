from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from ..models import Article, ArticleChange
from .test_views import UserDatabaseOperations


class ArticleTestCase(TestCase):
    def setUp(self):
        user = User(
             username='user',
             first_name='Jan',
             last_name='Kowalski',
             email='jan@kowalski.com',
             password='12345'
        )
        user.save()

        article = Article.objects.create(
            title='title',
            content='content',
            author=user
        )
        article.save()

    def test_valid_create_article(self):
        '''Valid article create'''
        user = User.objects.get(username='user')
        article = Article.objects.get(author=user)
        
        self.assertEqual(article.content, 'content')
        self.assertEqual(article.title, 'title')

    def test_invalid_create_article_without_author(self):
        '''Creating article without author causes error'''
        with self.assertRaises(IntegrityError):
            article = Article.objects.create(content='Some content.')

    def test_article_str_representation(self):
        user = User.objects.get(username='user')
        article = Article.objects.get(author=user)

        self.assertEqual(str(article), 'title')

    def test_article_date_published(self):
        '''Pub date is equal to save time'''
        user = User.objects.get(username='user')
        article = Article.objects.create(
            title='title',
            content='content',
            author=user
        )
        now = str(datetime.now())
        now = now.split()[0]
        article.save()
        
        self.assertEqual(str(article.pub_date), now)


class ArticleChangeTestCase(TestCase, UserDatabaseOperations):
    def setUp(self):
        self.create_user()
        self.title = 'title'
        self.content = 'content'
        article = Article.objects.create(
            title='title',
            content='content',
            author=self.get_user()
        )
        article.save()

    def test_str_representation(self):
        article = Article.objects.get(pk=1)
        new_title = 'new_title'
        change = ArticleChange(
            article=article,
            user=self.get_user(),
            new_title=new_title,
            new_content='new_content',
            old_title=self.title,
            old_content=self.content,
        )
        change.save()
        expected_repr = new_title + ' ' + str(change.edit_date)
        self.assertEqual(str(change), expected_repr)

    def test_valid_saved_change_after_edit_article(self):
        '''Valid change old title, content and user to new and save it to ArticleChange model'''
        new_user = User.objects.create_user(
            username='other_user',
            password='password'
        )
        new_user.save()

        old_article = Article.objects.get(author=self.get_user())
        
        self.client.login(username='other_user', password='password')

        url = reverse('cms:edit_article', kwargs={'id_article':old_article.pk})
        self.client.post(url, {
            'title': 'new_title',
            'content': 'new_content',
        })

        new_article = Article.objects.get(author=self.get_user()) # author doesn't change
        change = ArticleChange.objects.get(article=new_article)

        self.assertEqual(change.old_title, self.title)
        self.assertEqual(change.old_content, self.content)
        self.assertEqual(change.user, new_user)
