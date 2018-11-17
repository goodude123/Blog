from datetime import datetime
from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from ..models import Article


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
    