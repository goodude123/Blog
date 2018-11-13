from datetime import datetime
from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from ..models import Post


class PostTestCase(TestCase):
    def setUp(self):
        user = User(
             username='user',
             first_name='Jan',
             last_name='Kowalski',
             email='jan@kowalski.com',
             password='12345'
        )
        user.save()

        post = Post.objects.create(
            title='title',
            content='content',
            author=user
        )
        post.save()

    def test_valid_create_post(self):
        '''Valid post create'''
        user = User.objects.get(username='user')
        post = Post.objects.get(author=user)
        
        self.assertEqual(post.content, 'content')
        self.assertEqual(post.title, 'title')

    def test_invalid_create_post_without_author(self):
        '''Creating post without author causes error'''
        with self.assertRaises(IntegrityError):
            post = Post.objects.create(content='Some content.')

    def test_post_str_representation(self):
        user = User.objects.get(username='user')
        post = Post.objects.get(author=user)

        self.assertEqual(str(post), 'title')

    def test_post_date_published(self):
        '''Pub date is equal to save time'''
        user = User.objects.get(username='user')
        post = Post.objects.create(
            title='title',
            content='content',
            author=user
        )
        now = str(datetime.now())
        now = now.split()[0]
        post.save()
        
        self.assertEqual(str(post.pub_date), now)
    